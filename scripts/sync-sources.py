#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Download, verify, and upload component sources to Azure Blob Storage.

Combines the logic of download-sources.py and verify-sources.py into a single
workflow:

  1. Discover components — either auto-discover via ``azldev component list``
     (filtered by ``--component-filter``) or read from ``--components-file``.
  2. Download sources in parallel (with up to 3 retries per component).
  3. Verify file hashes from Fedora-style ``sources`` metadata files.
  4. Upload verified files to Azure Blob Storage, skipping blobs that
     already exist.

Failed component names are written to ``--failed-output`` so the script can
be re-run with ``--components-file`` pointing at the failure list.

Blob naming convention:

  pkgs/<pkg>/<filename>/<hashtype>/<hash>/<filename>

Authentication uses AzureCliCredential — run ``az login`` before invoking
this script.

Requires:  pip install azure-identity azure-storage-blob

Usage examples:

  # Full run — auto-discover, download, verify, upload:
  ./scripts/sync-sources.py \\
      --account-url https://<account>.blob.core.windows.net \\
      --container <name>

  # Retry only previously-failed components:
  ./scripts/sync-sources.py \\
      --components-file components.failed.list \\
      --account-url https://<account>.blob.core.windows.net \\
      --container <name>

  # Download + verify only (no Azure credentials needed):
  ./scripts/sync-sources.py --verify-only

  # Upload already-downloaded sources (skip download phase):
  ./scripts/sync-sources.py --skip-download \\
      --account-url https://<account>.blob.core.windows.net \\
      --container <name>
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import BinaryIO

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

_print_lock = threading.Lock()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _lock_print(*args, **kwargs) -> None:
    """Thread-safe wrapper around :func:`print`."""
    with _print_lock:
        print(*args, **kwargs)


def _flush_output(stdout_reader: BinaryIO, stderr_reader: BinaryIO) -> None:
    """Read available data from stdout/stderr readers and print it."""
    stdout_data = stdout_reader.read()
    stderr_data = stderr_reader.read()
    if stdout_data:
        _lock_print(stdout_data.decode(), end="")
    if stderr_data:
        _lock_print(stderr_data.decode(), end="", file=sys.stderr)


def _blob_name_for(
    pkg: str, filename: str, hash_type: str, expected_hex: str
) -> str:
    """Build the canonical blob path for a source file."""
    return (
        f"pkgs/{pkg}/{filename}"
        f"/{hash_type.lower()}/{expected_hex.lower()}/{filename}"
    )


def _parse_upstream_name(stderr_log: Path) -> str | None:
    """Extract the upstream component name from an azldev stderr log.

    Scans *stderr_log* for a line containing ``upstreamComponent=<name>``
    and returns *<name>*, or ``None`` if not found.
    """
    if not stderr_log.is_file():
        return None
    try:
        for line in stderr_log.read_text(errors="replace").splitlines():
            m = _UPSTREAM_COMP_RE.search(line)
            if m:
                return m.group(1)
    except OSError:
        pass
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
            "Download, verify, and upload component sources to "
            "Azure Blob Storage."
        ),
    )
    parser.add_argument(
        "--account-url",
        help=(
            "Azure Storage Account URL "
            "(e.g. https://<account>.blob.core.windows.net). "
            "Required unless --verify-only."
        ),
    )
    parser.add_argument(
        "--container",
        help="Name of the blob container to upload into. Required unless --verify-only.",
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
        help="Max parallel workers for download and upload (default: CPU count).",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Download and verify hashes only; do not upload to Azure.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip the download phase; only verify/upload already-downloaded sources.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress per-file success messages; only print errors and summary.",
    )
    return parser


