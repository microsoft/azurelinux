#!/usr/bin/env python3
"""Migrate Azure Linux lookaside source tarballs into a target storage account.

This script scans every ``specs/<letter>/<pkg>/sources`` file in the repo,
resolves each referenced source artifact to its blob path in the public
lookaside store, verifies that all of them actually exist there, and then
server-side copies each blob into a target storage account/container under the
*identical* path. Copies run in parallel with retries; failures are recorded so
a subsequent run can resume straight from the failed set.

Source layout (public, anonymous read access)::

    https://<source-account>.blob.core.windows.net/<source-container>/pkgs/$pkg/$filename/$hashtype/$hash/$filename

where ``$pkg`` is the parent directory of the ``sources`` file, ``$filename`` is
the artifact name, ``$hashtype``/``$hash`` come from the ``sources`` file (both
lower-cased in the URL), and ``md5`` is assumed for the legacy ``sources``
format that omits the hash type.

The destination uses the same ``pkgs/.../`` path inside a user-provided account
and container. The target requires authentication; the caller is expected to be
logged in via ``az login`` (credentials are taken from ``AzureCliCredential``).

Resume file: if the resume file exists and is non-empty, detection and
verification are skipped and only the source URLs it lists are (re)uploaded.
Otherwise all sources are detected, verified, and uploaded, and any failures are
written to the resume file for the next run.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from azure.core.exceptions import AzureError, ResourceNotFoundError
from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient, ContainerClient

if TYPE_CHECKING:
    from collections.abc import Iterator

    from azure.storage.blob import BlobClient

DEFAULT_SOURCE_ACCOUNT = "azltempstaginglookaside"
DEFAULT_SOURCE_CONTAINER = "repo"
BLOB_PREFIX = "pkgs"
DEFAULT_RESUME_FILE = "sources-upload-failures.txt"
DEFAULT_TAGS = (("Origin", "Initial hydration with Beta build sources"),)
DEFAULT_RETRIES = 3
DEFAULT_WORKERS_PER_CPU = 10
COPY_POLL_INTERVAL_S = 2.0
COPY_TIMEOUT_S = 600.0
BACKOFF_BASE_S = 2.0
PROGRESS_INTERVAL = 200
TERMINAL_FAILURE_STATES = frozenset({"failed", "aborted"})


def log_error(msg: str) -> None:
    """Print an ``ERROR:``-prefixed message to stderr."""
    print(f"ERROR: {msg}", file=sys.stderr)


def log_warning(msg: str) -> None:
    """Print a ``WARNING:``-prefixed message to stderr."""
    print(f"WARNING: {msg}", file=sys.stderr)


def report_progress(done: int, total: int, label: str, failed: int = 0, *, force: bool = False) -> None:
    """Print a throttled ``done/total`` progress line (every ``PROGRESS_INTERVAL`` or at the end)."""
    if force or done == total or done % PROGRESS_INTERVAL == 0:
        suffix = f" ({failed} failed)" if failed else ""
        print(f"  {label}: {done}/{total}{suffix}", flush=True)


# BSD digest format, e.g. ``SHA512 (foo-1.0.tar.gz) = abcdef...``.
_BSD_RE = re.compile(r"^(\w+) \((.+)\) = ([0-9a-fA-F]+)$")
# Legacy coreutils format with an implicit md5 type, e.g. ``abcd...  foo.tar.gz``.
_OLD_RE = re.compile(r"^([0-9a-fA-F]{32})\s+(.+)$")


@dataclass(slots=True)
class Entry:
    """A single source artifact to migrate.

    Attributes:
        blob_path: Path of the blob within its container (``pkgs/.../filename``),
            identical for the source and the target.
        source_url: Fully-qualified public URL of the source blob.
        source_size: Size of the source blob in bytes, when known.
    """

    blob_path: str
    source_url: str
    source_size: int | None = None


@dataclass(slots=True)
class CopyContext:
    """Shared state for the copy/tag pipeline.

    Attributes:
        target_container: Destination container client (authenticated).
        source_container: Public source container client (anonymous).
        tags: Blob index tags to apply to each uploaded source.
    """

    target_container: ContainerClient
    source_container: ContainerClient
    tags: dict[str, str]


def parse_sources_line(line: str) -> tuple[str, str, str] | None:
    """Parse one ``sources`` line into ``(filename, hashtype, hash)``.

    Both the hash type and hash value are lower-cased to match the URL scheme.
    Returns ``None`` when the line matches neither supported format.
    """
    bsd = _BSD_RE.match(line)
    if bsd is not None:
        hashtype, filename, hashval = bsd.group(1), bsd.group(2), bsd.group(3)
        return filename, hashtype.lower(), hashval.lower()

    old = _OLD_RE.match(line)
    if old is not None:
        hashval, filename = old.group(1), old.group(2)
        return filename.strip(), "md5", hashval.lower()

    return None


def parse_sources_file(path: Path) -> Iterator[tuple[str, str, str]]:
    """Yield ``(filename, hashtype, hash)`` for each entry in a ``sources`` file.

    Blank lines are ignored; unrecognized lines emit a warning and are skipped.
    """
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        parsed = parse_sources_line(line)
        if parsed is None:
            log_warning(f"unrecognized line in {path}: {raw!r}")
            continue
        yield parsed


def discover_entries(
    specs_dir: Path,
    source_base_url: str,
    components: set[str] | None = None,
) -> dict[str, Entry]:
    """Walk ``specs/*/*/sources`` and build a deduplicated map of blob path to entry.

    When ``components`` is given, only sources for those package names are included.
    """
    entries: dict[str, Entry] = {}
    for sources_file in sorted(specs_dir.glob("*/*/sources")):
        pkg = sources_file.parent.name
        # Skip compatibility symlinks (e.g. ``dbus-c%2B%2B`` -> ``dbus-c++``); the real
        # directory is walked separately, so the symlink would only add a phantom
        # entry whose percent-encoded name does not exist in the source store.
        if sources_file.parent.is_symlink():
            continue
        if components is not None and pkg not in components:
            continue
        for filename, hashtype, hashval in parse_sources_file(sources_file):
            blob_path = f"{BLOB_PREFIX}/{pkg}/{filename}/{hashtype}/{hashval}/{filename}"
            if blob_path not in entries:
                entries[blob_path] = Entry(
                    blob_path=blob_path,
                    source_url=f"{source_base_url}/{blob_path}",
                )
    return entries


def load_resume_entries(path: Path, source_base_url: str) -> list[Entry]:
    """Reconstruct entries from a resume file containing one source URL per line."""
    prefix = f"{source_base_url}/"
    entries: list[Entry] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        url = raw.strip()
        if not url or url.startswith("#"):
            continue
        if not url.startswith(prefix):
            log_warning(f"skipping resume URL with unexpected prefix: {url}")
            continue
        entries.append(Entry(blob_path=url[len(prefix) :], source_url=url))
    return entries


def verify_sources(
    entries: list[Entry],
    source_container: ContainerClient,
    workers: int,
) -> list[Entry]:
    """Check each source blob exists (anonymous read); fill sizes and return the missing ones.

    The public source grants anonymous blob read but not container listing, so each
    blob is probed individually rather than enumerated.
    """
    missing: list[Entry] = []

    def probe(entry: Entry) -> tuple[Entry, int | None]:
        return entry, fetch_source_size(source_container, entry.blob_path)

    total = len(entries)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for done, (entry, size) in enumerate(pool.map(probe, entries), start=1):
            if size is None:
                missing.append(entry)
            else:
                entry.source_size = size
            report_progress(done, total, "verified", len(missing))
    return missing


def fetch_source_size(source_container: ContainerClient, blob_path: str) -> int | None:
    """Return the size of a single source blob in bytes, or ``None`` if it is absent."""
    try:
        return source_container.get_blob_client(blob_path).get_blob_properties().size
    except ResourceNotFoundError:
        return None


def apply_tags(entry: Entry, dest: BlobClient, tags: dict[str, str]) -> bool:
    """Set blob index tags on a destination blob; return whether it succeeded."""
    if not tags:
        return True
    try:
        dest.set_blob_tags(tags)
    except AzureError as err:
        log_error(f"failed to set tags for {entry.blob_path}: {err}")
        return False
    return True


def initiate_copy(entry: Entry, ctx: CopyContext) -> tuple[Entry, str, BlobClient | None]:
    """Start a server-side copy for one entry, skipping it if already present.

    Returns the entry, an outcome (``"skipped"``, ``"initiated"`` or
    ``"error"``), and the destination blob client when a copy was started.
    Already-present blobs still have their tags refreshed.
    """
    dest = ctx.target_container.get_blob_client(entry.blob_path)

    source_size = entry.source_size
    if source_size is None:
        source_size = fetch_source_size(ctx.source_container, entry.blob_path)

    try:
        existing = dest.get_blob_properties()
    except ResourceNotFoundError:
        existing = None

    if existing is not None and source_size is not None and existing.size == source_size:
        if not apply_tags(entry, dest, ctx.tags):
            return entry, "error", None
        return entry, "skipped", None

    try:
        dest.start_copy_from_url(entry.source_url)
    except AzureError as err:
        log_error(f"failed to start copy for {entry.source_url}: {err}")
        return entry, "error", None

    return entry, "initiated", dest


def poll_copy(entry: Entry, dest: BlobClient, tags: dict[str, str]) -> tuple[Entry, bool]:
    """Poll a started copy until it completes, fails, or times out.

    On success the configured tags are applied. Returns the entry and whether
    the copy (and tagging) succeeded.
    """
    deadline = time.monotonic() + COPY_TIMEOUT_S
    while True:
        try:
            copy = dest.get_blob_properties().copy
        except AzureError as err:
            log_error(f"failed to query copy status for {entry.blob_path}: {err}")
            return entry, False

        status = copy.status or "unknown"
        if status == "success":
            return entry, apply_tags(entry, dest, tags)
        if status in TERMINAL_FAILURE_STATES:
            log_error(f"copy {status} for {entry.source_url}: {copy.status_description or 'no detail'}")
            return entry, False

        if time.monotonic() >= deadline:
            if copy.id is not None:
                try:
                    dest.abort_copy(copy.id)
                except AzureError as err:
                    log_warning(f"failed to abort timed-out copy for {entry.blob_path}: {err}")
            log_error(f"copy timed out after {COPY_TIMEOUT_S:.0f}s for {entry.source_url}")
            return entry, False

        time.sleep(COPY_POLL_INTERVAL_S)


def run_upload_round(entries: list[Entry], ctx: CopyContext, workers: int) -> list[Entry]:
    """Run one fire-all-copies-then-batch-poll round; return the entries that failed."""
    initiated: list[tuple[Entry, BlobClient]] = []
    failures: list[Entry] = []
    skipped = 0

    total = len(entries)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(initiate_copy, entry, ctx) for entry in entries]
        for done, future in enumerate(as_completed(futures), start=1):
            entry, outcome, dest = future.result()
            if outcome == "initiated" and dest is not None:
                initiated.append((entry, dest))
            elif outcome == "skipped":
                skipped += 1
            else:
                failures.append(entry)
            report_progress(done, total, "started", len(failures))

    if skipped:
        print(f"Skipped {skipped} blob(s) already present with matching size.", flush=True)
    if initiated:
        print(f"Waiting for {len(initiated)} copy operation(s) to complete...", flush=True)

    poll_total = len(initiated)
    poll_failures = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        poll_futures = [pool.submit(poll_copy, entry, dest, ctx.tags) for entry, dest in initiated]
        for done, future in enumerate(as_completed(poll_futures), start=1):
            entry, ok = future.result()
            if not ok:
                failures.append(entry)
                poll_failures += 1
            report_progress(done, poll_total, "copied", poll_failures)

    return failures


def upload_entries(entries: list[Entry], ctx: CopyContext, workers: int, retries: int) -> list[Entry]:
    """Upload all entries with retries; return the entries still failing after all attempts."""
    pending = entries
    for attempt in range(1, retries + 1):
        print(f"Upload attempt {attempt}/{retries} for {len(pending)} blob(s)...")
        failures = run_upload_round(pending, ctx, workers)
        if not failures:
            return []
        if attempt < retries:
            backoff = BACKOFF_BASE_S * 2 ** (attempt - 1)
            log_warning(f"{len(failures)} failure(s); retrying in {backoff:.0f}s...")
            time.sleep(backoff)
        pending = failures
    return pending


def write_failures(path: Path, failures: list[Entry]) -> None:
    """Write the source URLs of failed uploads to the resume file, one per line."""
    path.write_text("\n".join(entry.source_url for entry in failures) + "\n", encoding="utf-8")


def resolve_entries(
    args: argparse.Namespace,
    source_base_url: str,
    source_container: ContainerClient,
) -> list[Entry] | None:
    """Resolve the entries to upload, either from the resume file or by detection.

    Returns the list of entries, an empty list when there is nothing to do, or
    ``None`` when verification found missing sources (a hard error).
    """
    resume_path: Path = args.resume_file
    if resume_path.exists() and resume_path.stat().st_size > 0:
        print(f"Resume file {resume_path} found; uploading only its URLs (detection skipped).")
        return load_resume_entries(resume_path, source_base_url)

    discovered = discover_entries(
        args.specs_dir,
        source_base_url,
        set(args.component) if args.component else None,
    )
    if not discovered:
        print(f"No sources found under {args.specs_dir}.")
        return []
    entries = list(discovered.values())
    print(f"Discovered {len(entries)} unique source(s).")

    print(f"Verifying {len(entries)} source(s) exist under {source_base_url}/{BLOB_PREFIX}/ ...")
    missing = verify_sources(entries, source_container, args.workers)
    if missing:
        log_error(f"{len(missing)} source(s) missing from {source_base_url}:")
        for entry in missing:
            print(f"  {entry.source_url}", file=sys.stderr)
        return None
    return entries


def parse_tag(item: str) -> tuple[str, str]:
    """Parse one ``KEY=VALUE`` tag string for argparse ``type=``."""
    key, sep, value = item.partition("=")
    if not sep or not key:
        msg = f"invalid tag {item!r}; expected KEY=VALUE"
        raise argparse.ArgumentTypeError(msg)
    return key, value


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("account_name", help="Target storage account name.")
    parser.add_argument("container", help="Target container name.")
    parser.add_argument(
        "--specs-dir",
        type=Path,
        default=Path("specs"),
        help="Directory containing specs/<letter>/<pkg>/sources files (default: %(default)s).",
    )
    parser.add_argument(
        "--resume-file",
        type=Path,
        default=Path(DEFAULT_RESUME_FILE),
        help="File of failed source URLs; reused to resume a previous run (default: %(default)s).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS_PER_CPU * (os.cpu_count() or 1),
        help="Number of parallel copy/poll workers (default: 10x CPU count = %(default)s).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help="Number of upload attempts before giving up (default: %(default)s).",
    )
    parser.add_argument(
        "--source-account",
        default=DEFAULT_SOURCE_ACCOUNT,
        help="Public source storage account name (default: %(default)s).",
    )
    parser.add_argument(
        "--source-container",
        default=DEFAULT_SOURCE_CONTAINER,
        help="Public source container name (default: %(default)s).",
    )
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="PKG",
        help="Limit migration to this component (package) name. Repeatable.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        type=parse_tag,
        default=list(DEFAULT_TAGS),
        metavar="KEY=VALUE",
        help="Blob index tag to set on each uploaded source. Repeatable (default: Origin=...).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Detect and verify sources, print what would be copied, but do not copy.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the source migration and return a process exit code."""
    args = parse_args()
    tags: dict[str, str] = dict(args.tag)

    # Line-buffer stdout so progress is visible live, even when redirected to a file.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(line_buffering=True)

    source_account_url = f"https://{args.source_account}.blob.core.windows.net"
    source_base_url = f"{source_account_url}/{args.source_container}"
    source_container = ContainerClient(
        account_url=source_account_url,
        container_name=args.source_container,
        credential=None,
    )
    target_service = BlobServiceClient(
        account_url=f"https://{args.account_name}.blob.core.windows.net",
        credential=AzureCliCredential(),
    )
    target_container = target_service.get_container_client(args.container)

    # Cheap reachability/permission check so auth or naming problems surface early.
    try:
        target_container.get_container_properties()
    except AzureError as err:
        log_error(f"cannot access target container '{args.container}' in account '{args.account_name}': {err}")
        return 1

    entries = resolve_entries(args, source_base_url, source_container)
    if entries is None:
        return 1
    if not entries:
        return 0

    if args.dry_run:
        print(f"Dry run: would upload {len(entries)} blob(s):")
        for entry in sorted(entries, key=lambda e: e.blob_path):
            print(f"  {entry.blob_path}")
        if tags:
            print("Tags to apply: " + ", ".join(f"{k}={v}" for k, v in tags.items()))
        return 0

    resume_path: Path = args.resume_file
    ctx = CopyContext(target_container=target_container, source_container=source_container, tags=tags)
    failures = upload_entries(entries, ctx, args.workers, args.retries)
    if failures:
        write_failures(resume_path, failures)
        log_error(
            f"{len(failures)} upload(s) failed after {args.retries} attempt(s). "
            f"Failed source URLs written to {resume_path}.",
        )
        return 1

    print(f"Done: {len(entries)} source(s) uploaded or already present.")
    if resume_path.exists():
        resume_path.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
