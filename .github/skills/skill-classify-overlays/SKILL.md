---
name: skill-classify-overlays
description: "[Skill] Classify all overlays in base/comps/ into Backport-dist-git or AZL-customization buckets with sub-categories. Triggers: classify overlays, overlay inventory, overlay report, categorize overlays, overlay audit."
---

# Classify Overlays

Inventory and classify every overlay in the Azure Linux component tree by purpose and role.

## Prerequisites

- Python 3.11+ (for `tomllib`)
- Git (for `git blame`)

## Workflow

### Step 1 — Extract overlay data

```bash
python scripts/overlay-classifier/extract_overlays.py \
  --comps-dir base/comps \
  --output base/build/work/scratch/overlay-classifier/extracted_overlays.json
```

This parses all `.comp.toml` files and group TOML files, extracts overlay fields + TOML comments, and enriches each entry with git blame data (commit SHA, header, body, author, date).

### Step 2 — Run heuristic classification

```bash
cd scripts/overlay-classifier && python classify_overlays.py \
  --input ../../base/build/work/scratch/overlay-classifier/extracted_overlays.json \
  --output ../../base/build/work/scratch/overlay-classifier/classified_overlays.json \
  --cache classifications_cache.json
```

This applies deterministic heuristic rules from `taxonomy.py` against all three data sources (TOML fields, comments, git commit messages). Outputs a classified JSON with confidence scores.

**Cache behavior:** If `classifications_cache.json` exists and an overlay's fingerprint matches a cached entry, the cached classification is used (skip re-evaluation). Use `--force-reclassify` to ignore cache.

### Step 3 — LLM refinement (your job)

Load `classified_overlays.json` and review entries that need attention:

- **`low` confidence (no top-level):** No heuristic rules matched — needs full classification.
- **`low` confidence (with top-level):** Conflicting top-level signals — top-level needs verification, sub-category needs assignment.
- **`medium` confidence:** Top-level is reliable, but multiple sub-categories matched — pick the correct one.

For each entry needing review:

1. Read the `description`, `context_comments`, and `git.commit_header` / `git.commit_body`
2. Apply the following decision tree:

**Decision Tree:**

```
Q0: Is this a companion overlay that supports another overlay in the SAME component?
    Examples:
    - spec-add-tag (Source/Patch) referencing a .patch/.diff added by a sibling file-add
    - spec-search-replace or spec-append-lines that modifies %prep/%setup/%build to
      accommodate files or changes introduced by a sibling patch overlay
    - Multiple overlays that share the same git commit (same commit_sha) and clearly
      serve the same purpose
    → YES: Inherit the classification of the primary overlay they support.
    → NO: continue

Q1: Does any text reference a Fedora dist-git commit URL (src.fedoraproject.org/rpms/*/c/)?
    OR mention "backport", "backports", "cherry-pick", or "fixed in f4x/rawhide"?
    OR reference a CVE, upstream bug tracker URL, upstream commit URL, or upstream PR URL?
    → YES: verify fix vs. workaround (see Step 4 below)
    → NO: continue

Q2: Is this a file-add overlay adding a patch (.patch/.diff)?
    If YES, examine the patch content:
    a) Is the patch authored by an upstream contributor (not an AZL/Microsoft author)?
    b) Does the patch filename or commit message reference an upstream bug tracker ID
       (e.g., IVY-1652, bz#NNNN, GH-NNN) or fix a compatibility issue with a newer
       toolchain/runtime (e.g., Java 14+, GCC 15, Python 3.13)?
    c) Does the patch come from the upstream project's own repo (not an AZL-specific change)?
    → If (a) OR (b) OR (c):
      - Verify fix vs. workaround → Backport-dist-git if it applies the actual fix
    → Otherwise: continue

Q3: This is an AZL customization. Which AZL-* category?
    → Does it REMOVE a BuildRequires/Requires because the dep isn't in AZL? → AZL-dependency-pruning
    → Does it DISABLE a feature, subpackage, or build option? → AZL-feature-disablement
    → Does it change Fedora/Red Hat names/paths/branding to Azure Linux, or align with RHEL/enterprise conventions? → AZL-branding-policy
    → Does it fix a build toolchain, compiler, or mock environment difference? → AZL-build
    → Does it skip, disable, or work around tests? → AZL-test-disablement
    → Does it relate to FIPS, crypto policy, or security compliance? → AZL-security
    → Does it set/manage the Release tag or %autorelease? → AZL-release-management
    → Does it add a workaround for a package not yet imported into AZL? → AZL-missing-dependency-workaround
    → Does it adjust for architecture-specific behavior? → AZL-platform-adaptation
```

**Fix vs. workaround verification (Step 4):**

