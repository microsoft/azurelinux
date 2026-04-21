---
applyTo: ".github/workflows/ado/*.yml,.github/workflows/scripts/**"
description: "Authoring and maintenance rules for Azure DevOps YAML pipelines under .github/workflows/ado/ (and their helper scripts under .github/workflows/scripts/) that run as GitHub PR checks or in the merge queue. Apply when creating or modifying any pipeline in that folder, or any script invoked by one — covers required OneBranch templates (Official vs NonOfficial), Workload Identity Federation service connections, Control Tower audience URIs, internal-only dependency sources (Go / Python / container images), Python-over-shell scripting, and security hardening."
---

# Azure DevOps Pipelines (PR check & merge queue)

These instructions cover ADO YAML pipelines under `.github/workflows/ado/` that run as GitHub PR checks or in the merge queue, plus their helper scripts under `.github/workflows/scripts/`. Follow every MUST below — they encode internal Microsoft policy plus security hardening for this repo.

Helper scripts invoked from these pipelines MUST live under `.github/workflows/scripts/<area>/` (one subdirectory per logical area / pipeline). Keep them self-contained and follow the same security hardening rules as the pipeline YAML itself.

> If anything below conflicts with what the user is asking for, **stop and ask the user** rather than guessing — especially for the Official vs NonOfficial template choice.

## OneBranch templates (MANDATORY)

To comply with internal policy, every pipeline in this folder MUST extend a OneBranch governed template:

```yaml
resources:
  repositories:
    - repository: templates
      type: git
      name: OneBranch.Pipelines/GovernedTemplates
      ref: refs/heads/main   # exception to the "no floating refs" rule (see Security)

extends:
  template: v2/OneBranch.<Variant>.CrossPlat.yml@templates
```

Pick the variant by **what the pipeline talks to at runtime AND how it is classified in ADO**:

| Variant | When to use |
|---------|-------------|
| `v2/OneBranch.Official.CrossPlat.yml@templates` | Pipeline interacts with **production** resources, endpoints, registries, or feeds — **OR** the ADO pipeline itself is marked as a production pipeline, regardless of what its YAML logic appears to do. |
| `v2/OneBranch.NonOfficial.CrossPlat.yml@templates` | Everything else (PR validation hitting dev/staging only, lint/test, dry-runs) **and** the ADO pipeline is not classified as production. |

Production-classified pipelines MUST use `Official` even if the current YAML only does dev-looking work — the classification is the source of truth, not the inline logic. If you cannot determine the classification or whether the pipeline touches production, **ask the user** before choosing — do not default.

### Required / recommended OneBranch variables

OneBranch templates require these per job:

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `ob_outputDirectory` | **Required** | Where build outputs are staged (typically `$(Build.ArtifactStagingDirectory)/output`). |
| `ob_artifactBaseName` | Recommended | Base name for the published artifact; helps when multiple jobs publish artifacts. |
| `LinuxContainerImage` | Required when `pool.type: linux` with a container | Must come from `mcr.microsoft.com` (see Container images below). |

> Consult the **1ES MCP** at `https://eschat.microsoft.com/mcp` for the most current OneBranch guidance and feature flags. If it is not configured in this workspace, follow the setup notes at https://eng.ms/docs/coreai/devdiv/one-engineering-system-1es/1es-docs/es-chat/askeschat-mcp-vscode and surface that link to the user. Do not block on its absence.

## Triggers

Always set both triggers off in YAML — pipeline wiring (PR check / merge queue) is configured in the ADO pipeline settings, outside the YAML, and is out of scope here:

```yaml
trigger: none
pr: none
```

## Authentication & Azure access (MANDATORY)

**Service Connections backed by Workload Identity Federation (OIDC) are the only accepted way** to access Azure resources or Control Tower endpoints from these pipelines.

- Use `AzureCLI@2` with `azureSubscription: <service-connection-name>` to obtain credentials/tokens. The task auto-issues a federated token; no secret material is embedded in the pipeline.
- **Do not** use PATs, account passwords, client secrets stored in pipeline variables, or `az login -u/-p` flows.
- Use a **separate, least-privilege Service Connection per environment** (e.g. one for dev, one for prod), each scoped to the minimum subscription / resource group / role required.
- Federated credentials should be scoped to the specific ADO service connection (`subject: sc://<org>/<project>/<sc-name>`).

