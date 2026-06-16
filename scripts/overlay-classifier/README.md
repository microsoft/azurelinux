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

# Step 4: Resolve Fedora fix versions for Backport-dist-git overlays
# Queries Fedora Koji to find which version has the fix (tells you when overlays can be removed)
python resolve_fedora_versions.py \
  -i ../../base/build/work/scratch/overlay-classifier/final_report.json \
  -o ../../base/build/work/scratch/overlay-classifier/final_report.json \
  --azl-fedora-version 43

# Step 5: Generate markdown report and Sankey diagram from final_report.json
# NOTE: Always use final_report.json (LLM-refined + enriched) rather than
#        classified_overlays.json (heuristic-only) to include the most accurate data.
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
                            Phase 3.5 (Deterministic)              ▼
                            ┌────────────────────────────────────────┐
                            │ resolve_fedora_versions.py             │
                            │                                        │
                            │ • Query Fedora Koji for Backport-dist-git│
                            │ • Find fix NVR + earliest Fedora tag   │
                            │ • Add removable_when guidance          │
                            └──────────────────┬─────────────────────┘
                                               │
                            Phase 4 (Deterministic)                ▼
                            ┌────────────────────────────────────────┐
                            │ generate_report.py / generate_sankey.py│
                            │                                        │
                            │ • Markdown report (overlay_report.md)  │
                            │ • Fedora Fix Versions table            │
                            │ • Interactive Sankey diagram (HTML)     │
                            └────────────────────────────────────────┘
```

## Classification Labels

All labels are flat — no hierarchy. Labels with the `AZL-` prefix represent AZL-specific customizations; the Sankey diagram groups them under a virtual "AZL-customization" node for visual clarity.

| Label | Description |
|-------|-------------|
| **Backport-dist-git** | Fix IS in upstream dist-git (Fedora or upstream project repo). Overlay applies the actual fix. Self-resolves when AZL bumps its upstream pin. |
| **AZL-dependency-pruning** | Removing deps not shipped in AZL |
| **AZL-feature-disablement** | Disabling unneeded features/subpackages |
| **AZL-branding-policy** | Fedora→AzureLinux name/path changes; RHEL/enterprise convention alignment |
| **AZL-build** | Toolchain/mock/CI environment adjustments |
| **AZL-test-disablement** | Skipping failing tests |
| **AZL-security** | FIPS, crypto policy changes |
| **AZL-release-management** | Release tag and changelog mechanics |
| **AZL-missing-dependency-workaround** | Temporary workarounds for unimported packages |
| **AZL-platform-adaptation** | Architecture-specific adjustments |

> **Key distinction — fix vs. workaround:** If an overlay **applies the upstream fix** →
> Backport-dist-git. If it **works around** the problem (disables a feature,
> skips a test) → one of the AZL-* categories, even if the fix exists upstream.

## Data Sources

Each overlay is analyzed using four data sources:

1. **TOML fields** — parsed `type`, `description`, `tag`, `value`, `regex`, `replacement`, etc.
2. **TOML comments** — raw comment lines above each overlay block
3. **Git commit history** — `git blame` SHA → `git log` commit header + body + author
4. **Patch file headers** — first 4KB of `.patch`/`.diff` files: author, subject, PR URLs, bug IDs, close refs

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
        "top_level": "AZL-feature-disablement",
        "confidence": "high",
        "classified_by": "heuristic",
        "matched_rules": ["azl-feature-disable-keyword:disable-keyword"],
        "rationale": "...",
        "upstreamability": "yes",
        "upstreamability_rule": "upstream-yes-needs-fix",
        "upstreamability_rationale": "Matched rule: upstream-yes-needs-fix (signal: ...)"
      }
    }
  ],
  "group_entries": [ ... ],
  "summary": {
    "by_top_level": { "AZL-feature-disablement": 232, "AZL-test-disablement": 195, "Backport-dist-git": 59, ... },
    "by_upstreamability": { "yes": 120, "no": 380, "unknown": 302 },
    "by_confidence": { "high": 303, "medium": 340, "low": 159 },
    "pipeline_stats": { "from_cache": 0, "heuristic_high": 303, ... }
  }
}
```

## Files

| File | Role | Deterministic? |
|------|------|---------------|
| `extract_overlays.py` | TOML parser + git blame + patch header enrichment | ✅ |
| `classify_overlays.py` | Heuristic rule engine + cache | ✅ |
| `taxonomy.py` | Label definitions + signal patterns + 44 category rules + 9 upstreamability rules | ✅ |
| `resolve_fedora_versions.py` | Koji queries for Backport-dist-git fix NVRs | ✅ (network-dependent) |
| `generate_report.py` | Markdown report generator | ✅ |
| `generate_sankey.py` | Interactive Sankey diagram (HTML) | ✅ |
| `classifications_cache.json` | Pinned results for consistency | ✅ |
| `SKILL.md` | Agent skill for LLM refinement | ❌ (LLM) |

## Classification Logic Summary

### Pipeline Overview

```
Phase 1: Extract          Phase 2: Heuristic         Phase 3: LLM           Phase 3.5: Koji     Phase 4: Report
TOML + git + patch hdrs → 44 rules by priority      → Decision tree (Q0-Q4)→ Fix version lookup → MD + Sankey HTML
                          ↕ cache (fingerprint-keyed)
```

### Heuristic Engine (Phase 2)

- **44 rules** sorted by descending priority:
  - Workaround override (priority 85) — requires BOTH workaround + disable keywords (AND logic)
  - Backport-dist-git (priority 100→65) — Fedora dist-git URLs, backport/cherry-pick keywords, CVE, upstream URLs, PRs, bug IDs, upstream patch authors, patch-add without Fedora URL, fix commit headers
  - AZL-* categories (priority 55→35) — feature/test disablement, dependency pruning, branding, etc.
