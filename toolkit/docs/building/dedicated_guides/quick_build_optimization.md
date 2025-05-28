# Quick Build Optimization Guide

## Is this guide for you?

| If you want to... | Go to... |
|:------------------|:---------|
| Learn step-by-step how to use quick build flags | [Quick Start Tutorial](#quick-start-tutorial) |
| See examples of how to apply optimization flags | [How-To: Common Optimization Tasks](#how-to-common-optimization-tasks) |
| Understand the available optimization flags | [Reference: Optimization Flags](#reference-optimization-flags) |
| Learn why quick rebuilds matter | [Background: Why Use Build Optimizations?](#background-why-use-build-optimizations) |
| Troubleshoot optimization issues | [Troubleshooting Delta Builds](#troubleshooting-delta-builds) |

## Overview

This guide explains how to use Azure Linux's build optimization flags to significantly reduce build times. These optimizations are particularly useful for development workflows where rebuilding packages or images frequently is necessary.

## Quick Start Tutorial

Let's walk through a practical example of using build optimizations to accelerate your development workflow.

### Building Your First Package With Optimizations

This tutorial will show the difference between building with and without optimization flags:

1. Start with a clean environment:

```bash
# Clean the build environment
cd /path/to/azurelinux/toolkit
sudo make clean
```

2. Build a package WITHOUT optimization flags:

```bash
# Build without optimizations - this will take longer
time sudo make build-packages -j$(nproc) SRPM_PACK_LIST="bash" PACKAGE_REBUILD_LIST="bash"
```

3. Clean up and build the SAME package WITH optimization flags:

```bash
# Clean just the package artifacts
sudo make clean-build-packages

# Build with optimizations - notice the speed difference!
time sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="bash" PACKAGE_REBUILD_LIST="bash"
```

4. Now try an image build with optimizations:

```bash
# Build an optimized image
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json QUICK_REBUILD=y
```

The optimized build should be noticeably faster because it:
- Pre-fetches dependencies from the package repository
- Limits cascading rebuilds of dependent packages
- Uses delta builds to avoid rebuilding unchanged components

## How-To: Common Optimization Tasks

### How to Optimize Toolchain Builds

When working with toolchain components, use `QUICK_REBUILD_TOOLCHAIN=y` to prevent unnecessary rebuilds:

```bash
# Rebuild the toolchain with optimal performance settings
sudo make toolchain QUICK_REBUILD_TOOLCHAIN=y
```

### How to Optimize Package Builds

For package development:

```bash
# Build all packages with optimal performance settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE=""

# For targeted package building
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="openssh"
```

### How to Optimize Image Builds

For building images:

```bash
# Build a VHD image with optimal performance settings
sudo make image CONFIG_FILE=./imageconfigs/core-legacy.json QUICK_REBUILD=y

# Build an ISO with optimal performance settings
sudo make iso CONFIG_FILE=./imageconfigs/full.json QUICK_REBUILD=y
```

### How to Avoid Unnecessary Toolchain Rebuilds

The toolchain stage is the most time-consuming part of the build process. To avoid rebuilding it unnecessarily:

1. Always use stable tags when possible (`3.0-stable`)
2. Save your toolchain after building it:
   ```bash
   cp ../build/toolchain/toolchain_built_rpms_all.tar.gz ~/mariner_toolchain.tar.gz
   ```
3. Reuse your saved toolchain:
   ```bash
   sudo make toolchain TOOLCHAIN_ARCHIVE=~/mariner_toolchain.tar.gz
   ```
4. Use `DELTA_BUILD=y` to enable delta builds (already included in `QUICK_REBUILD_TOOLCHAIN=y`)

## Reference: Optimization Flags

Azure Linux provides several optimization flags to speed up builds across different stages:

### Quick Build Flag Reference Table

| Flag | Default | Purpose | Use When |
|:-----|:--------|:--------|:---------|
| `QUICK_REBUILD=y` | n | Master flag that sets both `QUICK_REBUILD_TOOLCHAIN=y` and `QUICK_REBUILD_PACKAGES=y` | You want to optimize the entire build pipeline |
| `QUICK_REBUILD_TOOLCHAIN=y` | n | Optimizes toolchain builds | Working specifically on toolchain components |
| `QUICK_REBUILD_PACKAGES=y` | n | Optimizes package builds | Focusing on package development |
| `DELTA_BUILD=y` | n | Enables delta builds to avoid rebuilding unchanged components | You want to avoid rebuilding unchanged packages |
| `DELTA_FETCH=y` | n | Downloads pre-built packages that match local specs | You want to use pre-built packages when possible |
| `PRECACHE=y` | n | Pre-loads the cache from upstream sources | You want to pre-fetch dependencies |
| `MAX_CASCADING_REBUILDS=1` | (unset) | Limits unnecessary rebuilds of dependent packages | You want to limit rebuilding dependencies |

### Flag Interactions and Dependencies

#### QUICK_REBUILD=y

This is the master optimization flag that enables optimizations across all build stages. When set, it automatically enables:

- `QUICK_REBUILD_TOOLCHAIN=y` - Optimizes toolchain builds
- `QUICK_REBUILD_PACKAGES=y` - Optimizes package builds

Using `QUICK_REBUILD=y` is recommended for most development workflows as it provides optimal settings for the entire build pipeline.

#### QUICK_REBUILD_TOOLCHAIN=y

This flag optimizes just the toolchain build stage by enabling:

- `REBUILD_TOOLCHAIN=y` - Builds the toolchain from source
- `DELTA_BUILD=y` - Enables delta builds
- `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL=y` - Attempts to download existing components where possible
- `REBUILD_TOOLS=y` - Rebuilds the go tools

#### QUICK_REBUILD_PACKAGES=y

This flag optimizes package builds by enabling:

- `DELTA_BUILD=y` - Enables delta builds
- `DELTA_FETCH=y` - Downloads pre-built packages when possible
- `PRECACHE=y` - Pre-loads the cache from upstream sources
- `MAX_CASCADING_REBUILDS=1` - Limits unnecessary rebuilds of dependent packages
- `REBUILD_TOOLS=y` - Rebuilds the go tools

## Background: Why Use Build Optimizations?

### Why Delta Builds Matter

Building Azure Linux from scratch can take hours, especially the toolchain stage. Delta builds dramatically reduce build times by:

1. Avoiding rebuilding packages that haven't changed
2. Limiting the cascading effect when dependencies change
3. Reusing pre-built components from published repositories

### What Happens During a Toolchain Rebuild?

When you rebuild the toolchain (`REBUILD_TOOLCHAIN=y`), the system:

1. Creates a bootstrap toolchain using your host system and Docker
2. Uses that bootstrap toolchain to build the final toolchain
3. Uses the final toolchain to build all other packages

This process can take several hours, but optimization flags can significantly reduce this time by leveraging existing published components and avoiding unnecessary rebuilds.

## Troubleshooting Delta Builds

### Common Issues with Delta Builds

1. **Missing dependencies**: If you get errors about missing packages, try:
   ```bash
   sudo make build-packages DELTA_FETCH=y PRECACHE=y
   ```

2. **Inconsistent package versions**: If you encounter version mismatches, clean and rebuild:
   ```bash
   sudo make clean
   sudo make build-packages QUICK_REBUILD_PACKAGES=y
   ```

3. **Toolchain errors**: If the toolchain build fails, try using a known good toolchain:
   ```bash
   sudo make toolchain TOOLCHAIN_ARCHIVE=/path/to/known-good-toolchain.tar.gz
   ```

4. **Cascading rebuilds**: If too many packages are being rebuilt, adjust:
   ```bash
   sudo make build-packages MAX_CASCADING_REBUILDS=0 QUICK_REBUILD_PACKAGES=y
   ```

## Performance Impact

These optimization flags can significantly reduce build times by:

- Using existing published components where possible
- Enabling delta builds to avoid unnecessary rebuilds
- Pre-fetching and caching dependencies
- Limiting cascading rebuilds when a dependency changes

For large projects, these optimizations can reduce build times from hours to minutes, making development iterations much faster.