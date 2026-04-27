#!/usr/bin/env python3
"""
Check rendered specs for drift.

Runs inside the render container: compares the committed specs tree against
the working tree (after `azldev component render -a` has been run) and writes
a JSON report and a git patch to the mounted output volume. The host never
invokes git against PR data, so this script runs in a trusted environment
and doesn't need host-side hardening against poisoned .git/config.

Usage:
    python3 check_rendered_specs.py --specs-dir specs
    python3 check_rendered_specs.py --specs-dir specs --report report.json --patch fix.patch

Exit codes:
    0 — specs are up to date (timestamp-only noise filtered)
    1 — real diffs, extra files, or missing files detected
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Matches the azldev-generated changelog line.
# Tightly coupled to the format emitted by azldev's render pipeline; if azldev
# ever changes the emitted form (email suffix, version tag, different
# whitespace) this regex must be updated or every spec will look like drift.
# Owner: azure-linux-dev-tools (cmd that emits "* <date> azldev <user@example.com>" lines).
# e.g. "* Wed Apr 08 2026 azldev <azurelinux@microsoft.com> - 1.0-1"
_CHANGELOG_DATE_RE = re.compile(
    r"^\* [A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-9]{4} azldev\b"
)

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _git_bytes(*args: str) -> bytes:
    """Run a git command and return stdout (bytes)."""
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def _git_lines_z(*args: str) -> list[str]:
    """Run a git command with -z-compatible args and return NULL-split lines."""
    out = _git_bytes(*args)
    return [p.decode("utf-8") for p in out.split(b"\x00") if p]


def _resolve_head_blobs(paths: list[str]) -> dict[str, str]:
    """Map each path to its HEAD blob SHA, or '' if not present in HEAD.

    Resolves paths via `git ls-tree -z HEAD -- <paths...>` rather than the
    `git show HEAD:<path>` rev-parse syntax. The latter chokes on perfectly
    legal filenames containing `:` (interpreted as the rev/path separator)
    and leading `-` (parsed as options); `--` after `ls-tree` makes the path
    list unambiguous, and `-z` keeps newline-bearing filenames intact.
    """
    if not paths:
        return {}
    raw = _git_bytes("ls-tree", "-z", "HEAD", "--", *paths).decode("utf-8")
    out: dict[str, str] = {p: "" for p in paths}
    for entry in raw.split("\0"):
        if not entry:
            continue
        # Format: "<mode> <type> <sha>\t<path>"
        meta, _, path = entry.partition("\t")
        try:
            _, kind, sha = meta.split(" ")
        except ValueError:
            continue
        if kind != "blob":
            # Submodule (commit) or tree — not a regular file we can diff.
            continue
        out[path] = sha
    return out


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------


def normalize_changelog_date(text: str) -> str:
    """Replace the date on azldev changelog entries with a placeholder."""
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        if _CHANGELOG_DATE_RE.match(line):
            line = _CHANGELOG_DATE_RE.sub("* DATEPLACEHOLDER azldev", line)
        out.append(line)
    return "".join(out)


# ---------------------------------------------------------------------------
# Diff / classification
# ---------------------------------------------------------------------------


def component_from_path(file_path: str) -> str:
    """Extract the component name from a specs path.

    The component is always the direct parent directory:
    specs/a/acl/acl.spec → acl
    /abs/path/specs/n/nano/nano.spec → nano
    """
    return Path(file_path).parent.name


def classify_changes(specs_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (changed, extra, missing) file lists under specs_dir.

    The three lists are disjoint: changed contains only modified files,
    missing contains only deleted files, and extra contains untracked files.

    Untracked enumeration deliberately does NOT honor `.gitignore` — a
    malicious PR could otherwise commit a `.gitignore` under specs_dir to
    hide newly rendered files and make the check green. We also drop any
    `.gitignore`/`.gitattributes` files found under specs_dir since they
    have no business in a rendered-output tree.
    """
    sd = str(specs_dir)
    changed = _git_lines_z("diff", "-z", "--diff-filter=M", "--name-only", "--", sd)
    # No --exclude-standard: list ALL untracked files so a PR-committed
    # .gitignore under specs_dir can't hide drift.
    extra_raw = _git_lines_z("ls-files", "-z", "--others", "--", sd)
    missing = _git_lines_z("ls-files", "-z", "--deleted", "--", sd)
    # Filter out .gitignore / .gitattributes anywhere under specs_dir — they
    # shouldn't be in rendered output and shouldn't influence our enumeration.
    extra = [
        p for p in extra_raw if Path(p).name not in (".gitignore", ".gitattributes")
    ]
    return changed, extra, missing