## Control Tower endpoints

When the pipeline calls a Control Tower API:

- **Audience URI MUST be correct for the target environment.** The token is issued for `api://<ControlTower-ClientId>` and that client ID differs per environment (DEV vs PROD). Pull both the audience URI and the base URL from a **variable group** — never hardcode them in YAML or scripts.
- Use the per-environment Service Connection that is paired with the matching Control Tower app registration. Mixing dev SC with a prod audience (or vice versa) will fail token validation.
- To look up Control Tower endpoint shapes and request/response contracts, consult the upstream repo at `https://dev.azure.com/mariner-org/azl/_git/azl-ControlTower`. Default to the `main` branch, but **confirm with the user** whether they want to target a different commit/branch (e.g. an in-flight feature branch).
- This is a private ADO repo. Two ways to read it, in order of preference:
  1. Use the **Azure DevOps MCP** (default name `ado`) to browse it directly. If it is not configured, point the user at the setup guide: https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops.
  2. Ask the user to provide a **path to a local clone** of `azl-ControlTower` and read endpoint definitions from there. Confirm which branch/commit the local clone is on before relying on it.

  If neither is available, fall back to best-effort guidance from what is in the current workspace and clearly flag the limitation to the user.

## Internal-only dependency sources (MANDATORY)

Pipelines MUST NOT pull from public/upstream registries. Use the internal mirrors / proxies for every dependency type.

### Go modules

Enable the OneBranch internal Go module proxy via feature flag on the `extends` block:

```yaml
extends:
  template: v2/OneBranch.NonOfficial.CrossPlat.yml@templates
  parameters:
    featureFlags:
      golang:
        internalModuleProxy:
          enabled: true
```

### Python (pip) packages

Authenticate pip against the internal feed before any `pip install`:

```yaml
- task: PipAuthenticate@1
  displayName: "Authenticate pip"
  inputs:
    artifactFeeds: "azl/ControlTowerFeed"
```

Use the appropriate internal feed name for the workload (this example matches the Control Tower feed). Do not invoke `pip install` from public PyPI without authenticating to an internal feed first.

### Container images

Third-party (non-Microsoft) images MUST come from `mcr.microsoft.com`. This applies to:

- `LinuxContainerImage` (and any `WindowsContainerImage`) on the OneBranch pool.
- Any image the pipeline pulls or builds from in a step (base images in Dockerfiles, sidecar containers, tools, etc.).

Example:

```yaml
variables:
  - name: LinuxContainerImage
    value: mcr.microsoft.com/onebranch/azurelinux/build:3.0
```

The authoritative list and rules live at https://eng.ms/docs/more/containers-secure-supply-chain/approved-images. The agent SHOULD attempt to fetch that page for the latest guidance; if the request fails (the page is auth-walled), try the **1ES MCP** at `https://eschat.microsoft.com/mcp` — it can surface the current approved-images guidance directly. If neither source is reachable, give the user both URLs and fall back to the `mcr.microsoft.com` rule above.

## Scripting

Avoid shell scripts beyond the smallest possible wiring (env exports, `##vso[...]` log commands, single-command tool invocations). For anything more complex — argument parsing, control flow, JSON/YAML handling, HTTP, branch-name/SHA parsing — write a **Python script** under `.github/workflows/scripts/<area>/` and invoke it from the pipeline:

```yaml
- task: AzureCLI@2
  displayName: "Call Control Tower endpoint"
  inputs:
    azureSubscription: <service-connection-name>
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: |
      set -euo pipefail
      python3 .github/workflows/scripts/<area>/<script>.py \
        --api-audience "$API_AUDIENCE" \
        --api-base-url "$API_BASE_URL"
  env:
    API_AUDIENCE: $(ApiAudience)
    API_BASE_URL: $(ApiBaseUrl)
```

Python scripts are easier to test locally, easier to review, and avoid the foot-guns of bash quoting / globbing.

## Security hardening

Apply all of these unless there is a documented reason not to:

