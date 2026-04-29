#!/usr/bin/env python3
"""
Post (or update/delete) a PR comment with rendered-spec drift results.

Reads the JSON report produced by check_rendered_specs.py and posts a
formatted comment on the PR. Designed to run in a workflow_run context
where the base repo's GITHUB_TOKEN is available (needed for fork PRs).

Usage:
    python post_render_comment.py \\
        --report render-check-report.json \\
        --repo owner/repo \\
        --pr 123 \\
        --artifacts-url https://... \\
        --run-id 12345

Exit codes:
    0 — comment posted/updated/deleted successfully
    1 — error reading report or missing arguments

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

COMMENT_MARKER = "<!-- RENDERED_SPEC_CHECK -->"
MAX_INLINE_DIFFS = 10
MAX_FILE_LIST = 50
MAX_COMMENT_CHARS = 60_000
# Safety margin under MAX_COMMENT_CHARS — leaves room for the trailing
# "... N more" summary + section footers that are appended after the budget
# check trips.
COMMENT_BUDGET_MARGIN = 2000
# Hard cap on any individual displayed path. Even though _SAFE_PATH_RE filters
# characters, a fork PR can still create validly-named paths near PATH_MAX;
# without a length cap, 50 of those can blow past GitHub's 65_536-char comment
# limit and cause the whole post to fail (which was silent before).
MAX_DISPLAY_PATH_LEN = 200

# Author of comments we own. Only comments from this user are eligible for
# update/delete — prevents hijacking a PR-author comment that happens to
# contain our marker.
BOT_AUTHOR = "github-actions[bot]"

# Bare-integer validator for comment IDs returned from the GitHub API.
_ID_RE = re.compile(r"^[0-9]+$")

# Paths rendered into markdown must not break code spans or introduce HTML.
# Rendered-spec paths are well-known and conservative; anything else is
# replaced with a placeholder rather than trusted.
_SAFE_PATH_RE = re.compile(r"^[A-Za-z0-9._/\-]+$")


def _safe_path(path: str) -> str:
    """Return a markdown-safe, length-bounded rendering of `path`.

    Rendered-spec paths are expected to be ASCII-ish component/file names.
    Anything with backticks, angle brackets, whitespace, or other markdown
    metacharacters is replaced with a placeholder so an attacker-controlled
    filename can't inject HTML or break out of a code span. Paths longer
    than ``MAX_DISPLAY_PATH_LEN`` are truncated with an ellipsis marker so
    a fork PR can't push the total comment size past the GitHub API limit
    via pathologically long (but otherwise valid) filenames.
    """
    if not _SAFE_PATH_RE.match(path):
        return "<unsafe path redacted>"
    if len(path) > MAX_DISPLAY_PATH_LEN:
        keep = MAX_DISPLAY_PATH_LEN - 20
        return f"{path[:keep]}...<{len(path) - keep} chars truncated>"
    return path


def _fence_for(text: str) -> str:
    """Pick a backtick fence longer than any run of backticks in `text`."""
    longest = max((len(m.group(0)) for m in re.finditer(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


# ---------------------------------------------------------------------------
# Comment formatting
# ---------------------------------------------------------------------------


# NOTE: _render_command is duplicated in check_rendered_specs.py
def _render_command(components: list[str], use_all: bool = False) -> str:
    if use_all or len(components) > 30:
        return "azldev component render -a --clean-stale"
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

    all_comps: list[str] = sorted(
        {item["component"] for item in content_diffs + missing_files}
    )
    use_all = bool(extra_files) or bool(missing_files)
    remediation_cmd = _render_command([] if use_all else all_comps, use_all=use_all)

    lines: list[str] = [
        COMMENT_MARKER,
        "## 📄❌ Rendered specs are out of date",
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
                    f"gh run download {run_id} -R {repo} -n rendered-specs-patch",
                    "git apply rendered-specs.patch",
                    "```",
                ]
            )
        else:
            lines.extend(
                [
                    "```bash",
                    "git apply rendered-specs.patch",
                    "```",
                ]
            )
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

    # Running total of comment body size. Every section that appends
    # PR-controlled content (paths, diff bodies) must check this budget
    # before appending and bail out with a "... and N more" summary once it
    # gets close to the GitHub API's 65_536-char comment limit. A comment
    # rejected for being too large is effectively invisible (the post step
    # has continue-on-error: true), so a fork PR author could otherwise
    # suppress the drift warning by spamming long or numerous paths.
    body_so_far = len("\n".join(lines))
    budget_cap = MAX_COMMENT_CHARS - COMMENT_BUDGET_MARGIN

    if content_diffs:
        lines.append("### Content diffs")
        lines.append("")
        shown = 0
        for item in content_diffs:
            if shown >= MAX_INLINE_DIFFS:
                remaining = n_diff - shown
                lines.append(
                    f"*… and {remaining} more file(s). "
                    "Run the remediation command above to see all changes.*"
                )
                lines.append("")
                break
            path = _safe_path(item["path"])
            diff_text = item.get("diff", "")
            fence = _fence_for(diff_text)
            # Emit fixed raw HTML for the collapsible wrapper (`<details>` and
            # `<summary>`), but keep attacker-controlled content in markdown
            # code formatting: the path is rendered as code in the summary, and
            # the diff body is inside a dynamically chosen fence longer than any
            # backtick run in the diff text.
            block = (
                "<details>\n"
                f"<summary>`{path}`</summary>\n\n"
                f"{fence}diff\n{diff_text}\n{fence}\n\n"
                "</details>\n"
            )
            if body_so_far + len(block) > budget_cap:
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

    def _append_file_list(
        header: str,
        description: str,
        items: list[dict],
    ) -> None:
        """Append a bulleted file list, enforcing the shared comment budget.

        Stops early once the cumulative body size gets near the GitHub
        limit, so a fork PR can't suppress the warning by producing either
        very long paths or a huge number of them.
        """
        nonlocal body_so_far
        lines.append(header)
        lines.append("")
        lines.append(description)
        lines.append("")
        shown = 0
        truncated_for_size = False
        for item in items[:MAX_FILE_LIST]:
            entry = f"- `{_safe_path(item['path'])}`"
            # +1 for the newline added by the final "\n".join(lines).
            if body_so_far + len(entry) + 1 > budget_cap:
                truncated_for_size = True
                break
            lines.append(entry)
            body_so_far += len(entry) + 1
            shown += 1
        if truncated_for_size:
            remaining = len(items) - shown
            note = (
                f"\n*… and {remaining} more file(s) — comment size limit reached. "
                "Run the remediation command above to see all changes.*"
            )
        elif len(items) > MAX_FILE_LIST:
            remaining = len(items) - MAX_FILE_LIST
            note = f"\n*… and {remaining} more file(s).*"
        else:
            note = None
        if note is not None:
            lines.append(note)
            body_so_far += len(note) + 1
        lines.append("")
        body_so_far += 1

    if extra_files:
        _append_file_list(
            "### Files to add",
            "These files are produced by `azldev component render` but are "
            "missing from your branch. Add them.",
            extra_files,
        )

    if missing_files:
        _append_file_list(
            "### Files to remove",
            "These files are in your branch but are not produced by render. "
            "Remove them.",
            missing_files,
        )

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
    fd, body_path = tempfile.mkstemp(prefix="render-check-comment-", suffix=".md")
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
        description="Post rendered-spec drift results as a PR comment."
    )
    parser.add_argument(
        "--report",
        type=Path,
        required=True,
        help="Path to the JSON report from check_rendered_specs.py",
    )
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--pr", required=True, help="PR number")
    parser.add_argument(
        "--artifacts-url", default=None, help="Direct URL to patch artifact"
    )
    parser.add_argument("--run-id", default=None, help="GitHub Actions run ID")
    args = parser.parse_args()

    try:
        with open(args.report, encoding="utf-8") as f:
            report = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error reading report: {exc}", file=sys.stderr)
        return 1

    total = (
        len(report.get("content_diffs", []))
        + len(report.get("extra_files", []))
        + len(report.get("missing_files", []))
    )

    body: str | None = None
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
