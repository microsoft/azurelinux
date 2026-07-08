# Azure DevOps pipeline helpers

Helpers for talking to the **Azure DevOps control plane** (the pipelines' own
build metadata) from ADO YAML pipelines, using the official
[`azure-devops`](https://github.com/microsoft/azure-devops-python-api) SDK.

| File | Purpose |
| ---- | ------- |
| `determine_commit_range.py` | Resolves the `(base, source)` commit range for the post-merge delta build and prints it to stdout as `sourceCommit=<sha>` / `baseCommit=<sha>` lines. The calling step sets the pipeline variables. |
| `requirements.txt` | Python dependencies (`azure-devops`), installed from the internal feed. |

## Conventions

- **Use the SDK.** Talk to ADO through the `azure-devops` package, not a
  bespoke REST layer. Pinned in `requirements.txt`; bump deliberately.
- **Auth + step ordering** follow the "Reading ADO build metadata" section of
  [`ado-pipeline.instructions.md`](../../../.github/instructions/ado-pipeline.instructions.md):
  build-identity `System.AccessToken` auth, and the helper runs **after** the
  dependency-install step because the SDK is a pip dependency.

## Caller contract

`determine_commit_range.py` expects:

- **Args:** `--definition-id`, `--current-build-id`, `--branch` (full ref, e.g.
  `refs/heads/4.0`), `--source-commit`, optional `--top`.
- **Env:** `SYSTEM_COLLECTIONURI`, `SYSTEM_TEAMPROJECT`, `SYSTEM_ACCESSTOKEN`.
- **Git:** read-only. It assumes the full history is already present (the
  pipeline's "Ensure full git history" step fetches it once up front) and never
  fetches — a `git fetch --depth=N` would re-shallow a full clone.
- **Output:** two `key=value` lines on **stdout** (`sourceCommit=<sha>` and
  `baseCommit=<sha>`); all diagnostics go to **stderr**. The caller parses
  stdout and owns the `##vso[task.setvariable]` wiring, so pipeline-variable
  assignment stays visible in the YAML.

It is best-effort: if the previous build cannot be found (first run) or the ADO
query fails, it falls back to `base = source^1` (warning on stderr) rather
than failing the pipeline. A hard failure (invalid source SHA, or no parent
found for the fallback) exits non-zero so the calling step fails.

## Callers

- `templates/steps/commit-range-postmerge.yml` "Determine source and base
  commit range" step → `determine_commit_range.py` (used by the post-merge
  package-build pipeline).
