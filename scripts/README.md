# Source Sync Scripts

This directory contains scripts for downloading, verifying, and uploading
component sources to the Azure Blob Storage lookaside cache used by the
Azure Linux build system.

The primary entry point is **`sync-sources.py`** — a single script that
combines the download, verify, and upload workflows.  An Azure DevOps (ADO)
pipeline at [`.azure-pipelines/sync-sources.yml`](../.azure-pipelines/sync-sources.yml)
automates this on every merge to the `tomls/base/main` branch.

---

## Table of Contents

- [Overview](#overview)
- [sync-sources.py — CLI Reference](#sync-sourcespy--cli-reference)
- [ADO Pipeline](#ado-pipeline)
  - [How It Triggers](#how-it-triggers)
  - [Pipeline Parameters](#pipeline-parameters)
  - [Service Connection Setup](#service-connection-setup)
  - [azldev Binary (ADO Artifacts)](#azldev-binary-ado-artifacts)
  - [How the Pipeline Invokes the Script](#how-the-pipeline-invokes-the-script)
  - [Failure Handling and Retries](#failure-handling-and-retries)
- [Running Locally](#running-locally)
- [Related Scripts](#related-scripts)

---

## Overview

Azure Linux imports RPM specs from upstream Fedora.  Each upstream component
has source tarballs whose integrity is tracked in Fedora-style `sources`
metadata files (`SHA512 (file.tar.xz) = <hex>` or GNU-coreutils format).

Before the build system can consume these sources, they must be mirrored into
an Azure Blob Storage **lookaside cache**.  The blob naming convention is:

```
pkgs/<package>/<filename>/<hashtype>/<hash>/<filename>
```

This matches the `lookaside-base-uri` template configured in
[`overrides/fedora.distro.azl.sources.toml`](../overrides/fedora.distro.azl.sources.toml):

```
https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs/$pkg/$filename/$hashtype/$hash/$filename
```

`sync-sources.py` automates the full workflow:

1. **Discover** components — either auto-discover via `azldev component list`
   (filtered by `--component-filter`, defaulting to `"Upstream: fedora"`) or
   read an explicit list from `--components-file`.
2. **Download** sources in parallel by running
   `./azldev component prepare-sources <name>` for each component.
3. **Verify** each downloaded file's hash against its `sources` metadata.
4. **Upload** verified files to Azure Blob Storage, skipping blobs that
   already exist.

---

## sync-sources.py — CLI Reference

```
python scripts/sync-sources.py [OPTIONS]
```

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `--account-url` | `str` | Yes (unless `--verify-only`) | — | Azure Storage Account URL (e.g. `https://<account>.blob.core.windows.net`). |
| `--container` | `str` | Yes (unless `--verify-only`) | — | Blob container name to upload into. |
| `--component-filter` | `str` | No | `"Upstream: fedora"` | Substring filter on `azldev component list -a -O markdown` output to select components. |
| `--components-file` | `Path` | No | — | Read component names from this file (one per line, blank lines and `#` comments ignored) instead of auto-discovering. Accepts the output of `--failed-output`. |
| `--failed-output` | `Path` | No | `components.failed.list` | Write failed component names here for retry. |
| `-j` / `--jobs` | `int` | No | CPU count | Max parallel workers for download and upload. |
| `--verify-only` | flag | No | `false` | Download and verify only — skip upload. No Azure credentials needed. |
| `--skip-download` | flag | No | `false` | Skip the download phase; only verify/upload already-downloaded sources. |
| `-q` / `--quiet` | flag | No | `false` | Suppress per-file success messages; only print errors and summary. |

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | All components downloaded and uploaded successfully. |
| `1` | One or more components failed (see `--failed-output` for the list). |
| `2` | Azure credential setup failed. |

### Examples

```bash
# Full run — auto-discover all Fedora-sourced components, download, verify, upload:
python scripts/sync-sources.py \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# Sync only specific components:
echo -e "bash\ncoreutils\ngcc" > my-components.list
python scripts/sync-sources.py \
    --components-file my-components.list \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# Retry previously failed components:
python scripts/sync-sources.py \
    --components-file components.failed.list \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# Download + verify only (no Azure credentials needed):
python scripts/sync-sources.py --verify-only

# Upload already-downloaded sources (skip download phase):
python scripts/sync-sources.py --skip-download \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo
```

### Authentication

The script uses **`AzureCliCredential`** from the `azure-identity` SDK.
This means you must run `az login` before invoking the script (unless using
`--verify-only`, which doesn't touch Azure storage).

```bash
az login
python scripts/sync-sources.py --account-url ... --container ...
```

In the ADO pipeline, authentication is handled automatically — see
[Service Connection Setup](#service-connection-setup) below.

### Dependencies

```bash
pip install azure-identity azure-storage-blob
```

The script also requires the **`azldev`** binary at the repository root
(`./azldev`).  See [azldev Binary](#azldev-binary-ado-artifacts) for how
the pipeline obtains it.

---

## ADO Pipeline

The pipeline definition lives at
[`.azure-pipelines/sync-sources.yml`](../.azure-pipelines/sync-sources.yml).

### How It Triggers

| Trigger type | Details |
|---|---|
| **CI (automatic)** | Fires on every push to `tomls/base/main`. The `batch: true` setting coalesces concurrent commits so only the latest one triggers a run — no redundant runs for intermediate commits. |
| **Manual** | Click **"Run pipeline"** in the ADO UI. All parameters can be overridden at queue time, e.g. to sync a specific component or point at a different storage account. |

### Pipeline Parameters

These are configurable when manually triggering the pipeline:

| Parameter | Default | Description |
|---|---|---|
| `accountUrl` | `https://azltempstaginglookaside.blob.core.windows.net` | Azure Storage Account URL passed to `--account-url`. |
| `container` | `repo` | Blob container name passed to `--container`. |
| `components` | *(empty)* | Newline-separated list of component names. When empty, the script auto-discovers all components matching the default filter (`"Upstream: fedora"`). When non-empty, the pipeline writes this list to a temporary file and passes it via `--components-file`. |

**Example — syncing specific components manually:**

1. Go to the pipeline in ADO → **Run pipeline**.
2. Set `components` to:
   ```
   bash
   coreutils
   gcc
   ```
3. Click **Run**.

The pipeline writes these names into `components.pipeline.list` and passes
`--components-file components.pipeline.list` to the script.

### Service Connection Setup

The pipeline uses the
[`AzureCLI@2`](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/azure-cliv2)
task, which performs `az login` automatically using an ADO **Service Connection**.
This satisfies the script's `AzureCliCredential` without any code changes.

**Setup steps:**

1. In the ADO project, go to **Project Settings → Service connections**.
2. Create (or identify) an **Azure Resource Manager** service connection that
   has the **"Storage Blob Data Contributor"** role on the target storage
   account (`azltempstaginglookaside` by default).
3. Copy the service connection's name.
4. In the pipeline YAML, replace the placeholder:
   ```yaml
   serviceConnectionName: "<YOUR_AZURE_SERVICE_CONNECTION>"
   ```
   with the actual name.

> **Security note:** The service connection grants the pipeline write access
> to the blob container.  Follow your organization's least-privilege policies
> when assigning roles.

### azldev Binary (ADO Artifacts)

The `azldev` CLI is required for source preparation (`./azldev component
prepare-sources`).  The pipeline downloads it from an **Azure DevOps Artifacts
Universal Package feed** using the
[`UniversalPackages@0`](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/universal-packages-v0)
task.

**Setup steps:**

1. Publish the `azldev` binary to a Universal Package feed in your ADO
   organization (see
   [Publish Universal Packages](https://learn.microsoft.com/en-us/azure/devops/artifacts/quickstarts/universal-packages)).
2. In the pipeline YAML, replace the placeholder variables:
   ```yaml
   azldevFeed: "<YOUR_FEED>"               # e.g. "MyProject/azldev-feed" or "azldev-feed"
   azldevPackageName: "azldev"             # name of the Universal Package
   azldevPackageVersion: "*"               # "*" = latest; pin for reproducibility
   ```
3. Ensure the pipeline's build service identity has **Reader** access to the
   feed.  For organization-scoped feeds this is automatic; for project-scoped
   feeds you may need to add the identity explicitly.

### How the Pipeline Invokes the Script

The pipeline maps its parameters to `sync-sources.py` arguments as follows:

```
Pipeline parameter        →  Script argument
─────────────────────────────────────────────────
accountUrl                →  --account-url
container                 →  --container
components (non-empty)    →  --components-file components.pipeline.list
components (empty)        →  (omitted — script auto-discovers)
```

The `AzureCLI@2` task performs `az login` via the Service Connection before
the inline script runs, so `AzureCliCredential` picks up the session
automatically.

### Failure Handling and Retries

- **Partial failures:** If some components fail to download or upload, the
  script writes their names to `components.failed.list` and exits with
  code `1`.
- **Artifact:** The pipeline publishes `components.failed.list` as a pipeline
  artifact named `failed-components` (runs on `succeededOrFailed()`, so it's
  available even when the pipeline reports a failure).
- **Retry workflow:**
  1. Download the `failed-components` artifact from the failed pipeline run.
  2. Re-trigger the pipeline manually, pasting the failed component names
     into the `components` parameter.
  3. Alternatively, run locally:
     ```bash
     python scripts/sync-sources.py \
         --components-file components.failed.list \
         --account-url https://azltempstaginglookaside.blob.core.windows.net \
         --container repo
     ```

---

## Running Locally

```bash
# 1. Ensure azldev is present at the repo root
ls ./azldev

# 2. Install Python dependencies
pip install azure-identity azure-storage-blob

# 3. Authenticate to Azure
az login

# 4. Run a full sync (all Fedora-sourced components)
python scripts/sync-sources.py \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# 5. Or verify-only (no Azure credentials needed)
python scripts/sync-sources.py --verify-only
```

Downloaded sources are saved under `sources/downloads/<component>/` and logs
under `sources/logs/`.  With ~590 components, expect significant disk usage
for a full sync.

---

## Related Scripts

| Script | Purpose |
|---|---|
| `update-components-list.py` | Maintains `components.list` — adds missing components from image builds or prunes stale entries. |
