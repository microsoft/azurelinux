# Azure DevOps REST helpers

Shared helpers for talking to the **Azure DevOps control plane** (the
pipelines' own build metadata) from ADO YAML pipelines. Reusable across
pipelines — add new ADO REST helpers here rather than re-implementing auth and
paging per pipeline.

| File | Purpose |
| ---- | ------- |
| `ado_rest.py` | Stdlib-only (`urllib`) ADO REST client: `AdoConnection` (with `from_env()`), `get_json` (auth + retry), `list_builds`. |
| `determine_commit_range.py` | Resolves the `(target, source)` commit range for the post-merge delta build and prints it to stdout as `sourceCommit=<sha>` / `targetCommit=<sha>` lines. The calling step sets the pipeline variables. |

## Conventions

- **Stdlib only.** `ado_rest.py` uses `urllib`, not `requests`, so it can run
  in any step **without** a prior `pip install` — including before the
  dependency-install step. Keep it dependency-free.
- **Build-identity auth.** Calls authenticate with the pipeline's
  `System.AccessToken` (a bearer token the ADO REST API accepts directly). This
  is the ADO control plane, **not** Azure Resource Manager or Control Tower, so
  the Workload Identity Federation service-connection rule does not apply. In a
  **YAML** pipeline there is no "Allow scripts to access the OAuth token"
  toggle (that is a Classic-only setting) — the token is available as long as
  it is mapped into the step via `env:` (see below). The REST call only reads
  builds of this pipeline's own definition in the same project, so the default
  **project** job-authorization scope is sufficient and the `{Project} Build
  Service ({Org})` identity's default build-read permission covers it. Only
  revisit these if your org has tightened the defaults.
- **Secrets via `env:`.** Pass `System.AccessToken` through the step `env:`
  block (as `SYSTEM_ACCESSTOKEN`), never inline on the command line.
- **Pinned API version.** `ado_rest._API_VERSION` is pinned; bump deliberately.

## Caller contract

`determine_commit_range.py` expects:

- **Args:** `--definition-id`, `--current-build-id`, `--branch` (full ref, e.g.
  `refs/heads/4.0`), `--source-commit`, `--repo-uri`, optional `--top`.
- **Env:** `SYSTEM_COLLECTIONURI`, `SYSTEM_TEAMPROJECT`, `SYSTEM_ACCESSTOKEN`.
- **Output:** two `key=value` lines on **stdout** (`sourceCommit=<sha>` and
  `targetCommit=<sha>`); all diagnostics go to **stderr**. The caller parses
  stdout and owns the `##vso[task.setvariable]` wiring, so pipeline-variable
  assignment stays visible in the YAML.

It is best-effort: if the previous build cannot be found (first run) or the ADO
query fails, it falls back to `target = source^1` (warning on stderr) rather
than failing the pipeline. A hard failure (invalid source SHA, or no parent
found for the fallback) exits non-zero so the calling step fails.

## Callers

- `sources-upload-stages.yml` "Determine source and target commit range" step →
  `determine_commit_range.py`
