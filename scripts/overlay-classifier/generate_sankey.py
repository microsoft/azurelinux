#!/usr/bin/env python3
"""Generate an interactive Sankey diagram of overlay classifications.

Reads classified_overlays.json and produces a standalone HTML file with
a Plotly Sankey diagram showing the flow:

    Overlay Type → Top-level Label → Sub-category (AZL-customization + Upstream-fix)

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

# -- Color palette ----------------------------------------------------------

TOP_LEVEL_COLORS = {
    "Backport-fedora": "rgba(31, 119, 180, 0.8)",
    "Upstream-fix": "rgba(255, 127, 14, 0.8)",
    "AZL-customization": "rgba(44, 160, 44, 0.8)",
}

SUB_CATEGORY_COLORS = {
    # Upstream-fix sub-categories
    "Upstreamable": "rgba(255, 187, 120, 0.7)",
    "Waiting-for-fedora": "rgba(255, 152, 48, 0.7)",
    # AZL-customization sub-categories
    "Feature-disablement": "rgba(77, 175, 74, 0.7)",
    "Test-disablement": "rgba(152, 78, 163, 0.7)",
    "Dependency-pruning": "rgba(255, 127, 0, 0.7)",
    "Build-environment": "rgba(55, 126, 184, 0.7)",
    "Missing-dependency-workaround": "rgba(228, 26, 28, 0.7)",
    "Security/compliance": "rgba(166, 86, 40, 0.7)",
    "Release-management": "rgba(247, 129, 191, 0.7)",
    "Branding": "rgba(0, 191, 255, 0.7)",
    "Platform-adaptation": "rgba(153, 153, 153, 0.7)",
    "Distro-policy-alignment": "rgba(255, 215, 0, 0.7)",
    "uncategorized": "rgba(200, 200, 200, 0.7)",
}

# -- Fallback color for unknown types/categories --
_FALLBACK = "rgba(180, 180, 180, 0.5)"


def _get_color(name: str, palette: dict[str, str]) -> str:
    return palette.get(name, _FALLBACK)


def _build_sankey_data(
    data: dict[str, Any],
) -> dict[str, Any]:
    """Build Plotly Sankey node/link structures from classified data.

    Three-layer flow:
        All Overlays → Top-level Label → Sub-category (AZL-customization + Upstream-fix)
    """
    overlays: list[dict[str, Any]] = data.get("overlays", [])
    groups: list[dict[str, Any]] = data.get("group_entries", [])
    total = len(overlays) + len(groups)

    # Top-level labels that have sub-categories
    labels_with_subcats = {"AZL-customization", "Upstream-fix"}

    # --- Count flows ---
    top_counts: Counter[str] = Counter()
    top_to_sub: Counter[tuple[str, str]] = Counter()

    for entry in [*overlays, *groups]:
        cl = entry.get("classification", {})
        top = cl.get("top_level") or "unclassified"
        sub = cl.get("sub_category") or "uncategorized"

        top_counts[top] += 1
        if top in labels_with_subcats:
            top_to_sub[(top, sub)] += 1

    # --- Build node list ---
    # Layer 0: single aggregate node
    aggregate_label = f"All Overlays ({total})"
    top_levels = sorted(top_counts.keys())
    sub_cats = sorted({k[1] for k in top_to_sub})

    nodes: list[str] = [aggregate_label]
    node_colors: list[str] = ["rgba(100, 100, 100, 0.8)"]

    for tl in top_levels:
        nodes.append(tl)
        node_colors.append(_get_color(tl, TOP_LEVEL_COLORS))

    for sc in sub_cats:
        nodes.append(sc)
        node_colors.append(_get_color(sc, SUB_CATEGORY_COLORS))

    node_index = {name: i for i, name in enumerate(nodes)}

    # --- Build links ---
    sources: list[int] = []
    targets: list[int] = []
    values: list[int] = []
    link_colors: list[str] = []

    # Layer 1 links: aggregate → top-level
    agg_idx = node_index[aggregate_label]
    for tl in top_levels:
        sources.append(agg_idx)
        targets.append(node_index[tl])
        values.append(top_counts[tl])
        color = _get_color(tl, TOP_LEVEL_COLORS).replace("0.8", "0.3")
        link_colors.append(color)

    # Layer 2 links: top-level → sub-category
    for (top, sub), count in sorted(top_to_sub.items()):
        sources.append(node_index[top])
        targets.append(node_index[sub])
        values.append(count)
        color = _get_color(sub, SUB_CATEGORY_COLORS).replace("0.7", "0.3")
        link_colors.append(color)

    return {
        "nodes": nodes,
        "node_colors": node_colors,
        "sources": sources,
        "targets": targets,
        "values": values,
        "link_colors": link_colors,
        "top_counts": dict(top_counts),
    }


def _generate_html(sankey_data: dict[str, Any], total: int) -> str:
    """Generate standalone HTML with embedded Plotly Sankey diagram."""
    nodes = sankey_data["nodes"]
    node_colors = sankey_data["node_colors"]

    # Build labels with counts
    top_counts = sankey_data.get("top_counts", {})
    node_labels: list[str] = []
    for i, n in enumerate(nodes):
        if n.startswith("All Overlays"):
            # Aggregate node already includes count in name
            node_labels.append(n)
        elif n in top_counts:
            node_labels.append(f"{n} ({top_counts[n]})")
        else:
            # Sub-category: sum incoming link values
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

    legend_tops = "".join(_swatch(n, c) for n, c in TOP_LEVEL_COLORS.items())
    legend_subs = "".join(_swatch(n, c) for n, c in SUB_CATEGORY_COLORS.items())

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
    <h3>Top-level Labels</h3>
    {legend_tops}
  </div>
  <div class="legend-section">
    <h3>Sub-categories</h3>
    {legend_subs}
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