- **Signal types:** compiled regexes matching against text fields, OR structural checks (overlay type, build config, patch author domain)
- **Rule logic:** Most rules use OR (any signal fires the rule). The workaround rule uses AND (`require_all=True` — both signals must match).
- **Winner:** highest-priority matching rule determines the flat category label.
- **3-tier confidence:**
  - `high` — single label matched
  - `medium` — multiple AZL-* categories matched (conflicting AZL labels)
  - `low` — conflicting between Backport and AZL labels, or no rules matched
- **Upstreamability** — 9 additional rules (separate from category rules) evaluate independently:
  - Backport-dist-git → always `no` (fix already upstream)
  - AZL-branding-policy, AZL-release-management → fallback `no` (inherently AZL-specific)
  - Signal-based `yes`: self-authored patches without upstream PR, workaround keywords, flaky test skips, "upstream lacks" patterns, missing dependency workarounds
  - Signal-based `no`: branding/vendor keywords, release tag overlays, AZL-specific infra
  - Default: `unknown` when no signals match

### LLM Decision Tree (Phase 3)

```
Q0: Companion overlay? (same component, supports a sibling overlay)
    → YES: Inherit sibling's classification
    → NO: continue

Q1: Does any text reference a Fedora dist-git commit URL, upstream commit/PR/bug URL,
    CVE, "backport", "cherry-pick", or "fixed in f4x/rawhide"?
    → YES: verify fix vs. workaround
      → Overlay applies the actual fix → Backport-dist-git
      → Overlay works around the problem → AZL-customization
    → NO: continue

Q2: Is this a file-add overlay adding a patch (.patch/.diff)?
    If YES, examine the patch content:
    a) Is the patch authored by an upstream contributor (not an AZL/Microsoft author)?
    b) Does the patch filename or commit message reference an upstream bug tracker ID?
    c) Does the patch come from the upstream project's own repo?
    → If (a) OR (b) OR (c): Backport-dist-git
    → Otherwise: continue

Q3: This is an AZL customization. Which AZL-* category?
    → pick from the 9 AZL-* categories
```

**Key principles:**
1. Always check patch authorship and origin before defaulting to AZL-customization.
2. Companion overlays (file-add + spec-add-tag + spec-search-replace serving the same
   purpose) should share the same classification.
3. When a patch has a PR URL or bug reference, verify whether the fix is included in
   the version Fedora currently ships. A merged PR does NOT mean it's in Fedora.
4. "In Fedora" means available in **any** Fedora branch, not just AZL's tracked branch.
   If the overlay applies the upstream fix → Backport-dist-git. If it works around the
   problem → AZL-customization.

## Difficulties & Limitations

### Missing Metadata

~144 overlays have no description, no comments, and no git blame data (inline syntax
in `components.toml`). Heuristics have nothing to match against — these always fall
to low confidence and require LLM review.

### Companion Overlay Grouping

A single logical change often spans 2–6 overlays (e.g., `file-add` + `spec-add-tag` +
`spec-search-replace` to add and apply a patch). The heuristic engine classifies each
overlay independently with no cross-overlay context. Only the LLM decision tree (Q0)
handles grouping by checking sibling overlays and shared `commit_sha`.

### Ambiguous Categories

~315 overlays match multiple AZL-* categories (e.g., removing a `BuildRequires` could be
AZL-dependency-pruning OR AZL-feature-disablement). Priority ordering resolves the conflict
deterministically but may not always pick the most appropriate category.

### Fix vs. Workaround Distinction

The classifier must distinguish overlays that **apply the actual fix** (Backport-dist-git)
from those that **work around** the problem (AZL-customization). This
requires understanding semantic intent, not just pattern matching:
- "Disable doc generation to work around cliff incompatibility" → workaround → AZL-customization
- "Add patch to fix Makefile race from upstream" → actual fix → Backport-dist-git

The `require_all` AND-logic on the workaround rule (`workaround-keyword` + `disable-keyword`)
helps but doesn't cover all cases. The LLM is significantly more precise here.

### Upstream vs. AZL-specific Patches

A `file-add` patch with no description requires reading the actual `.patch` file content
to determine authorship and origin. The heuristic reads the first 4KB of patch headers
for author/subject/PR URLs, but cannot follow URLs to verify PR merge status or check
which upstream release contains the fix.

### Temporal Context

The `resolve_fedora_versions.py` script queries Koji to find fix NVRs for
Backport-dist-git entries. The initial classification relies on description text
containing phrases like "fixed in rawhide" or Fedora dist-git URLs.

### Cache Contamination

The fingerprint-keyed cache can accumulate stale LLM overrides from `final_report.json`.
If the heuristic rules change, the cache must be **fully deleted** before re-running —
`--force` alone is not sufficient because it reclassifies but writes results back into
the same cache file. Always `rm -f classifications_cache.json` before a clean re-run
after taxonomy or rule changes.

### LLM Non-determinism

Phase 3 classifications may vary between runs. Mitigated by the fingerprint-keyed cache
(pinned after first classification), but the initial LLM pass needs manual spot-checking.
Past cases of LLM misclassification include:
- apache-ivy: upstream patches misclassified as Feature-disablement
- vamp-plugin-sdk: upstream fix misclassified as AZL-customization (misleading commit header)

### No Spec Content Analysis

The classifier does not read the rendered spec or upstream spec — it only sees overlay
fields (regex, replacement, tag, value). Context like "what spec section this overlay
modifies" is inferred from patterns, not parsed from the actual spec file.
