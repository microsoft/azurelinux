# Building Packages in the Core Repo

## Overview

This document describes how to build packages in the core repo. Most people should start with [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials).

The following document shows the correct way to build packages for CBL-Mariner. Follow the instructions if you want to build the `.spec` files present in the core repo.

## **1. Install Prerequisites**

Prepare your system by [installing the necessary prerequisites here](../prerequisites.md).

## **2. Pick a Branch or Tag**

Please read [Clone and Sync to Stable Commit](../building.md#clone-and-sync-to-stable-commit) for details on picking a branch to develop from.

For working with packages, the `hybrid` approach is often the most powerful, but the `stable` branches are the easiest. **Be aware that the stable branches trail behind the development branches and this can result in merge conflicts when it is time to create a PR.**

The `hybrid` option minimizes the chance of package conflicts, but runs the risk of seeing unresolvable build cycles appearing.

> **Regardless of your choice**, once you have done the initial development work, you should rebase and run a build on the development branch corresponding to your stable branch before creating a PR. Please reference the [Contribution Guide](CONTRIBUTING.md) for branch descriptions and further PR instructions.

**If you are working on a package found in the [toolchain manifests](../../resources/manifests/package/)**, you should work directly in the development branches. Please refer to [Rebuild the Toolchain](../building.md#rebuild-the-toolchain) for instructions on rebuilding the toolchain.

## **3. Get a Toolchain**

If you are using the `stable` or `hybrid` branch strategy, the toolchain will be handled automatically. Just invoke the `sudo make build-packages ...` commands as needed and the tooling will deal with the rest.

If you are working on a development branch or getting ready for a PR, you will need to build a toolchain. Refer to [Rebuild the Toolchain](../building.md#rebuild-the-toolchain) for details. **Save your toolchain archive for later!**

## **4. Add/Modify a Package**

See [Working with Packages](https://github.com/microsoft/CBL-MarinerTutorials/blob/-/docs/packages/working_with_packages.md#tutorial-customize-your-image-with-unsupported-packages) from the [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials) repo for details on working with RPM packages. This will cover:

* Working with source files
* Calculating package signatures
* Writing .spec files

The core repo behaves slightly differently than the dedicated build environment described in [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials), so use the steps described below to build your package instead.

## **5. Build the Package**

### Setup

```bash
# Clone the CBL-Mariner repo
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner

# Sync to the latest stable build
git checkout 2.0-stable
cd ./toolkit
sudo make clean QUICK_REBUILD=y
```

### Build a toolchain if using an unstable branch

```bash
# OPTIONAL:
#   Build the latest toolchain **if you are NOT working on a stable branch**
git checkout main
sudo make toolchain QUICK_REBUILD_TOOLCHAIN=y

# Copy it somewhere safe if  you want (you can also just leave QUICK_REBUILD_TOOLCHAIN=y set)
cp ../build/toolchain/toolchain_built_rpms_all.tar.gz ~/mariner_toolchain.tar.gz
```

### Decide if you filter out all other packages

There are two ways to build packages:

1) Let the scheduler figure out all of the required packages and build everything from source with the versions in the current branch.
2) Only build the very specific packages you care about, and get **EVERYTHING ELSE** from the stable releases.

Option #2 is generally faster, but can lead to accuracy issues. If one of your packages' dependencies has also been changed in your branch but not published, the build will use the older published version. This is often fine for quick development work, but is not good enough for final testing.

### Signatures

See [Source Hashes](/toolkit/docs/building/building.md#source-hashes) and [Create a Signature Meta-data File](https://github.com/microsoft/CBL-MarinerTutorials/blob/-/docs/packages/working_with_packages.md#create-a-signature-meta-data-file) for details on how source signatures work. You will need to update the signature files for a package if you change the sources at all.

### Dev Loop

```bash
# These are the packages we want to iterate on
package_list="openssh nano"

# OPTIONAL:
#   If you want a fast (but possibly less accurate) build, only pack the specific packages we want to build and
#   use upstream stable packages to fulfill all dependencies.
pkg_filter="SRPM_PACK_LIST='$package_list'"
#   Otherwise, trust the scheduler to optimize the build
pkg_filter=""

# Modify your package
touch ../SPECS/nano/nano.spec
touch ../SPECS/openssh/openssh.spec

# Update signature files, or tell the tools to do it automatically
sha256sum ../SPECS/nano/my_new_nano_file.txt
vim ../SPECS/nano/nano.signatures.json
# --- or ---
signature_handle="SRPM_FILE_SIGNATURE_HANDLING=update"

# OPTIONAL:
#   This is the path to the toolchain as described above.
#   There are three options here:
#       1) Use the toolchain you saved from above
#       2) Trust the build system to update it when needed (changing branches will often cause a rebuild)
#       3) Use a stable branch and don't worry about it
toolchain="TOOLCHAIN_ARCHIVE='~/mariner_toolchain.tar.gz'"
# --- or ---
toolchain="QUICK_REBUILD_TOOLCHAIN=y"
# --- or ---
toolchain=""

# OPTIONAL:
#   Older versions of packages can accumulate if you keep adding new versions (i.e. 1.2.3-1, 1.2.3-2, 1.3.0-1, etc.).
#   The tools are smart enough to detect changes to the .spec files and re-package the SRPMs as needed, but won't delete old
#   versions. You can delete all copies using:
sudo make clean-expand-specs clean-input-srpms 

# Build the packages listed, they will end up in ../out/RPMS
#   -j$(nproc)              Number of parallel threads to use in the Makefile. The pkg scheduler will make its own choices
#   QUICK_REBUILD_PACKAGES=y Try to avoid building packages as much as possible (ie download what we can from the package repo)
#   CONFIG_FILE=""          Do not base package selection on an image config
#   REBUILD_TOOLS=y         Rebuild the go tools if needed
#   $pkg_filer              Optionally only package specific .spec files (see above)
#   $toolchain              Where to get our toolchain (see above)
#   PACKAGE_REBUILD_LIST    List of packages to ALWAYS rebuild, even if they look unchanged (PACKAGE_BUILD_LIST will build them only if they are missing)
#   SRPM_FILE_SIGNATURE_HANDLING Auto update the signature files
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE="" REBUILD_TOOLS=y $pkg_filter $toolchain PACKAGE_REBUILD_LIST="$package_list" $signature_handle

# Repeat as needed
```

### Rebuild All Packages

The following command rebuilds all CBL-Mariner packages in the repo.

```bash
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE="" REBUILD_TOOLS=y $toolchain
```

### Rebuild Minimal Required Packages for an Image

The following command rebuilds packages for the basic VHD on the **stable** branch.

```bash
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE=./imageconfigs/core-legacy.json REBUILD_TOOLS=y $toolchain
```

### Ignoring Packages

In the event the ncurses package is currently having issues, `PACKAGE_IGNORE_LIST="ncurses"` will tell the build system to pretend the `ncurses.spec` file was already successfully built regardless of the actual local state. As before, explicitly clear the `CONFIG_FILE` variable to skip adding `core-efi.json`'s packages.

```bash
# Work on the nano package while ignoring the state of the ncurses package
sudo make build-packages PACKAGE_REBUILD_LIST="nano" PACKAGE_IGNORE_LIST="ncurses" CONFIG_FILE=
```

Any build which requires the ignored packages will still attempt to use them during a build, so ensure they are available in the `../out/RPMS` folder.

## Sources

While the build tools will inject sources found inside a package's folder, we prefer to host the sources on a source server (see [building.md](../building.md) for details about `$SOURCE_URL`). For the core repo, please file a [GitHub issue](https://github.com/microsoft/CBL-Mariner/issues) if you need assistance uploading sources to the CBL-Mariner.
