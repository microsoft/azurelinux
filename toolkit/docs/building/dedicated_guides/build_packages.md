# Building Packages with Azure Linux

## Overview

This document describes how to efficiently build packages in the Azure Linux repository. For most users looking to add or customize packages, we recommend starting with the [Azure Linux Tutorials](https://github.com/microsoft/AzureLinux-Tutorials) repository.

This guide focuses on building packages in the core repo with optimal performance, particularly using the quick build optimization flags.

## Prerequisites

Before proceeding, make sure you have:

1. Installed the [necessary prerequisites](../prerequisites.md)
2. Cloned the repository and checked out the appropriate branch
3. Have basic familiarity with Azure Linux's build system

## Building Packages with Optimizations

### Building All Packages

To build all packages with optimal performance settings:

```bash
# Build ALL packages with optimal settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE=""

# For even faster builds, use QUICK_REBUILD=y
sudo make build-packages -j$(nproc) QUICK_REBUILD=y CONFIG_FILE=""
```

The `QUICK_REBUILD_PACKAGES=y` flag enables:
- Delta builds with `DELTA_BUILD=y`
- Pre-built package downloads with `DELTA_FETCH=y`
- Caching with `PRECACHE=y`
- Limited cascading rebuilds with `MAX_CASCADING_REBUILDS=1`
- Go tool rebuilds with `REBUILD_TOOLS=y`

### Building Packages for a Specific Image

To build only the packages needed for a specific image:

```bash
# Build packages for a specific image with optimal settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE=./imageconfigs/core-legacy.json
```

This approach is more efficient as it will only build packages required by the specified image configuration.

### Building Specific Packages

To build one or more specific packages:

```bash
# Build specific packages with optimal settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="openssh nano"
```

The `SRPM_PACK_LIST` parameter tells the build system to only process the specified packages.

### Forcing Package Rebuilds

To force rebuilding a package even if it's already built:

```bash
# Force rebuild specific packages with optimal settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y PACKAGE_REBUILD_LIST="openssh"
```

### Optimizing Build Workflow

For an efficient development workflow when iterating on package changes:

```bash
# Clean existing build artifacts
sudo make clean-build-packages

# Build with optimizations and skip worker chroot rebuild
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="at openssh" REFRESH_WORKER_CHROOT=n
```

The `REFRESH_WORKER_CHROOT=n` option avoids rebuilding the worker chroot between builds, saving significant time.

## Handling Package Dependencies

Azure Linux will automatically resolve and build package dependencies. However, you can optimize this process:

### Ignoring Problematic Packages

If a dependency package is problematic:

```bash
# Work on a package while ignoring a problematic dependency
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y PACKAGE_BUILD_LIST="nano" PACKAGE_IGNORE_LIST="ncurses"
```

### Limiting Cascading Rebuilds

To prevent a single package change from triggering excessive rebuilds:

```bash
# Limit cascading rebuilds to one level
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="openssh" MAX_CASCADING_REBUILDS=1
```

## Working with Source Files

When modifying package sources, you need to update the signature files:

```bash
# Automatically update signature files
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="openssh" SRPM_FILE_SIGNATURE_HANDLING=update
```

## Further Information

For more detailed information on:
- Build parameters and flags: See the [main building documentation](../building.md)
- Advanced optimization techniques: See the [Quick Build Optimization Guide](./quick_build_optimization.md)
- Working with RPM spec files: See the [Azure Linux Tutorials](https://github.com/microsoft/AzureLinux-Tutorials) repository