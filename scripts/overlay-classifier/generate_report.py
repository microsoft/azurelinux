# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Generate a markdown report from classified overlay data.

Reads the classified JSON output and produces a human-readable markdown report
matching the format of overlay_report.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _pct(count: int, total: int) -> str:
    """Format a percentage string."""
    if total == 0:
        return "0.0%"
    return f"{count / total * 100:.1f}%"


def _render_overlay_row(entry: dict[str, Any]) -> str:
    """Render a single overlay as a markdown table row."""
    component = entry.get("component", "?")
    file_path = entry.get("file", "?")
    idx = entry.get("overlay_index", "?")
    cl = entry.get("classification", {})
    confidence = cl.get("confidence", "?")
    desc = entry.get("description", "(no description)")
    return f"| `{component}` | `{file_path}` | {idx} | {confidence} | {desc} |"


def _render_group_row(entry: dict[str, Any]) -> str:
    """Render a single group entry as a markdown table row."""
    component = entry.get("component", "?")
    group = entry.get("group", "?")
    file_path = entry.get("file", "?")
    cl = entry.get("classification", {})
    confidence = cl.get("confidence", "?")
    desc = entry.get("group_description", "(no description)")
    return f"| `{component}` | `{file_path}` | {group} | {confidence} | {desc} |"


def generate_report(data: dict[str, Any]) -> str:  # noqa: C901, PLR0912, PLR0915
    """Generate a markdown report from classified overlay data."""
    lines: list[str] = []
    overlays = data.get("overlays", [])
    group_entries = data.get("group_entries", [])
    total = len(overlays) + len(group_entries)

    lines.append("# Overlay Classification Report")
    lines.append("")
    lines.append(
        f"Total entries classified: **{total}** ({len(overlays)} overlays + {len(group_entries)} group entries)"
    )
    lines.append("")

    # --- Top-level distribution ---
    top_level_counts: dict[str, int] = {}
    for entry in overlays + group_entries:
        cl = entry.get("classification", {})
        tl = cl.get("top_level") or "unclassified"
        top_level_counts[tl] = top_level_counts.get(tl, 0) + 1

    lines.append("## Top-level distribution")
    lines.append("")
    lines.append("| Label | Count | % |")
    lines.append("|---|---:|---:|")
    for label in ["Backport-fedora", "Upstream-fix", "AZL-customization", "unclassified"]:
        count = top_level_counts.get(label, 0)
        if count > 0:
            lines.append(f"| `{label}` | {count} | {_pct(count, total)} |")
    lines.append("")

    # --- Backport-fedora section ---
    backports = [e for e in overlays if (e.get("classification", {}).get("top_level") == "Backport-fedora")]
    if backports:
        lines.append(f"## Backport-fedora ({len(backports)})")
        lines.append("")
        lines.append("| component | file | idx | confidence | description |")
        lines.append("|---|---|---|---|---|")
        lines.extend(
            _render_overlay_row(entry)
            for entry in sorted(backports, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0)))
        )
        lines.append("")

    # --- Upstream-fix section ---
    upstream_fixes = [e for e in overlays if (e.get("classification", {}).get("top_level") == "Upstream-fix")]
    if upstream_fixes:
        lines.append(f"## Upstream-fix ({len(upstream_fixes)})")
        lines.append("")
        lines.append("| component | file | idx | confidence | description |")
        lines.append("|---|---|---|---|---|")
        lines.extend(
            _render_overlay_row(entry)
            for entry in sorted(upstream_fixes, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0)))
        )
        lines.append("")

    # --- AZL-customization section ---
    azl_overlays = [e for e in overlays if (e.get("classification", {}).get("top_level") == "AZL-customization")]
    azl_groups = [e for e in group_entries if (e.get("classification", {}).get("top_level") == "AZL-customization")]
    azl_total = len(azl_overlays) + len(azl_groups)

    if azl_total > 0:
        lines.append(f"## AZL-customization ({azl_total})")
        lines.append("")

        # Sub-category frequencies
        sub_counts: dict[str, int] = {}
        for entry in azl_overlays + azl_groups:
            cl = entry.get("classification", {})
            sc = cl.get("sub_category") or "uncategorized"
            sub_counts[sc] = sub_counts.get(sc, 0) + 1

        lines.append("### Sub-category frequencies")
        lines.append("")
        lines.append("| Sub-category | Count |")
        lines.append("|---|---:|")
        for cat, count in sorted(sub_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| `{cat}` | {count} |")
        lines.append("")

        # Per sub-category sections
        for cat, _count in sorted(sub_counts.items(), key=lambda x: -x[1]):
            cat_overlays = [
                e for e in azl_overlays if (e.get("classification", {}).get("sub_category") or "uncategorized") == cat
            ]
            cat_groups = [
                e for e in azl_groups if (e.get("classification", {}).get("sub_category") or "uncategorized") == cat
            ]

            cat_total = len(cat_overlays) + len(cat_groups)
            lines.append(f"### {cat} ({cat_total})")
            lines.append("")

            if cat_overlays:
                lines.append("| component | file | idx | confidence | description |")
                lines.append("|---|---|---|---|---|")
                lines.extend(
                    _render_overlay_row(entry)
                    for entry in sorted(cat_overlays, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0)))
                )
                lines.append("")

            if cat_groups:
                lines.append("**Group entries:**")
                lines.append("")
                lines.append("| component | file | group | confidence | group description |")
                lines.append("|---|---|---|---|---|")
                lines.extend(
                    _render_group_row(entry) for entry in sorted(cat_groups, key=lambda e: e.get("component", ""))
                )
                lines.append("")

    # --- Unclassified section ---
    unclassified = [e for e in overlays if not e.get("classification", {}).get("top_level")]
    if unclassified:
        lines.append(f"## Unclassified ({len(unclassified)})")
        lines.append("")
        lines.append("These overlays need LLM refinement or manual classification.")
        lines.append("")
        lines.append("| component | file | idx | confidence | description |")
        lines.append("|---|---|---|---|---|")
        lines.extend(
            _render_overlay_row(entry)
            for entry in sorted(unclassified, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0)))
        )
        lines.append("")

    # --- Confidence summary ---
    lines.append("## Confidence Summary")
    lines.append("")
    conf_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    for entry in overlays + group_entries:
        cl = entry.get("classification", {})
        conf = cl.get("confidence") or "unknown"
        src = cl.get("classified_by") or "unknown"
        conf_counts[conf] = conf_counts.get(conf, 0) + 1
        source_counts[src] = source_counts.get(src, 0) + 1

    lines.append("| Confidence | Count | % |")
    lines.append("|---|---:|---:|")
    for conf in ["high", "medium", "low", "unknown"]:
        count = conf_counts.get(conf, 0)
        if count > 0:
            lines.append(f"| `{conf}` | {count} | {_pct(count, total)} |")
    lines.append("")

    lines.append("| Classified by | Count |")
    lines.append("|---|---:|")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{src}` | {count} |")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point for the markdown report generator."""
    parser = argparse.ArgumentParser(description="Generate markdown report from classified overlay data")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input classified JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output markdown file",
    )
    args = parser.parse_args()

    data = json.loads(args.input.read_text())
    report = generate_report(data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n")

    # Print summary
    total_lines = report.count("\n")
    print(f"Report written to {args.output} ({total_lines} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
