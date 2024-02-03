# Mariner Image Customizer ISO Support

## Overview

Given a full disk image, the Mariner Image Customizer (MIC) can generate a
LiveOS ISO image when the `--output-image-format` is set to `iso`.

The LiveOS ISO image is a bootable image that boots into the rootfs of the
input full disk image. This eliminates the requirement to install that image
to persistent storage before booting it.

All customizations can still be made to the input full disk image rootfs as
usual using MIC, and will naturally carry over into the LiveOS ISO. This
includes customizations for kernel modules, dracut, and other early boot-time
actions.

While converting the input full disk image into a LiveOS ISO involves copying
almost all the artifacts unchanged - some artifacts are changed as follows:
- `grub.cfg` is replaced with a stock one that serves the LiveOS boot flow.
  This can be important to account for if you rely on certain grub
  configurations in your current grub.cfg.
- `/etc/fstab` is dropped from the rootfs as it typically conflicts with the
  overlay setup required by the LiveOS.
- `initrd.img` is regenerated to serve the LiveOS boot flow. This should have
  no impact as long as the included rootfs is where the original `initrd.img`
  was generated using `dracut`. The use of such rootfs guarantees that the same
  dracut configuration that got used before will be re-used again when we are
  re-generating the `initrd.img` and hence the original behavior is retained.

The current implementation for the LiveOS ISO does not support the following:
- persistent storage.
  - The machine loses all its state on reboot or shutdown.
- dm-verity.
  - The ISO image cannot run dm-verity for the LiveOS partitions.
- disk layout.
  - There is always one disk generated when an `iso` output format is
    specified.

## ISO Specific Customizations

- The user can specify one or more files to be copied to the iso media.
- The user can add kernel parameters.

For a full list of capabilities, see Mariner Image Customizer's iso configuration 
section: [Config.ISO](./configuration.md#iso-type).

## cloud-init Support

In some user scenarios, it desired to embed the cloud-init data files into the
iso media. The easiest way is to include the data files on the media, and then
the cloud-init `ds` kernel parameter to where the files are.

The files can be placed directly within the iso file system or they can be
placed within the LiveOS root file system.

Placing those files directly on the iso file system will allow a more efficient
replacement flow in the future (i.e. when it is desired to only replace the
cloud-init data files).

#### Example 1

If cloud-init data is to be placed directly within the iso file system:

```yaml
Iso:
  AdditionalFiles:
    cloud-init-data/user-data: /cloud-init-data/user-data
    cloud-init-data/network-config: /cloud-init-data/network-config
    cloud-init-data/meta-data: /cloud-init-data/meta-data
  KernelCommandLine: ds=nocloud;s=file://run/initramfs/live/cloud-init-data
SystemConfig:
  Users:
  - Name: test
    Password: testpassword
    PrimaryGroup: sudo
```

#### Example 2

If cloud-init data is to be placed within the LiveOS root file system:

```yaml
Iso:
  KernelCommandLine:
    ExtraCommandLine: ds=nocloud;s=file://cloud-init-data
  SystemConfig:
    Users:
    - Name: test
      Password: testpassword
      PrimaryGroup: sudo
    AdditionalFiles:
      cloud-init-data/user-data: /cloud-init-data/user-data
      cloud-init-data/network-config: /cloud-init-data/network-config
      cloud-init-data/meta-data: /cloud-init-data/meta-data
```