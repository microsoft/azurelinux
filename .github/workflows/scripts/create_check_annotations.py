#!/usr/bin/env python3
"""
Generate GitHub Check annotations from spec review report.

Usage:
    python create_check_annotations.py report.json --workflow-commands
    python create_check_annotations.py report.json --json
    python create_check_annotations.py report.json --repo-root /path/to/repo
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from _common import get_repo_relative_path

# Mapping from finding category to (workflow command level, checks API level, checks API title)
_SEVERITY_MAP = {
    "errors":      ("error",   "failure", "Spec Error"),
    "warnings":    ("warning", "warning", "Spec Warning"),
    "suggestions": ("notice",  "notice",  "Suggestion"),
}


def _iter_findings(report: dict, repo_root: Optional[Path] = None):
    """Yield (spec_file, category, finding) for every finding in the report."""
    for review in report.get("spec_reviews", []):
        spec_file = get_repo_relative_path(review.get("spec_file", ""), repo_root)
        for category in _SEVERITY_MAP:
            for finding in review.get(category, []):
                yield spec_file, category, finding


def _format_message(finding: dict, escape_fn=None) -> str:
    """Build a message string from a finding, optionally escaping it."""
    desc = finding.get("description", "")
    citation = finding.get("citation")
    if escape_fn:
        desc = escape_fn(desc)
    msg = desc
    if citation and citation not in ("N/A", "n/a", ""):
        cite = escape_fn(citation) if escape_fn else citation
        msg += f" (Ref: {cite})" if escape_fn else f"\n\nRef: {citation}"
    return msg


def escape_workflow_command(s: str) -> str:
    """Escape special characters for GitHub Actions workflow commands.

    See https://github.com/actions/toolkit/issues/193
    Order matters: % must be escaped first to avoid double-escaping.
    """
    return (
        s.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
        .replace(",", "%2C")
    )


def generate_workflow_commands(report: dict, repo_root: Optional[Path] = None) -> list[str]:
    """Generate GitHub Actions workflow commands for annotations."""
    commands = []
    for spec_file, category, finding in _iter_findings(report, repo_root):
        level = _SEVERITY_MAP[category][0]
        line = finding.get("line") or 1
        msg = _format_message(finding, escape_fn=escape_workflow_command)
        escaped_file = escape_workflow_command(spec_file)
        commands.append(f"::{level} file={escaped_file},line={line}::{msg}")
    return commands


def generate_check_annotations(report: dict, repo_root: Optional[Path] = None) -> list[dict]:
    """Generate annotations for GitHub Checks API."""
    annotations = []
    for spec_file, category, finding in _iter_findings(report, repo_root):
        _, api_level, title = _SEVERITY_MAP[category]
        line = finding.get("line") or 1
        msg = _format_message(finding)
        annotations.append({
            "path": spec_file,
            "start_line": line,
            "end_line": line,
            "annotation_level": api_level,
            "message": msg,
            "title": title,
        })
    return annotations


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate check annotations from spec review")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--workflow-commands", action="store_true",
                        help="Output GitHub Actions workflow commands")
    parser.add_argument("--json", action="store_true",
                        help="Output annotations as JSON for Checks API")
    parser.add_argument("--repo-root", type=Path, default=None,
                        help="Repository root for converting absolute paths to relative (default: auto-detect via git)")
    args = parser.parse_args()

    try:
        with open(args.file, encoding="utf-8") as f:
            report = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Use provided repo root, or fall back to cwd
    repo_root = args.repo_root or Path.cwd()

    if args.workflow_commands:
        commands = generate_workflow_commands(report, repo_root)
        for cmd in commands:
            print(cmd)
    elif args.json:
        annotations = generate_check_annotations(report, repo_root)
        print(json.dumps(annotations, indent=2))
    else:
        # Default: workflow commands
        commands = generate_workflow_commands(report, repo_root)
        for cmd in commands:
            print(cmd)

    return 0


if __name__ == "__main__":
    sys.exit(main())
