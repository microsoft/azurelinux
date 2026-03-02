#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Download and upload component sources to Azure Blob Storage.

Workflow:

  1. Discover components — either auto-discover via ``azldev component list``
     (filtered by ``--component-filter``) or read from ``--components-file``.
  2. For each component (in parallel):
     a. Download sources via ``azldev component prepare-sources``.
     b. Upload source files to Azure Blob Storage (skip existing blobs).
     c. Remove local download artifacts to free disk space.

Failed component names are written to ``--failed-output`` so the script can
be re-run with ``--components-file`` pointing at the failure list.

Blob naming convention:

  pkgs/<pkg>/<filename>/<hashtype>/<hash>/<filename>

Hash values used in blob paths are computed from the **actual** downloaded
files (not the upstream ``sources`` metadata).  This is intentional — TOML
overlay configuration may modify source files after download, so the real
on-disk hash is the authoritative one.  Upstream integrity verification is
handled by ``azldev component prepare-sources`` itself and is not duplicated
here.

Authentication uses ``AzureCliCredential`` — run ``az login`` before
invoking this script.

Requires:

  pip install azure-identity azure-storage-blob

Usage examples:

  # Full run — auto-discover, download, upload:
  ./scripts/sync-sources.py \\
      --account-url https://<account>.blob.core.windows.net \\
      --container <name>

  # Retry only previously-failed components:
  ./scripts/sync-sources.py \\
      --components-file components.failed.list \\
      --account-url https://<account>.blob.core.windows.net \\
      --container <name>
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("sync-sources")


def _setup_logging(*, quiet: bool) -> None:
    """Configure the root logger with a console handler.

    Per-component file handlers are attached/detached dynamically by
    :func:`process_component`.
    """
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(message)s"))
    console.setLevel(logging.WARNING if quiet else logging.INFO)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = REPO_ROOT / "sources"
DOWNLOADS_DIR = SOURCES_DIR / "downloads"
LOG_DIR = SOURCES_DIR / "logs"

MAX_RETRIES = 1

_DEFAULT_COMPONENT_FILTER = "Upstream: fedora"
_DEFAULT_FAILED_OUTPUT = "components.failed.list"

# BSD-style: HASH (filename) = hexdigest
_BSD_RE = re.compile(r"^(\w+)\s+\((.+?)\)\s*=\s*(\S+)$")

# GNU-style: hexdigest  filename  (two-space separator is conventional)
_GNU_RE = re.compile(r"^([0-9a-fA-F]+)\s+(.+)$")

# Map hex-digest length -> canonical hash name (for GNU-style lines).
_HEX_LEN_TO_HASH: dict[int, str] = {
    32: "MD5",
    40: "SHA1",
    64: "SHA256",
    128: "SHA512",
}

# Canonical hash names -> hashlib algorithm strings.
_HASH_TO_ALGO: dict[str, str] = {
    "MD5": "md5",
    "SHA1": "sha1",
    "SHA256": "sha256",
    "SHA512": "sha512",
}

# Matches the azldev stderr line that maps component -> upstream component.
# Example: "Getting component from git repo component=fuse3-42 upstreamComponent=fuse3 branch=f43"
_UPSTREAM_COMP_RE = re.compile(r"upstreamComponent=(\S+)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _blob_name_for(
    pkg: str, filename: str, hash_type: str, hex_digest: str
) -> str:
    """Build the canonical blob path for a source file."""
    return (
        f"pkgs/{pkg}/{filename}"
        f"/{hash_type.lower()}/{hex_digest.lower()}/{filename}"
    )


def _parse_upstream_name(text: str) -> str | None:
    """Extract the upstream component name from azldev stderr output.

    Scans *text* for a token ``upstreamComponent=<name>`` and returns
    *<name>*, or ``None`` if not found.
    """
    for line in text.splitlines():
        m = _UPSTREAM_COMP_RE.search(line)
        if m:
            return m.group(1)
    return None


