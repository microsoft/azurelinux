# Source Sync Scripts

This directory contains scripts for downloading and uploading component
sources to the Azure Blob Storage lookaside cache used by the Azure Linux
build system.

The entry point is **`sync-sources.py`** — a single script that
combines the download and upload workflows. An Azure DevOps (ADO)
pipeline at [`.azure-pipelines/sync-sources.yml`](../../.azure-pipelines/sync-sources.yml)
automates this on merges to the `tomls/base/main` branch.

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

---

## Overview

Azure Linux imports RPM specs from upstream Fedora. Each upstream component
has source tarballs whose integrity is tracked in Fedora-style `sources`
metadata files (`SHA512 (file.tar.xz) = <hex>` or GNU-coreutils format).

Before the build system can consume these sources, they must be mirrored into
an Azure Blob Storage **lookaside cache**. The blob naming convention is:

```
pkgs/<package>/<filename>/<hashtype>/<hash>/<filename>
```

This matches the `lookaside-base-uri` template configured in
[`overrides/fedora.distro.azl.sources.toml`](../../overrides/fedora.distro.azl.sources.toml):

```
https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs/$pkg/$filename/$hashtype/$hash/$filename
```

`sync-sources.py` automates the full workflow:

1. **Discover** components — either auto-discover via `azldev component list`
   (filtered by `--component-filter`, defaulting to `"Upstream: fedora"`) or
   read an explicit list from `--components-file`.
2. **Process** each component in parallel (`-j` workers):
   1. **Download** sources via `./azldev component prepare-sources <name>`.
   2. **Upload** source files to Azure Blob Storage, skipping blobs that
      already exist.
   3. **Clean up** local download artifacts to free disk space. On failure,
      artifacts are preserved for debugging.
3. **Report** — write any failed component names to `--failed-output` and
   print a summary.

> **Hash computation:** The hash values used in blob paths are computed from
> the **actual downloaded files on disk**, not from the upstream `sources`
> metadata. This is intentional — TOML overlay configuration may modify
> source files after download, so the real on-disk hash is the authoritative
> one. Upstream integrity verification is handled by
> `azldev component prepare-sources` itself and is not duplicated here.

> **Upstream name mapping:** When a component's Azure Linux name differs from
> its upstream Fedora name (e.g. `fuse3-42` vs `fuse3`), the script extracts
> the upstream name from `azldev` stderr (`upstreamComponent=<name>`) and
> uses it as the package name in the blob path. This ensures blob paths
> match the lookaside URI template.

---

## sync-sources.py — CLI Reference

```
python scripts/sources-sync/sync-sources.py [OPTIONS]
```

| Argument | Type | Required | Default | Description |
|---|---|---|---|---|
| `--account-url` | `str` | Yes | — | Azure Storage Account URL (e.g. `https://<account>.blob.core.windows.net`). |
| `--container` | `str` | Yes | — | Blob container name to upload into. |
| `--component-filter` | `str` | No | `"Upstream: fedora"` | Substring filter on `azldev component list -a -O markdown` output to select components. |
| `--components-file` | `Path` | No | — | Read component names from this file (one per line, blank lines and `#` comments ignored) instead of auto-discovering. Accepts the output of `--failed-output`. |
| `--failed-output` | `Path` | No | `components.failed.list` | Write failed component names here for retry. Can be passed back as `--components-file`. |
| `-j` / `--jobs` | `int` | No | CPU count | Max parallel workers for download and upload. |
| `-q` / `--quiet` | flag | No | `false` | Suppress per-file success messages; only print errors and summary. |

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | All components downloaded and uploaded successfully. |
| `1` | One or more components failed (see `--failed-output` for the list). |
| `2` | Azure credential setup failed (run `az login` first). |

### Examples

```bash
# Full run — auto-discover all Fedora-sourced components, download, upload:
python scripts/sources-sync/sync-sources.py \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# Sync only specific components:
echo -e "bash\ncoreutils\ngcc" > my-components.list
python scripts/sources-sync/sync-sources.py \
    --components-file my-components.list \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo

# Retry previously failed components:
python scripts/sources-sync/sync-sources.py \
    --components-file components.failed.list \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo
```

### Authentication

