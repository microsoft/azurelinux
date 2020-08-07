Composing Images
===
## Prev: [Package Building](3_package_building.md), Next: [Misc](5_misc.md)
## Configuration Files
Image generation is based entirely on configuration files. These configuration files define the image format, the layout and size of disks, the boot configurations, the package composition, and other details.

To learn more about the image configuration file format, see [formats/imageconfig.md](../formats/imageconfig.md)

## Default Image Configs
The toolkit includes several image configurations in `./imageconfigs/` which can be used as a starting point.

The most straightforward, and default, config is `./imageconfigs/core-efi.json`. This config will create `core.vhdx` which can be booted on `Gen-2 Hyper-V VMs`. A legacy version is also available which creates a `core.vhd` image for `Gen-1` VMs.

### Stage 1: Validation
The `imageconfigvalidator` tool is used to validate configuration files before they are used anywhere in the build.

### Stage 2: Imager
The first stage of image generation is to create the desired filesystem locally. This can be either in the form of a raw disk image (`*.raw`) or a directory tree. If it is a raw disk image the `*.raw` file is mounted as a `loopback` device.

The `imager` tool uses a chroot environment (see [Chroot Worker](1_initial_prep.md#chroot_worker)) to install all the required packages into the filesystem.

### Stage 3: Roast
The `roast` tool bakes the raw disk image into its final format (`*.ext4`, `*.vhd`, `*.vhdx`, etc.).

## ISO Builds
ISOs are slightly different than simple images. They require a stand-alone installer which is responsible for taking the configured image, and applying it to a target computer.

### Initrd
The core of the ISO installer is an `initrd` image, (aka `ramdisk`,`initramfs`) which can be booted from memory. Two versions are available, a `calamares` based GUI installer and a terminal based installer (see [Building ISOs](../building/building.md#isos)).

The `initrd` image is based on a static configuration included with the toolkit. Building the `initrd` image requires a recursive call to `Make`. Since a number of components in the build system have a dependency on the `CONFIG_FILE` variable (see [Config Tracking](1_initial_prep.md#config_tracking)) rebuilding the `initrd` will invalidate a number of components and cause a brief rebuild.

Once the `initrd` image is available it is combined with the requested images in the config file using the `isomaker` tool.

## Prev: [Package Building](3_package_building.md), Next: [Misc](5_misc.md)
