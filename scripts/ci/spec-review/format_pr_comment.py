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

from _common import get_repo_relative_path

# GitHub PR comment body limit is 65535 chars. Leave room for the
# surrounding markdown structure.
MAX_RAW_JSON_CHARS = 50_000


def _status(total_errors: int, total_warnings: int) -> str:
    """Return the report status heading."""
    if total_errors > 0:
        return "❌ **Spec Review Failed**"
    if total_warnings > 0:
        return "⚠️ **Spec Review Passed with Warnings**"
    return "✅ **Spec Review Passed**"


def _append_findings(lines: list[str], findings: list[dict], emoji: str, label: str) -> None:
    """Append one categorized group of findings."""
    if not findings:
        return
    lines.extend(["<details>", f"<summary>{emoji} {label} ({len(findings)})</summary>", ""])
    for finding in findings:
        description = finding.get("description", "")
        citation = finding.get("citation")
        lines.append(f"- {description}")
        if citation and citation not in ("N/A", "n/a", ""):
            lines.append(f"  - 📖 [{citation}]({citation})")
    lines.extend(["", "</details>", ""])


def _append_review(lines: list[str], review: dict, repo: str, sha: str, repo_root: Path | None) -> None:
    """Append all findings for one reviewed spec."""
    categorized = [
        (review.get("errors", []), "❌", "Errors"),
        (review.get("warnings", []), "⚠️", "Warnings"),
        (review.get("suggestions", []), "💡", "Suggestions"),
    ]
    if not any(findings for findings, _emoji, _label in categorized):
        return

    spec_file = review.get("spec_file", "unknown")
    spec_path = get_repo_relative_path(spec_file, repo_root)
    spec_name = Path(spec_file).name
    if Path(spec_path).is_absolute():
        spec_link = f"`{spec_name}`"
    else:
        spec_link = f"[`{spec_name}`](https://github.com/{repo}/blob/{sha}/{spec_path})"
    lines.extend([f"### {spec_link}", ""])
    for findings, emoji, label in categorized:
        _append_findings(lines, findings, emoji, label)


def _append_raw_json(lines: list[str], report: dict) -> None:
    """Append the raw report within GitHub's comment size budget."""
    raw_json = json.dumps(report, indent=2)
    lines.extend(["<details>", "<summary>📄 Raw JSON Report</summary>", ""])
    if len(raw_json) > MAX_RAW_JSON_CHARS:
        lines.append("*Report too large to display inline. See uploaded artifacts for the full report.*")
    else:
        lines.extend(["```json", raw_json, "```"])
    lines.extend(["", "</details>"])


def format_comment(report: dict, repo: str, sha: str, repo_root: Path | None = None) -> str:
    """Format the report as a markdown comment."""
    reviews = report.get("spec_reviews", [])
    total_errors = sum(len(review.get("errors", [])) for review in reviews)
    total_warnings = sum(len(review.get("warnings", [])) for review in reviews)
    total_suggestions = sum(len(review.get("suggestions", [])) for review in reviews)

    lines = [
        "<!-- SPEC_REVIEW_BOT -->",
        f"## {_status(total_errors, total_warnings)}",
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

    for review in reviews:
        _append_review(lines, review, repo, sha, repo_root)

    if total_errors == 0 and total_warnings == 0 and total_suggestions == 0:
        lines.extend(["✨ No issues found in any reviewed spec files.", ""])
    _append_raw_json(lines, report)
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
