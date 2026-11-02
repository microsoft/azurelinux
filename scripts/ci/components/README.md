# Shared azldev component helpers

Pipeline-agnostic shell + Python helpers consumed by the GitHub Actions
PR gates (`.github/workflows/check-rendered-specs.yml` and
`.github/workflows/check-base-promotions.yml`), the ADO post-merge
package-build pipeline
(`.github/workflows/ado/templates/package-build-stages.yml`), and the ADO
PR Control Tower check
(`.github/workflows/ado/templates/pr-check-ct-stages.yml`).

| Script | Purpose |
| ------ | ------- |
| `compute_render_set.py` | Computes the union of (azldev-flagged components) and (components with hand-edited rendered specs), then drops deleted entries. |
| `compute_change_set.sh` | Runs `azldev component changed --from <base> --to <head>` inline, unions the result with `compute_render_set.py`, and writes the three change-set artifacts without enforcing publishing policy. |
| `check_base_promotions.py` | Requires every newly listed Base component to have `changeType` of `added` or `changed` in the same range's `changed-components.json`. |
| `prepare_base_promotion_merge.sh` | Creates and checks out a temporary merge of the captured target and PR head for the Base promotion comparison; conflicts fail the gate. |

## Base promotion gate

Publishing configuration does not affect build fingerprints. A routing-only
change therefore does not submit an official rebuild or republish old RPMs.
The guard reads committed TOML at both refs and checks membership additions
against the actual build selection, not spec-tree changes or `sourcesChange`.
New components and genuine input changes pass without an extra manual bump;
reordering, comments, and removals do not require one.

The dedicated GitHub workflow
[`Check Base Promotions`](../../../.github/workflows/check-base-promotions.yml)
computes the change set and explicitly invokes the guard. It runs independently
of rendered-spec checks, including when the azldev pin changes. The workflow
captures the trusted checkout's SHA once and uses it for both version resolution
and a prospective merge with the PR head, rather than mixing it with the
event-time base. Both membership and build selection compare that target snapshot
to the merged commit, with the merged checkout supplying azldev configuration.
Already-landed bumps therefore do not count even when a stacked parent landed
under rewritten SHAs. Target-only changes are retained rather than misread as PR
changes, and merge conflicts fail explicitly.
Lock freshness and rendered-spec correctness remain companion checks; keep those
and the new promotion check required in branch policy. Change-set helpers, the
runner, merge helper, and promotion checker come from the trusted base. Only when
that base lacks a promotion helper during bootstrap does the workflow use its
PR-head copy. Both paths run
inside the unprivileged, secret-free container. A trusted-checker failure remains
fatal; it never falls back to the proposed copy. Tests exercise proposed checker
changes independently of the trusted policy check.

Promotion policy runs only in the GitHub PR workflow, not in Azure Pipelines or
after merge. The workflow retains the change-set JSON artifact on failure.
Missing build selections and malformed input fail the check; there is no
warning-only mode. Existing ADO change-set preparation and render validation
remain unchanged.

For the contributor workflow and publication verification, see
[Package publishing channels](../../../DEVELOPING.md#package-publishing-channels).

## Tests

```bash
python3 -m pip install -r scripts/ci/components/tests/requirements.txt
mkdir -p base/build/work/scratch
python3 -m pytest scripts/ci/components/tests \
  --basetemp base/build/work/scratch/base-promotion-tests
```

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
- `check-base-promotions.yml` → `prepare_base_promotion_merge.sh`, `compute_change_set.sh`, then `check_base_promotions.py`
- `package-build-stages.yml` (via `steps/prepare-change-set.yml`) → `compute_change_set.sh`
- `pr-check-ct-stages.yml` (via `steps/prepare-change-set.yml`) → `compute_change_set.sh`
