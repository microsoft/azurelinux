#!/usr/bin/env python3
"""Generate an interactive Sankey diagram of overlay classifications.

Reads classified_overlays.json and produces a standalone HTML file with
a Plotly Sankey diagram showing the flow:

    All Overlays → {Backport-dist-git, AZL-customization}
                   → AZL-* categories → Upstreamability {yes, no, unknown}

Usage:
    python generate_sankey.py -i classified_overlays.json -o sankey.html
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from taxonomy import AZL_PREFIX

# -- Color palette ----------------------------------------------------------

# Visual group for the first Sankey column
GROUP_COLORS = {
    "Backport-dist-git": "rgba(31, 119, 180, 0.8)",
    "AZL-customization": "rgba(44, 160, 44, 0.8)",
}

# Individual AZL-* category colors for the second column
AZL_CATEGORY_COLORS = {
    "AZL-dependency-pruning": "rgba(255, 127, 0, 0.7)",
    "AZL-feature-disablement": "rgba(77, 175, 74, 0.7)",
    "AZL-branding-policy": "rgba(0, 191, 255, 0.7)",
    "AZL-build": "rgba(55, 126, 184, 0.7)",
    "AZL-test-disablement": "rgba(152, 78, 163, 0.7)",
    "AZL-security": "rgba(166, 86, 40, 0.7)",
    "AZL-release-management": "rgba(247, 129, 191, 0.7)",
    "AZL-missing-dependency-workaround": "rgba(228, 26, 28, 0.7)",
    "AZL-platform-adaptation": "rgba(153, 153, 153, 0.7)",
    "uncategorized": "rgba(200, 200, 200, 0.7)",
}

UPSTREAMABILITY_COLORS = {
    "yes": "rgba(50, 205, 50, 0.8)",
    "no": "rgba(220, 20, 60, 0.8)",
    "unknown": "rgba(180, 180, 180, 0.8)",
}

# -- Fallback color for unknown types/categories --
_FALLBACK = "rgba(180, 180, 180, 0.5)"


def _get_color(name: str, palette: dict[str, str]) -> str:
    return palette.get(name, _FALLBACK)


def _build_sankey_data(  # noqa: PLR0915
    data: dict[str, Any],
) -> dict[str, Any]:
    """Build Plotly Sankey node/link structures from classified data.

    Four-layer flow:
        All Overlays → {Backport-dist-git, AZL-customization}
                       → AZL-* categories → Upstreamability {yes, no, unknown}

    AZL-customization is a virtual aggregate node — AZL-* labels in the data
    are grouped under it by detecting the ``AZL-`` prefix.
    """
    overlays: list[dict[str, Any]] = data.get("overlays", [])
    groups: list[dict[str, Any]] = data.get("group_entries", [])
    total = len(overlays) + len(groups)

    # --- Count flows ---
    # Visual groups (Backport-dist-git, AZL-customization aggregate)
    group_counts: Counter[str] = Counter()
    # Per AZL-* category breakdown
    azl_cat_counts: Counter[str] = Counter()
    # AZL category → upstreamability flows
    cat_to_upstream: Counter[tuple[str, str]] = Counter()

    for entry in [*overlays, *groups]:
        cl = entry.get("classification", {})
        top = cl.get("top_level") or "unclassified"
        upstream = cl.get("upstreamability") or "unknown"

        if top.startswith(AZL_PREFIX):
            group_counts["AZL-customization"] += 1
            azl_cat_counts[top] += 1
            cat_to_upstream[(top, upstream)] += 1
        else:
            group_counts[top] += 1

    # --- Build node list ---
    # Layer 0: single aggregate node
    aggregate_label = f"All Overlays ({total})"
    visual_groups = sorted(group_counts.keys())
    azl_cats = sorted(azl_cat_counts.keys())
    upstream_tags = sorted({k[1] for k in cat_to_upstream})

    nodes: list[str] = [aggregate_label]
    node_colors: list[str] = ["rgba(100, 100, 100, 0.8)"]

    for grp in visual_groups:
        nodes.append(grp)
        node_colors.append(_get_color(grp, GROUP_COLORS))

    for cat in azl_cats:
        nodes.append(cat)
        node_colors.append(_get_color(cat, AZL_CATEGORY_COLORS))

    # Upstreamability nodes — use display labels
    upstream_display = {"yes": "Upstreamable", "no": "Not upstreamable", "unknown": "Unknown"}
    for tag in upstream_tags:
        display = upstream_display.get(tag, tag)
        nodes.append(display)
        node_colors.append(_get_color(tag, UPSTREAMABILITY_COLORS))

    node_index = {name: i for i, name in enumerate(nodes)}

    # --- Build links ---
    sources: list[int] = []
    targets: list[int] = []
    values: list[int] = []
    link_colors: list[str] = []

    # Layer 1 links: aggregate → visual group
    agg_idx = node_index[aggregate_label]
    for grp in visual_groups:
        sources.append(agg_idx)
        targets.append(node_index[grp])
        values.append(group_counts[grp])
        color = _get_color(grp, GROUP_COLORS).replace("0.8", "0.3")
        link_colors.append(color)

    # Layer 2 links: AZL-customization → individual AZL-* categories
    if "AZL-customization" in node_index:
        azl_idx = node_index["AZL-customization"]
        for cat in azl_cats:
            sources.append(azl_idx)
            targets.append(node_index[cat])
            values.append(azl_cat_counts[cat])
            color = _get_color(cat, AZL_CATEGORY_COLORS).replace("0.7", "0.3")
            link_colors.append(color)

    # Layer 3 links: AZL-* category → upstreamability
    for (cat, tag), count in sorted(cat_to_upstream.items()):
        display = upstream_display.get(tag, tag)
        sources.append(node_index[cat])
        targets.append(node_index[display])
        values.append(count)
        color = _get_color(tag, UPSTREAMABILITY_COLORS).replace("0.8", "0.3")
        link_colors.append(color)

    return {
        "nodes": nodes,
        "node_colors": node_colors,
        "sources": sources,
        "targets": targets,
        "values": values,
        "link_colors": link_colors,
        "group_counts": dict(group_counts),
    }


def _generate_html(sankey_data: dict[str, Any], total: int) -> str:
    """Generate standalone HTML with embedded Plotly Sankey diagram."""
    nodes = sankey_data["nodes"]
    node_colors = sankey_data["node_colors"]

    # Build labels with counts
    group_counts = sankey_data.get("group_counts", {})
    node_labels: list[str] = []
    for i, n in enumerate(nodes):
        if n.startswith("All Overlays"):
            node_labels.append(n)
        elif n in group_counts:
            node_labels.append(f"{n} ({group_counts[n]})")
        else:
            # AZL-* category: sum incoming link values
            incoming = sum(
                v
                for s, t, v in zip(
                    sankey_data["sources"],
                    sankey_data["targets"],
                    sankey_data["values"],
                    strict=True,
                )
                if t == i
            )
            node_labels.append(f"{n} ({incoming})")

    fig_data = json.dumps(
        {
            "type": "sankey",
            "orientation": "h",
            "arrangement": "snap",
            "node": {
                "pad": 20,
                "thickness": 25,
                "line": {"color": "rgba(0,0,0,0.3)", "width": 0.5},
                "label": node_labels,
                "color": node_colors,
                "hovertemplate": "%{label}<extra></extra>",
            },
            "link": {
                "source": sankey_data["sources"],
                "target": sankey_data["targets"],
                "value": sankey_data["values"],
                "color": sankey_data["link_colors"],
                "hovertemplate": "%{source.label} → %{target.label}: %{value}<extra></extra>",
            },
        }
    )

    layout = json.dumps(
        {
            "title": {
                "text": f"Azure Linux Overlay Classification ({total} entries)",
                "font": {"size": 20, "color": "#333"},
            },
            "font": {"size": 13, "family": "Inter, system-ui, sans-serif"},
            "paper_bgcolor": "#fafafa",
            "plot_bgcolor": "#fafafa",
            "margin": {"l": 30, "r": 30, "t": 60, "b": 30},
            "height": 700,
        }
    )

    def _swatch(name: str, color: str) -> str:
        return f'<div class="legend-item"><span class="legend-swatch" style="background:{color}"></span>{name}</div>'

    legend_groups = "".join(_swatch(n, c) for n, c in GROUP_COLORS.items())
    legend_cats = "".join(_swatch(n, c) for n, c in AZL_CATEGORY_COLORS.items() if n != "uncategorized")
    upstream_display = {"yes": "Upstreamable", "no": "Not upstreamable", "unknown": "Unknown"}
    legend_upstream = "".join(
        _swatch(upstream_display.get(n, n), c) for n, c in UPSTREAMABILITY_COLORS.items()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Overlay Classification - Sankey Diagram</title>
<style>
  body {{
    margin: 0;
    padding: 20px;
    background: #fafafa;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    color: #333;
  }}
  #chart {{ width: 100%; max-width: 1400px; margin: 0 auto; }}
  .legend {{
    max-width: 1400px;
    margin: 20px auto;
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
  }}
  .legend-section {{ min-width: 200px; }}
  .legend-section h3 {{
    margin: 0 0 8px 0;
    font-size: 14px;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
    font-size: 13px;
  }}
  .legend-swatch {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    flex-shrink: 0;
  }}
  .footer {{
    max-width: 1400px;
    margin: 30px auto 0;
    padding-top: 15px;
    border-top: 1px solid #ddd;
    font-size: 12px;
    color: #999;
    text-align: center;
  }}
</style>
</head>
<body>
<div id="chart"></div>

<div class="legend">
  <div class="legend-section">
    <h3>Groups</h3>
    {legend_groups}
  </div>
  <div class="legend-section">
    <h3>AZL Categories</h3>
    {legend_cats}
  </div>
  <div class="legend-section">
    <h3>Upstreamability</h3>
    {legend_upstream}
  </div>
</div>

<div class="footer">
  Generated by overlay-classifier · Azure Linux
</div>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<script>
Plotly.newPlot('chart', [{fig_data}], {layout}, {{
  responsive: true,
  displayModeBar: true,
  modeBarButtonsToRemove: ['select2d', 'lasso2d'],
  displaylogo: false
}});
</script>
</body>
</html>"""


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate Sankey diagram of overlay classifications")
    parser.add_argument("-i", "--input", required=True, help="Path to classified_overlays.json")
    parser.add_argument("-o", "--output", required=True, help="Output HTML file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(input_path.read_text())
    total = len(data.get("overlays", [])) + len(data.get("group_entries", []))

    sankey_data = _build_sankey_data(data)
    html = _generate_html(sankey_data, total)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"Sankey diagram written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
