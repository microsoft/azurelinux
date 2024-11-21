# Building
- [Overview](#overview)
- [Building in Stages](#building-in-stages)
   - [Install Prerequisites](#install-prerequisites)
   - [Clone and Sync To Stable Commit](#clone-and-sync-to-stable-commit)
   - [Toolchain Stage](#toolchain-stage)
     - [Populate Toolchain](#populate-toolchain)
     - [Rebuild Toolchain](#rebuild-toolchain)
   - [Package Stage](#package-stage)
     - [Rebuild All Packages](#rebuild-all-packages)
     - [Rebuild Minimal Required Packages](#rebuild-minimal-required-packages)
     - [Targeted Package Building](#targeted-package-building)
   - [Image Stage](#image-stage)
     - [Virtual Hard Disks and Containers](#virtual-hard-disks-and-containers)
     - [ISO Images](#iso-images)
- [Further Reading](#further-reading)
 - [Packages](#packages)
   - [Working on Packages](#working-on-packages)
      - [DOWNLOAD_SRPMS](#download_srpms)
      - [Force Rebuilds](#force-rebuilds)
      - [Ignoring Packages](#ignoring-packages)
      - [Source Hashes](#source-hashes)
  - [packages.microsoft.com Repository Structure](#packagesmicrosoftcom-repository-structure)
      - [CBL-Mariner 1.0](#cbl-mariner-10)
      - [CBL-Mariner 2.0](#cbl-mariner-20)
  - [Keys, Certs, and Remote Sources](#keys-certs-and-remote-sources)
    - [Sources](#sources)
    - [Authentication](#authentication)
  - [Building Everything From Scratch](#building-everything-from-scratch)
    - [Bootstrapping the Toolchain and Building Everything from Scratch](#bootstrapping-the-toolchain-and-building-everything-from-scratch)
    - [Local Build Variables](#local-build-variables)
      - [URLS and Repos](#urls-and-repos)
      - [`SOURCE_URL=...`](#source_url)
      - [`PACKAGE_URL_LIST=...`](#package_url_list)
      - [`SRPM_URL_LIST=...`](#srpm_url_list)
      - [`REPO_LIST=...`](#repo_list)
      - [Build Enable/Disable Flags](#build-enabledisable-flags)
      - [`REBUILD_TOOLCHAIN=...`](#rebuild_toolchain)
        - [`REBUILD_TOOLCHAIN=`**`n`** *(default)*](#rebuild_toolchainn-default)
        - [`REBUILD_TOOLCHAIN=`**`y`**](#rebuild_toolchainy)
      - [`DOWNLOAD_SRPMS=...`](#download_srpms-1)
        - [`DOWNLOAD_SRPMS=`**`n`** *(default)*](#download_srpmsn-default)
        - [`DOWNLOAD_SRPMS=`**`y`**](#download_srpmsy)
      - [`USE_PREVIEW_REPO=...`](#use_preview_repo)
        - [`USE_PREVIEW_REPO=`**`n`** *(default)*](#use_preview_repon-default)
        - [`USE_PREVIEW_REPO=`**`y`**](#use_preview_repoy)
      - [`DISABLE_UPSTREAM_REPOS=...`](#disable_upstream_repos)
        - [`DISABLE_UPSTREAM_REPOS=`**`n`** *(default)*](#disable_upstream_reposn-default)
        - [`DISABLE_UPSTREAM_REPOS=`**`y`**](#disable_upstream_reposy)
      - [`DISABLE_DEFAULT_REPOS=...`](#disable_default_repos)
        - [`DISABLE_DEFAULT_REPOS=`**`n`** *(default)*](#disable_default_reposn-default)
        - [`DISABLE_DEFAULT_REPOS=`**`y`**](#disable_default_reposy)
      - [`REBUILD_PACKAGES=...`](#rebuild_packages)
        - [`REBUILD_PACKAGES=`**`y`** *(default)*](#rebuild_packagesy-default)
        - [`REBUILD_PACKAGES=`**`n`**](#rebuild_packagesn)
      - [`REBUILD_TOOLS=...`](#rebuild_tools)
        - [`REBUILD_TOOLS=`**`n`** *(default)*](#rebuild_toolsn-default)
        - [`REBUILD_TOOLS=`**`y`**](#rebuild_toolsy)
      - [`REFRESH_WORKER_CHROOT=...`](#refresh_worker_chroot)
        - [`REFRESH_WORKER_CHROOT=`**`n`**](#refresh_worker_chrootn)
        - [`REFRESH_WORKER_CHROOT=`**`y`** *(default)*](#refresh_worker_chrooty-default)
      - [`HYDRATED_BUILD=...`](#hydrated_build)
        - [`HYDRATED_BUILD=`**`y`**](#hydraded_buildy)
        - [`HYDRATED_BUILD=`**`n`** *(default)*](#hydrated_build-default)
      - [`DELTA_BUILD=...`](#delta_build)
        - [`DELTA_BUILD=`**`y`**`](#delta_buildy)
        - [`DELTA_BUILD=`**`n`** *(default)*](#delta_build-default)
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

## Overview

The following documentation describes how to fully build CBL-Mariner end-to-end as well as advanced techniques for performing toolchain, or package builds.  Full builds of CBL-Mariner _**is not**_ generally needed.  All CBL-Mariner packages are built signed and released to an RPM repository at [packages.microsoft.com](https://packages.microsoft.com/cbl-mariner/2.0/prod/)

If you simply want to test-drive CBL-Mariner you may download and install the ISO (see: [readme.md](../../README.md)).  If you want to experiment with CBL-Mariner and build custom images or add packages in a more focused environment, refer to the tutorial in the [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials) repository.

The CBL-Mariner build system consists of several phases and tools, but at a high level it can be viewed simply as 3 distinct build stages:

- **Toolchain** This stage builds a bootstrap toolchain and then builds the official toolchain.  The official toolchain is used in the subsequent package build stage.  Building is highly scripted and serialized in this stage.

- **Package** This stage uses outputs from the toolchain stage to build any package not built in toolchain stage.  Packages are built in parallel during this stage.

- **Image** This stage generates the resulting ISO, VHD, VHDX, and/or container images from the rpm packages built in the package stage.

Each stage can be built completely from scratch, or in many cases may be seeded from pre-built packages and then partially built.


## **Building in Stages**

The following sections run through a build one step at a time, briefly explaining the purpose. `Make` will generally automate this flow if given an image target, however building in stages can be useful for debugging and assists in understanding the build process.

## **Install Prerequisites**

Prepare your system by installing the necessary prerequisites [here](prerequisites.md).

## **Clone and Sync To Stable Commit**

Clone the 2.0-stable build of CBL-Mariner as shown here.

```bash
# Get the source code
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner/toolkit

# Checkout the desired release branch. The 2.0-stable tag tracks the most recent successful release of the 2.0 branch.
git checkout 2.0-stable
```

**IMPORTANT:** The 2.0-stable tag always points to the latest known good build of CBL-Mariner of the 2.0 branch. A similar tag, 1.0-stable, exists for the 1.0 branch. Other branchses are also buildable but not guarnateed to be stable.  The 1.0 and 2.0 branches are periodically updated with bug fixes, security vulnerability fixes or occasional feature enhancements.  As those fixes are integrated into the branch the head of a branch may be temporarily unstable.  The 2.0-stable tag will remain fixed until the tip of the branch is validated and the latest source and binary packages (SRPMs and RPMs) are published.  At that point, the 2.0-stable tag is advanced.  To ensure you have the latest invoke _git fetch --tags_ before building.

It is also possible to build an older version of CBL-Mariner from the 2.0 branch.  CBL-Mariner may be updated at any time, but an aggregate release is declared monthly and [tagged in github](https://github.com/microsoft/CBL-Mariner/releases).  These monthly builds are stable and their tags can be substituted for the 2.0-stable label above.

Alternate branches are not generally buildable because community builds require the SRPMs and/or RPMs be published.  At this time, published files are only available for the 2.0 branch.

**NOTE: All subsequent commands are assumed to be executed from inside the toolkit directory.**

## **Toolchain Stage**

The toolchain builds in two sub-phases.  The first phase builds an initial _bootstrap_ toolchain which is then used to build the _final_ toolchain used in package building.  In the first phase, the bootstrap toolchain downloads a series of source packages from upstream sources.  The second phase downloads SRPMS from packages.microsoft.com.

For expediency, the toolchain may be populated from upstream binaries, or may be completely rebuilt.

### **Populate Toolchain**

A set of bootstrapped toolchain packages (gcc etc.) are used to build CBL-Mariner packages and images.  Rather than build the toolchain, the prebuilt binaries can be downloaded to your local machine.  This happens automatically when the `REBUILD_TOOLCHAIN=` parameter is set to `n` (the default).

```bash
# Populate Toolchain from pre-existing binaries
sudo make toolchain REBUILD_TOOLS=y
```

### **Rebuild Toolchain**

Depending on hardware, rebuilding the toolchain can take several hours. The following builds **the entire toolchain** from scratch:

```bash
# Add REBUILD_TOOLCHAIN=y to any subsequent command to ensure locally built toolchain packages are used
sudo make toolchain REBUILD_TOOLS=y REBUILD_TOOLCHAIN=y
```

## **Package Stage**

After the toolchain is built or populated, package building is possible.  The CBL-Mariner ecosystem provides a significant number of packages, but most of those packages are not used in an image.  When rebuilding packages, you can choose to build everything, or you can choose to build just what you need for a specific image.  This can save significant time because only the subset of the CBL-Mariner packages needed for an image are built.

The CONFIG_FILE argument provides a quick way to declare what to build. To manually build **all** packages you can use the default configuration (`CONFIG_FILE=""`) and invoke the package build target.  To build packages needed for a specific image, you must set the CONFIG_FILE= parameter to an image configuration file of your choice.  The standard image configuration files are in the toolkit/imageconfigs folder.

Large parts of the package build stage are parallelized. Enable this by setting the `-j` flag for `make` to the number of parallel jobs to allow. (Recommend setting this value to the number of logical cores available on your system, or less)

There are several more package build options.  For example it's possible to build a single package with all of its prerequisites.  For more details on package building options see [Packages](#packages).

### **Rebuild All Packages**

The following command rebuilds all CBL-Mariner packages.

```bash
# Build ALL packages
# (NOTE: CBL-Mariner compiles natively, an ARM64 build machine is required to create ARM64 packages/images)
sudo make build-packages -j$(nproc) REBUILD_TOOLS=y
```

### **Rebuild Minimal Required Packages**

The following command rebuilds packages for the basic VHD.

```bash
# Build the subset of packages needed to build the basic VHD
# (NOTE: CBL-Mariner compiles natively, an ARM64 build machine is required to create ARM64 packages/images)
sudo make build-packages -j$(nproc) CONFIG_FILE=./imageconfigs/core-legacy.json REBUILD_TOOLS=y
```

Note that the image config file passed to the CONFIG_FILE option _only_ builds the packages included in the image plus all packages needed to build those packages.  That is, more will be built than needed by the image, but only a subset of packages will be built.

### **Targeted Package Building**
Beginning with the CBL-Mariner 2.0's 2022 October Release (2.0.20221007) it is possible to rapidly build one or more packages "in-tree".  This technique can be helpful for modifying an existing SPEC file or adding a new one to CBL-Mariner.

```bash
# Build targeted packages
sudo make build-packages -j$(nproc) REBUILD_TOOLS=y SRPM_PACK_LIST="openssh"
```
Note that this process will download dependencies from packages.microsoft.com and rebuild just the SPEC files indicated by the SRPM_PACK_LIST

After building a package you may choose to rebuild it or build additional packages.  The optional `REFRESH_WORKER_CHROOT=n` option (default is `y`) will avoid rebuilding the worker chroot saving some additional build overhead

```bash
# Clean and rebuild targeted packages
sudo make clean-build-packages
sudo make build-packages -j$(nproc) REBUILD_TOOLS=y SRPM_PACK_LIST="at openssh" REFRESH_WORKER_CHROOT=n

# Rebuild single package
sudo make build-packages -j$(nproc) REBUILD_TOOLS=y SRPM_PACK_LIST="at" PACKAGE_REBUILD_LIST="at" REFRESH_WORKER_CHROOT=n
```

## **Image Stage**

Different images and image formats can be produced from the build system.  Images are assembled from a combination of _Image Configuration_ files and _Package list_ files.  Each [Package List](https://github.com/microsoft/CBL-MarinerTutorials#package-lists) file (in [toolkit/imageconfigs/packagelists](https://github.com/microsoft/CBL-Mariner/tree/2.0/toolkit/imageconfigs/packagelists)) describes a set of packages to install in an image.  Each Image Configuration file defines the image output format and selects one or more Package Lists to include in the image.

By default, the `make image` and `make iso` commands (discussed below) build missing packages before starting the image build sequence.  By adding the `REBUILD_PACKAGES=n` argument, the image build phase will supplement missing packages with those on packages.microsoft.com.  This can accelerate the image build process, especially when performing targeted package builds ([targeted Package Building](#targeted-package-building)

All images are generated in the `out/images` folder.

### Virtual Hard Disks and Containers

```bash
# To build a Mariner VHD Image (VHD folder: ../out/images/core-legacy)
sudo make image CONFIG_FILE=./imageconfigs/core-legacy.json REBUILD_TOOLS=y

# To build a Mariner VHDX Image (VHDX folder ../out/images/core-efi)
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json REBUILD_TOOLS=y

# To build a core Mariner Contianer (Container Folder: ../out/images/core-container/*.tar.gz
sudo make image CONFIG_FILE=./imageconfigs/core-container.json REBUILD_TOOLS=y
```

### ISO Images
ISOs are bootable images that install CBL-Mariner to either a physical or virtual machine.  The installation process can be manually guided through user prompting, or automated through unattended installation.

NOTE: ISOs require additional packaging and build steps (such as the creation of a separate `initrd` installer image used to install the final image to disk).  These additional resources are stored in the toolkit/resources/imagesconfigs folder.


The following builds an ISO with an interactive UI and selectable image configurations.
```bash
# To build a CBL-Mariner ISO Image (ISO folder: ../out/images/full)
sudo make iso CONFIG_FILE=./imageconfigs/full.json REBUILD_TOOLS=y
```

To create an unattended ISO installer (no interactive UI) use `UNATTENDED_INSTALLER=y` and run with a [`CONFIG_FILE`](https://github.com/microsoft/CBL-MarinerTutorials#image-config-file) that only specifies a _single_ SystemConfig.

```bash
# Build the standard ISO with unattended installer that installs onto the default Gen1 HyperV VM. Needs to cloud-init provision the user once unattended installation finishes.
sudo make iso -j$(nproc) CONFIG_FILE=./imageconfigs/core-legacy-unattended-hyperv.json REBUILD_TOOLS=y UNATTENDED_INSTALLER=y
```

# Further Reading

## Packages

The toolkit can download packages from remote RPM repositories, or build them locally. By default any `*.spec` files found in `SPECS_DIR="./SPECS"` will be built locally. Dependencies will be downloaded as needed. Only those packages needed to build the current [config](https://github.com/microsoft/CBL-MarinerTutorials#image-config-file) will be built (`core-efi.json` by default). An additional space separated list of packages may be added using the `PACKAGE_BUILD_LIST=` variable.

Build all local packages needed for the default `core-efi.json`:

```bash
sudo make build-packages -j$(nproc)
```

Build only two packages along with their prerequisites:

```bash
sudo make build-packages PACKAGE_BUILD_LIST="vim nano" -j$(nproc)
```

Build packages from a custom SPECS dir:

```bash
sudo make build-packages SPECS_DIR="/my/packages/SPECS" -j$(nproc)
```

### Working on Packages

The build system will attempt to minimize rebuilds, but sometimes it is useful to force packages to rebuild, or ignore missing packages. Say you want to iterate on the `nano` package, but the `ncurses-devel` package is broken (`ncurses-devel` is a dependency of `nano`)...

#### DOWNLOAD_SRPMS

When `DOWNLOAD_SRPMS=y` is set, the local sources and spec files will not be used, and changes will not be reflected in the final packages.

#### Force Rebuilds

Adding `PACKAGE_REBUILD_LIST="nano"` will tell the build system to always rebuild `nano.spec` even if it thinks the rpm file is up to date.

#### Ignoring Packages

In the event the ncurses package is currently having issues, `PACKAGE_IGNORE_LIST="ncurses"` will tell the build system to pretend the `ncurses.spec` file was already successfully built regardless of the actual local state.

```bash
# Work on the nano package while ignoring the state of the ncurses package
sudo make build-packages PACKAGE_BUILD_LIST="nano" PACKAGE_REBUILD_LIST="nano" PACKAGE_IGNORE_LIST="ncurses"
```

Any build which requires the ignored packages will still attempt to use them during a build, so ensure they are available in the `../out/RPMS` folder.

#### Source Hashes

The build system also enforces hash checking for sources when packaging SRPMs. For a given `*.spec` file a hash of each source is recorded in `*.signatures.json`. The build system will attempt to find a source which matches the recorded hash. If you change a source the signature file can be updated by setting `SRPM_FILE_SIGNATURE_HANDLING=update`.

```bash
# Just update the intermediate SRPMs and their source signatures by using the input-srpms target
sudo make input-srpms SRPM_FILE_SIGNATURE_HANDLING=update
```

### packages.microsoft.com Repository Structure

CBL-Mariner packages are available on [packages.microsoft.com](https://packages.microsoft.com/cbl-mariner/). The CBL-Mariner repositories are divided into major release folders (1.0, 2.0, etc). Each top level folder is subdivided into "preview" and "production" (prod) repositories.

The "preview" and "production" folders are further subdivided into purpose, and then again for architecture. This includes locations for source-rpms.

#### CBL-Mariner 1.0

For CBL-Mariner 1.0, the repositories are structured as follows:

- **Base:** Packages released with CBL-Mariner 1.0.
- **Update:** Base packages added or updated since CBL-Mariner 1.0's release date.
- **CoreUI:** Targeted UI related packages.
- **Extras:** CBL-Mariner 1.0 packages that are built by Microsoft and are closed source.
- **NVIDIA:** Specially licensed NVIDIA packages.
- **Microsoft:** Packages built by other, non-CBL-Mariner, Microsoft teams.

#### CBL-Mariner 2.0

For CBL-Mariner 2.0, the repositories are structured as follows:

- **Base:** Packages released with CBL-Mariner 2.0 and their updates.
- **Extras:** CBL-Mariner 2.0 packages that are built by Microsoft and are closed source
- **Extended:** CBL-Mariner 2.0 packages that are not considered part of core. Generally, viewed as experimental or for development purposes.
- **NVIDIA:** Specially licensed NVIDIA packages.
- **Microsoft:** Packages built by other, non-CBL-Mariner, Microsoft teams.

## Keys, Certs, and Remote Sources

### Sources

The build system pulls files two ways:

- Downloading files directly.
- Using the `tdnf` package management tool running inside a chroot.

Direct file downloads are by default pulled from:

```makefile
SOURCE_URL         ?=
PACKAGE_URL_LIST   ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)
SRPM_URL_LIST      ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms
```

While `tdnf` uses a list of repo files:

```makefile
REPO_LIST ?=
```

The `REPO_LIST` variable supports multiple repo files, and they are prioritized in the order they appear in the list.
The CBL-Mariner base repo is implicitly provided and an optional preview repo is available by setting `USE_PREVIEW_REPO=y`.
If `DISABLE_UPSTREAM_REPOS=y` is set, any repo that is accessed through the network is disabled.

### Authentication

If supplying custom endpoints for source/SRPM/package servers, accessing these resources may require keys and certificates. The keys and certificates can be set using:

```bash
sudo make image CONFIG_FILE="./imageconfigs/core-efi.json" CA_CERT=/path/to/rootca.crt TLS_CERT=/path/to/user.crt TLS_KEY=/path/to/user.key
```

## Building Everything From Scratch

**NOTE: Source files must be made available for all packages. They can be placed manually in the corresponding SPEC/\* folders, `SOURCE_URL=<YOUR_SOURCE_SERVER>` may be provided, or DOWNLOAD_SRPMS=y may be used to use pre-packages sources. Core Mariner source packages are available at `SOURCE_URL=https://cblmarinerstorage.blob.core.windows.net/sources/core`**

The build system can operate without using pre-built components if desired. There are several variables which enable/disable build components and sources of data. They are listed here along with their default values:

```makefile
SOURCE_URL         ?= https://cblmarinerstorage.blob.core.windows.net/sources/core
PACKAGE_URL_LIST   ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)
SRPM_URL_LIST      ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms
REPO_LIST          ?=
```

```makefile
DOWNLOAD_SRPMS         ?= n
REBUILD_TOOLCHAIN      ?= n
REBUILD_PACKAGES       ?= y
REBUILD_TOOLS          ?= n
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
# - DOWNLOAD_SRPMS=y (will download pre-packages sources from SRPM_URL_LIST=...)
# - manually placing the correct sources in each /SPECS/* package folder
#     (SRPM_FILE_SIGNATURE_HANDLING=update must be used if the new sources files to not match the existing hashes)
sudo make toolchain PACKAGE_URL_LIST="" REPO_LIST="" DISABLE_UPSTREAM_REPOS=y REBUILD_TOOLCHAIN=y REBUILD_TOOLS=y
```

```bash
# Complete rebuild of all tool, package, and image files from source.
# NOTE: Source files must made available via one of:
# - `SOURCE_URL=<YOUR_SOURCE_SERVER>`
# - DOWNLOAD_SRPMS=y (will download pre-packages sources from SRPM_URL_LIST=...)
# - manually placing the correct sources in each /SPECS/* package folder
#     (SRPM_FILE_SIGNATURE_HANDLING=update must be used if the new sources files to not match the existing hashes)
sudo make image CONFIG_FILE="./imageconfigs/core-efi.json" PACKAGE_URL_LIST="" REPO_LIST="" DISABLE_UPSTREAM_REPOS=y REBUILD_TOOLCHAIN=y REBUILD_PACKAGES=y REBUILD_TOOLS=y
```

### Local Build Variables

#### Quickrebuild Defaults

Quickrebuild flags will set some flags to try and optimize builds for speed. This involves using as many packages as possible from the upstream repos for both package building and for toolchain creation. These flags are meant to work on any branch.

#### `QUICK_REBUILD=...`

##### `QUICK_REBUILD=`**`n`** _(default)_

> Do not set any additional quickbuild flags

##### `QUICK_REBUILD=`**`y`**

> If they are not set, set `QUICK_REBUILD_TOOLCHAIN=y` and `QUICK_REBUILD_PACKAGES=y`.

#### `QUICK_REBUILD_TOOLCHAIN=...`

##### `QUICK_REBUILD_TOOLCHAIN=`**`n`** _(default)_

> Do not set toolchain specific quick rebuild flags

##### `QUICK_REBUILD_TOOLCHAIN=`**`y`**

> Set `REBUILD_TOOLCHAIN = y`, `INCREMENTAL_TOOLCHAIN = y`, `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL = y`, `REBUILD_TOOLS ?= y`.

#### `QUICK_REBUILD_PACKAGES=...`

##### `QUICK_REBUILD_PACKAGES=`**`n`** _(default)_

> Do not set toolchain specific quick rebuild flags

##### `QUICK_REBUILD_PACKAGES=`**`y`**

> Set `DELTA_BUILD = y`, `REBUILD_TOOLS ?= y`, `REBUILD_TOOLS ?= y`.

#### URLS and Repos

The build can be configured to prioritize local builds but still use the remote sources if needed. For example: If a locally defined `*.spec` file has build dependencies which are not satisfied locally.

If that is not desired all remote sources can be disabled by clearing the following variable:

#### `SOURCE_URL=...`

> URL to download unavailable source files from when creating `*.src.rpm` files prior to build. Only one URL can be set at a time; there is no support for a list of multiple source URLs.

#### `PACKAGE_URL_LIST=...`

> Space separated list of URLs to download toolchain RPM packages from, used to populate the toolchain packages if `$(REBUILD_TOOLCHAIN)` is set to `n`. Defaults to the standard distro repos. Overriding this will clear all the default values. May be augmented by passing `USE_PREVIEW_REPO=y` which will uncondinally append the distro's preview repos to what ever set of URLs is being used.

#### `SRPM_URL_LIST=...`

> Space separated list of URLs to download packed SRPM packages from prior to build if `$(DOWNLOAD_SRPMS)` is set to `y`.

#### `REPO_LIST=...`

> Space separated list of `.repo` files pointing to RPM repositories to pull packages from. These packages are used to satisfy dependencies during the build process, and to compose a final image. Locally available packages are always prioritized. The repos are prioritized based on the order they appear in the list: repos earlier in the list are higher priority. CBL-Mariner provides a set of pre-populated RPM repositories accessible inside the toolkit folder under `toolkit/repos`:
>
> - `mariner-official-base.repo` and `mariner-official-update.repo` - default, always-on CBL-Mariner repositories.
> - `mariner-preview.repo` - CBL-Mariner repository containing pre-release versions of RPMs **subject to change without notice**. Using this .repo file is equivalent to adding the [`USE_PREVIEW_REPO=y`](#use_preview_repoy) argument to your build command.
> - `mariner-ui.repo` and `mariner-ui-preview.repo` - CBL-Mariner repository containing packages related to any UI components. The preview version serves the same purpose as the official preview repo.
> - `mariner-extras.repo` and `mariner-extras-preview.repo` - CBL-Mariner repository containing proprietory RPMs with sources not viewable to the public. The preview version serves the same purpose as the official preview repo.
>

#### Build Enable/Disable Flags

#### `REBUILD_TOOLCHAIN=...`

##### `REBUILD_TOOLCHAIN=`**`n`** *(default)*

> Use pre-existing toolchain packages from another source. If `TOOLCHAIN_ARCHIVE=my_toolchain.tar.gz` is also set the build system will extract the required packages from that archive. If `TOOLCHAIN_ARCHIVE` is not set the build system will download the required toolchain packages from `$(PACKAGE_URL_LIST)`.

##### `REBUILD_TOOLCHAIN=`**`y`**

> Bootstrap the toolchain from the host environment in a docker container. The toolchain consists of those packages which are required to build all other packages (*gcc, tdnf, etc*)

#### `INCREMENTAL_TOOLCHAIN=...`

##### `INCREMENTAL_TOOLCHAIN=`**`n`** *(default)*

> If rebuilding the toolchain (`REBUILD_TOOLCHAIN=y`), perform a full build of the final toolchain packages. No RPMs from (a) previous failed builds or (b) upstream package repos will be reused.

##### `INCREMENTAL_TOOLCHAIN=`**`y`**

> Do not clear out the toolchain build chroot before performing a build of the final toolchain packages. RPMs within the toolchain build chroot will be used as a cache to avoid rebuilding already-built SRPMs. These RPMs can be seeded by (a) previous failed builds or (b) upstream package repos.

#### `CLEAN_TOOLCHAIN_CONTAINERS=...`

##### `CLEAN_TOOLCHAIN_CONTAINERS=n`

> Leave the raw toolchain containers in docker when running `make clean`. If they match the configuration of the current build they will be re-used.

##### `CLEAN_TOOLCHAIN_CONTAINERS=`**`y`** *(default)*

> Delete all `marinertoolchain*` containers and images associated with this working directory when running `make clean`.

#### `DELTA_FETCH=...`

##### `DELTA_FETCH=n`

> Don't download pre-built packages to avoid rebuilds..

##### `DELTA_FETCH=`**`y`** *(default)*

> Try to download pre-built packages if the versions match the local spec files.

#### `PRECACHE=...`

##### `PRECACHE=`**`n`** *(default)*

> Don't pre-load the cache from upstream sources

##### `PRECACHE=y`

> Load the cache with RPMs from the upstream repos before starting to build.

#### `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL=...`

##### `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL=`**`n`** *(default)*

> If performing an incremental toolchain build (`INCREMENTAL_TOOLCHAIN=y`), do not attempt to pull any packages from `$(PACKAGE_URL_LIST)`.

##### `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL=`**`y`**

> If performing an incremental toolchain build (`INCREMENTAL_TOOLCHAIN=y`), attempt to pull as many RPMs listed in the arch-specific toolchain manifest from the repos listed in `$(PACKAGE_URL_LIST)`. These RPMs will used as a cache to avoid rebuilding already-built SRPMs.

#### `DOWNLOAD_SRPMS=...`

##### `DOWNLOAD_SRPMS=`**`n`** *(default)*

> Pack SRPMs to be built from local SPECs. Will retrieve sources from the SPEC's folder if available, and will download missing sources from `$(SOURCE_URL)`.

##### `DOWNLOAD_SRPMS=`**`y`**

> Download official pre-packed SRPMs from `$(SRPM_URL)`. Use this option if `$(SOURCE_URL)` is not available.

#### `USE_PREVIEW_REPO=...`

##### `USE_PREVIEW_REPO=`**`n`** *(default)*

> Do not pull missing packages from the upstream preview repository.

##### `USE_PREVIEW_REPO=`**`y`**

> Pull missing packages from the upstream preview repository in addition to the base repository. This will uncondinally append the preview repo sources to `PACKAGE_URL_LIST`, `SRPM_URL_LIST`, and `REPO_LIST`.

#### `DISABLE_UPSTREAM_REPOS=...`

##### `DISABLE_UPSTREAM_REPOS=`**`n`** *(default)*

> Pull packages from all set repositories, including external ones accessed through the network.

##### `DISABLE_UPSTREAM_REPOS=`**`y`**

> Only pull missing packages from local repositories. This does not affect hydrating the toolchain from `$(PACKAGE_URL_LIST)`.

#### `DISABLE_DEFAULT_REPOS=...`

##### `DISABLE_DEFAULT_REPOS=`**`n`** *(default)*

> Pull packages from all set repositories, including PMC repositories.

##### `DISABLE_DEFAULT_REPOS=`**`y`**

> Only pull missing packages from local and repositories specified in `$(REPO_LIST)` files.

#### `REBUILD_PACKAGES=...`

##### `REBUILD_PACKAGES=`**`y`** *(default)*

> Parse all local `*.spec` files, and build them if needed.
> A package will be built
>
> - If:
>   - it is present in `CONFIG_FILE=config.json`
>   - or it is listed in `PACKAGE_BUILD_LIST="..."`
>   - or it is listed in `PACKAGE_REBUILD_LIST="..."`
>   - or it is a dependency of a package listed in one of the above
> - And:
>   - the corresponding *.rpm files are missing
>   - or the *.rpm files are out of date (based on version numbers)

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

#### `REFRESH_WORKER_CHROOT=...`

##### `REFRESH_WORKER_CHROOT=`**`n`**

> If exists, don't attempt to rebuild the worker chroot, even if its build script, its manifest, or the packages it consists of have been modified in the local repository.

##### `REFRESH_WORKER_CHROOT=`**`y`** *(default)*

> Rebuild the worker chroot every time at least one of the following has changed:
>
> - worker chroot's manifest file,
> - at least one of the RPM packages mentioned in the manifest file, or
> - the script responsible for building the chroot.

#### `HYDRATED_BUILD=...`

##### `HYDRATED_BUILD=`**`y`**

> If exists, all the dependency RUN nodes will be replaced with PreBuilt Nodes if those RPMs are hydrated already. So if any dependency package fails to build, the subsequent dependent packages will not be stuck as their dependency will be satisfied by hydrated RPM. This is even applicable to the packages mentioned in REBUILD_PACKAGES.

##### `HYDRATED_BUILD=`**`n`** *(default)*

> Normal build. No hydrated RPMs will be used.

#### `DELTA_BUILD=...`

##### `DELTA_BUILD=`**`y`**

> Delta build. Used for fast delta builds where published packages are pre-populated and only new or added packages are built.

##### `DELTA_BUILD=`**`n`** *(default)*

> Normal build.

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
| copy-toolchain-rpms              | **[DEPRECATED]: This should no longer be needed as a work around in core repo builds. Will be removed in future versions.** Copy all toolchain RPMS from `../build/toolchain_rpms` to  `../out/RPMS`.
| expand-specs                     | Extract working copies of the `*.spec` files from the local `*.src.rpm` files.
| fetch-image-packages             | Locate and download all packages required for an image build.
| fetch-external-image-packages    | Download all external packages required for an image build.
| go-\<tool\>                      | Build a specific tool (ensure `REBUILD_TOOLS=y`).
| go-fmt-all                       | Auto format all `*.go` files.
| go-mod-tidy                      | Tidy the go module files.
| go-test-coverage                 | Run and publish test coverage for all go tools.
| go-tidy-all                      | Runs `go-fmt-all` and `go-mod-tidy`.
| go-tools                         | Preps all go tools (ensure `REBUILD_TOOLS=y` to rebuild).
| help                             | Display basic usage information for most commonly used build targets and variables.
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

The build system supports this behavior through summary files, a JSON representation of packages consumed during a build. By referencing these summary files, the build system can consume the exact same version of packages later on.

Since the summary files are regenerated every build, if you wish to reproduce a build, you should save the summary files to another location for future use.

| Type of Build                 | Summary File Location                                                                                  | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| Package Build                 | `$(PKGBUILD_DIR)/graph_external_deps.json`                                                             | Generated every package build. Can be saved and used later with the `PACKAGE_CACHE_SUMMARY` variable to reproduce a package build. Contains **only the external** packages required to build the local packages.
| Image Build                   | `$(IMAGEGEN_DIR)/{imagename}/image_deps.json`                                                          | Generated every image build. Can be saved and used later with the `IMAGE_CACHE_SUMMARY` variable to reproduce an image build. Contains **all (both external and local)** packages required to build the image.
| Initrd Build                  | `$(IMAGEGEN_DIR)/iso_initrd/image_deps.json`                                                           | Generated every initrd and ISO build. Can be saved and used later with the `INITRD_CACHE_SUMMARY` variable to reproduce an initrd build. Contains **all (both external and local)** packages required to build the image. However, unless you modified the initrd image packages JSON or have your own version of its PMC packages locally, all the required packages are external.

**WARNING**: the `graph_external_deps.json` contains **ALL** external packages required to build your local spec files. If you depend on any external packages outside the core CBL-Mariner's PMC repository, you **MUST** make sure you still have access to them when attempting to reproduce a build.

### Building From Summaries

To reproduce a build, there are four constraints:

1. The local SPEC files must be the same. That is, you cannot reproduce a build having modified any of the local SPEC files since when the summary files were generated.
2. What is being built must be the same. That is, if the summary files were generated from an image build then the reproduced build must be building the exact same image configuration.
3. The toolkit version must be the same. That is, if the summary files were generated from a `2.0` toolkit, then the reproduced build must be done using the `2.0` toolkit.
4. The builds must be from clean. Both the build that generated the summary files and the reproduced build must be done from a clean state, otherwise there may be leftover files that affect the summary files. The only exception is the mentioned case of using external packages not present in the PMC repository - in this case you'll need to pre-populate the local cache with these packages after cleaning your repository, but before running the build.

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
| CONFIG_FILE                   | `""`                                                                                                   | [Image config file](https://github.com/microsoft/CBL-MarinerTutorials#image-config-file) to build.
| CONFIG_BASE_DIR               | `$(dir $(CONFIG_FILE))`                                                                                | Base directory on the **build machine** to search for any **relative** file paths mentioned inside the [image config file](https://github.com/microsoft/CBL-MarinerTutorials#image-config-file). This has no effect on **absolute** file paths or file paths on the **built image**.
| UNATTENDED_INSTALLER          |                                                                                                        | Create unattended ISO installer if set. Overrides all other installer options.
| PACKAGE_BUILD_LIST            |                                                                                                        | Explicit list of packages to build. The package will be skipped if the build system thinks it is already up-to-date. The argument accepts both spec and package names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package both `python-werkzeug` and `python3-werkzeug` are correct.
| PACKAGE_REBUILD_LIST          |                                                                                                        | Always rebuild this package, even if it is up-to-date. Base package name, will match all virtual packages produced as well. The argument accepts both spec and package names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package both `python-werkzeug` and `python3-werkzeug` are correct.
| SRPM_PACK_LIST                |                                                                                                        | List of spec basenames to build into SRPMs. If empty, all specs under `$(SPECS_DIR)` will be packed. The argument accepts **ONLY** spec names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package only `python-werkzeug` is correct. Using `python3-werkzeug` will return an error.
| SSH_KEY_FILE                  |                                                                                                        | Use with `make meta-user-data` to add the ssh key from this file into `user-data`.
| TEST_RUN_LIST                 |                                                                                                        | Explicit list of packages to test. The package test will be skipped if the build system thinks it is already up-to-date. The argument accepts both spec and package names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package both `python-werkzeug` and `python3-werkzeug` are correct.
| TEST_RERUN_LIST               |                                                                                                        | Always test these package, even if it its corresponding package is up-to-date. The argument accepts both spec and package names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package both `python-werkzeug` and `python3-werkzeug` are correct.
| TEST_IGNORE_LIST              |                                                                                                        | Ignore testing these packages. Ignoring and forcing the same test re-run is invalid and will fail the build. The argument accepts both spec and package names. Example: for `python-werkzeug.spec`, which builds the `python3-werkzeug` package both `python-werkzeug` and `python3-werkzeug` are correct.

---

### Rebuild vs. Download

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| REBUILD_TOOLCHAIN             | n                                                                                                      | Bootstrap the toolchain packages locally or download them?
| ALLOW_TOOLCHAIN_DOWNLOAD_FAIL | n                                                                                                      | Allow for partial rehydration of the toolchain from `$(PACKAGE_URL_LIST)`? Only applicable if `REBUILD_TOOLCHAIN=y` and `INCREMENTAL_TOOLCHAIN=y`.
| REBUILD_PACKAGES              | y                                                                                                      | Build packages locally or download them? Only packages with a local spec file will be built.
| REBUILD_TOOLS                 | n                                                                                                      | Build the go tools locally or take them from the SDK?
| TOOLCHAIN_ARCHIVE             |                                                                                                        | Instead of downloading toolchain *.rpms, extract them from here (see `REBUILD_TOOLCHAIN`).
| PACKAGE_ARCHIVE               |                                                                                                        | Use with `make hydrate-rpms` to populate a set of rpms from an archive.
| DOWNLOAD_SRPMS                | n                                                                                                      | Pack SRPMs from local SPECs or download published ones?
| USE_PREVIEW_REPO              | n                                                                                                      | Pull missing packages from the upstream preview repository in addition to the base repository?
| DISABLE_UPSTREAM_REPOS        | n                                                                                                      | Only pull missing packages from local repositories? This does not affect hydrating the toolchain from `$(PACKAGE_URL_LIST)`.
| DISABLE_DEFAULT_REPOS         | n                                                                                                      | Disable pulling packages from PMC. Use this option with `REPO_LIST` if you want to use your own repository exclusively.
| CACHED_PACKAGES_ARCHIVE       |                                                                                                        | Use with `make hydrate-cached-rpms` to populate the external RPMs cache from an archive.

---

### Remote Connections

| Variable                      | Default                                                                                                  | Description
|:------------------------------|:---------------------------------------------------------------------------------------------------------|:---
| SOURCE_URL                    |                                                                                                          | URL to request package sources from
| SRPM_URL_LIST                 | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms`                         | Space separated list of URLs to request packed SRPMs from if `$(DOWNLOAD_SRPMS)` is set to `y`
| PACKAGE_URL_LIST              | `https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)`...              | Space separated list of URLs to download toolchain RPM packages from, used to populate the toolchain packages if `$(REBUILD_TOOLCHAIN)` is set to `y`.
| REPO_LIST                     |                                                                                                          | Space separated list of repo files for tdnf to pull packages form
| CA_CERT                       |                                                                                                          | CA cert to access the above resources, in addition to the system certificate store
| TLS_CERT                      |                                                                                                          | TLS cert to access the above resources
| TLS_KEY                       |                                                                                                          | TLS key to access the above resources

---

### Misc Build

| Variable                      | Default                                                                                                | Description
|:------------------------------|:-------------------------------------------------------------------------------------------------------|:---
| LOG_LEVEL                     | info                                                                                                   | Console log level for go tools (`panic, fatal, error, warn, info, debug, trace`)
| LOG_COLOR                     | auto                                                                                                   | Console log color for go tools (`always`, `auto`, `never`). `always` enables color in both logs and terminal output, `auto`(default option) enables color in terminal output, and `never` disables color in all.
| STOP_ON_WARNING               | n                                                                                                      | Stop on non-fatal makefile failures (see `$(call print_warning, message)`)
| STOP_ON_PKG_FAIL              | n                                                                                                      | Stop all package builds on any failure rather than try and continue.
| SRPM_FILE_SIGNATURE_HANDLING  | enforce                                                                                                | Behavior when checking source file hashes from SPEC files. `update` will create a new entry in the signature file (`enforce, skip, update`)
| ARCHIVE_TOOL                  | $(shell if command -v pigz 1>/dev/null 2>&1 ; then echo pigz ; else echo gzip ; fi )                   | Default tool to use in conjunction with `tar` to extract `*.tar.gz` files. Tries to use `pigz` if available, otherwise uses `gzip`
| INCREMENTAL_TOOLCHAIN         | n                                                                                                      | Only build toolchain RPM packages if they are not already present
| RUN_CHECK                     | n                                                                                                      | Run the %check sections when compiling packages
| ALLOW_TOOLCHAIN_REBUILDS      | n                                                                                                      | Do not treat rebuilds of toolchain packages during regular package build phase as errors.
|  PACKAGE_BUILD_RETRIES        | 1                                                                                                      | Number of build retries for each package
| CHECK_BUILD_RETRIES           | 1                                                                                                      | Minimum number of check section retries for each package if RUN_CHECK=y and tests fail.
| MAX_CASCADING_REBUILDS        |                                                                                                        | When a package rebuilds, how many additional layers of dependent packages will be forced to rebuild (leave unset for unbounded, i.e., all downstream packages will rebuild)
| EXTRA_BUILD_LAYERS            | 0                                                                                                      | How many additional layers of the build graph to build beyond the requested packages (useful for testing changes in dependent packages)
| IMAGE_TAG                     | (empty)                                                                                                | Text appended to a resulting image name - empty by default. Does not apply to the initrd. The text will be prepended with a hyphen.
| CONCURRENT_PACKAGE_BUILDS     | 0                                                                                                      | The maximum number of concurrent package builds that are allowed at once. If set to 0 this defaults to the number of logical CPUs.
| CLEANUP_PACKAGE_BUILDS        | y                                                                                                      | Cleanup a package build's working directory when it finishes. Note that `build` directory will still be removed on a successful package build even when this is turned off.
| USE_PACKAGE_BUILD_CACHE       | y                                                                                                      | Skip building a package if it and its dependencies are already built.
| NUM_OF_ANALYTICS_RESULTS      | 10                                                                                                     | The number of entries to print when using the `graphanalytics` tool. If set to 0 this will print all available results.
| TARGET_ARCH                   |                                                                                                        | The architecture of the machine that will run the package binaries.
| USE_CCACHE                    | n                                                                                                      | Use ccache automatically to speed up repeat package builds.
| MAX_CPU                       |                                                                                                        | Max number of CPUs used for package building. Use 0 for unlimited. Overrides `%_smp_ncpus_max` macro.

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
| TIMESTAMP_DIR                 | `S(BUILD_DIR)`/timestamp                                                                               | Location of timestamps generated during the last build
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