def _validate_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    """Validate argument combinations; call ``parser.error`` on failure."""
    if not args.verify_only and (not args.account_url or not args.container):
        parser.error(
            "--account-url and --container are required unless --verify-only"
        )
    if args.components_file and not args.components_file.is_file():
        parser.error(f"Cannot read components file: {args.components_file}")


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
        print(
            f"ERROR: azldev component list failed (exit {result.returncode}):\n"
            f"{result.stderr}",
            file=sys.stderr,
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
        components = parse_components_file(args.components_file)
        print(
            f"Read {len(components)} component(s) from {args.components_file}"
        )
    else:
        print(
            f"Discovering components (filter: {args.component_filter!r})…"
        )
        components = discover_components(args.component_filter)
        print(f"Discovered {len(components)} component(s)")
    return components


# ---------------------------------------------------------------------------
# Download phase
# ---------------------------------------------------------------------------


def _download_component_once(component: str) -> tuple[bool, str | None]:
    """Download sources for a single component (single attempt).

    Returns ``(success, upstream_name)`` where *upstream_name* is the
    upstream component name extracted from the azldev stderr log (e.g.
    ``"fuse3"`` when the component is ``"fuse3-42"``), or ``None`` when
    the upstream name matches the component name.
    """
    output_dir = DOWNLOADS_DIR / component
    stdout_log = LOG_DIR / f"{component}.stdout.log"
    stderr_log = LOG_DIR / f"{component}.stderr.log"

    output_dir.mkdir(parents=True, exist_ok=True)

    with (
        io.open(stdout_log, "wb") as stdout_writer,
        io.open(stdout_log, "rb") as stdout_reader,
        io.open(stderr_log, "wb") as stderr_writer,
        io.open(stderr_log, "rb") as stderr_reader,
    ):
        proc = subprocess.Popen(
            [
                "./azldev",
                "component",
                "prepare-sources",
                component,
                "--force",
                "-o",
                str(output_dir),
            ],
            stdout=stdout_writer,
            stderr=stderr_writer,
            cwd=REPO_ROOT,
        )

        while proc.poll() is None:
            _flush_output(stdout_reader, stderr_reader)
            time.sleep(0.5)

        _flush_output(stdout_reader, stderr_reader)

    upstream_name = _parse_upstream_name(stderr_log)
    return proc.returncode == 0, upstream_name


def download_component(component: str) -> tuple[bool, str | None]:
    """Download sources for *component*, retrying up to *MAX_RETRIES* times.

    Returns ``(success, upstream_name)``.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        _lock_print(
            f">>> Starting: {component} (attempt {attempt}/{MAX_RETRIES})"
        )
        ok, upstream_name = _download_component_once(component)
        if ok:
            _lock_print(f">>> Completed: {component}")
            return True, upstream_name
        if attempt < MAX_RETRIES:
            _lock_print(
                f">>> Retry: {component} (attempt {attempt} failed, retrying…)",
                file=sys.stderr,
            )
        else:
            _lock_print(
                f">>> FAILED: {component} "
                f"(all {MAX_RETRIES} attempts exhausted)",
                file=sys.stderr,
            )
    return False, None


def _build_upstream_map(components: list[str]) -> dict[str, str]:
    """Build an upstream-name map by scanning existing stderr logs.

    Useful when ``--skip-download`` is set and we still need the mapping.
    Only adds entries where the upstream name differs from the component.
    """
    upstream_map: dict[str, str] = {}
    for component in components:
        stderr_log = LOG_DIR / f"{component}.stderr.log"
        upstream = _parse_upstream_name(stderr_log)
        if upstream and upstream != component:
            upstream_map[component] = upstream
    return upstream_map


def run_download_phase(
    components: list[str], jobs: int
) -> tuple[list[str], list[str], dict[str, str]]:
    """Download sources for all *components* in parallel.

    Returns ``(succeeded, failed, upstream_map)`` where *upstream_map*
    maps component names to their upstream package names when they differ.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    succeeded: list[str] = []
    failed: list[str] = []
    upstream_map: dict[str, str] = {}
    result_lock = threading.Lock()

    def _wrapper(component: str) -> None:
        ok, upstream_name = download_component(component)
        with result_lock:
            (succeeded if ok else failed).append(component)
            if upstream_name and upstream_name != component:
                upstream_map[component] = upstream_name

    with ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(_wrapper, c) for c in components]
        for future in as_completed(futures):
            future.result()  # propagate unexpected exceptions

    return succeeded, failed, upstream_map


def write_failed_components(
    failed: list[str], output_path: Path
) -> None:
    """Persist *failed* component names to *output_path* (or clean up)."""
    if failed:
        output_path.write_text("\n".join(sorted(failed)) + "\n")
        print(
            f"\nFailed components written to {output_path} "
            f"(re-run with --components-file {output_path} to retry)"
        )
    elif output_path.exists():
        output_path.unlink()


# ---------------------------------------------------------------------------
# Hash verification
# ---------------------------------------------------------------------------