Before classifying as Backport-dist-git, determine whether the overlay APPLIES the actual
fix or merely WORKS AROUND the problem:
- Example: python-heatclient disables doc generation because python-cliff has a sphinxext
  bug → The overlay does NOT apply the cliff fix — it disables docs → AZL-customization
- Contrast: sos/Policy-Fix-os_release_name-value.patch backports the actual upstream fix
  → Backport-dist-git

> **Key principle 1:** When an overlay adds a patch file, always check patch authorship and
> origin before defaulting to AZL-customization. Patches from upstream projects that fix
> bugs or compatibility issues are Backport-dist-git, even if they aren't referenced by URL.
>
> **Key principle 2:** Overlays often come in groups (e.g., file-add + spec-add-tag +
> spec-search-replace to apply a patch). Companion overlays that serve the same purpose
> should share the same classification as the primary overlay they support.
>
> **Key principle 3:** When a patch has a PR URL or bug reference, always verify whether
> the fix is included in the version Fedora currently ships. A merged PR does NOT
> automatically mean it's in Fedora — it must be in a released version that Fedora
> packages. Use `gh` and Fedora APIs to check programmatically.
>
> **Key principle 4:** "In Fedora" means available in **any** Fedora branch, not just
> AZL's tracked branch. If the actual fix is in Fedora F45 but AZL tracks F43, and
> the overlay **applies the upstream fix** (backports it), that's Backport-dist-git.
> But if the overlay **works around** the problem (e.g., disables a feature because
> a dependency is too old), that's AZL-customization — the overlay itself isn't
> upstreamable even though the underlying fix exists somewhere.

3. For **low-confidence entries**: assign the correct `top_level` (flat AZL-* label), set `confidence` to "high", and `classified_by` to "llm".
4. For **medium-confidence entries**: verify the `top_level`, pick the correct AZL-* category, upgrade `confidence` to "high", and set `classified_by` to "llm".
5. For **high-confidence heuristic entries**: spot-check ~10% to validate accuracy. Override any misclassifications.

### Step 4 — Write final report

Write the completed report to:
```
base/build/work/scratch/overlay-classifier/final_report.json
```

### Step 4.5 — Resolve Fedora fix versions for Backport-dist-git overlays

For each Backport-dist-git overlay, query Fedora Koji to determine which Fedora
package version contains the backported fix. This tells the team when overlays
can be safely removed (i.e., when AZL bumps its upstream pin).

```bash
python scripts/overlay-classifier/resolve_fedora_versions.py \
  -i base/build/work/scratch/overlay-classifier/final_report.json \
  -o base/build/work/scratch/overlay-classifier/final_report.json \
  --azl-fedora-version 43
```

> The `--azl-fedora-version` should match `default-version` in
> `distro/fedora.distro.toml` (currently `43`).

Each Backport-dist-git entry gets a `fedora_fix_info` field:
- `azl_tag` / `azl_nvr` — Fedora tag and NVR that AZL currently tracks
- `fix_tag` / `fix_nvr` — Earliest newer Fedora tag that has a different (fixed) NVR
- `removable_when` — Human-readable guidance (e.g., "Remove overlay when bumping to f44+")
- `fedora_commits` — Any Fedora dist-git commit hashes referenced in overlay text

### Step 5 — Update cache

After classification, update the cache so future runs are deterministic for these overlays:
```bash
cp base/build/work/scratch/overlay-classifier/final_report.json \
   base/build/work/scratch/overlay-classifier/classified_overlays.json
```

The cache file (`scripts/overlay-classifier/classifications_cache.json`) is updated automatically by `classify_overlays.py`.

### Step 6 — Generate reports and diagram

Generate the markdown report and interactive Sankey diagram:

```bash
python scripts/overlay-classifier/generate_report.py \
  -i base/build/work/scratch/overlay-classifier/final_report.json \
  -o base/build/work/scratch/overlay-classifier/overlay_report.md

python scripts/overlay-classifier/generate_sankey.py \
  -i base/build/work/scratch/overlay-classifier/final_report.json \
  -o base/build/work/scratch/overlay-classifier/sankey.html
```

**Outputs:**
- `overlay_report.md` — Markdown tables grouped by top-level label and sub-category, with per-entry details and summary statistics. Backport-dist-git section includes a **Fedora Fix Versions** table showing the AZL-tracked NVR, the fixed NVR, and when overlays can be removed.
- `sankey.html` — Interactive Plotly Sankey diagram showing the flow: All Overlays → Top-level Label → Sub-category (open in a browser).

### Step 7 — Summary

Print a summary table to the console showing:
- Count per top-level label
- Count per sub-category
- Count by confidence level
- Count by classification source (heuristic vs cache vs llm)

## Output Schema

See `scripts/overlay-classifier/README.md` for the full JSON schema documentation.

## Taxonomy Reference

See `.github/instructions/overlay-classification.instructions.md` for the full taxonomy definitions, sub-category descriptions, and heuristic signal map.
