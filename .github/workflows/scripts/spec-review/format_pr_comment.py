#!/usr/bin/env python3
"""
Format spec review report as a GitHub PR comment with clickable links.

Usage:
    python format_pr_comment.py report.json --repo owner/repo --sha abc123
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from _common import get_repo_relative_path

# GitHub PR comment body limit is 65535 chars. Leave room for the
# surrounding markdown structure.
MAX_RAW_JSON_CHARS = 50_000


def format_comment(report: dict, repo: str, sha: str, repo_root: Optional[Path] = None) -> str:
    """Format the report as a markdown comment."""
    reviews = report.get("spec_reviews", [])

    total_errors = sum(len(r.get("errors", [])) for r in reviews)
    total_warnings = sum(len(r.get("warnings", [])) for r in reviews)
    total_suggestions = sum(len(r.get("suggestions", [])) for r in reviews)

    # Status header
    if total_errors > 0:
        status = "❌ **Spec Review Failed**"
    elif total_warnings > 0:
        status = "⚠️ **Spec Review Passed with Warnings**"
    else:
        status = "✅ **Spec Review Passed**"

    # Hidden marker for finding/updating this comment
    lines = [
        "<!-- SPEC_REVIEW_BOT -->",
        f"## {status}",
        "",
        "| Type | Count |",
        "|------|-------|",
        f"| Errors | {total_errors} |",
        f"| Warnings | {total_warnings} |",
        f"| Suggestions | {total_suggestions} |",
        "",
        f"🛠️ Debug locally: [.github/workflows/scripts/README.md](https://github.com/{repo}/blob/{sha}/.github/workflows/scripts/README.md)",
        "",
    ]

    # Format each spec file's findings
    for review in reviews:
        spec_file = review.get("spec_file", "unknown")
        errors = review.get("errors", [])
        warnings = review.get("warnings", [])
        suggestions = review.get("suggestions", [])

        if not (errors or warnings or suggestions):
            continue

        # Make spec file a clickable link (only if we resolved a relative path)
        spec_path = get_repo_relative_path(spec_file, repo_root)
        spec_name = Path(spec_file).name
        if Path(spec_path).is_absolute():
            spec_link = f"`{spec_name}`"
        else:
            spec_link = f"[`{spec_name}`](https://github.com/{repo}/blob/{sha}/{spec_path})"
        lines.append(f"### {spec_link}")
        lines.append("")

        for findings, emoji, label in [
            (errors, "❌", "Errors"),
            (warnings, "⚠️", "Warnings"),
            (suggestions, "💡", "Suggestions"),
        ]:
            if findings:
                lines.append("<details>")
                lines.append(f"<summary>{emoji} {label} ({len(findings)})</summary>")
                lines.append("")
                for f in findings:
                    desc = f.get("description", "")
                    citation = f.get("citation")
                    if citation and citation not in ("N/A", "n/a", ""):
                        lines.append(f"- {desc}")
                        lines.append(f"  - 📖 [{citation}]({citation})")
                    else:
                        lines.append(f"- {desc}")
                lines.append("")
                lines.append("</details>")
                lines.append("")

    # If no spec files had any findings, add an all-clear message
    if total_errors == 0 and total_warnings == 0 and total_suggestions == 0:
        lines.append("✨ No issues found in any reviewed spec files.")
        lines.append("")

    # Add raw JSON in collapsed section (truncate if too large for GH comment limit)
    raw_json = json.dumps(report, indent=2)
    lines.append("<details>")
    lines.append("<summary>📄 Raw JSON Report</summary>")
    lines.append("")
    if len(raw_json) > MAX_RAW_JSON_CHARS:
        lines.append("*Report too large to display inline. See uploaded artifacts for the full report.*")
    else:
        lines.append("```json")
        lines.append(raw_json)
        lines.append("```")
    lines.append("")
    lines.append("</details>")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Format spec review as PR comment")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--sha", required=True, help="Commit SHA for file links")
    parser.add_argument("--repo-root", type=Path, default=None,
                        help="Repository root for converting absolute paths to relative")
    args = parser.parse_args()

    try:
        with open(args.file, encoding="utf-8") as f:
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
