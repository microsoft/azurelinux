---
applyTo: ".github/workflows/ado/*.yml,.github/workflows/ado/templates/*.yml,.github/workflows/scripts/**"
description: "Authoring and maintenance rules for Azure DevOps YAML pipelines under .github/workflows/ado/ (wrappers + raw stage templates under templates/) and their helper scripts under .github/workflows/scripts/ that run as GitHub PR checks or in the merge queue. Apply when creating or modifying any pipeline in that folder, or any script invoked by one — covers the wrapper/raw split, required OneBranch templates (Official vs NonOfficial), Workload Identity Federation service connections, Control Tower audience URIs, internal-only dependency sources (Go / Python / container images), Python-over-shell scripting, and security hardening."
---

# Azure DevOps Pipelines (PR check & merge queue)

These instructions cover ADO YAML pipelines under `.github/workflows/ado/` that run as GitHub PR checks or in the merge queue, plus their helper scripts under `.github/workflows/scripts/`. Follow every MUST below — they encode internal Microsoft policy plus security hardening for this repo.

Helper scripts invoked from these pipelines MUST live under `.github/workflows/scripts/<area>/` (one subdirectory per logical area / pipeline). Keep them self-contained and follow the same security hardening rules as the pipeline YAML itself.

> If anything below conflicts with what the user is asking for, **stop and ask the user** rather than guessing — especially for the Official vs NonOfficial template choice.

## Pipeline structure: wrapper + raw stages (MANDATORY)

Every ADO pipeline in this repo is split into **two YAML files**:

1. **Wrapper** — `.github/workflows/ado/<name>.yml`. This is the file passed to ADO as the pipeline definition. It is the *only* place that knows about OneBranch:
   - declares `resources.repositories` for `OneBranch.Pipelines/GovernedTemplates`,
   - picks the OneBranch variant via `extends:` (`Official` vs `NonOfficial` — see next section),
   - configures the OneBranch `parameters.featureFlags`,
   - injects the raw stages template via `parameters.stages: - template: …@self` and supplies concrete values for its `parameters:`.

   The wrapper MUST NOT contain `stages:`, `jobs:`, or `steps:` directly. If you find yourself adding a `script:` block to a wrapper, stop — it belongs in the raw stages template.

2. **Raw stages template** — `.github/workflows/ado/templates/<name>-stages.yml`. This file declares `parameters:` + `stages:` and contains the actual jobs/steps. It MUST be OneBranch-agnostic:
   - no `resources:`, no `extends:`, no `featureFlags:`,
   - no string mentions of `OneBranch` or `GovernedTemplates`,
   - any value coupled to the OneBranch contract (output dir, artifact base name, container image, pool type, service connection, variable group, timeout) is exposed as a **parameter with a neutral name** and bound by the wrapper.

   `ob_*` job-scope variables and `LinuxContainerImage` still appear here (ADO requires them at job scope), but they are set from `${{ parameters.* }}`, so the raw author never has to know which OneBranch convention they satisfy.

File-pairing convention: a wrapper at `.github/workflows/ado/<name>.yml` pairs with a raw stages template at `.github/workflows/ado/templates/<stem>-stages.yml`. **Multiple wrappers MAY share a single raw stages template** — that is in fact a primary motivation for the split: define several ADO pipelines (e.g. a DEV NonOfficial wrapper and a PROD Official wrapper, or per-environment variants) that all run the same stages/jobs/steps but differ in OneBranch variant, `featureFlags`, service connection, variable group, container image, etc. When wrappers share a raw template, name them so the relationship is obvious (e.g. `sources-upload-dev.yml` + `sources-upload-prod.yml` both pointing at `templates/sources-upload-stages.yml`). The variant choice cannot be hoisted into a shared sub-template because ADO requires `extends:` at the root of the entry pipeline — that is exactly why each wrapper exists.

See [.github/workflows/ado/sources-upload.yml](.github/workflows/ado/sources-upload.yml) and [.github/workflows/ado/templates/sources-upload-stages.yml](.github/workflows/ado/templates/sources-upload-stages.yml) for the canonical example.

## OneBranch templates (MANDATORY — wrapper only)

The rules in this section apply to the **wrapper** file. The raw stages template MUST NOT reference OneBranch at all.

To comply with internal policy, every wrapper MUST extend a OneBranch governed template:

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

OneBranch templates require these per job. In the wrapper/raw split, the raw stages template declares them in its `variables:` block but binds them from `${{ parameters.* }}`; the **wrapper** supplies the concrete values when invoking the raw template.

| Variable | Required? | Purpose | Suggested raw parameter name |
|----------|-----------|---------|------------------------------|
| `ob_outputDirectory` | **Required** | Where build outputs are staged (typically `$(Build.ArtifactStagingDirectory)/output`). | `outputDirectory` |
| `ob_artifactBaseName` | Recommended | Base name for the published artifact; helps when multiple jobs publish artifacts. | `artifactBaseName` |
| `LinuxContainerImage` | Required when `pool.type: linux` with a container | Must come from `mcr.microsoft.com` (see Container images below). | `containerImage` |