def _run_parallel(
    items: list[str],
    worker_fn,
    jobs: int,
) -> tuple[list[str], list[str]]:
    """Run *worker_fn(item)* -> bool in parallel across *items*.

    Returns ``(succeeded, failed)`` lists.
    """
    succeeded: list[str] = []
    failed: list[str] = []
    result_lock = threading.Lock()

    def _wrapper(item: str) -> None:
        ok = worker_fn(item)
        with result_lock:
            (succeeded if ok else failed).append(item)

    with ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(_wrapper, item) for item in items]
        for future in as_completed(futures):
            future.result()  # propagate unexpected exceptions

    return succeeded, failed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Download and upload component sources to Azure Blob Storage."
        ),
    )
    parser.add_argument(
        "--account-url",
        required=True,
        help=(
            "Azure Storage Account URL "
            "(e.g. https://<account>.blob.core.windows.net)."
        ),
    )
    parser.add_argument(
        "--container",
        required=True,
        help="Name of the blob container to upload into.",
    )
    parser.add_argument(
        "--component-filter",
        default=_DEFAULT_COMPONENT_FILTER,
        help=(
            "Substring filter applied to azldev markdown output lines to "
            f"select components (default: {_DEFAULT_COMPONENT_FILTER!r})."
        ),
    )
    parser.add_argument(
        "--components-file",
        type=Path,
        help=(
            "Read component names from this file (one per line) instead of "
            "auto-discovering via azldev. Accepts the output of --failed-output."
        ),
    )
    parser.add_argument(
        "--failed-output",
        type=Path,
        default=Path(_DEFAULT_FAILED_OUTPUT),
        help=(
            "Write failed component names to this file, one per line "
            f"(default: {_DEFAULT_FAILED_OUTPUT}). Can be passed back as "
            "--components-file to retry."
        ),
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=os.cpu_count(),
        help="Max parallel workers (default: CPU count).",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress per-file success messages; only print errors and summary.",
    )
    return parser


# ---------------------------------------------------------------------------
# Component discovery
# ---------------------------------------------------------------------------


