# Overlay Classifier

Inventory and classify all overlays in Azure Linux's `base/comps/` tree into purpose-based buckets.

## Quick Start

```bash
# Step 1: Extract overlay data (TOML parsing + git blame enrichment)
python scripts/overlay-classifier/extract_overlays.py \
  --output base/build/work/scratch/overlay-classifier/extracted_overlays.json

# Step 2: Run heuristic classification
cd scripts/overlay-classifier
python classify_overlays.py \
  --input ../../base/build/work/scratch/overlay-classifier/extracted_overlays.json \
  --output ../../base/build/work/scratch/overlay-classifier/classified_overlays.json \
  --cache classifications_cache.json

# Step 3 (optional): LLM refinement via Copilot skill
# Invoke the skill to review low/medium confidence entries and write final_report.json.
# See .github/skills/skill-classify-overlays/SKILL.md for the full workflow.
# If skipping LLM refinement, copy the heuristic output as the final report:
#   cp ../../base/build/work/scratch/overlay-classifier/classified_overlays.json \
#      ../../base/build/work/scratch/overlay-classifier/final_report.json

# Step 4: Generate markdown report and Sankey diagram from final_report.json
# NOTE: Always use final_report.json (LLM-refined) rather than classified_overlays.json
#        (heuristic-only) to include the most accurate classifications.
python generate_report.py \
  -i ../../base/build/work/scratch/overlay-classifier/final_report.json \
  -o ../../base/build/work/scratch/overlay-classifier/overlay_report.md

python generate_sankey.py \
  -i ../../base/build/work/scratch/overlay-classifier/final_report.json \
  -o ../../base/build/work/scratch/overlay-classifier/sankey.html
```

## Architecture

```
Phase 1 (Deterministic)     Phase 2 (Deterministic)     Phase 3 (Non-deterministic)
┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
│ extract_overlays.py│ ───► │classify_overlays.py │ ───► │  Agent LLM pass    │
│                    │      │                     │      │  (Copilot skill)   │
│ • Parse TOML       │      │ • Apply rules from  │      │ • Classify low-    │
│ • Extract comments │      │   taxonomy.py       │      │   confidence items │
│ • git blame        │      │ • Score confidence  │      │ • Spot-check high  │
│ • Fetch commits    │      │ • Read/write cache  │      │ • Write final JSON │
└────────────────────┘      └────────────────────┘      └──────────┬─────────┘
                                                                   │
                            Phase 4 (Deterministic)                ▼
                            ┌────────────────────────────────────────┐
                            │ generate_report.py / generate_sankey.py│
                            │                                        │
                            │ • Markdown report (overlay_report.md)  │
                            │ • Interactive Sankey diagram (HTML)     │
                            └────────────────────────────────────────┘
```

## Classification Labels

### Top-level (3 buckets)

| Label | Description |
|-------|-------------|
| **Backport-fedora** | Already in newer Fedora; self-resolves when snapshot advances |
| **Upstream-fix** | Bug fix not yet in Fedora; candidate for upstreaming |
| **AZL-customization** | Intentional AZL-specific deviation |

### AZL-customization sub-categories (10 buckets)

| Sub-category | Description |
|-------------|-------------|
| Dependency-pruning | Removing deps not shipped in AZL |
| Feature-disablement | Disabling unneeded features/subpackages |
| Branding | Fedora→AzureLinux name/path changes |
| Build-environment | Toolchain/mock/CI environment adjustments |
| Test-disablement | Skipping failing tests |
| Security/compliance | FIPS, crypto policy changes |
| Release-management | Release tag and changelog mechanics |
| Missing-dependency-workaround | Temporary workarounds for unimported packages |
| Platform-adaptation | Architecture-specific adjustments |
| Distro-policy-alignment | RHEL/enterprise convention alignment |

## Data Sources

Each overlay is analyzed using three data sources:

1. **TOML fields** — parsed `type`, `description`, `tag`, `value`, `regex`, `replacement`, etc.
2. **TOML comments** — raw comment lines above each overlay block
3. **Git commit history** — `git blame` SHA → `git log` commit header + body

## Cache / Consistency

The `classifications_cache.json` file pins classification results by overlay fingerprint (hash of component + index + description + type + commit SHA). On subsequent runs:

- **Unchanged overlays** → cached classification (deterministic)
- **New/changed overlays** → heuristic re-evaluation
- **`--force-reclassify`** → ignore cache, re-run all heuristics

Human reviewers can edit the cache to correct misclassifications — corrections persist across future runs.

## Output Schema

```json
{
  "metadata": {
    "comp_toml_files_scanned": 415,
    "total_overlays": 584,
    "total_group_entries": 218,
    "unique_commits_analyzed": 188
  },
  "overlays": [
    {
      "component": "grub2",
      "file": "base/comps/grub2/grub2.comp.toml",
      "overlay_index": 0,
      "type": "file-search-replace",
      "description": "...",
      "context_comments": "...",
      "git": {
        "commit_sha": "f170384d...",
        "commit_header": "feat(grub2): disable Xen module builds",
        "commit_body": "Azure Linux targets Hyper-V/KVM, not Xen...",
        "author": "Chris Co",
        "date": "2026-04-03T12:00:00-07:00"
      },
      "fingerprint": "a1b2c3d4e5f6g7h8",
      "classification": {
        "top_level": "AZL-customization",
        "sub_category": "Feature-disablement",
        "confidence": "high",
        "classified_by": "heuristic",
        "matched_rules": ["azl-feature-disable-keyword:disable-keyword"],
        "rationale": "..."
      }
    }
  ],
  "group_entries": [ ... ],
  "summary": {
    "by_top_level": { "AZL-customization": 584, "Backport-fedora": 28, "Upstream-fix": 31 },
    "by_sub_category": { "Feature-disablement": 232, "Test-disablement": 195, ... },
    "by_confidence": { "high": 303, "medium": 340, "low": 159 },
    "pipeline_stats": { "from_cache": 0, "heuristic_high": 303, ... }
  }
}
```