- **`set -euo pipefail`** at the top of every non-trivial bash block.
- **Pass secrets via the `env:` block** of the step, never via inline `$(SecretVar)` interpolation in the script body (interpolation can leak into logs and into argv on `ps`-like inspection).
- Prefer ADO secret variables sourced from a **variable group linked to Azure Key Vault** over plaintext pipeline variables.
- **Pin all tool versions** (e.g. `go install ...@<commit>`, `pip install -r requirements.txt`, container image tags). No `@latest` / floating tags. **Single exception:** the OneBranch `GovernedTemplates` repo `ref` may be `refs/heads/main` — that's the documented OneBranch usage pattern.
- **Validate / sanitize PR-supplied data** (branch names, commit SHAs, PR numbers) with strict regex before using it in shell, file paths, or HTTP calls. Treat anything that came from the PR as untrusted input.
- Set an explicit, conservative **`timeoutInMinutes`** on each job (long enough to cover the slowest legitimate run, no longer).
- Do **not** use `persistCredentials: true` on `checkout:` unless a step genuinely needs to push back to the repo; if it does, scope and audit it.
- Never `echo` secret values or write them to files. Use `##[group]` / `##[endgroup]` to keep logs structured and reviewable.
- Keep the pipeline definition self-contained — avoid sourcing arbitrary scripts fetched at runtime from the internet.

## Minimal skeleton

Use this as a starting point for a new PR-check pipeline (NonOfficial variant — switch to Official if it touches production):

```yaml
trigger: none
pr: none

resources:
  repositories:
    - repository: templates
      type: git
      name: OneBranch.Pipelines/GovernedTemplates
      ref: refs/heads/main

extends:
  template: v2/OneBranch.NonOfficial.CrossPlat.yml@templates
  parameters:
    featureFlags:
      golang:
        internalModuleProxy:
          enabled: true
    stages:
      - stage: <StageName>
        jobs:
          - job: <JobName>
            timeoutInMinutes: <int>   # explicit, conservative
            pool:
              type: linux
            variables:
              - group: <variable-group-name>      # audience URI, base URL, etc.
              - name: ob_outputDirectory
                value: $(Build.ArtifactStagingDirectory)/output
              - name: ob_artifactBaseName
                value: <artifact-base-name>
              - name: LinuxContainerImage
                value: mcr.microsoft.com/onebranch/azurelinux/build:3.0
            steps:
              - task: PipAuthenticate@1
                displayName: "Authenticate pip"
                inputs:
                  artifactFeeds: "<internal-feed>"

              - task: AzureCLI@2
                displayName: "<what this step does>"
                inputs:
                  azureSubscription: <service-connection-name>
                  scriptType: bash
                  scriptLocation: inlineScript
                  inlineScript: |
                    set -euo pipefail
                    python3 .github/workflows/scripts/<area>/<script>.py \
                      --api-audience "$API_AUDIENCE" \
                      --api-base-url "$API_BASE_URL"
                env:
                  API_AUDIENCE: $(ApiAudience)
                  API_BASE_URL: $(ApiBaseUrl)
```

Replace every `<...>` placeholder.

## Maintenance checklist

Run through this list whenever you add or modify a pipeline in `.github/workflows/ado/`:

- [ ] Extends a OneBranch governed template; **Official** vs **NonOfficial** matches whether it touches production.
- [ ] `trigger: none` and `pr: none` set in YAML.
- [ ] `ob_outputDirectory` set on every job; `ob_artifactBaseName` set when artifacts are published.
- [ ] All Azure / Control Tower access goes through `AzureCLI@2` with a least-privilege Service Connection (WIF/OIDC). No PATs or password logins.
- [ ] Control Tower calls use the correct **per-environment audience URI** sourced from a variable group; nothing hardcoded.
- [ ] No upstream dependency pulls: Go uses `internalModuleProxy`, Python uses `PipAuthenticate@1`, container images come from `mcr.microsoft.com`.
- [ ] Any non-trivial logic lives in a Python script under `.github/workflows/scripts/`, not inline bash.
- [ ] Secrets passed via `env:` (never inline `$(...)`); `set -euo pipefail` in shell blocks; tool versions pinned (only `GovernedTemplates@main` exempted).
- [ ] Explicit `timeoutInMinutes` on each job; PR-supplied inputs validated with strict regex.
