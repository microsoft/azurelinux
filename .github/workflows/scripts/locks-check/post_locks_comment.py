#!/usr/bin/env python3
"""
Post (or update/delete) a PR comment with `azldev component update` results.

Reads the JSON output produced by `azldev component update -a -O json` and
posts a formatted comment listing components whose lock files would change.
Designed to run in a workflow_run-style context where the base repo's
GITHUB_TOKEN is available (needed for fork PRs).

Update JSON shape (top-level on stdout):
    null                                     — no entries produced
    [ {component, upstreamCommit, changed},  — one entry per component;
      ... ]                                    only entries with changed=true
                                               are reflected in the comment

Usage:
    python post_locks_comment.py \\
        --update-output update-output.json \\
        --repo owner/repo \\
        --pr 123 \\
        --artifacts-url https://... \\
        --run-id 12345

Exit codes:
    0 — comment posted/updated/deleted successfully
    1 — error reading update output, unexpected JSON shape, or missing arguments

Environment:
    GH_TOKEN — required for GitHub API calls
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMMENT_MARKER = "<!-- LOCKS_CHECK -->"
MAX_FILE_LIST = 50
MAX_COMMENT_CHARS = 60_000
# Safety margin under MAX_COMMENT_CHARS — leaves room for the trailing
# "... N more" summary + section footers that are appended after the budget
# check trips.
COMMENT_BUDGET_MARGIN = 2000
# Hard cap on any individual displayed component name. See post_render_comment.py
# for the rationale; lock files are keyed on component names which are
# similarly conservative but we still bound them defensively.
MAX_DISPLAY_NAME_LEN = 200

# Author of comments we own. Only comments from this user are eligible for
# update/delete — prevents hijacking a PR-author comment that happens to
# contain our marker.
BOT_AUTHOR = "github-actions[bot]"

# Bare-integer validator for comment IDs returned from the GitHub API.
_ID_RE = re.compile(r"^[0-9]+$")

# Component names rendered into markdown must not break code spans or
# introduce HTML. Component names in this repo are conservative ASCII.
_SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._\-+]+$")

# Upstream commit hashes are 40-char (or shorter abbreviated) hex.
_SAFE_COMMIT_RE = re.compile(r"^[a-f0-9]{4,64}$")


def _safe_name(name: str) -> str:
    """Return a markdown-safe, length-bounded rendering of a component name."""
    if not _SAFE_NAME_RE.match(name):
        return "<unsafe name redacted>"
    if len(name) > MAX_DISPLAY_NAME_LEN:
        keep = MAX_DISPLAY_NAME_LEN - 20
        return f"{name[:keep]}...<{len(name) - keep} chars truncated>"
    return name


def _safe_commit(commit: str) -> str:
    """Return a markdown-safe rendering of an upstream commit hash."""
    if not _SAFE_COMMIT_RE.match(commit):
        return "<unsafe commit redacted>"
    return commit


# ---------------------------------------------------------------------------
# Update-output parsing
# ---------------------------------------------------------------------------


def parse_update_output(path: Path) -> list[dict]:
    """Parse the JSON emitted by `azldev component update -a -O json`.

    Returns a list of components whose ``changed`` field is True (possibly
    empty). Don't assume the JSON only contains changed entries — filter
    explicitly on the boolean. Hard-fails on unexpected JSON shape rather
    than silently treating it as "no drift" — better to surface a loud
    error than miss real drift.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise SystemExit(f"Error: update output not found: {exc}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: update output is not valid JSON: {exc}")

    # azldev emits a literal JSON `null` when no entries are produced.
    if data is None:
        return []

    if not isinstance(data, list):
        raise SystemExit(
            f"Error: update output has unexpected shape (expected null or list, "
            f"got {type(data).__name__})"
        )

    for entry in data:
        if (
            not isinstance(entry, dict)
            or "component" not in entry
            or "changed" not in entry
        ):
            raise SystemExit(
                f"Error: update output entry has unexpected shape: {entry!r}"
            )

    return [entry for entry in data if entry["changed"] is True]


# ---------------------------------------------------------------------------
# Comment formatting
# ---------------------------------------------------------------------------


def _update_command(components: list[str], use_all: bool = False) -> str:
    if use_all or len(components) > 30:
        return "azldev component update -a"
    return f"azldev component update {' '.join('-p ' + c for c in components)}"