## Files

| File | Role | Deterministic? |
|------|------|---------------|
| `extract_overlays.py` | TOML parser + git blame enrichment | ✅ |
| `classify_overlays.py` | Heuristic rule engine + cache | ✅ |
| `taxonomy.py` | Label definitions + signal patterns | ✅ |
| `generate_report.py` | Markdown report generator | ✅ |
| `generate_sankey.py` | Interactive Sankey diagram (HTML) | ✅ |
| `classifications_cache.json` | Pinned results for consistency | ✅ |
| `SKILL.md` | Agent skill for LLM refinement | ❌ (LLM) |

## Classification Logic Summary

### Pipeline Overview

```
Phase 1: Extract          Phase 2: Heuristic         Phase 3: LLM           Phase 4: Report
TOML parse + git blame → 41 regex rules by priority → Decision tree (Q0-Q4) → MD + Sankey HTML
                          ↕ cache (fingerprint-keyed)
```

### Heuristic Engine (Phase 2)

- **41 rules** sorted by descending priority:
  - Backport-fedora (priority 100→90)
  - Upstream-fix (priority 80→65)
  - AZL sub-categories (priority 55→35)
- Each rule has signal patterns (compiled regexes) that match against specific overlay
  fields or `all_text` (description + comments + commit header + commit body).
- **Winner:** highest-priority matching rule.
- **3-tier confidence:**
  - `high` — single top-level + single sub-category matched
  - `medium` — same top-level, conflicting sub-categories
  - `low` — conflicting top-levels or no rules matched at all

### LLM Decision Tree (Phase 3)

```
Q0: Companion overlay? (same component, supports a sibling overlay)
    → YES: Inherit sibling's classification
    → NO: continue

Q1: Fedora backport signals? (dist-git URL, "backport", "cherry-pick", "rawhide")
    → YES: Backport-fedora
    → NO: continue

Q2: CVE / upstream URL / bug tracker reference?
    → YES: Upstream-fix
    → NO: continue

Q3: file-add adding a .patch from upstream author / upstream bug ID / toolchain compat?
    → YES: Upstream-fix
    → NO: continue

Q4: AZL-customization → pick from 10 sub-categories
```

**Key principles:**
1. Always check patch authorship and origin before defaulting to AZL-customization.
2. Companion overlays (file-add + spec-add-tag + spec-search-replace serving the same
   purpose) should share the same classification.

## Difficulties & Limitations

### Missing Metadata

~95 overlays have no description, no comments, and no git blame data (inline syntax
in `components.toml`). Heuristics have nothing to match against — these always fall
to low confidence and require LLM review.

### Companion Overlay Grouping

A single logical change often spans 2–6 overlays (e.g., `file-add` + `spec-add-tag` +
`spec-search-replace` to add and apply a patch). The heuristic engine classifies each
overlay independently with no cross-overlay context. Only the LLM decision tree (Q0)
handles grouping by checking sibling overlays and shared `commit_sha`.

### Ambiguous Sub-categories

306 overlays match multiple sub-categories (e.g., removing a `BuildRequires` could be
Dependency-pruning OR Feature-disablement). Priority ordering resolves the conflict
deterministically but may not always pick the most appropriate sub-category.

### Upstream vs. AZL-specific Patches

A `file-add` patch with no description requires reading the actual `.patch` file content
to determine authorship and origin. The heuristic engine only sees the filename; the LLM
must inspect the file itself (Q3 in the decision tree).

### Temporal Context

Distinguishing "Backport-fedora" from "Upstream-fix" depends on whether a fix has landed
in Fedora's tracked branch *at classification time*. This is not checked programmatically
— it relies on description text containing phrases like "fixed in rawhide" or Fedora
dist-git URLs.

### LLM Non-determinism

Phase 3 classifications may vary between runs. Mitigated by the fingerprint-keyed cache
(pinned after first classification), but the initial LLM pass needs manual spot-checking.
The apache-ivy case showed the LLM misclassifying upstream patches as Feature-disablement.

### No Spec Content Analysis

The classifier does not read the rendered spec or upstream spec — it only sees overlay
fields (regex, replacement, tag, value). Context like "what spec section this overlay
modifies" is inferred from patterns, not parsed from the actual spec file.

### Group Entry Granularity

The 218 entries from `component-check-disablement.toml` and
`component-mingw-disablement.toml` are bulk-classified by group description. Individual
component context is lost — all entries in a group share the same classification.

### Cache Staleness

Cache keys include `commit_sha`. If an overlay is re-committed (amended/rebased), the
fingerprint changes and it needs re-classification, even if the overlay content is
identical.

## Accuracy Estimates

| Tier | Count | Estimated Accuracy | Notes |
|------|------:|-------------------:|-------|
| High confidence (heuristic) | 305 | ~95% | Single consistent signal |
| Medium confidence (heuristic) | 306 | ~85% | Top-level correct, sub-category may be wrong |
| Low / LLM-classified | 191 | ~75% | Needs spot-checking (e.g., apache-ivy misclassification) |
