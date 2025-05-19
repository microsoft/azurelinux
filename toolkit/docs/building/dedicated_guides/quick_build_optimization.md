# Quick Build Optimization Guide

## Overview

This guide explains how to use Azure Linux's build optimization flags to significantly reduce build times. These optimizations are particularly useful for development workflows where rebuilding packages or images frequently is necessary.

## Available Optimization Flags

Azure Linux provides several optimization flags to speed up builds across different stages:

### QUICK_REBUILD=y

This is the master optimization flag that enables optimizations across all build stages. When set, it automatically enables:

- `QUICK_REBUILD_TOOLCHAIN=y` - Optimizes toolchain builds
- `QUICK_REBUILD_PACKAGES=y` - Optimizes package builds

Using `QUICK_REBUILD=y` is recommended for most development workflows as it provides optimal settings for the entire build pipeline. It's equivalent to setting both specialized flags mentioned above.

### QUICK_REBUILD_TOOLCHAIN=y

This flag optimizes just the toolchain build stage by enabling:

- `REBUILD_TOOLCHAIN=y` - Builds the toolchain from source
- `DELTA_BUILD=y` - Enables delta builds
- `ALLOW_TOOLCHAIN_DOWNLOAD_FAIL=y` - Attempts to download existing components where possible
- `REBUILD_TOOLS=y` - Rebuilds the go tools

Use this flag when working specifically on toolchain components or when you need to rebuild the toolchain but want it done as efficiently as possible.

### QUICK_REBUILD_PACKAGES=y

This flag optimizes package builds by enabling:

- `DELTA_BUILD=y` - Enables delta builds
- `DELTA_FETCH=y` - Downloads pre-built packages when possible
- `PRECACHE=y` - Pre-loads the cache from upstream sources
- `MAX_CASCADING_REBUILDS=1` - Limits unnecessary rebuilds of dependent packages
- `REBUILD_TOOLS=y` - Rebuilds the go tools

Use this flag when focusing on package development to reduce build times significantly.

## Common Usage Examples

### Optimized Toolchain Build

```bash
# Rebuild the toolchain with optimal performance settings
sudo make toolchain QUICK_REBUILD_TOOLCHAIN=y
```

### Optimized Package Build

```bash
# Build packages with optimal performance settings
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y CONFIG_FILE="./imageconfigs/core-efi.json"

# For targeted package building
sudo make build-packages -j$(nproc) QUICK_REBUILD_PACKAGES=y SRPM_PACK_LIST="openssh"
```

### Optimized Image Build

```bash
# Build an image with optimal performance settings
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json QUICK_REBUILD=y

# Build an ISO with optimal performance settings
sudo make iso CONFIG_FILE=./imageconfigs/full.json QUICK_REBUILD=y
```

## Performance Impact

These optimization flags can significantly reduce build times by:

- Using existing published components where possible
- Enabling delta builds to avoid unnecessary rebuilds
- Pre-fetching and caching dependencies
- Limiting cascading rebuilds when a dependency changes

For large projects, these optimizations can reduce build times from hours to minutes, making development iterations much faster.