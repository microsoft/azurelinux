#!/usr/bin/env python3
"""
Check rendered specs for drift and (optionally) post a PR comment.

Compares the committed specs tree against the working tree (after
`azldev component render -a` has been run) and reports meaningful differences,
filtering out changelog-timestamp noise.

Usage:
    # Just check (local dev, CI without comment posting):
    python check_rendered_specs.py --specs-dir specs

    # Check and post/update a PR comment:
    python check_rendered_specs.py --specs-dir specs --repo owner/repo --pr 123

Exit codes:
    0 — specs are up to date (timestamp-only noise filtered)
    1 — real diffs, extra files, or missing files detected

Environment:
    GH_TOKEN — required when --repo/--pr are given
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMMENT_MARKER = "<!-- RENDERED_SPEC_CHECK -->"
MAX_INLINE_DIFFS = 10
MAX_FILE_LIST = 50  # cap extra/missing file lists in comment
MAX_COMMENT_CHARS = 60_000  # GH limit is 65 535; leave headroom
MAX_STEP_SUMMARY = 1_000_000  # GH step summary limit is 1024 KiB

# Matches the azldev-generated changelog line.
# e.g. "* Wed Apr 08 2026 azldev <> - 1.0-1"
_CHANGELOG_DATE_RE = re.compile(
    r"^\* [A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-9]{4} azldev "
)

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _git(*args: str) -> str:
    """Run a git command and return stdout."""
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout


def _git_lines(*args: str) -> list[str]:
    """Run a git command and return non-empty output lines."""
    return [line for line in _git(*args).splitlines() if line]


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------


def normalize_changelog_date(text: str) -> str:
    """Replace the date on azldev changelog entries with a placeholder."""
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        if _CHANGELOG_DATE_RE.match(line):
            line = _CHANGELOG_DATE_RE.sub("* DATEPLACEHOLDER azldev ", line)
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
    """
    sd = str(specs_dir)
    changed = _git_lines("diff", "--diff-filter=M", "--name-only", "--", sd)
    extra = _git_lines("ls-files", "--others", "--exclude-standard", "--", sd)
    missing = _git_lines("ls-files", "--deleted", "--", sd)
    return changed, extra, missing