def format_comment(
    changed: list[dict],
    artifacts_url: str | None = None,
    run_id: str | None = None,
    repo: str | None = None,
) -> str:
    n_changed = len(changed)

    comp_names: list[str] = sorted({entry["component"] for entry in changed})
    # Component names come from PR-controlled TOML; the remediation command
    # is rendered into a copy/paste-able `bash` code block, so any name
    # containing shell metacharacters or whitespace would let a fork PR
    # inject arbitrary commands into a maintainer's terminal. Fall back to
    # `-a` if any name fails the same regex used for display so the
    # printed command is always safe to run as-is.
    use_all = n_changed > 30 or any(
        not _SAFE_NAME_RE.match(name) for name in comp_names
    )
    remediation_cmd = _update_command([] if use_all else comp_names, use_all=use_all)

    lines: list[str] = [
        COMMENT_MARKER,
        "## 🔒❌ Lock files are out of date",
        "",
        "🚧🚧🚧🚧🚧",
        "",
        "> [!WARNING]",
        ">",
        "> **Disregard this comment.**",
        ">",
        "> Lock-file generation is still under development and checked-in",
        "> lock files should not be updated in PRs yet.",
        "> Please ignore this comment for now unless you are actively",
        "> working on the update pipeline.",
        "",
        "🚧🚧🚧🚧🚧",
        "",
        "**FIX:** — run this and commit the result:",
        "",
        "```bash",
        remediation_cmd,
        "```",
        "",
    ]

    if artifacts_url:
        lines.append(f"Or [download the fix patch]({artifacts_url}) and apply it:")
        lines.append("")
        if run_id and repo:
            lines.extend(
                [
                    "```bash",
                    f"gh run download {run_id} -R {repo} -n locks-patch",
                    "git apply locks.patch",
                    "```",
                ]
            )
        else:
            lines.extend(
                [
                    "```bash",
                    "git apply locks.patch",
                    "```",
                ]
            )
        lines.append("")

    lines.extend(
        [
            f"### Changed components ({n_changed})",
            "",
            "| Component | New upstream commit |",
            "|-----------|---------------------|",
        ]
    )

    body_so_far = len("\n".join(lines))
    budget_cap = MAX_COMMENT_CHARS - COMMENT_BUDGET_MARGIN

    shown = 0
    truncated_for_size = False
    # Sort by component name so the table is stable across reruns.
    for entry in sorted(changed[:MAX_FILE_LIST], key=lambda e: e["component"]):
        name = _safe_name(entry["component"])
        commit = entry.get("upstreamCommit", "")
        commit_display = _safe_commit(commit) if commit else "-"
        row = f"| `{name}` | `{commit_display}` |"
        if body_so_far + len(row) + 1 > budget_cap:
            truncated_for_size = True
            break
        lines.append(row)
        body_so_far += len(row) + 1
        shown += 1

    if truncated_for_size:
        remaining = n_changed - shown
        lines.append("")
        lines.append(
            f"*… and {remaining} more component(s) — comment size limit reached. "
            "Run the remediation command above to see all changes.*"
        )
    elif n_changed > MAX_FILE_LIST:
        remaining = n_changed - MAX_FILE_LIST
        lines.append("")
        lines.append(f"*… and {remaining} more component(s).*")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# GitHub comment posting
# ---------------------------------------------------------------------------


def _gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def find_existing_comments(repo: str, pr: str) -> list[str]:
    """Return IDs of all comments authored by the bot that carry our marker.

    Filtering by author prevents a PR author from posing as our comment
    (they could write a body containing the marker and get their comment
    edited/deleted by the bot). Returns all matches so stale duplicates
    (from past bugs or races) can be cleaned up.
    """
    try:
        output = _gh(
            "api",
            "--paginate",
            f"/repos/{repo}/issues/{pr}/comments",
            "--jq",
            (
                f'.[] | select(.user.login == "{BOT_AUTHOR}") '
                f'| select(.body | contains("{COMMENT_MARKER}")) '
                "| .id"
            ),
        )
    except subprocess.CalledProcessError:
        return []
    ids = [line.strip() for line in output.splitlines() if line.strip()]
    # Validate IDs are bare integers before interpolating into API URLs.
    return [i for i in ids if _ID_RE.match(i)]


def post_or_update_comment(repo: str, pr: str, body: str) -> None:
    existing_ids = find_existing_comments(repo, pr)
    fd, body_path = tempfile.mkstemp(prefix="locks-check-comment-", suffix=".md")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(body)
        if existing_ids:
            # Update the first, delete the rest (shouldn't normally exist).
            primary, *stale = existing_ids
            print(f"Updating existing comment {primary}")
            _gh(
                "api",
                "--method",
                "PATCH",
                f"/repos/{repo}/issues/comments/{primary}",
                "-F",
                f"body=@{body_path}",
            )
            for stale_id in stale:
                print(f"Deleting stale duplicate comment {stale_id}")
                try:
                    _gh(
                        "api",
                        "--method",
                        "DELETE",
                        f"/repos/{repo}/issues/comments/{stale_id}",
                    )
                except subprocess.CalledProcessError:
                    print(
                        f"Warning: failed to delete stale comment {stale_id}",
                        file=sys.stderr,
                    )
        else:
            print("Creating new comment")
            _gh("pr", "comment", pr, "--repo", repo, "--body-file", body_path)
    finally:
        Path(body_path).unlink(missing_ok=True)


def delete_comment_if_exists(repo: str, pr: str) -> None:
    for existing_id in find_existing_comments(repo, pr):
        print(f"Deleting stale comment {existing_id}")
        try:
            _gh(
                "api",
                "--method",
                "DELETE",
                f"/repos/{repo}/issues/comments/{existing_id}",
            )
        except subprocess.CalledProcessError:
            print(
                f"Warning: failed to delete stale comment {existing_id}",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Post `azldev component update` drift as a PR comment."
    )
    parser.add_argument(
        "--update-output",
        type=Path,
        required=True,
        help="Path to JSON output from `azldev component update -a -O json`",
    )
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--pr", required=True, help="PR number")
    parser.add_argument(
        "--artifacts-url", default=None, help="Direct URL to patch artifact"
    )
    parser.add_argument("--run-id", default=None, help="GitHub Actions run ID")
    args = parser.parse_args()

    changed = parse_update_output(args.update_output)

    body: str | None = None
    try:
        if not changed:
            delete_comment_if_exists(args.repo, args.pr)
        else:
            body = format_comment(
                changed,
                artifacts_url=args.artifacts_url,
                run_id=args.run_id,
                repo=args.repo,
            )
            post_or_update_comment(args.repo, args.pr, body)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"Warning: failed to post/update PR comment: {exc}", file=sys.stderr)

    # Write to GitHub step summary if available
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file and body:
        max_summary = 1_000_000  # GH step summary limit is 1024 KiB
        summary = body[:max_summary] if len(body) > max_summary else body
        with open(summary_file, "a", encoding="utf-8") as sf:
            sf.write(summary)
            sf.write("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
