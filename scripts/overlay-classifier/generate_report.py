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
    upstream = cl.get("upstreamability", "?")
    desc = entry.get("description", "(no description)")
    return f"| `{component}` | `{file_path}` | {idx} | {confidence} | {upstream} | {desc} |"


def _render_group_row(entry: dict[str, Any]) -> str:
    """Render a single group entry as a markdown table row."""
    component = entry.get("component", "?")
    group = entry.get("group", "?")
    file_path = entry.get("file", "?")
    cl = entry.get("classification", {})
    confidence = cl.get("confidence", "?")
    upstream = cl.get("upstreamability", "?")
    desc = entry.get("group_description", "(no description)")
    return f"| `{component}` | `{file_path}` | {group} | {confidence} | {upstream} | {desc} |"


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

    lines.append("## Classification distribution")
    lines.append("")
    lines.append("| Label | Count | % |")
    lines.append("|---|---:|---:|")
    for label in sorted(top_level_counts, key=lambda k: -top_level_counts[k]):
        count = top_level_counts[label]
        lines.append(f"| `{label}` | {count} | {_pct(count, total)} |")
    lines.append("")

    # --- Backport-dist-git section ---
    backport_overlays = [e for e in overlays if (e.get("classification", {}).get("top_level") == "Backport-dist-git")]
    backport_groups = [
        e for e in group_entries if (e.get("classification", {}).get("top_level") == "Backport-dist-git")
    ]
    backport_total = len(backport_overlays) + len(backport_groups)

    if backport_total > 0:
        lines.append(f"## Backport-dist-git ({backport_total})")
        lines.append("")
        if backport_overlays:
            lines.append("| component | file | idx | confidence | upstream | description |")
            lines.append("|---|---|---|---|---|---|")
            lines.extend(
                _render_overlay_row(entry)
                for entry in sorted(
                    backport_overlays, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0))
                )
            )
            lines.append("")

        if backport_groups:
            lines.append("**Group entries:**")
            lines.append("")
            lines.append("| component | file | group | confidence | upstream | group description |")
            lines.append("|---|---|---|---|---|---|")
            lines.extend(
                _render_group_row(entry) for entry in sorted(backport_groups, key=lambda e: e.get("component", ""))
            )
            lines.append("")

        # Fedora fix version table (if enriched data is available)
        enriched = [e for e in backport_overlays if e.get("fedora_fix_info")]
        if enriched:
            # Deduplicate by component (multiple overlays per component share the same fix info)
            seen_components: set[str] = set()
            unique_entries: list[dict[str, Any]] = []
            for entry in sorted(enriched, key=lambda e: e.get("component", "")):
                comp = entry.get("component", "")
                if comp not in seen_components:
                    seen_components.add(comp)
                    unique_entries.append(entry)

            lines.append("### Fedora Fix Versions (when can overlays be removed?)")
            lines.append("")
            lines.append("| Package | AZL tracks | Fix available in | Action |")
            lines.append("|---|---|---|---|")
            for entry in unique_entries:
                fi = entry["fedora_fix_info"]
                pkg = fi.get("package", "?")
                azl_nvr = fi.get("azl_nvr") or "not found"
                fix_nvr = fi.get("fix_nvr")
                fix_tag = fi.get("fix_tag", "")
                if fix_nvr:
                    action = f"Remove overlay when bumping to `{fix_tag}`+"
                    lines.append(f"| `{pkg}` | `{azl_nvr}` | `{fix_nvr}` | {action} |")
                else:
                    lines.append(f"| `{pkg}` | `{azl_nvr}` | _(not found)_ | Manual verification needed |")
            lines.append("")

    # --- AZL-* category sections ---
    azl_prefix = "AZL-"
    azl_overlays = [e for e in overlays if (e.get("classification", {}).get("top_level") or "").startswith(azl_prefix)]
    azl_groups = [
        e for e in group_entries if (e.get("classification", {}).get("top_level") or "").startswith(azl_prefix)
    ]
    azl_total = len(azl_overlays) + len(azl_groups)

    if azl_total > 0:
        # Category frequencies
        cat_counts: dict[str, int] = {}
        for entry in azl_overlays + azl_groups:
            cl = entry.get("classification", {})
            cat = cl.get("top_level") or "uncategorized"
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        lines.append(f"## AZL categories ({azl_total})")
        lines.append("")
        lines.append("| Category | Count |")
        lines.append("|---|---:|")
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| `{cat}` | {count} |")
        lines.append("")

        # Per category sections
        for cat, _count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            cat_overlays_list = [
                e for e in azl_overlays if (e.get("classification", {}).get("top_level")) == cat
            ]
            cat_groups_list = [
                e for e in azl_groups if (e.get("classification", {}).get("top_level")) == cat
            ]

            cat_total = len(cat_overlays_list) + len(cat_groups_list)
            lines.append(f"### {cat} ({cat_total})")
            lines.append("")

            if cat_overlays_list:
                lines.append("| component | file | idx | confidence | upstream | description |")
                lines.append("|---|---|---|---|---|---|")
                lines.extend(
                    _render_overlay_row(entry)
                    for entry in sorted(
                        cat_overlays_list, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0))
                    )
                )
                lines.append("")

            if cat_groups_list:
                lines.append("**Group entries:**")
                lines.append("")
                lines.append("| component | file | group | confidence | upstream | group description |")
                lines.append("|---|---|---|---|---|---|")
                lines.extend(
                    _render_group_row(entry) for entry in sorted(cat_groups_list, key=lambda e: e.get("component", ""))
                )
                lines.append("")

    # --- Unclassified section ---
    unclassified = [e for e in overlays if not e.get("classification", {}).get("top_level")]
    if unclassified:
        lines.append(f"## Unclassified ({len(unclassified)})")
        lines.append("")
        lines.append("These overlays need LLM refinement or manual classification.")
        lines.append("")
        lines.append("| component | file | idx | confidence | upstream | description |")
        lines.append("|---|---|---|---|---|---|")
        lines.extend(
            _render_overlay_row(entry)
            for entry in sorted(unclassified, key=lambda e: (e.get("component", ""), e.get("overlay_index", 0)))
        )
        lines.append("")

    # --- Upstreamability summary ---
    lines.append("## Upstreamability Summary")
    lines.append("")
    upstream_counts: dict[str, int] = {}
    for entry in overlays + group_entries:
        cl = entry.get("classification", {})
        upstream = cl.get("upstreamability") or "unknown"
        upstream_counts[upstream] = upstream_counts.get(upstream, 0) + 1

    lines.append("| Upstreamability | Count | % |")
    lines.append("|---|---:|---:|")
    for tag in ["yes", "no", "unknown"]:
        count = upstream_counts.get(tag, 0)
        if count > 0:
            lines.append(f"| `{tag}` | {count} | {_pct(count, total)} |")
    lines.append("")

    # Cross-tabulation: category × upstreamability
    cat_upstream: dict[str, dict[str, int]] = {}
    for entry in overlays + group_entries:
        cl = entry.get("classification", {})
        tl = cl.get("top_level") or "unclassified"
        upstream = cl.get("upstreamability") or "unknown"
        if tl not in cat_upstream:
            cat_upstream[tl] = {}
        cat_upstream[tl][upstream] = cat_upstream[tl].get(upstream, 0) + 1

    lines.append("### Upstreamability by category")
    lines.append("")
    lines.append("| Category | yes | no | unknown | Total |")
    lines.append("|---|---:|---:|---:|---:|")
    for cat in sorted(cat_upstream, key=lambda c: -sum(cat_upstream[c].values())):
        yes = cat_upstream[cat].get("yes", 0)
        no = cat_upstream[cat].get("no", 0)
        unk = cat_upstream[cat].get("unknown", 0)
        cat_total = yes + no + unk
        lines.append(f"| `{cat}` | {yes} | {no} | {unk} | {cat_total} |")
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