> Consult the **1ES MCP** at `https://eschat.microsoft.com/mcp` for the most current OneBranch guidance and feature flags. If it is not configured in this workspace, follow the setup notes at https://eng.ms/docs/coreai/devdiv/one-engineering-system-1es/1es-docs/es-chat/askeschat-mcp-vscode and surface that link to the user. Do not block on its absence.

## Triggers

Always set both triggers off in the **wrapper** YAML — pipeline wiring (PR check / merge queue) is configured in the ADO pipeline settings, outside the YAML, and is out of scope here. Raw stage templates do not declare triggers (they are not entry points):

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

## Minimal skeletons

Use these as a starting point for a new pipeline. Two files: a wrapper (NonOfficial variant — switch to Official if it touches production) and a raw stages template.

### Wrapper — `.github/workflows/ado/<name>.yml`

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
      - template: /.github/workflows/ado/templates/<name>-stages.yml@self
        parameters:
          outputDirectory: $(Build.ArtifactStagingDirectory)/output
          artifactBaseName: <artifact-base-name>
          containerImage: mcr.microsoft.com/onebranch/azurelinux/build:3.0
          poolType: linux
          serviceConnection: <service-connection-name>
          variableGroup: <variable-group-name>
          timeoutInMinutes: <int>   # explicit, conservative
```

### Raw stages — `.github/workflows/ado/templates/<name>-stages.yml`

```yaml
parameters:
  - name: outputDirectory
    type: string
  - name: artifactBaseName
    type: string
  - name: containerImage
    type: string
  - name: poolType
    type: string
    default: linux
  - name: serviceConnection
    type: string
  - name: variableGroup
    type: string
  - name: timeoutInMinutes
    type: number

stages:
  - stage: <StageName>
    jobs:
      - job: <JobName>
        timeoutInMinutes: ${{ parameters.timeoutInMinutes }}
        pool:
          type: ${{ parameters.poolType }}
        variables:
          - group: ${{ parameters.variableGroup }}      # audience URI, base URL, etc.
          - name: ob_outputDirectory
            value: ${{ parameters.outputDirectory }}
          - name: ob_artifactBaseName
            value: ${{ parameters.artifactBaseName }}
          - name: LinuxContainerImage
            value: ${{ parameters.containerImage }}
        steps:
          - task: PipAuthenticate@1
            displayName: "Authenticate pip"
            inputs:
              artifactFeeds: "<internal-feed>"

          - task: AzureCLI@2
            displayName: "<what this step does>"
            inputs:
              azureSubscription: ${{ parameters.serviceConnection }}
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

- [ ] Pipeline is split into a **wrapper** (`.github/workflows/ado/<name>.yml`) and a **raw stages template** (`.github/workflows/ado/templates/<stem>-stages.yml`). A raw stages template MAY be shared by multiple wrappers (e.g. DEV vs PROD variants).
- [ ] Wrapper is the *only* place that names OneBranch — extends a governed template; **Official** vs **NonOfficial** matches whether it touches production.
- [ ] Wrapper has no `stages:` / `jobs:` / `steps:` / `script:` of its own; it only invokes the raw stages template via `parameters.stages: - template: …@self` and supplies its parameters.
- [ ] Raw stages template is OneBranch-agnostic: no `resources:`, no `extends:`, no `featureFlags:`, no string mentions of `OneBranch` / `GovernedTemplates`. OneBranch-coupled values (`ob_outputDirectory`, `ob_artifactBaseName`, `LinuxContainerImage`, pool type, service connection, variable group, timeout) are exposed as neutral-named `parameters:` and bound from the wrapper.
- [ ] `trigger: none` and `pr: none` set in the wrapper YAML.
- [ ] `ob_outputDirectory` set on every job; `ob_artifactBaseName` set when artifacts are published.
- [ ] All Azure / Control Tower access goes through `AzureCLI@2` with a least-privilege Service Connection (WIF/OIDC). No PATs or password logins.
- [ ] Control Tower calls use the correct **per-environment audience URI** sourced from a variable group; nothing hardcoded.
- [ ] No upstream dependency pulls: Go uses `internalModuleProxy`, Python uses `PipAuthenticate@1`, container images come from `mcr.microsoft.com`.
- [ ] Any non-trivial logic lives in a Python script under `.github/workflows/scripts/`, not inline bash.
- [ ] Secrets passed via `env:` (never inline `$(...)`); `set -euo pipefail` in shell blocks; tool versions pinned (only `GovernedTemplates@main` exempted).
- [ ] Explicit `timeoutInMinutes` on each job; PR-supplied inputs validated with strict regex.
