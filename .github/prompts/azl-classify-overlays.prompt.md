---
description: "Classify all overlays in base/comps/ by type and purpose — inventory and justify AZL deviations from Fedora"
---

# Overlay Classification

Follow the [skill-classify-overlays skill](../skills/skill-classify-overlays/SKILL.md)
to extract, classify, and report on all overlays in the repository.

The pipeline includes:
1. **Extract** overlay data from TOML files + git blame + patch headers
2. **Classify** using heuristic rules (Backport-fedora / Upstream-fix / AZL-customization)
3. **LLM refine** low/medium confidence entries
4. **Resolve Fedora versions** for Backport-fedora overlays (queries Koji to find when overlays can be removed)
5. **Generate reports** — markdown tables with Fedora fix version info + Sankey diagram

Output the final report to `base/build/work/scratch/overlay-classifier/final_report.json`.