def filter_timestamp_noise(changed_files: list[str], specs_dir: Path) -> list[dict]:
    """Filter changed files to only those with real (non-timestamp) diffs.

    Only .spec files are checked for timestamp noise — other file types
    (patches, GPG keys, etc.) are always treated as real changes.
    """
    real_diffs: list[dict] = []
    # Resolve all HEAD blob hashes up front so we can fetch each file's
    # committed contents by hash (`git cat-file blob <sha>`) instead of by
    # rev-parse string (`git show HEAD:<path>`). The hash form sidesteps a
    # whole class of path-parsing pitfalls — colons, leading dashes, etc.
    head_blobs = _resolve_head_blobs(changed_files)
    for path_str in changed_files:
        file_path = Path(path_str)
        is_spec = file_path.suffix == ".spec"

        # Symlinks in a rendered-output tree are suspicious (could point
        # anywhere on the runner's filesystem). Flag and skip content reads.
        if file_path.is_symlink():
            print(
                f"::warning::Symlink in rendered-specs tree, treated as drift: {path_str}",
                file=sys.stderr,
            )
            real_diffs.append(
                {
                    "path": path_str,
                    "component": component_from_path(path_str),
                    "diff": f"Symlink {path_str} — refusing to follow",
                }
            )
            continue

        # Read committed version via blob hash (path-safe). If the path
        # didn't resolve to a blob in HEAD, treat it as drift rather than
        # silently dropping it — git diff said it changed, so something
        # really is going on.
        sha = head_blobs.get(path_str, "")
        if not sha:
            print(
                f"::warning::could not resolve HEAD blob for {path_str}; "
                "treating as drift",
                file=sys.stderr,
            )
            real_diffs.append(
                {
                    "path": path_str,
                    "component": component_from_path(path_str),
                    "diff": f"{path_str} changed but HEAD blob unresolved",
                }
            )
            continue
        try:
            committed_bytes = _git_bytes("cat-file", "blob", sha)
        except subprocess.CalledProcessError as exc:
            print(
                f"::warning::git cat-file blob {sha} ({path_str}) failed: {exc}; "
                "treating as drift",
                file=sys.stderr,
            )
            real_diffs.append(
                {
                    "path": path_str,
                    "component": component_from_path(path_str),
                    "diff": f"{path_str} changed but HEAD content unreadable",
                }
            )
            continue

        # Try to decode as UTF-8; if it fails, it's binary — always a real diff
        try:
            committed = committed_bytes.decode("utf-8")
        except UnicodeDecodeError:
            real_diffs.append(
                {
                    "path": path_str,
                    "component": component_from_path(path_str),
                    "diff": f"Binary file {path_str} differs",
                }
            )
            continue

        # Read working tree; use O_NOFOLLOW-equivalent guard above (is_symlink),
        # and strict decode so true binaries route through the binary branch.
        try:
            working_bytes = file_path.read_bytes()
        except FileNotFoundError:
            print(
                f"::warning::working tree file missing during read: {path_str}",
                file=sys.stderr,
            )
            continue
        try:
            working = working_bytes.decode("utf-8")
        except UnicodeDecodeError:
            real_diffs.append(
                {
                    "path": path_str,
                    "component": component_from_path(path_str),
                    "diff": f"Binary file {path_str} differs",
                }
            )
            continue

        if is_spec:
            norm_committed = normalize_changelog_date(committed)
            norm_working = normalize_changelog_date(working)
        else:
            norm_committed = committed
            norm_working = working

        # Equality check on the *normalised* text filters out timestamp-only
        # drift (the whole point of this function). If the normalised
        # versions match, skip.
        if norm_committed == norm_working:
            continue

        # Use the original diff for display purposes.
        udiff = "".join(
            difflib.unified_diff(
                committed.splitlines(keepends=True),
                working.splitlines(keepends=True),
                fromfile=f"committed/{path_str}",
                tofile=f"rendered/{path_str}",
            )
        )

        real_diffs.append(
            {
                "path": path_str,
                "component": component_from_path(path_str),
                "diff": udiff,
            }
        )

    return real_diffs


# ---------------------------------------------------------------------------
# Report building
# ---------------------------------------------------------------------------


def build_report(
    content_diffs: list[dict],
    extra_files: list[str],
    missing_files: list[str],
) -> dict:
    """Build the JSON-serialisable report."""
    return {
        "content_diffs": content_diffs,
        "extra_files": [
            {"path": p, "component": component_from_path(p)} for p in extra_files
        ],
        "missing_files": [
            {"path": p, "component": component_from_path(p)} for p in missing_files
        ],
    }


# ---------------------------------------------------------------------------
# Comment formatting
# ---------------------------------------------------------------------------


