# Building Images with Azure Linux

## Overview

This document describes how to efficiently build images in the Azure Linux repository. For most users looking to customize images, we recommend starting with the [Azure Linux Tutorials](https://github.com/microsoft/AzureLinux-Tutorials) repository.

This guide focuses on building images from the core repo with optimal performance, particularly using the quick build optimization flags.

## Prerequisites

Before proceeding, make sure you have:

1. Installed the [necessary prerequisites](../prerequisites.md)
2. Cloned the repository and checked out the appropriate branch
3. Have basic familiarity with Azure Linux's build system

## Building Images with Optimizations

### VHDX and VHD Images

```bash
# To build an Azure Linux VHD Image with optimal performance settings
sudo make image CONFIG_FILE=./imageconfigs/core-legacy.json QUICK_REBUILD=y

# To build an Azure Linux VHDX Image with optimal performance settings
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json QUICK_REBUILD=y
```

The `QUICK_REBUILD=y` flag enables optimal build settings including:
- Downloading pre-built components when possible
- Delta builds to avoid unnecessary rebuilds
- Toolchain optimizations

### Container Images

```bash
# To build a core Azure Linux Container with optimal settings
sudo make image CONFIG_FILE=./imageconfigs/core-container.json QUICK_REBUILD=y

# To build a distroless container with optimal settings
sudo make image CONFIG_FILE=./imageconfigs/distroless-minimal.json QUICK_REBUILD=y
```

### ISO Images

ISOs are bootable images that install Azure Linux to either a physical or virtual machine:

```bash
# To build a full ISO with optimal performance settings
sudo make iso CONFIG_FILE=./imageconfigs/full.json QUICK_REBUILD=y
```

To create an unattended ISO installer (no interactive UI):

```bash
# Build an unattended installer ISO with optimal settings
sudo make iso CONFIG_FILE=./imageconfigs/core-legacy-unattended-hyperv.json QUICK_REBUILD=y UNATTENDED_INSTALLER=y
```

## Using Pre-Built Packages

To speed up image building even further by skipping local package builds completely:

```bash
# Build using only packages from packages.microsoft.com
sudo make image CONFIG_FILE=./imageconfigs/core-efi.json REBUILD_PACKAGES=n REBUILD_TOOLS=y
```

This approach is especially useful when you're only interested in the image configuration and not in modifying any packages.

## Working with Custom Configurations

If you want to create custom image configurations:

1. Start by exploring existing configurations in the `toolkit/imageconfigs/` directory
2. Make a copy of an existing configuration as a starting point
3. Modify package lists in `toolkit/imageconfigs/packagelists/` as needed
4. Build your custom image using the optimization flags:

```bash
# Build a custom image with optimal settings
sudo make image CONFIG_FILE=./path/to/my-custom-config.json QUICK_REBUILD=y
```

## Testing Images

After building the image, you can test it in a virtual environment:

1. For VHDs/VHDXs: Use Hyper-V or other virtualization tools to create a VM using the image
2. For containers: Use Docker to import and run the container image
3. For ISOs: Boot from the ISO in a VM to test the installation process

## Further Information

For more detailed information on:
- Build parameters and flags: See the [main building documentation](../building.md)
- Advanced optimization techniques: See the [Quick Build Optimization Guide](./quick_build_optimization.md)
- Working with package lists: See the [Azure Linux Tutorials](https://github.com/microsoft/AzureLinux-Tutorials) repository