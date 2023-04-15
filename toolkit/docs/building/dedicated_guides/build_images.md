# Building Images in the Core Repo

## Overview

This document describes how to build images in the core repo. Most people should start with [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials).

The following document shows the correct way to build custom images for CBL-Mariner. Follow the instructions if you want to build the `.spec` files present in the core repo, and then convert the `.rpm` packages into an image.

> This guide will closely follow [Building Packages](./build_packages.md) to take advantage of bleeding edge, unpublished packages. If you do not need this, consider using [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials).

However, sometimes building quickly in any repo is valuable. The next section will show how to use the core repo in a similar way to what is described in the [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials) repo.

## **Build only an image**

Sometimes you just need to build an image quickly, and you don't want to fuss around with additional repos or directories. The following commands use flags that will make the core repo behave in a very similar manner to the [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials).

Prepare your system by [installing the necessary prerequisites](../prerequisites.md).

```bash
# Clone the CBL-Mariner repo
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner

# Sync to the latest stable build
git checkout 2.0-stable
cd ./toolkit
sudo make clean QUICK_REBUILD=y

# Build the full iso without looking at any local packages. REBUILD_PACKAGES=n fully
#   disables all of the package building mechanisms.
sudo make iso CONFIG_FILE=./imageconfigs/full.json REBUILD_PACKAGES=n REBUILD_TOOLS=y
# --- or ---
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json REBUILD_PACKAGES=n REBUILD_TOOLS=y
```

## **Validate Changes with Local Packages**

The following directions will build both packages and images locally.

### **1. Install Prerequisites**

Prepare your system by [installing the necessary prerequisites here](../prerequisites.md).

### **2. Picking a Branch or Tag**

Please read [Clone and Sync to Stable Commit](../building.md#clone-and-sync-to-stable-commit) for details on picking a branch to develop from.

When working with images, the `stable` approach is often the better choice but will lack bleeding edge packages. Generally, when working with images, the version of a package is less important than simply having the package available. **While less likely when working with images, be cautious of stable branches trailing behind the development branches; this can result in merge conflicts when it is time to create a PR.**

The `hybrid` option minimizes the chance of package conflicts, but runs the risk of seeing unresolvable build cycles appearing.

> Unlike when working on package changes, image changes are generally self-contained enough that a build with a `hybrid` or `stable` setup is sufficient for validation.

### **3. Get a Toolchain**

If you are using the `stable` or `hybrid` branch strategy, the toolchain will be handled automatically. Invoke the `sudo make image ...` or `sudo make iso ...` commands as needed, and the tooling will handle the rest.

If you are working on a development branch, you will need to build a toolchain. Refer to [Rebuild the Toolchain](../building.md#rebuild-the-toolchain) for details. **Save your toolchain archive for later!**

### **4. Create a Custom Image Definition**

See [Image Config Files](https://github.com/microsoft/CBL-MarinerTutorials/blob/-/docs/packages/working_with_packages.md#image-config-file) and [Building an Image](https://github.com/microsoft/CBL-MarinerTutorials/blob/-/docs/building/building.md) from the [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials) repo for details on working with custom images. This will cover:

* Setting up an image config file
* Adding packages to the image

The image config format is [documented here](../../formats/imageconfig.md). This covers instructions on how to:

* Define partition layouts
* Configure advanced storage
* Add users
* Add user-defined customizations
* Configure unattended installer behavior
* And more...

The core repo behaves slightly different than the dedicated build environment described in [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials). If you want to use locally built packages to build your images, use the following commands. Otherwise, please refer to [CBL-MarinerTutorials](https://github.com/microsoft/CBL-MarinerTutorials).

### **5. Build an Image**

#### Setup

```bash
# Clone the CBL-Mariner repo
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner

# Sync to the latest stable build
git checkout 2.0-stable
cd ./toolkit
sudo make clean QUICK_REBUILD=y
```

#### Build a toolchain if using an unstable branch

```bash
# OPTIONAL:
#   Build the latest toolchain **if you are NOT working on a stable branch**
git checkout main
sudo make toolchain QUICK_REBUILD_TOOLCHAIN=y

# Copy it somewhere safe if you want (you can also just leave QUICK_REBUILD_TOOLCHAIN=y set)
cp ../build/toolchain/toolchain_built_rpms_all.tar.gz ~/mariner_toolchain.tar.gz
```

#### Building Packages for the Image

The tools will automatically rebuild any packages that are needed to create the image; there is no need to manually build packages, but if desired, this can be done via [Build Packages](./build_packages.md#rebuild-minimal-required-packages-for-an-image).

#### Dev Loop

```bash
# Modify your image config
touch ./imageconfigs/core-efi.json

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

# Build the desired image config. It will end up in ../out/images/<name>
#   -j$(nproc)              Number of parallel threads to use in the Makefile. The pkg scheduler will
#                               make its own choices
#   QUICK_REBUILD_PACKAGES=y Try to avoid building packages as much as possible (ie download what we can
#                               from the package repo)
#   CONFIG_FILE="./imageconfigs/core-efi.json"  Build this image config
#   REBUILD_TOOLS=y         Rebuild the go tools if needed
#   $pkg_filer              Optionally only package specific .spec files (see above)
#   $toolchain              Where to get our toolchain (see above)
sudo make image -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE="./imageconfigs/core-efi.json" REBUILD_TOOLS=y $toolchain
# --- or ---
sudo make iso -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE="./imageconfigs/full.json" REBUILD_TOOLS=y $toolchain
# Repeat as needed
```