def discover_components(component_filter: str) -> list[str]:
    """Auto-discover components by running ``azldev component list``.

    Runs ``azldev component list -a -O markdown`` and filters lines that
    contain *component_filter*.  The component name is extracted as the
    second whitespace-delimited field (equivalent to ``cut -d' ' -f2``).
    """
    result = subprocess.run(
        ["./azldev", "component", "list", "-a", "-O", "markdown"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        logger.error(
            "azldev component list failed (exit %d):\n%s",
            result.returncode,
            result.stderr,
        )
        sys.exit(1)

    components: list[str] = []
    for line in result.stdout.splitlines():
        if component_filter in line:
            fields = line.split()
            if len(fields) >= 2:
                components.append(fields[1])
    return components


def parse_components_file(components_file: Path) -> list[str]:
    """Read component names from *components_file*, skipping blanks/comments."""
    components: list[str] = []
    for line in components_file.read_text().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            components.append(stripped)
    return components


def resolve_components(args: argparse.Namespace) -> list[str]:
    """Return the component list, either from a file or via auto-discovery."""
    if args.components_file:
        if not args.components_file.is_file():
            logger.error("Cannot read components file: %s", args.components_file)
            sys.exit(1)
        components = parse_components_file(args.components_file)
        logger.info(
            "Read %d component(s) from %s",
            len(components),
            args.components_file,
        )
    else:
        logger.info(
            "Discovering components (filter: %r)…", args.component_filter
        )
        components = discover_components(args.component_filter)
        logger.info("Discovered %d component(s)", len(components))
    return components


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------


def _download_component_once(
    component: str,
) -> tuple[bool, str | None]:
    """Download sources for a single component (single attempt).

    Returns ``(success, upstream_name)`` where *upstream_name* is the
    upstream component name extracted from the azldev stderr output (e.g.
    ``"fuse3"`` when the component is ``"fuse3-42"``), or ``None`` when
    the upstream name cannot be determined or matches the component name.
    """
    output_dir = DOWNLOADS_DIR / component
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "./azldev",
            "component",
            "prepare-sources",
            component,
            "--force",
            "-o",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    # Log subprocess output at DEBUG level (captured by file handler).
    if result.stdout:
        logger.debug("[azldev stdout]\n%s", result.stdout)
    if result.stderr:
        logger.debug("[azldev stderr]\n%s", result.stderr)

    upstream_name = _parse_upstream_name(result.stderr)
    return result.returncode == 0, upstream_name


def download_component(component: str) -> tuple[bool, str | None]:
    """Download sources for *component*, retrying up to *MAX_RETRIES* times.

    Returns ``(success, upstream_name)``.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(
            ">>> Download: %s (attempt %d/%d)", component, attempt, MAX_RETRIES
        )
        ok, upstream_name = _download_component_once(component)
        if ok:
            logger.info(">>> Download OK: %s", component)
            return True, upstream_name
        if attempt < MAX_RETRIES:
            logger.warning(
                ">>> Retry: %s (attempt %d failed, retrying…)",
                component,
                attempt,
            )
        else:
            logger.error(
                ">>> FAILED download: %s (all %d attempts exhausted)",
                component,
                MAX_RETRIES,
            )
    return False, None


# ---------------------------------------------------------------------------
# Sources metadata parsing
# ---------------------------------------------------------------------------

# NOTE: We do NOT verify downloaded file hashes against the upstream
# ``sources`` metadata.  Upstream integrity is validated by
# ``azldev component prepare-sources`` itself.  We parse the ``sources``
# file only to discover which files exist and what hash algorithm to use
# when computing the actual on-disk hash for blob naming.  The actual hash
# (rather than the metadata hash) is used because TOML overlay configuration
# may modify source files after download.


def parse_source_line(
    line: str, lineno: int, sources_path: Path
) -> tuple[str, str] | None:
    """Parse a single line from a ``sources`` metadata file.

    Returns ``(hash_type, filename)`` or ``None`` for blank/comment lines.
    Logs a warning for unparseable non-blank lines.
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    # Try BSD-style first: HASH (filename) = hexdigest
    m = _BSD_RE.match(stripped)
    if m:
        return m.group(1).upper(), m.group(2)

    # Try GNU-style: hexdigest  filename
    m = _GNU_RE.match(stripped)
    if m:
        hex_digest = m.group(1)
        filename = m.group(2).strip()
        hash_type = _HEX_LEN_TO_HASH.get(len(hex_digest))
        if hash_type is None:
            logger.warning(
                "%s:%d: cannot infer hash type from %d-char hex digest",
                sources_path,
                lineno,
                len(hex_digest),
            )
            return None
        return hash_type, filename

    logger.warning(
        "%s:%d: unparseable line: %r", sources_path, lineno, stripped
    )
    return None


def compute_file_hash(filepath: Path, hash_type: str) -> str | None:
    """Compute and return the hex digest of *filepath* using *hash_type*.

    Returns ``None`` if the file is missing or the hash type is unsupported.
    """
    algo = _HASH_TO_ALGO.get(hash_type)
    if algo is None:
        logger.error("Unsupported hash type '%s' for %s", hash_type, filepath)
        return None

    if not filepath.exists():
        logger.error("File not found: %s", filepath)
        return None

    with open(filepath, "rb") as f:
        return hashlib.file_digest(f, algo).hexdigest()


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------


def list_existing_blobs(blob_service_client, container: str) -> set[str]:
    """Return the set of all blob names in *container*.

    The full listing is fetched once so that individual upload calls can
    do a cheap ``in`` check instead of a per-blob network round-trip.
    """
    container_client = blob_service_client.get_container_client(container)
    logger.info("Listing existing blobs in container %r…", container)
    existing = {blob.name for blob in container_client.list_blobs()}
    logger.info("Found %d existing blob(s)", len(existing))
    return existing


def _upload_file_if_missing(
    blob_service_client,
    container: str,
    existing_blobs: set[str],
    filepath: Path,
    blob_name: str,
) -> bool:
    """Upload a single file, skipping if the blob already exists.

    Returns ``True`` on success (including skip).
    """
    from azure.core.exceptions import AzureError

    if blob_name in existing_blobs:
        logger.info("SKIP (exists): %s", blob_name)
        return True

    blob_client = blob_service_client.get_blob_client(
        container=container, blob=blob_name
    )
    try:
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data)
    except AzureError as exc:
        logger.error("Upload failed %s -> %s: %s", filepath, blob_name, exc)
        return False

    logger.info("UPLOADED: %s -> %s", filepath, blob_name)
    return True


def _upload_component_sources(
    component: str,
    blob_service_client,
    container: str,
    existing_blobs: set[str],
    *,
    upload_name: str | None = None,
) -> bool:
    """Upload source files for a single component.

    Reads ``sources/downloads/<component>/sources`` to discover files and
    their hash types, computes actual on-disk hashes, and uploads to Azure.
    When *upload_name* is provided, the blob path uses that name instead
    of *component* (to handle upstream name differences).

    Returns ``True`` if all entries succeed.
    """
    pkg = upload_name or component
    sources_path = DOWNLOADS_DIR / component / "sources"
    if not sources_path.is_file():
        logger.warning("No sources file for %s: %s", component, sources_path)
        return True

    sources_dir = sources_path.parent
    all_ok = True

    for lineno, line in enumerate(
        sources_path.read_text().splitlines(), start=1
    ):
        parsed = parse_source_line(line, lineno, sources_path)
        if parsed is None:
            continue
        hash_type, filename = parsed

        filepath = sources_dir / filename
        actual_hex = compute_file_hash(filepath, hash_type)
        if actual_hex is None:
            all_ok = False
            continue

        blob_name = _blob_name_for(pkg, filename, hash_type, actual_hex)
        if not _upload_file_if_missing(
            blob_service_client,
            container,
            existing_blobs,
            filepath,
            blob_name,
        ):
            all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# Per-component processing (download → upload → cleanup)
# ---------------------------------------------------------------------------


def process_component(
    component: str,
    blob_service_client,
    container: str,
    existing_blobs: set[str],
) -> bool:
    """Download, upload, and clean up sources for a single component.

    Attaches a per-component file handler to ``logger`` so that all
    messages (including DEBUG-level azldev output) are captured in
    ``sources/logs/<component>.log``.

    Returns ``True`` on success.
    """
    log_file = LOG_DIR / f"{component}.log"
    fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    logger.addHandler(fh)

    try:
        return _process_component_inner(
            component, blob_service_client, container, existing_blobs
        )
    finally:
        logger.removeHandler(fh)
        fh.close()


def _process_component_inner(
    component: str,
    blob_service_client,
    container: str,
    existing_blobs: set[str],
) -> bool:
    """Core logic for :func:`process_component` (no handler management)."""
    # ---- Download ----
    ok, upstream_name = download_component(component)
    if not ok:
        logger.error(
            "Keeping artifacts for %s in %s for debugging",
            component,
            DOWNLOADS_DIR / component,
        )
        return False

    upload_name = (
        upstream_name if upstream_name and upstream_name != component else None
    )
    if upload_name:
        logger.info("Upstream name mapping: %s -> %s", component, upload_name)

    # ---- Upload ----
    upload_ok = _upload_component_sources(
        component,
        blob_service_client,
        container,
        existing_blobs,
        upload_name=upload_name,
    )

    if not upload_ok:
        logger.error(
            "Keeping artifacts for %s in %s for debugging",
            component,
            DOWNLOADS_DIR / component,
        )
        return False

    # ---- Cleanup ----
    artifact_dir = DOWNLOADS_DIR / component
    if artifact_dir.is_dir():
        shutil.rmtree(artifact_dir)
        logger.debug("Cleaned up %s", artifact_dir)

    logger.info(">>> Done: %s", component)
    return True


# ---------------------------------------------------------------------------
# Azure client setup
# ---------------------------------------------------------------------------


def create_blob_service_client(account_url: str):
    """Create and return an authenticated :class:`BlobServiceClient`.

    Exits with code 2 on credential or connection errors.
    """
    from azure.identity import AzureCliCredential, CredentialUnavailableError
    from azure.storage.blob import BlobServiceClient
    from azure.core.exceptions import AzureError

    try:
        credential = AzureCliCredential()
        return BlobServiceClient(
            account_url=account_url, credential=credential
        )
    except CredentialUnavailableError as exc:
        logger.error(
            "Azure CLI credentials not available. Run 'az login' first.\n  %s",
            exc,
        )
        sys.exit(2)
    except AzureError as exc:
        logger.error("Failed to create Azure Blob Storage client: %s", exc)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Failed-components bookkeeping
# ---------------------------------------------------------------------------


def write_failed_components(failed: list[str], output_path: Path) -> None:
    """Persist *failed* component names to *output_path* (or clean up)."""
    if failed:
        output_path.write_text("\n".join(sorted(failed)) + "\n")
        logger.info(
            "Failed components written to %s "
            "(re-run with --components-file %s to retry)",
            output_path,
            output_path,
        )
    elif output_path.exists():
        output_path.unlink()


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def _log_summary(
    *,
    total: int,
    succeeded: list[str],
    failed: list[str],
    failed_output: Path,
    jobs: int,
) -> None:
    """Log a human-readable run summary."""
    logger.info("")
    logger.info("========================================")
    logger.info(" Sync Summary")
    logger.info("========================================")
    logger.info(" Total components:  %d", total)
    logger.info(" Succeeded:         %d", len(succeeded))
    logger.info(" Failed:            %d", len(failed))
    logger.info(" Parallel workers:  %d", jobs)
    logger.info("========================================")

    if failed:
        logger.info("")
        logger.info("Failures (see %s):", failed_output)
        for name in sorted(failed):
            logger.info(
                "  - %s  (log: %s/%s.log)",
                name,
                LOG_DIR.relative_to(REPO_ROOT),
                name,
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    if not (REPO_ROOT / "azldev.toml").exists():
        print(
            "ERROR: This script must be run from the root of the repo "
            "(where azldev.toml lives).",
            file=sys.stderr,
        )
        return 1

    parser = _build_parser()
    args = parser.parse_args()

    _setup_logging(quiet=args.quiet)

    # ---- Resolve component list ----
    components = resolve_components(args)
    if not components:
        logger.info("No components to process.")
        return 0

    # ---- Azure client setup ----
    blob_service_client = create_blob_service_client(args.account_url)
    existing_blobs = list_existing_blobs(blob_service_client, args.container)

    # ---- Process components (download → upload → cleanup) ----
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(
        "\n=== Processing %d component(s) with %d workers ===\n",
        len(components),
        args.jobs,
    )

    def worker(component: str) -> bool:
        return process_component(
            component, blob_service_client, args.container, existing_blobs
        )

    succeeded, failed = _run_parallel(components, worker, args.jobs)

    # ---- Write failures & summary ----
    write_failed_components(failed, args.failed_output)

    _log_summary(
        total=len(components),
        succeeded=succeeded,
        failed=failed,
        failed_output=args.failed_output,
        jobs=args.jobs,
    )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
