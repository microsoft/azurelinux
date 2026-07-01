# Shared azldev component helpers

Pipeline-agnostic shell + Python helpers consumed by the GitHub Actions
PR gates (`.github/workflows/check-rendered-specs.yml`), the ADO post-merge
package-build pipeline
(`.github/workflows/ado/templates/package-build-stages.yml`), and the ADO
PR Control Tower check
(`.github/workflows/ado/templates/pr-check-ct-stages.yml`).

| Script | Purpose |
| ------ | ------- |
| `compute_render_set.py` | Computes the union of (azldev-flagged components) and (components with hand-edited rendered specs), then drops deleted entries. |
| `compute_change_set.sh` | Runs `azldev component changed --from <base> --to <head>` inline, unions the result with `compute_render_set.py`, and writes `changed-components.json`, `specs-diff.txt`, and `render-set.txt` into a caller-chosen output directory. |

## Conventions

- **Pipeline-agnostic.** No ADO `##[group]` markers, no GH `::group::`
  markers — callers add their own. No artifact-publish trap — callers
  upload the output dir as they see fit.
- **azldev as root.** All `azldev` invocations use an inline
  `AZLDEV_ALLOW_ROOT=1` prefix per
  [`ado-pipeline.instructions.md`](../../../.github/instructions/ado-pipeline.instructions.md).
  Callers do **not** set this at step scope.
- **Single source of truth.** Every consumer should call these scripts
  rather than re-implementing the change-set computation. A regression
  here breaks every gate simultaneously, so changes need extra care.

## Callers

- `check-rendered-specs.yml` `render` job → `compute_change_set.sh`
- `package-build-stages.yml` (via `steps/prepare-change-set.yml`) → `compute_change_set.sh`
- `pr-check-ct-stages.yml` (via `steps/prepare-change-set.yml`) → `compute_change_set.sh`