The script uses **`AzureCliCredential`** from the `azure-identity` SDK.
You must run `az login` before invoking the script.

```bash
az login
python scripts/sources-sync/sync-sources.py --account-url ... --container ...
```

In the ADO pipeline, authentication is handled automatically — see
[Service Connection Setup](#service-connection-setup) below.

### Dependencies

```bash
pip install azure-identity azure-storage-blob
```

The script also requires the **`azldev`** binary at the repository root
(`./azldev`). See [azldev Binary](#azldev-binary-ado-artifacts) for how
the pipeline obtains it.

### Logging

Each component gets a dedicated log file at `sources/logs/<component>.log`.
These capture all output including DEBUG-level `azldev` stdout/stderr, which
is useful for diagnosing download or upload failures. Console output respects
the `-q` / `--quiet` flag.

---

## ADO Pipeline

The pipeline definition lives at
[`.azure-pipelines/sync-sources.yml`](../../.azure-pipelines/sync-sources.yml).

It uses the **OneBranch `v2/OneBranch.Official.CrossPlat.yml`** governed
template and runs in a single stage (`SyncSources`) with a single job
(`SyncFedoraSources`). The job has a **180-minute timeout**.

Because `azldev` cannot run as root, the pipeline creates a non-root user
(`azldevuser`) and runs the script under that account.

### How It Triggers

| Trigger type | Details |
|---|---|
| **CI (automatic)** | Runs on merges to `tomls/base/main`. The trigger is configured in the ADO portal (the YAML sets `trigger: none` and `pr: none` — trigger rules are managed ADO-side, not in YAML). |
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

The service connection name is configured in the pipeline variable
`serviceConnectionName` (currently `"Temp lookaside cache uploader CS"`).

**Setup steps:**

1. In the ADO project, go to **Project Settings → Service connections**.
2. Create (or identify) an **Azure Resource Manager** service connection that
   has the **"Storage Blob Data Contributor"** role on the target storage
   account (`azltempstaginglookaside` by default).
3. Copy the service connection's name.
4. In the pipeline YAML, update the variable:
   ```yaml
   serviceConnectionName: "Temp lookaside cache uploader CS"
   ```

The `AzureCLI@2` task copies the Azure CLI config to the `azldevuser` home
directory so that `AzureCliCredential` works under the non-root account.

> **Security note:** The service connection grants the pipeline write access
> to the blob container. Follow your organization's least-privilege policies
> when assigning roles.

### azldev Binary (ADO Artifacts)

The `azldev` CLI is required for source preparation (`./azldev component
prepare-sources`). The pipeline downloads it from an **Azure DevOps Artifacts
Universal Package feed** using the
[`UniversalPackages@0`](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/universal-packages-v0)
task.

Current feed coordinates (defined as pipeline variables):

```yaml
azldevFeed: "mariner/azldev-preview-feed"
azldevPackageName: "azldev-preview-pkg-x86_64"
azldevPackageVersion: "*"               # "*" = latest; pin for reproducibility
```

**Setup steps:**

1. Publish the `azldev` binary to a Universal Package feed in your ADO
   organization (see
   [Publish Universal Packages](https://learn.microsoft.com/en-us/azure/devops/artifacts/quickstarts/universal-packages)).
2. Update the feed coordinates in the pipeline YAML if they differ from the
   defaults above.
3. Ensure the pipeline's build service identity has **Reader** access to the
   feed. For organization-scoped feeds this is automatic; for project-scoped
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
- **Output artifact:** The pipeline copies `components.failed.list` to the
  OneBranch output directory (`ob_outputDirectory`). OneBranch handles
  publishing artifacts from this directory automatically.
- **Retry workflow:**
  1. Download the failed-components list from the failed pipeline run's
     artifacts.
  2. Re-trigger the pipeline manually, pasting the failed component names
     into the `components` parameter.
  3. Alternatively, run locally:
     ```bash
     python scripts/sources-sync/sync-sources.py \
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
python scripts/sources-sync/sync-sources.py \
    --account-url https://azltempstaginglookaside.blob.core.windows.net \
    --container repo
```

Downloaded sources are temporarily saved under `sources/downloads/<component>/`
during processing and removed after successful upload. Per-component logs are
written to `sources/logs/<component>.log`.

---
