#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Format spec review report as a GitHub PR comment with clickable links.

Usage:
    python format_pr_comment.py report.json --repo owner/repo --sha abc123
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

from _common import get_repo_relative_path

# GitHub PR comment body limit is 65535 chars. Leave room for the
# surrounding markdown structure.
MAX_RAW_JSON_CHARS = 50_000


class RawFinding(TypedDict, total=False):
    """Finding fields consumed by the PR comment renderer."""

    description: str
    citation: str | None


class RawReview(TypedDict, total=False):
    """Per-spec fields consumed by the PR comment renderer."""

    spec_file: str
    errors: list[RawFinding]
    warnings: list[RawFinding]
    suggestions: list[RawFinding]


class RawReport(TypedDict, total=False):
    """Report fields consumed by the PR comment renderer."""

    spec_reviews: list[RawReview]


def _status_text(total_errors: int, total_warnings: int) -> str:
    """Return the pull request status heading for aggregate finding counts."""
    if total_errors > 0:
        return "❌ **Spec Review Failed**"
    if total_warnings > 0:
        return "⚠️ **Spec Review Passed with Warnings**"
    return "✅ **Spec Review Passed**"


def _append_finding_group(
    lines: list[str],
    findings: list[RawFinding],
    emoji: str,
    label: str,
) -> None:
    """Append one expandable severity group to the comment."""
    if not findings:
        return
    lines.extend(["<details>", f"<summary>{emoji} {label} ({len(findings)})</summary>", ""])
    for finding in findings:
        description = finding.get("description", "")
        citation = finding.get("citation")
        lines.append(f"- {description}")
        if citation and citation not in ("N/A", "n/a"):
            lines.append(f"  - 📖 [{citation}]({citation})")
    lines.extend(["", "</details>", ""])


def _append_review(
    lines: list[str],
    review: RawReview,
    repo: str,
    sha: str,
    repo_root: Path | None,
) -> None:
    """Append all findings for one reviewed spec file."""
    groups = (
        (review.get("errors", []), "❌", "Errors"),
        (review.get("warnings", []), "⚠️", "Warnings"),
        (review.get("suggestions", []), "💡", "Suggestions"),
    )
    if not any(findings for findings, _, _ in groups):
        return

    spec_file = review.get("spec_file", "unknown")
    spec_path = get_repo_relative_path(spec_file, repo_root)
    spec_name = Path(spec_file).name
    if Path(spec_path).is_absolute():
        spec_link = f"`{spec_name}`"
    else:
        spec_link = f"[`{spec_name}`](https://github.com/{repo}/blob/{sha}/{spec_path})"
    lines.extend([f"### {spec_link}", ""])

    for findings, emoji, label in groups:
        _append_finding_group(lines, findings, emoji, label)


def _append_raw_report(lines: list[str], report: RawReport) -> None:
    """Append the collapsible raw JSON report, respecting GitHub's size limit."""
    raw_json = json.dumps(report, indent=2)
    lines.extend(["<details>", "<summary>📄 Raw JSON Report</summary>", ""])
    if len(raw_json) > MAX_RAW_JSON_CHARS:
        lines.append("*Report too large to display inline. See uploaded artifacts for the full report.*")
    else:
        lines.extend(["```json", raw_json, "```"])
    lines.extend(["", "</details>"])


def format_comment(
    report: RawReport,
    repo: str,
    sha: str,
    repo_root: Path | None = None,
) -> str:
    """Format the report as a markdown comment."""
    reviews = report.get("spec_reviews", [])

    total_errors = sum(len(r.get("errors", [])) for r in reviews)
    total_warnings = sum(len(r.get("warnings", [])) for r in reviews)
    total_suggestions = sum(len(r.get("suggestions", [])) for r in reviews)

    # Hidden marker for finding/updating this comment
    lines = [
        "<!-- SPEC_REVIEW_BOT -->",
        f"## {_status_text(total_errors, total_warnings)}",
        "",
        "| Type | Count |",
        "|------|-------|",
        f"| Errors | {total_errors} |",
        f"| Warnings | {total_warnings} |",
        f"| Suggestions | {total_suggestions} |",
        "",
        f"🛠️ Debug locally: [scripts/ci/spec-review/README.md](https://github.com/{repo}/blob/{sha}/scripts/ci/spec-review/README.md)",
        "",
    ]

    # Format each spec file's findings
    for review in reviews:
        _append_review(lines, review, repo, sha, repo_root)

    # If no spec files had any findings, add an all-clear message
    if total_errors == 0 and total_warnings == 0 and total_suggestions == 0:
        lines.append("✨ No issues found in any reviewed spec files.")
        lines.append("")

    _append_raw_report(lines, report)

    return "\n".join(lines)


def main() -> int:
    """Format a spec-review report as a pull request comment."""
    parser = argparse.ArgumentParser(description="Format spec review as PR comment")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--sha", required=True, help="Commit SHA for file links")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root for converting absolute paths to relative",
    )
    args = parser.parse_args()

    try:
        with args.file.open(encoding="utf-8") as f:
            report = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    repo_root = args.repo_root or Path.cwd()
    comment = format_comment(report, args.repo, args.sha, repo_root)
    print(comment)
    return 0


if __name__ == "__main__":
    sys.exit(main())
