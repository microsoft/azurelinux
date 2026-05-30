# Shared azldev component helpers

Pipeline-agnostic shell + Python helpers consumed by both the GitHub Actions
PR gates (`.github/workflows/check-rendered-specs.yml`) and the ADO
Control Tower integration pipeline
(`.github/workflows/ado/templates/sources-upload-stages.yml`).

| Script | Purpose |
| ------ | ------- |
| `compute_changed.sh` | Wraps `azldev component changed --from <target> --to <source> -O json`. |
| `compute_render_set.py` | Computes the union of (azldev-flagged components) and (components with hand-edited rendered specs), then drops deleted entries. |
| `compute_change_set.sh` | Orchestrates the two above: writes `changed-components.json`, `specs-diff.txt`, and `render-set.txt` into a caller-chosen output directory. |

## Conventions

- **Pipeline-agnostic.** No ADO `##[group]` markers, no GH `::group::`
  markers — callers add their own. No artifact-publish trap — callers
  upload the output dir as they see fit.
- **azldev as root.** All `azldev` invocations use an inline
  `AZLDEV_ALLOW_ROOT=1` prefix per
  [`ado-pipeline.instructions.md`](../../../instructions/ado-pipeline.instructions.md).
  Callers do **not** set this at step scope.
- **Single source of truth.** Both pipelines should call these scripts
  rather than re-implementing the change-set computation. A regression
  here breaks both gates simultaneously, so changes need extra care.

## Callers

- `check-rendered-specs.yml` `render` job → `compute_change_set.sh`
- `sources-upload-stages.yml` "Prepare change set" step → `compute_change_set.sh`
