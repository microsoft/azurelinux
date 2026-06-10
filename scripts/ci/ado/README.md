# Azure DevOps pipeline helpers

Helpers for talking to the **Azure DevOps control plane** (the pipelines' own
build metadata) from ADO YAML pipelines. These use the official
[`azure-devops`](https://github.com/microsoft/azure-devops-python-api) SDK
rather than a hand-rolled REST client.

| File | Purpose |
| ---- | ------- |
| `determine_commit_range.py` | Resolves the `(target, source)` commit range for the post-merge delta build and prints it to stdout as `sourceCommit=<sha>` / `targetCommit=<sha>` lines. The calling step sets the pipeline variables. |
| `requirements.txt` | Python dependencies (`azure-devops`), installed from the internal feed via `PipAuthenticate@1`. |

## Conventions

- **Use the SDK.** Talk to ADO through the `azure-devops` package
  (`azure.devops.connection.Connection` + the typed clients), not a bespoke
  REST/`urllib` layer. The package is pinned in `requirements.txt`; bump
  deliberately.
- **Runs after dependency install.** Because the SDK is a pip dependency (not
  stdlib), any step invoking these helpers must run **after** the
  dependency-install step that does
  `pip install -r scripts/ci/ado/requirements.txt` (which itself follows
  `PipAuthenticate@1`).
- **Build-identity auth.** Calls authenticate with the pipeline's
  `System.AccessToken` using the SDK's documented `BasicAuthentication("",
  token)` pattern — the ADO REST API accepts the job access token as a
  PAT-equivalent credential. This is the ADO control plane, **not** Azure
  Resource Manager or Control Tower, so the Workload Identity Federation
  service-connection rule does not apply. In a **YAML** pipeline there is no
  "Allow scripts to access the OAuth token" toggle (that is a Classic-only
  setting) — the token is available as long as it is mapped into the step via
  `env:` (see below). The call only reads builds of this pipeline's own
  definition in the same project, so the default **project** job-authorization
  scope is sufficient and the `{Project} Build Service ({Org})` identity's
  default build-read permission covers it. Only revisit these if your org has
  tightened the defaults.
- **Secrets via `env:`.** Pass `System.AccessToken` through the step `env:`
  block (as `SYSTEM_ACCESSTOKEN`), never inline on the command line.

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