def parse_source_line(
    line: str, lineno: int, sources_path: Path
) -> tuple[str, str, str] | None:
    """Parse a single line from a ``sources`` metadata file.

    Returns ``(hash_type, filename, expected_hex)`` or ``None`` for
    blank/comment lines.  Prints a warning for unparseable non-blank lines.
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    # Try BSD-style first.
    m = _BSD_RE.match(stripped)
    if m:
        return m.group(1).upper(), m.group(2), m.group(3)

    # Try GNU-style.
    m = _GNU_RE.match(stripped)
    if m:
        hex_digest = m.group(1)
        filename = m.group(2).strip()
        hash_type = _HEX_LEN_TO_HASH.get(len(hex_digest))
        if hash_type is None:
            print(
                f"WARNING: {sources_path}:{lineno}: "
                f"cannot infer hash type from {len(hex_digest)}-char hex digest",
                file=sys.stderr,
            )
            return None
        return hash_type, filename, hex_digest

    print(
        f"WARNING: {sources_path}:{lineno}: unparseable line: {stripped!r}",
        file=sys.stderr,
    )
    return None


def verify_file(
    sources_dir: Path,
    hash_type: str,
    filename: str,
    expected_hex: str,
    *,
    quiet: bool = False,
) -> bool:
    """Verify a single file's hash.  Returns True on match."""
    algo = _HASH_TO_ALGO.get(hash_type)
    if algo is None:
        print(
            f"ERROR: unsupported hash type '{hash_type}' for {filename}",
            file=sys.stderr,
        )
        return False

    filepath = sources_dir / filename
    if not filepath.exists():
        print(f"ERROR: file not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, "rb") as f:
        actual_hex = hashlib.file_digest(f, algo).hexdigest()

    if actual_hex.lower() != expected_hex.lower():
        print(
            f"ERROR: hash mismatch for {filepath}\n"
            f"  expected: {expected_hex.lower()}\n"
            f"  actual:   {actual_hex}",
            file=sys.stderr,
        )
        return False

    if not quiet:
        _lock_print(f"OK: {filepath} ({hash_type})")
    return True


# ---------------------------------------------------------------------------
# Upload phase
# ---------------------------------------------------------------------------


def list_existing_blobs(
    blob_service_client, container: str
) -> set[str]:
    """Return the set of all blob names in *container*.

    The full listing is fetched once so that individual upload calls can
    do a cheap ``in`` check instead of a per-blob network round-trip.
    """
    container_client = blob_service_client.get_container_client(container)
    print(f"Listing existing blobs in container {container!r}…")
    existing = {blob.name for blob in container_client.list_blobs()}
    print(f"Found {len(existing)} existing blob(s)")
    return existing


def _upload_file_if_missing(
    blob_service_client,
    container: str,
    existing_blobs: set[str],
    sources_dir: Path,
    pkg: str,
    hash_type: str,
    filename: str,
    expected_hex: str,
    *,
    quiet: bool = False,
) -> bool:
    """Verify and upload a single file, skipping if the blob already exists.

    Returns True on success (including skip).
    """
    from azure.core.exceptions import AzureError

    filepath = sources_dir / filename
    blob_name = _blob_name_for(pkg, filename, hash_type, expected_hex)

    if blob_name in existing_blobs:
        if not quiet:
            _lock_print(f"SKIPPED: {blob_name} (already exists)")
        return True

    blob_client = blob_service_client.get_blob_client(
        container=container, blob=blob_name
    )

    try:
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data)
    except AzureError as exc:
        print(
            f"ERROR: failed to upload {filepath} as {blob_name}: {exc}",
            file=sys.stderr,
        )
        return False

    if not quiet:
        _lock_print(f"UPLOADED: {filepath} -> {blob_name}")
    return True


def _process_component_sources(
    component: str,
    blob_service_client=None,
    container: str | None = None,
    existing_blobs: set[str] | None = None,
    *,
    upload_name: str | None = None,
    verify_only: bool = False,
    quiet: bool = False,
) -> bool:
    """Verify (and optionally upload) sources for a single component.

    Reads ``sources/downloads/<component>/sources`` and processes each entry.
    When *upload_name* is provided, the blob path uses that name instead of
    *component* (to handle upstream name differences like ``fuse3-42`` ->
    ``fuse3``).
    Returns True if all entries succeed.
    """
    pkg = upload_name or component
    sources_path = DOWNLOADS_DIR / component / "sources"
    if not sources_path.is_file():
        print(
            f"WARNING: no sources file for {component}: {sources_path}",
            file=sys.stderr,
        )
        return True

    sources_dir = sources_path.parent
    all_ok = True

    for lineno, line in enumerate(
        sources_path.read_text().splitlines(), start=1
    ):
        parsed = parse_source_line(line, lineno, sources_path)
        if parsed is None:
            continue
        hash_type, filename, expected_hex = parsed

        if not verify_file(
            sources_dir, hash_type, filename, expected_hex, quiet=quiet
        ):
            all_ok = False
            continue

        if not verify_only:
            if not _upload_file_if_missing(
                blob_service_client,
                container,
                existing_blobs,
                sources_dir,
                pkg,
                hash_type,
                filename,
                expected_hex,
                quiet=quiet,
            ):
                all_ok = False

    return all_ok