def filter_timestamp_noise(changed_files: list[str], specs_dir: Path) -> list[dict]:
    """Filter changed files to only those with real (non-timestamp) diffs.

    Only .spec files are checked for timestamp noise — other file types
    (patches, GPG keys, etc.) are always treated as real changes.
    """
    real_diffs: list[dict] = []
    for path_str in changed_files:
        file_path = Path(path_str)
        is_spec = file_path.suffix == ".spec"

        # Read committed version — use bytes to handle binary files
        try:
            committed_bytes = subprocess.run(
                ["git", "show", f"HEAD:{path_str}"],
                capture_output=True,
                check=True,
            ).stdout
        except subprocess.CalledProcessError:
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

        try:
            working = file_path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            continue

        if is_spec:
            norm_committed = normalize_changelog_date(committed)
            norm_working = normalize_changelog_date(working)
        else:
            norm_committed = committed
            norm_working = working

        if norm_committed == norm_working:
            continue

        udiff = "".join(
            difflib.unified_diff(
                norm_committed.splitlines(keepends=True),
                norm_working.splitlines(keepends=True),
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


def _render_command(components: list[str], use_all: bool = False) -> str:
    if use_all or len(components) > 30:
        return "azldev component render -a"
    return f"azldev component render {' '.join(components)}"


def format_comment(
    report: dict,
    artifacts_url: str | None = None,
    run_id: str | None = None,
    repo: str | None = None,
) -> str:
    content_diffs = report.get("content_diffs", [])
    extra_files = report.get("extra_files", [])
    missing_files = report.get("missing_files", [])

    n_diff = len(content_diffs)
    n_extra = len(extra_files)
    n_missing = len(missing_files)
    total = n_diff + n_extra + n_missing

    if total == 0:
        return f"{COMMENT_MARKER}\n## ✅ Rendered specs are up to date\n"

    all_comps: list[str] = sorted(
        set(_unique_components(content_diffs) + _unique_components(missing_files))
    )
    use_all = bool(extra_files)
    remediation_cmd = _render_command([] if use_all else all_comps, use_all=use_all)

    lines: list[str] = [
        COMMENT_MARKER,
        "## ❌ Rendered specs are out of date",
        "",
        "🚧🚧🚧🚧🚧",
        "",
        "> [!WARNING]",
        ">",
        "> **Disregard this comment.**",
        ">",
        "> Spec rendering is still under development and checked-in specs",
        "> should not be updated in PRs yet.",
        "> Please ignore this comment for now unless you are actively",
        "> working on the render pipeline.",
        "",
        "🚧🚧🚧🚧🚧",
        "",
        "**FIX:** — run this and commit the result:",
        "",
        f"```bash\n{remediation_cmd}\n```",
        "",
    ]

    if artifacts_url:
        lines.append(f"Or [download the fix patch]({artifacts_url}) and apply it:")
        lines.append("")
        if run_id and repo:
            lines.append(
                "```bash\n"
                f"gh run download {run_id} -R {repo} -n rendered-specs-patch\n"
                "git apply rendered-specs.patch\n"
                "```"
            )
        else:
            lines.append("```bash\ngit apply rendered-specs.patch\n```")
        lines.append("")

    lines.extend(
        [
            "| Category | Count |",
            "|----------|-------|",
            f"| Content diffs | {n_diff} |",
            f"| Extra files (untracked) | {n_extra} |",
            f"| Missing files (deleted) | {n_missing} |",
            "",
        ]
    )

    if content_diffs:
        lines.append("### Content diffs")
        lines.append("")
        shown = 0
        body_so_far = len("\n".join(lines))
        for item in content_diffs:
            if shown >= MAX_INLINE_DIFFS:
                remaining = n_diff - shown
                lines.append(
                    f"*… and {remaining} more file(s). "
                    "Run the remediation command above to see all changes.*"
                )
                lines.append("")
                break
            path = item["path"]
            diff_text = item.get("diff", "")
            block = (
                "<details>\n"
                f"<summary><code>{path}</code></summary>\n\n"
                f"```diff\n{diff_text}\n```\n\n"
                "</details>\n"
            )
            if body_so_far + len(block) > MAX_COMMENT_CHARS - 2000:
                remaining = n_diff - shown
                lines.append(
                    f"*… and {remaining} more file(s) — comment size limit reached. "
                    "Run the remediation command above to see all changes.*"
                )
                lines.append("")
                break
            lines.append(block)
            body_so_far += len(block)
            shown += 1

    if extra_files:
        lines.append("### Files to add")
        lines.append("")
        lines.append(
            "These files are produced by `azldev component render` but are "
            "missing from your branch. Add them."
        )
        lines.append("")
        for item in extra_files[:MAX_FILE_LIST]:
            lines.append(f"- `{item['path']}`")
        if len(extra_files) > MAX_FILE_LIST:
            lines.append(f"\n*… and {len(extra_files) - MAX_FILE_LIST} more file(s).*")
        lines.append("")

    if missing_files:
        lines.append("### Files to remove")
        lines.append("")
        lines.append(
            "These files are in your branch but are not produced by render. "
            "Remove them."
        )
        lines.append("")
        for item in missing_files[:MAX_FILE_LIST]:
            lines.append(f"- `{item['path']}`")
        if len(missing_files) > MAX_FILE_LIST:
            lines.append(
                f"\n*… and {len(missing_files) - MAX_FILE_LIST} more file(s).*"
            )
        lines.append("")

    return "\n".join(lines)


def generate_patch(
    content_diffs: list[dict],
    extra_files: list[str],
    missing_files: list[str],
) -> bytes:
    """Generate a git patch covering all detected drift.

    Uses `git add -N` to mark untracked (extra) files as intent-to-add,
    then runs `git diff` on the specific affected files to capture
    modified, new, and deleted files in one clean patch.
    """
    paths = [d["path"] for d in content_diffs] + extra_files + missing_files
    if not paths:
        return b""

    # Mark untracked files as intent-to-add so git diff includes them
    if extra_files:
        try:
            subprocess.run(
                ["git", "add", "-N", "--", *extra_files],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            pass

    try:
        result = subprocess.run(
            ["git", "diff", "--", *paths],
            capture_output=True,
            check=True,
        )
        patch = result.stdout
    except subprocess.CalledProcessError:
        patch = b""

    # Undo the intent-to-add so we don't leave index dirty
    if extra_files:
        try:
            subprocess.run(
                ["git", "reset", "--", *extra_files],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            pass

    return patch


# ---------------------------------------------------------------------------
# GitHub comment posting
# ---------------------------------------------------------------------------


def _gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def find_existing_comment(repo: str, pr: str) -> str | None:
    try:
        output = _gh(
            "api",
            "--paginate",
            f"/repos/{repo}/issues/{pr}/comments",
            "--jq",
            f'.[] | select(.body | contains("{COMMENT_MARKER}")) | .id',
        )
    except subprocess.CalledProcessError:
        return None
    comment_id = output.split("\n")[0].strip() if output else None
    return comment_id or None


def post_or_update_comment(repo: str, pr: str, body: str) -> None:
    existing_id = find_existing_comment(repo, pr)

    # Write body to a temp file to avoid ARG_MAX limits
    body_path = Path("render-check-comment.md")
    body_path.write_text(body, encoding="utf-8")
    try:
        if existing_id:
            print(f"Updating existing comment {existing_id}")
            _gh(
                "api",
                "--method",
                "PATCH",
                f"/repos/{repo}/issues/comments/{existing_id}",
                "-F",
                f"body=@{body_path}",
            )
        else:
            print("Creating new comment")
            _gh("pr", "comment", pr, "--repo", repo, "--body-file", str(body_path))
    finally:
        body_path.unlink(missing_ok=True)


def delete_comment_if_exists(repo: str, pr: str) -> None:
    existing_id = find_existing_comment(repo, pr)
    if existing_id:
        print(f"Deleting stale comment {existing_id}")
        try:
            _gh(
                "api",
                "--method",
                "DELETE",
                f"/repos/{repo}/issues/comments/{existing_id}",
            )
        except subprocess.CalledProcessError:
            print("Warning: failed to delete stale comment", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check rendered specs for drift and optionally post a PR comment."
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
    parser.add_argument("--repo", default=None, help="GitHub repo (owner/repo)")
    parser.add_argument("--pr", default=None, help="PR number")
    parser.add_argument(
        "--patch",
        type=Path,
        default=None,
        help="Write a .patch file for real content diffs",
    )
    parser.add_argument(
        "--artifacts-url",
        default=None,
        help="URL to the workflow run artifacts (linked in PR comment)",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="GitHub Actions run ID (for gh run download command in PR comment)",
    )
    args = parser.parse_args()

    if bool(args.repo) != bool(args.pr):
        print("Error: --repo and --pr must be provided together", file=sys.stderr)
        return 1

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

    # 3b. Generate patch for all drift
    if args.patch and total > 0:
        patch_content = generate_patch(content_diffs, extra, missing)
        if patch_content:
            args.patch.parent.mkdir(parents=True, exist_ok=True)
            args.patch.write_bytes(patch_content)
            print(f"Patch written to {args.patch}")

    # 4. Post comment or clean up (best-effort — exit code is authoritative)
    if args.repo and args.pr:
        try:
            if total == 0:
                delete_comment_if_exists(args.repo, args.pr)
            else:
                body = format_comment(
                    report,
                    artifacts_url=args.artifacts_url,
                    run_id=args.run_id,
                    repo=args.repo,
                )
                post_or_update_comment(args.repo, args.pr, body)
        except (subprocess.CalledProcessError, OSError) as exc:
            print(f"Warning: failed to post/update PR comment: {exc}", file=sys.stderr)

    # 5. Write to GitHub step summary if available
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file and total > 0:
        summary_body = format_comment(
            report, artifacts_url=args.artifacts_url, run_id=args.run_id, repo=args.repo
        )
        if len(summary_body) <= MAX_STEP_SUMMARY:
            with open(summary_file, "a", encoding="utf-8") as sf:
                sf.write(summary_body)
                sf.write("\n")
        else:
            print("Warning: step summary too large, skipping", file=sys.stderr)

    # 6. Print summary and exit
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
    if extra:
        print("Remediation: azldev component render -a")
    elif all_comps:
        print(f"Remediation: {_render_command(all_comps)}")

    return 1


if __name__ == "__main__":
    sys.exit(main())