def _unique_components(items: list[dict]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        c = item["component"]
        if c not in seen:
            seen.add(c)
            out.append(c)
    out.sort()
    return out


# NOTE: _unique_components and _render_command are duplicated in post_render_comment.py
def _render_command(components: list[str], use_all: bool = False) -> str:
    if use_all or len(components) > 30:
        return "azldev component render -a --clean-stale"
    return f"azldev component render {' '.join(components)}"


def generate_patch(
    content_diffs: list[dict],
    extra_files: list[str],
    missing_files: list[str],
    specs_dir: Path,
) -> bytes:
    """Generate a git patch covering all detected drift.

    Uses `git add -N` to mark untracked (extra) files as intent-to-add,
    then runs `git diff` scoped to `specs_dir` to capture modified,
    new, and deleted files in one clean patch.

    Scaling + path-safety notes:
      * `git add -N` / `git reset` receive the exact extra-file list via
        `--pathspec-from-file=- --pathspec-file-nul` (NUL-separated stdin).
        NUL separators match the rest of this script (`-z` on every reading
        side) and are the only delimiter that's safe for arbitrary paths —
        filenames may legally contain newlines, which would otherwise be
        split into bogus pathspec entries. This also avoids both ARG_MAX
        limits and the "pathspec file outside working tree" check that
        `git` does on on-disk pathspec files.
      * `git diff` does *not* support `--pathspec-from-file` (verified
        on git 2.45 — only `add`/`reset`/`commit`/`checkout`/`restore`
        do). Instead of batching, we scope the diff to `specs_dir` with a
        single positional pathspec. Render only touches files under that
        directory, so this captures exactly the same drift regardless of
        file count — scales cleanly to 10k+ files.
    """
    if not (content_diffs or extra_files or missing_files):
        return b""

    # NUL-separated stdin for --pathspec-file-nul. See docstring for why.
    extra_stdin = (
        b"\x00".join(p.encode("utf-8") for p in extra_files) + b"\x00"
        if extra_files
        else b""
    )

    # Mark untracked files as intent-to-add so `git diff` picks them up as
    # "new file" entries instead of silently skipping them.
    if extra_files:
        try:
            subprocess.run(
                [
                    "git",
                    "add",
                    "-N",
                    "--pathspec-from-file=-",
                    "--pathspec-file-nul",
                ],
                input=extra_stdin,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
            print(
                f"::warning::git add -N failed: exit={exc.returncode}: {stderr}",
                file=sys.stderr,
            )

    try:
        try:
            result = subprocess.run(
                ["git", "diff", "--", str(specs_dir)],
                capture_output=True,
                check=True,
            )
            patch = result.stdout
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
            print(
                f"::warning::git diff failed while generating patch: "
                f"exit={exc.returncode}: {stderr}",
                file=sys.stderr,
            )
            patch = b""
    finally:
        # Undo the intent-to-add so the index is left the way we found it.
        if extra_files:
            try:
                subprocess.run(
                    [
                        "git",
                        "reset",
                        "--pathspec-from-file=-",
                        "--pathspec-file-nul",
                    ],
                    input=extra_stdin,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as exc:
                stderr = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
                print(
                    f"::warning::git reset (undo intent-to-add) failed: "
                    f"exit={exc.returncode}: {stderr}",
                    file=sys.stderr,
                )

    return patch


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check rendered specs for drift. Outputs a JSON report and optional patch."
    )
    parser.add_argument(
        "--specs-dir",
        type=Path,
        required=True,
        help="Path to the rendered specs directory",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Write JSON report to this path",
    )
    parser.add_argument(
        "--patch",
        type=Path,
        default=None,
        help="Write a .patch file for all detected drift",
    )
    args = parser.parse_args()

    specs_dir = args.specs_dir

    # 1. Classify changes
    changed, extra, missing = classify_changes(specs_dir)
    print(
        f"Raw counts: changed={len(changed)} extra={len(extra)} missing={len(missing)}"
    )

    # 2. Filter timestamp noise from content diffs
    content_diffs = filter_timestamp_noise(changed, specs_dir)
    print(f"After timestamp filtering: {len(content_diffs)} real content diff(s)")

    # 3. Build report
    report = build_report(content_diffs, extra, missing)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Report written to {args.report}")

    total = len(content_diffs) + len(extra) + len(missing)

    # 4. Generate patch for all drift
    if args.patch and total > 0:
        patch_content = generate_patch(content_diffs, extra, missing, specs_dir)
        if patch_content:
            args.patch.parent.mkdir(parents=True, exist_ok=True)
            args.patch.write_bytes(patch_content)
            print(f"Patch written to {args.patch}")

    # 5. Print summary and exit
    if total == 0:
        print("All rendered specs are up to date (timestamp-only noise filtered).")
        return 0

    print(
        f"::error::{len(content_diffs)} content diff(s), "
        f"{len(extra)} extra file(s), {len(missing)} missing file(s)"
    )
    all_comps = sorted(
        set(
            _unique_components(content_diffs)
            + _unique_components(report.get("missing_files", []))
        )
    )
    if extra or missing:
        print(f"Remediation: {_render_command([], use_all=True)}")
    elif all_comps:
        print(f"Remediation: {_render_command(all_comps)}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