def run_upload_phase(
    components: list[str],
    jobs: int,
    blob_service_client=None,
    container: str | None = None,
    existing_blobs: set[str] | None = None,
    *,
    upstream_map: dict[str, str] | None = None,
    verify_only: bool = False,
    quiet: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify/upload sources for all *components* in parallel.

    *upstream_map* maps component names to their upstream package names
    (used for the blob upload path when they differ).

    Returns ``(succeeded, failed)`` lists.
    """
    _upstream = upstream_map or {}

    def worker(component: str) -> bool:
        return _process_component_sources(
            component,
            blob_service_client=blob_service_client,
            container=container,
            existing_blobs=existing_blobs,
            upload_name=_upstream.get(component),
            verify_only=verify_only,
            quiet=quiet,
        )

    return _run_parallel(components, worker, jobs)


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
        print(
            f"ERROR: Azure CLI credentials not available. "
            f"Run 'az login' first.\n  {exc}",
            file=sys.stderr,
        )
        sys.exit(2)
    except AzureError as exc:
        print(
            f"ERROR: failed to create Azure Blob Storage client: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def _print_summary(
    *,
    total: int,
    download_failed: list[str],
    upload_succeeded: list[str],
    upload_failed: list[str],
    failed_output: Path,
    phase_label: str,
    skip_download: bool,
    jobs: int,
) -> None:
    """Print a human-readable run summary to stdout."""
    dl_ok = total - len(download_failed)

    print()
    print("========================================")
    print(" Sync Summary")
    print("========================================")
    print(f" Total components:     {total}")
    if not skip_download:
        print(f" Download succeeded:   {dl_ok}")
        print(f" Download failed:      {len(download_failed)}")
    print(f" {phase_label} succeeded: {len(upload_succeeded)}")
    print(f" {phase_label} failed:    {len(upload_failed)}")
    print(f" Parallel workers:     {jobs}")
    print("========================================")

    if download_failed:
        print(f"\nDownload failures ({failed_output}):")
        for name in sorted(download_failed):
            print(
                f"  - {name}  "
                f"(see {LOG_DIR.relative_to(REPO_ROOT)}/{name}.stderr.log)"
            )

    if upload_failed:
        print(f"\n{phase_label} failures:")
        for name in sorted(upload_failed):
            print(f"  - {name}")


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
    _validate_args(args, parser)

    # ---- Resolve component list ----
    components = resolve_components(args)
    if not components:
        print("No components to process.")
        return 0

    # ---- Download phase ----
    download_failed: list[str] = []
    upstream_map: dict[str, str] = {}
    if args.skip_download:
        print("Skipping download phase (--skip-download).")
        upload_candidates = components
        # Recover upstream name mapping from existing stderr logs.
        upstream_map = _build_upstream_map(components)
    else:
        print(f"\n=== Download phase ({args.jobs} workers) ===\n")
        download_succeeded, download_failed, upstream_map = run_download_phase(
            components, args.jobs
        )
        upload_candidates = download_succeeded

    if upstream_map:
        print(f"\nUpstream name mappings ({len(upstream_map)}):")
        for comp, upstream in sorted(upstream_map.items()):
            print(f"  {comp} -> {upstream}")

    write_failed_components(download_failed, args.failed_output)

    if not upload_candidates:
        print("No components to verify/upload.")
        return 1 if download_failed else 0

    # ---- Azure client setup ----
    blob_service_client = None
    existing_blobs: set[str] | None = None
    if not args.verify_only:
        blob_service_client = create_blob_service_client(args.account_url)
        existing_blobs = list_existing_blobs(
            blob_service_client, args.container
        )

    # ---- Verify / upload phase ----
    phase_label = "Verify" if args.verify_only else "Verify + upload"
    print(f"\n=== {phase_label} phase ({args.jobs} workers) ===\n")

    upload_succeeded, upload_failed = run_upload_phase(
        upload_candidates,
        args.jobs,
        blob_service_client=blob_service_client,
        container=args.container,
        existing_blobs=existing_blobs,
        upstream_map=upstream_map,
        verify_only=args.verify_only,
        quiet=args.quiet,
    )

    # ---- Summary ----
    _print_summary(
        total=len(components),
        download_failed=download_failed,
        upload_succeeded=upload_succeeded,
        upload_failed=upload_failed,
        failed_output=args.failed_output,
        phase_label=phase_label,
        skip_download=args.skip_download,
        jobs=args.jobs,
    )

    return 1 if (download_failed or upload_failed) else 0


if __name__ == "__main__":
    sys.exit(main())
