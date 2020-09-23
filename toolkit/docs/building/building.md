# Building

- [Building](#building)
  - [Quick Start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Configure the Environment](#configure-the-environment)
    - [ISO Quick Start](#iso-quick-start)
    - [VHDX Quick Start](#vhdx-quick-start)
    - [Build from Sources Quick Start](#build-from-sources-quick-start)
  - [Further Reading](#further-reading)
    - [Building in Stages](#building-in-stages)
      - [1) Bootstrap Toolchain](#1-bootstrap-toolchain)
        - [Full toolchain Bootstrap From Sources](#full-toolchain-bootstrap-from-sources)
      - [2) Build All Packages](#2-build-all-packages)
      - [3) Build Images](#3-build-images)
    - [ISOs](#isos)
    - [Packages](#packages)
      - [Working on Packages](#working-on-packages)
        - [DOWNLOAD_SRPMS](#download_srpms)
        - [Force Rebuilds](#force-rebuilds)
        - [Ignoring Packages](#ignoring-packages)
        - [Source Hashes](#source-hashes)
  - [Keys, Certs, and Remote Sources](#keys-certs-and-remote-sources)
    - [Sources](#sources)
    - [Authentication](#authentication)
  - [Building Everything From Scratch](#building-everything-from-scratch)
    - [Bootstrapping the Toolchain and Building Everything from Scratch](#bootstrapping-the-toolchain-and-building-everything-from-scratch)
    - [Local Build Variables](#local-build-variables)
      - [URLS and Repos](#urls-and-repos)
      - [`SOURCE_URL=...`](#source_url)
      - [`PACKAGE_URL=...`](#package_url)
      - [`PACKAGE_UPDATE_URL=...`](#package_update_url)
      - [`SRPM_URL=...`](#srpm_url)
      - [`SRPM_UPDATE_URL=...`](#srpm_update_url)
      - [`REPO_LIST=...`](#repo_list)
      - [Build Enable/Disable Flags](#build-enabledisable-flags)
      - [`REBUILD_TOOLCHAIN=...`](#rebuild_toolchain)
        - [`REBUILD_TOOLCHAIN=`**`n`** *(default)*](#rebuild_toolchainn-default)
        - [`REBUILD_TOOLCHAIN=`**`y`**](#rebuild_toolchainy)
      - [`DOWNLOAD_SRPMS=...`](#download_srpms-1)
        - [`DOWNLOAD_SRPMS=`**`n`** *(default)*](#download_srpmsn-default)
        - [`DOWNLOAD_SRPMS=`**`y`**](#download_srpmsy)
      - [`USE_UPDATE_REPO=...`](#use_update_repo)
        - [`USE_UPDATE_REPO=`**`y`** *(default)*](#use_update_repoy-default)
        - [`USE_UPDATE_REPO=`**`n`**](#use_update_repon)
      - [`DISABLE_UPSTREAM_REPOS=...`](#disable_upstream_repos)
        - [`DISABLE_UPSTREAM_REPOS=`**`n`** *(default)*](#disable_upstream_reposn-default)
        - [`DISABLE_UPSTREAM_REPOS=`**`y`**](#disable_upstream_reposy)
      - [`REBUILD_PACKAGES=...`](#rebuild_packages)
        - [`REBUILD_PACKAGES=`**`y`** *(default)*](#rebuild_packagesy-default)
        - [`REBUILD_PACKAGES=`**`n`**](#rebuild_packagesn)
      - [`REBUILD_TOOLS=...`](#rebuild_tools)
        - [`REBUILD_TOOLS=`**`n`** *(default)*](#rebuild_toolsn-default)
        - [`REBUILD_TOOLS=`**`y`**](#rebuild_toolsy)
  - [All Build Targets](#all-build-targets)
  - [Reproducing a Build](#reproducing-a-build)
    - [Build Summaries](#build-summaries)
    - [Building From Summaries](#building-from-summaries)
    - [Reproducing a Package Build](#reproducing-a-package-build)
    - [Reproducing an Image Build](#reproducing-an-image-build)
    - [Reproducing an ISO Build](#reproducing-an-iso-build)
  - [All Build Variables](#all-build-variables)
    - [Targets](#targets)
    - [Rebuild vs. Download](#rebuild-vs-download)
    - [Remote Connections](#remote-connections)
    - [Misc Build](#misc-build)
    - [Reproducing Builds](#reproducing-builds)
    - [Directory Customization](#directory-customization)
    - [Build Details](#build-details)

## Quick Start

### Prerequisites

Install prerequisites [here](prerequisites.md).

### Configure the Environment

By default all build commands are executed from inside the `./toolkit` folder.

A few one-time steps can be run now (they will re-run automatically later if needed)

Remote files are generally only available for release branches.

**IMPORTANT:** HEAD of many branches is not guaranteed to build successfully. To avoid build issues it is recommended to check out the `[BRANCH-NAME]-stable` tag.

Example: to safely build the `1.0`  branch check out the `1.0-stable` tag.


```bash
# Get the source code
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner/toolkit

# Checkout the desired release branch. The 1.0-stable tag tracks the most recent successful release of the 1.0 branch.
git checkout 1.0-stable

# Build the Go tools
sudo make go-tools REBUILD_TOOLS=y

# Get the package sources
sudo make input-srpms DOWNLOAD_SRPMS=y
```

**NOTE: All subsequent commands are assumed to be executed from inside the toolkit directory.**

### ISO Quick Start

```bash
# Build an ISO version of ./imageconfigs/core-efi.json entirely from downloaded, pre-built packages
sudo make iso REBUILD_TOOLS=y REBUILD_PACKAGES=n
```

### VHDX Quick Start

```bash
# Build a VHDX of ./imageconfigs/core-efi.json entirely from downloaded, pre-built packages
sudo make image REBUILD_TOOLS=y REBUILD_PACKAGES=n
```

### Build from Sources Quick Start

This is a **much slower** process which will download and compile sources rather than use pre-compiled packages.

```bash
# Build an image without downloading pre-compiled packages
sudo make image REBUILD_TOOLS=y REBUILD_TOOLCHAIN=y DOWNLOAD_SRPMS=y PACKAGE_IGNORE_LIST="openjdk8 openjdk8_aarch64 shim-unsigned-aarch64" -j$(nproc)
```

## Further Reading

### Building in Stages

This section runs through a build one step at a time, briefly explaining the purpose. `Make` will generally automate this flow if given a target, however it can be useful for debugging.

#### 1) Bootstrap Toolchain

A set of bootstrapped toolchain packages (gcc etc.) are used to build CBL-Mariner packages and images.

```bash
# Download the pre-built toolchain packages (REBUILD_TOOLCHAIN=n is the default value)
sudo make toolchain REBUILD_TOOLS=y

# Move the downloaded bootstrap packages to the general RPM out folder
sudo make copy-toolchain-rpms
```

NOTE: A full list of targets and options to `make` is available [here](#all-build-targets) and [here](#all-build-variables).

##### Full toolchain Bootstrap From Sources

If you want to build **everything** from scratch, including the bootstrapping process, run:

```bash
cd ~/git/CBL-Mariner/toolkit

# Do a FULL bootstrap + rebuild from sources instead (much slower)
# Add REBUILD_TOOLCHAIN=y to any subsequent command to ensure locally built toolchain packages are used
sudo make toolchain REBUILD_TOOLS=y REBUILD_TOOLCHAIN=y DOWNLOAD_SRPMS=y PACKAGE_IGNORE_LIST="openjdk8 openjdk8_aarch64 shim-unsigned-aarch64"
```

This will download the source files (SRPMs) from the package sever, and build them locally.
See the detailed section on building from scratch [here](#building-everything-from-scratch)

#### 2) Build All Packages

(**this step may be omitted if desired**)

Once the toolchain is bootstrapped, packages can be built with the toolchain.

The image build commands in [3) Build Images](#3-build-images) will **automatically** build only the required packages based on the selected configuration.

However, to manually build **all** packages you can clear the configuration with `CONFIG_FILE=` and invoke the package build target.

Large parts of the build are parallelized. Enable this by setting the `-j` flag for `make` to the number of parallel jobs to allow. (Recommend setting this value to the number of logical cores available on your system, or less)

**NOTE: If you are building your toolchain packages from source, add `REBUILD_TOOLCHAIN=y`**

```bash
# Build ALL packages FOR AMD64
sudo make build-packages -j$(nproc) CONFIG_FILE= DOWNLOAD_SRPMS=y REBUILD_TOOLS=y PACKAGE_IGNORE_LIST="openjdk8 openjdk8_aarch64 shim-unsigned-aarch64"

# Build ALL packages FOR ARM64
# (NOTE: CBL-Mariner compiles natively, an ARM64 build machine is required to create ARM64 packages/images)
sudo make build-packages -j$(nproc) CONFIG_FILE= DOWNLOAD_SRPMS=y REBUILD_TOOLS=y PACKAGE_IGNORE_LIST="openjdk8 openjdk8_aarch64 shim-unsigned-amd64"
```

#### 3) Build Images

Different images can be produced from the build system.  All images are generated in the `out/images` folder.

**NOTE: If you are building your toolchain packages from source, add `REBUILD_TOOLCHAIN=y`**

```bash
# To build a Mariner VHD Image (VHD folder: ../out/images/core-legacy)
sudo make image CONFIG_FILE=./imageconfigs/core-legacy.json REBUILD_TOOLS=y DOWNLOAD_SRPMS=y

# To build a Mariner VHDX Image (VHDX folder ../out/images/core-efi)
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json REBUILD_TOOLS=y DOWNLOAD_SRPMS=y

# To build a Mariner ISO Image (ISO folder: ../out/images/full)
sudo make iso CONFIG_FILE=./imageconfigs/full.json REBUILD_TOOLS=y DOWNLOAD_SRPMS=y

# To build a Mariner Contianer Image (Container Folder: ../out/images/core-container/*.tar.gz
sudo make image CONFIG_FILE=./imageconfigs/core-container.json REBUILD_TOOLS=y DOWNLOAD_SRPMS=y
```

### ISOs

ISO installers can be built with:

```bash
# Build out/images/developer_iso/*.iso from remote components
sudo make iso -j$(nproc) CONFIG_FILE=./resources/imageconfigs/developer_iso/developer_iso.json
```

To create an unattended ISO installer (no interactive UI) use `UNATTENDED_INSTALLER=y`:

```bash
# Build out/images/developer_iso/*.iso from remote components with unattended installer
sudo make iso -j$(nproc) CONFIG_FILE=./resources/imageconfigs/developer_iso/developer_iso.json UNATTENDED_INSTALLER=y
```

NOTE: ISOs require additional packaging and build steps (such as the creation of a separate `initrd` installer image used to install the final image to disk).

### Packages

The toolkit can download packages from remote RPM repositories, or build them locally. By default any `*.spec` files found in `SPECS_DIR="./SPECS"` will be built locally. Dependencies will be downloaded as needed. Only those packages needed to build the current config will be built (`core-efi.json` by default). An additional space separated list of packages may be added using the `PACKAGE_BUILD_LIST=` variable.

Build all local packages needed for the default `core-efi.json`:

```bash
sudo make build-packages -j$(nproc)
```

Build only two packages along with their prerequisites (note `CONFIG_FILE` is explicitly cleared, not specifying it will use the default `core-efi.json` config):

```bash
sudo make build-packages PACKAGE_BUILD_LIST="vim nano" CONFIG_FILE= -j$(nproc)
```

Build packages from a custom SPECS dir:

```bash
sudo make build-packages SPECS_DIR="/my/packages/SPECS" -j$(nproc)
```

#### Working on Packages

The build system will attempt to minimize rebuilds, but sometimes it is useful to force packages to rebuild, or ignore missing packages. Say you want to iterate on the `nano` package, but the `ncurses-devel` package is broken (`ncurses-devel` is a dependency of `nano`)...

##### DOWNLOAD_SRPMS

When `DOWNLOAD_SRPMS=y` is set, the local sources and spec files will not be used, and changes will not be reflected in the final packages.

##### Force Rebuilds

Adding `PACKAGE_REBUILD_LIST="nano"` will tell the build system to always rebuild `nano.spec` even if it thinks the rpm file is up to date.

##### Ignoring Packages

In the event the ncurses package is currently having issues, `PACKAGE_IGNORE_LIST="ncurses"` will tell the build system to pretend the `ncurses.spec` file was already successfully built regardless of the actual local state. As before, explicitly clear the `CONFIG_FILE` variable to skip adding `core-efi.json`'s packages.

```bash
# Work on the nano package while ignoring the state of the ncurses package
sudo make build-packages PACKAGE_BUILD_LIST="nano" PACKAGE_REBUILD_LIST="nano" PACKAGE_IGNORE_LIST="ncurses" CONFIG_FILE=
```

Any build which requires the ignored packages will still attempt to use them during a build, so ensure they are available in the `../out/RPMS` folder.

##### Source Hashes

The build system also enforces hash checking for sources when packaging SRPMs. For a given `*.spec` file a hash of each source is recorded in `*.signatures.json`. The build system will attempt to find a source which matches the recorded hash. If you change a source the signature file can be updated by setting `SRPM_FILE_SIGNATURE_HANDLING=update`.

```bash
# Just update the intermediate SRPMs and their source signatures by using the input-srpms target
sudo make input-srpms SRPM_FILE_SIGNATURE_HANDLING=update
```

## Keys, Certs, and Remote Sources

### Sources

The build system pulls files two ways:

- Downloading files directly.
- Using the `tdnf` package management tool running inside a chroot.

Direct file downloads are by default pulled from:

```makefile
SOURCE_URL         ?=
PACKAGE_URL        ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)/rpms
PACKAGE_UPDATE_URL ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/$(build_arch)/rpms
SRPM_URL           ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms
SRPM_UPDATE_URL    ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/srpms
```

While `tdnf` uses a list of repo files:

```makefile
REPO_LIST ?=
```

The `REPO_LIST` variable supports multiple repo files, and they are prioritized in the order they appear in the list.
The CBL-Mariner base repo is implicitly provided, and an optional update repo is available by setting `USE_UPDATE_REPO=y`. If `$(DISABLE_UPSTREAM_REPOS)` is set to `y`, any repo that is accessed through the network is disabled.

### Authentication

If supplying custom endpoints for source/SRPM/package servers, accessing these resources may require keys and certificates. The keys and certificates can be set using:

```bash
sudo make image CA_CERT=/path/to/rootca.crt TLS_CERT=/path/to/user.crt TLS_KEY=/path/to/user.key
```

## Building Everything From Scratch

**NOTE: Source files must be made available for all packages. They can be placed manually in the corresponding SPEC/\* folders, `SOURCE_URL=<YOUR_SOURCE_SERVER>` may be provided, or DOWNLOAD_SRPMS=y may be used to use pre-packages sources**

The build system can operate without using pre-built components if desired. There are several variables which enable/disable build components and sources of data. They are listed here along with their default values:

```makefile
SOURCE_URL         ?=
PACKAGE_URL        ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)/rpms
PACKAGE_UPDATE_URL ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/$(build_arch)/rpms
SRPM_URL           ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms
SRPM_UPDATE_URL    ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/srpms
REPO_LIST          ?=
```

```makefile
DOWNLOAD_SRPMS         ?= n
REBUILD_TOOLCHAIN      ?= n
REBUILD_PACKAGES       ?= y
REBUILD_TOOLS          ?= n
USE_UPDATE_REPO        ?= y
DISABLE_UPSTREAM_REPOS ?= n
TOOLCHAIN_ARCHIVE      ?=
PACKAGE_ARCHIVE        ?=
```

See [Local Build Variables](#local-build-variables) for details on what each variable does.

### Bootstrapping the Toolchain and Building Everything from Scratch

This command will build all components locally, including all toolchain packages using a two stage bootstrap process. No sources will be pulled remotely **(Unless a package build explicitly attempts to do so within its `*.spec` file)**.

Just the toolchain build will take several hours, building `core-efi.json` may take the better part of a day.

```bash
# Rebuild just the Go tools
sudo make go-tools REBUILD_TOOLS=y

# Bootstrap just the toolchain using publicly available sources via wget (or from SOURCE_URL if set),
#  then rebuild the toolchain properly using the provided sources
# NOTE: Source files must made available via one of:
# - `SOURCE_URL=<YOUR_SOURCE_SERVER>`
# - DOWNLOAD_SRPMS=y (will download pre-packages sources from SRPM_URL=... and SRPM_UPDATE_URL=...)
# - manually placing the correct sources in each /SPECS/* package folder
#     (SRPM_FILE_SIGNATURE_HANDLING=update must be used if the new sources files to not match the existing hashes)
sudo make toolchain PACKAGE_URL="" PACKAGE_UPDATE_URL="" REPO_LIST="" DISABLE_UPSTREAM_REPOS=y REBUILD_TOOLCHAIN=y REBUILD_TOOLS=y
```

```bash
# Complete rebuild of all tool, package, and image files from source.
# NOTE: Source files must made available via one of:
# - `SOURCE_URL=<YOUR_SOURCE_SERVER>`
# - DOWNLOAD_SRPMS=y (will download pre-packages sources from SRPM_URL=... and SRPM_UPDATE_URL=...)
# - manually placing the correct sources in each /SPECS/* package folder
#     (SRPM_FILE_SIGNATURE_HANDLING=update must be used if the new sources files to not match the existing hashes)
sudo make image PACKAGE_URL="" PACKAGE_UPDATE_URL="" REPO_LIST="" DISABLE_UPSTREAM_REPOS=y REBUILD_TOOLCHAIN=y REBUILD_PACKAGES=y REBUILD_TOOLS=y
```

### Local Build Variables

#### URLS and Repos

The build can be configured to prioritize local builds but still use the remote sources if needed. For example: If a locally defined `*.spec` file has build dependencies which are not satisfied locally.

If that is not desired all remote sources can be disabled by clearing the following variable:

#### `SOURCE_URL=...`

> URL to download unavailable source files from when creating `*.src.rpm` files prior to build.

#### `PACKAGE_URL=...`

> URL to download RPM packages from, used to populate the toolchain packages if they are missing.

#### `PACKAGE_UPDATE_URL=...`

> URL to download RPM packages from if not found under `$(PACKAGE_URL)` and `$(USE_UPDATE_REPO)` is set to `y`, used to populate the toolchain packages if they are missing.

#### `SRPM_URL=...`

> URL to download packed SRPM packages from prior to build if `$(DOWNLOAD_SRPMS)` is set to `y`.

#### `SRPM_UPDATE_URL=...`

> URL to download updated versions of packed SRPM packages from prior to build if `$(DOWNLOAD_SRPMS)` is set to `y`.

#### `REPO_LIST=...`

> List of RPM repositories to pull packages from. These packages are used to satisfy dependencies during the build process, and to compose a final image. Locally available packages are always prioritized. The repos are prioritized based on the order they appear in the list: Repos earlier in the list are higher priority.

#### Build Enable/Disable Flags

#### `REBUILD_TOOLCHAIN=...`

##### `REBUILD_TOOLCHAIN=`**`n`** *(default)*

> Use pre-existing toolchain packages from another source. If `TOOLCHAIN_ARCHIVE=my_toolchain.tar.gz` is also set the build system will extract the required packages from that archive. If `TOOLCHAIN_ARCHIVE` is not set the build system will download the required toolchain packages from `$(PACKAGE_URL)` and `$(PACKAGE_UPDATE_URL)`.

##### `REBUILD_TOOLCHAIN=`**`y`**

> Bootstrap the toolchain from the host environment in a docker container. The toolchain consists of those packages which are required to build all other packages (*gcc, tdnf, etc*)

#### `DOWNLOAD_SRPMS=...`

##### `DOWNLOAD_SRPMS=`**`n`** *(default)*

> Pack SRPMs to be built from local SPECs. Will retrieve sources from the SPEC's folder if available, and will download missing sources from `$(SOURCE_URL)`.

##### `DOWNLOAD_SRPMS=`**`y`**

> Download official pre-packed SRPMs from `$(SRPM_URL)`. Use this option if `$(SOURCE_URL)` is not available.

#### `USE_UPDATE_REPO=...`

##### `USE_UPDATE_REPO=`**`y`** *(default)*

> Pull missing packages from the upstream update repository in addition to the base repository.

##### `USE_UPDATE_REPO=`**`n`**

> Only pull missing packages from the upstream base repository.

#### `DISABLE_UPSTREAM_REPOS=...`

##### `DISABLE_UPSTREAM_REPOS=`**`n`** *(default)*

> Pull packages from all set repositories, including external ones accessed through the network.

##### `DISABLE_UPSTREAM_REPOS=`**`y`**

> Only pull missing packages from local repositories. This does not affect hydrating the toolchain from `$(PACKAGE_URL)` and `$(PACKAGE_UPDATE_URL)`.

#### `REBUILD_PACKAGES=...`

##### `REBUILD_PACKAGES=`**`y`** *(default)*

> Parse all local `*.spec` files, and build them if needed.
> A package will be built
>
> - If:
>   - it is present in `CONFIG_FILE=config.json`
>   - or it is listed in `PACKAGE_BUILD_LIST="..."`
>   - or it is a dependency of a package listed in one of the above
> - And:
>   - the corresponding *.rpm files are missing
>   - or the *.rpm files are out of date (based on version numbers)
>   - or the base package is listed in `PACKAGE_REBUILD_LIST`

**NOTE:**

The `*.spec` files are converted to `*.src.rpm` files which bundle the spec files with their source files. If the build tools are not able to find valid source files **which match the SHA1 hash recorded in `*.signatures.json`** then they will attempt to locate the source files from `$(SOURCE_URL)` and download them.

##### `REBUILD_PACKAGES=`**`n`**

> Do not attempt to build any local specs, always download the packages via `tdnf` from the internet if they are missing.

**NOTE:**

It is possible to hydrate the local `*.rpm` files with a one-time manual operation:

```bash
# Create ./out/rpms.tar.gz from the *.rpm files locally available:
sudo make compress-rpms
```

```bash
# Extract all rpms present in rpms.tar.gz into a build environment:
sudo make hydrate-rpms PACKAGE_ARCHIVE=./rpms.tar.gz
```

#### `REBUILD_TOOLS=...`

##### `REBUILD_TOOLS=`**`n`** *(default)*

> Use pre-compiled go binaries, likely provided as part of an SDK. The binaries are expected to be found in `$(TOOL_BINS_DIR)`

##### `REBUILD_TOOLS=`**`y`**

> Build the go tools from source as needed.

## All Build Targets

These are the useful build targets:
| Target                           | Description
|:---------------------------------|:---
| build-packages                   | Build requested `*.rpm` files (see [Packages](#packages)).
| chroot-tools                     | Create the chroot working from the toolchain RPMs.
| clean                            | Clean all built files.
| clean-*                          | Most targets have a `clean-<target>` target which selectively cleans the target's output.
| compress-rpms                    | Compresses all RPMs in `../out/RPMS` into `../out/rpms.tar.gz`. See `hydrate-rpms` target.
| compress-srpms                   | Compresses all SRPMs in `../out/SRPMS` into `../out/srpms.tar.gz`.
| copy-toolchain-rpms              | Copy all toolchain RPMS from `../build/rpm_cache/cache` to  `../out/RPMS`.
| expand-specs                     | Extract working copies of the `*.spec` files from the local `*.src.rpm` files.
| fetch-image-packages             | Locate and download all packages required for an image build.
| fetch-external-image-packages    | Download all external packages required for an image build.
| go-\<tool\>                      | Build a specific tool (ensure `REBUILD_TOOLS=y`).
| go-fmt-all                       | Auto format all `*.go` files.
| go-mod-tidy                      | Tidy the go module files.
| go-test-coverage                 | Run and publish test coverage for all go tools.
| go-tidy-all                      | Runs `go-fmt-all` and `go-mod-tidy`.
| go-tools                         | Preps all go tools (ensure `REBUILD_TOOLS=y` to rebuild).
| hydrate-rpms                     | Hydrates the `../out/RPMS` directory from `rpms.tar.gz`. See `compress-rpms` target.
| image                            | Generate an image (see [Images](#images)).
| initrd                           | Create the initrd for the ISO installer.
| input-srpms                      | Scan the local `*.spec` files, locate sources, and create `*.src.rpm` files.
| iso                              | Create an installable ISO (see [ISOs](#isos)).
| macro-tools                      | Create the directory with expanded rpm macros.
| make-raw-image                   | Create the raw base image.
| meta-user-data                   | Create a `meta-user-data.iso` file under `IMAGES_DIR` using `meta-data` and `user-data` from `META_USER_DATA_DIR`.
| package-toolkit                  | Create this toolkit.
| raw-toolchain                    | Build the initial toolchain bootstrap stage.
| toolchain                        | Ensure all toolchain RPMs are present.
| toolchain_stage2                 | Perform the second stage bootstrap.
| validate-image-config            | Validate the selected image config.
| workplan                         | Create the package build workplan.

## Reproducing a Build

By default the build system will pull the highest possible version of external packages when building. However, there may be circumstances when you wish to reproduce a build using the exact same external package versions as before, even if newer versions are available.

### Build Summaries

The build system supports this behavior through summary files, a JSON representation of packages consumed during a build. By referencing these summary files, the build system can consume the exact same version of external packages later on.

Since the summary files are regenerated every build, if you wish to reproduce a build, you should save the summary files to another location for future use.

| Type of Build                 | Summary File Location                                                                                  | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| Package Build                 | `$(PKGBUILD_DIR)/graph_external_deps.json`                                                             | Generated every package build. Can be saved and used later with the `$(PACKAGE_CACHE_SUMMARY)` variable to reproduce a package build.
| Image Build                   | `$(IMAGEGEN_DIR)/{imagename}/image_deps.json`                                                          | Generated every image build. Can be saved and used later with the `$(IMAGE_CACHE_SUMMARY)` variable to reproduce an image build.
| Initrd Build                  | `$(IMAGEGEN_DIR)/iso_initrd/image_deps.json`                                                           | Generated every initrd and ISO build. Can be saved and used later with the `$(INITRD_CACHE_SUMMARY)` variable to reproduce an initrd build.

### Building From Summaries

To reproduce a build, there are four constraints:

1. The local SPEC files must be the same. That is, you cannot reproduce a build having modified any of the local SPEC files since when the summary files were generated.
2. What is being built must be the same. That is, if the summary files were generated from an image build then the reproduced build must be building the exact same image configuration.
3. The toolkit version must be the same. That is, if the summary files were generated from a `1.0` toolkit, then the reproduced build must be done using the `1.0` toolkit.
4. The builds must be from clean. Both the build that generated the summary files and the reproduced build must be done from a clean state, otherwise there may be leftover files that affect the summary files.

If the above constraints are met then a build can be reproduced from summary files.

### Reproducing a Package Build

To reproduce a package build, run the same make invocation as before, but set:

- `PACKAGE_CACHE_SUMMARY=<path>` to the path of the package build summary file.

### Reproducing an Image Build

To reproduce an image build, run the same make invocation as before, but set:

- `PACKAGE_CACHE_SUMMARY=<path>` to the path of the package build summary file.
- `IMAGE_CACHE_SUMMMARY=<path>` to the path of the image build summary file.

### Reproducing an ISO Build

To reproduce an ISO build, run the same make invocation as before, but set:

- `PACKAGE_CACHE_SUMMARY=<path>` to the path of the package build summary file.
- `IMAGE_CACHE_SUMMMARY=<path>` to the path of the image build summary file.
- `INITRD_CACHE_SUMMMARY=<path>` to the path of the initrd build summary file.

## All Build Variables

---

### Targets

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| CONFIG_FILE                   | `$(RESOURCES_DIR)`/imageconfigs/core-efi/core-efi.json                                                 | Image config file to build
| CONFIG_BASE_DIR               | `$(dir $(CONFIG_FILE))`                                                                               | Base directory to search for image files in (see [image_config.md](../images/image_config.md))
| TERMINAL_ISO_INSTALLER        | n                                                                                                      | Use a command line ISO installer instead of the GUI installer
| UNATTENDED_INSTALLER          |                                                                                                        | Create unattended ISO installer if set. Overrides all other installer options.
| PACKAGE_BUILD_LIST            |                                                                                                        | Additional packages to build
| PACKAGE_REBUILD_LIST          |                                                                                                        | Always rebuild this package, even if it is up-to-date. Base package name, will match all virtual packages produced as well.
| PACKAGE_IGNORE_LIST           |                                                                                                        | Pretend this package is always available, never rebuild it. Base package name, will match all virtual packages produced as well.
| SSH_KEY_FILE                  |                                                                                                        | Use with `make meta-user-data` to add the ssh key from this file into `user-data`.

---

### Rebuild vs. Download

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| REBUILD_TOOLCHAIN             | n                                                                                                      | Bootstrap the toolchain packages locally or download them?
| REBUILD_PACKAGES              | y                                                                                                      | Build packages locally or download them? Only packages with a local spec file will be built.
| REBUILD_TOOLS                 | n                                                                                                      | Build the go tools locally or take them from the SDK?
| TOOLCHAIN_ARCHIVE             |                                                                                                        | Instead of downloading toolchain *.rpms, extract them from here (see `REBUILD_TOOLCHAIN`).
| PACKAGE_ARCHIVE               |                                                                                                        | Use with `make hydrate-rpms` to populate a set of rpms from an archive.
| DOWNLOAD_SRPMS                | n                                                                                                      | Pack SRPMs from local SPECs or download published ones?
| USE_UPDATE_REPO               | y                                                                                                      | Pull missing packages from the upstream update repository in addition to the base repository?
| DISABLE_UPSTREAM_REPOS        | n                                                                                                      | Only pull missing packages from local repositories? This does not affect hydrating the toolchain from `$(PACKAGE_URL)` and `$(PACKAGE_UPDATE_URL)`.

---

### Remote Connections

| Variable                      | Default                                                                                                  | Description
|:------------------------------|:---------------------------------------------------------------------------------------------------------|:---
| SOURCE_URL                    |                                             | URL to request package sources from
| SRPM_URL                      | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms`                           | URL to request packed SRPMs from if `$(DOWNLOAD_SRPMS)` is set to `y`
| SRPM_UPDATE_URL               | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/srpms`                         | URL to request updated versions of packed SRPMs from if `$(DOWNLOAD_SRPMS)` is set to `y`
| PACKAGE_URL                   | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)/rpms`              | URL to request full toolchain packages from
| PACKAGE_UPDATE_URL            | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/update/$(build_arch)/rpms`            | URL to request full toolchain packages from if not found under `$(PACKAGE_URL)` and `$(USE_UPDATE_REPO)` is set to `y`
| REPO_LIST                     |                                                                                                          | Space separated list of repo files for tdnf to pull packages form
| CA_CERT                       |                                                                                                          | CA cert to access the above resources
| TLS_CERT                      |                                                                                                          | TLS cert to access the above resources
| TLS_KEY                       |                                                                                                          | TLS key to access the above resources

---

### Misc Build

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| LOG_LEVEL                     | info                                                                                                   | Console log level for go tools (`panic, fatal, error, warn, info, debug, trace`)
| STOP_ON_WARNING               | n                                                                                                      | Stop on non-fatal makefile failures (see `$(call print_warning, message)`)
| STOP_ON_PKG_FAIL              | n                                                                                                      | Stop all package builds on any failure rather than try and continue.
| SRPM_FILE_SIGNATURE_HANDLING  | enforce                                                                                                | Behavior when checking source file hashes from SPEC files. `update` will create a new entry in the signature file (`enforce, skip, update`)
| ARCHIVE_TOOL                  | $(shell if command -v pigz 1>/dev/null 2>&1 ; then echo pigz ; else echo gzip ; fi )                   | Default tool to use in conjunction with `tar` to extract `*.tar.gz` files. Tries to use `pigz` if available, otherwise uses `gzip`
| INCREMENTAL_TOOLCHAIN         | n                                                                                                      | Only build toolchain RPM packages if they are not already present
| RUN_CHECK                     | n                                                                                                      | Run the %check sections when compiling packages
| PACKAGE_BUILD_RETRIES         | 1                                                                                                      | Number of build retries for each package
| IMAGE_TAG                     | (empty)                                                                                                | Text appended to a resulting image name - empty by default. Does not apply to the initrd. The text will be prepended with a hyphen.

---

### Reproducing Builds

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| PACKAGE_CACHE_SUMMARY         |                                                                                                        | Path to a summary json file that describes what the package RPM cache should contain.
| IMAGE_CACHE_SUMMARY           |                                                                                                        | Path to a summary json file that describes what the image RPM cache should contain.
| INITRD_CACHE_SUMMARY          |                                                                                                        | Path to a summary json file that describes what the initrd RPM cache should contain.

---

### Directory Customization

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| toolkit_root                  | `$(abspath $(dir $(lastword $(MAKEFILE_LIST))))`                                                       | **Calculated automatically and cannot be overwritten.** Location of toolkit (`./toolkit/`). Used to set the default directories
| TOOLS_DIR                     | `$(toolkit_root)`/tools                                                                                | Location of go tools sources
| TOOL_BINS_DIR                 | `$(toolkit_root)`/out/tools                                                                            | Directory to place go tools in
| RESOURCES_DIR                 | `$(toolkit_root)`/resources                                                                            | Location to find default configuration files and other static components
| SCRIPTS_DIR                   | `$(toolkit_root)`/scripts                                                                              | Location of build system scripts
| PROJECT_ROOT                  | `$(toolkit_root)`/..                                                                                   | Root directory of the project
| BUILD_DIR                     | `$(PROJECT_ROOT)`/build                                                                                | Location to put intermediate build artifacts
| OUT_DIR                       | `$(PROJECT_ROOT)`/out                                                                                  | Location to place final artifacts
| SPECS_DIR                     | `$(PROJECT_ROOT)`/SPECS                                                                                | Location to scan for local `*.spec` files
| LOGS_DIR                      | `$(BUILD_DIR)`/logs                                                                                    | Location of log files
| PKGBUILD_DIR                  | `$(BUILD_DIR)`/pkg_artifacts                                                                           | Location of package generation build plan artifacts
| CACHED_RPMS_DIR               | `$(BUILD_DIR)`/rpm_cache                                                                               | Location of the remote rpms which are cached locally
| BUILD_SRPMS_DIR               | `$(BUILD_DIR)`/INTERMEDIATE_SRPMS                                                                      | Location of `*.src.rpm` files generated from local `*.spec` files
| MACRO_DIR                     | `$(BUILD_DIR)`/macros                                                                                  | Location of macro files to use during spec parsing
| BUILD_SPECS_DIR               | `$(BUILD_DIR)`/INTERMEDIATE_SPECS                                                                      | Location of `*.spec` files extracted from the `*.src.rpm` files
| STATUS_FLAGS_DIR              | `$(BUILD_DIR)`/make_status                                                                             | Location of build system status tracking files
| CHROOT_DIR                    | `$(BUILD_DIR)`/worker/chroot                                                                           | Location of package build chroot environments
| IMAGEGEN_DIR                  | `$(BUILD_DIR)`/imagegen                                                                                | Location of image generation workspace
| PKGGEN_DIR                    | `$(TOOLS_DIR)`/pkggen                                                                                  | Location of package build workspace
| TOOLKIT_BINS_DIR              | `$(TOOLS_DIR)`/toolkit_bins                                                                            | Location of go tool binary backups, used to restore the toolkit bins if needed.
| MANIFESTS_DIR                 | `$(RESOURCES_DIR)`/manifests                                                                           | Location of build system static configurations
| TOOLCHAIN_MANIFESTS_DIR       | `$(MANIFESTS_DIR)`/package                                                                             | Location of `toolchain_%{arch}.txt` and `pkggen_core_%{arch}.txt`
| META_USER_DATA_DIR            | `$(RESOURCES_DIR)`/assets/meta-user-data                                                               | Location of `user-data` and `meta-data` files to create the `meta-user-data.iso` file for `cloud-init` initialization.
| RPMS_DIR                      | `$(OUT_DIR)`/RPMS                                                                                      | Directory to place RPMs in
| SRPMS_DIR                     | `$(OUT_DIR)`/SRPMS                                                                                     | Directory to place SRPMs in
| IMAGES_DIR                    | `$(OUT_DIR)`/images                                                                                    | Directory to place images in

---

### Build Details

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| DIST_TAG                      | Version dependent, refer to [Makefile](../../Makefile)                                                 | Distribution tag to customize packages with
| BUILD_NUMBER                  | Version dependent, refer to [Makefile](../../Makefile)                                                 | Build number to customize packages with
| RELEASE_MAJOR_ID              | Version dependent, refer to [Makefile](../../Makefile)                                                 | Major release number
| RELEASE_MINOR_ID              | Version dependent, refer to [Makefile](../../Makefile)                                                 | Minor release number
| RELEASE_VERSION               | Version dependent, refer to [Makefile](../../Makefile)                                                 | Full release version
