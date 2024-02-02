# Mariner Image Customizer ISO Support

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