# Mariner Image Customizer

The Mariner Image Customizer (MIC) is a tool that can take an existing generic Mariner
image and modify it to be suited for particular scenario.

MIC uses [chroot](https://en.wikipedia.org/wiki/Chroot) (and loopback block devices) to
customize the image.
This is the same technology used to build the Mariner images (along with most other
Linux distros).
This is in contrast to some other image customization tools, like Packer, which
customize the image by booting it inside a VM.

There are a number of advantages and disadvantages to the `chroot` approach to
customizing images.

Advantages:

- Lower overhead, since you don't need to boot up and shutdown the OS.
- More precision when making changes, since you won't see any side effects that come
  from the OS running.
- The image has fewer requirements (e.g. ssh doesn't need to be installed).

Disadvantages:

- Not all Linux tools play nicely when run under chroot. (Though most of the most
  common tools do play nicely since they are used to build Linux images under chroot.)
  So, some customizations aren't possible to do using MIC.
  (For example, initializing a Kubernetes cluster node.)

## Getting started

1. Download a Mariner core image.

2. Create a customization config file.

   For example:

    ```yaml
    SystemConfig:
      PackagesInstall:
      - dnf
    ```

   For documentation on the supported configuration options, see:
   [Mariner Image Customizer configuration](./docs/configuration.md)

3. Run the Mariner Image Customizer tool.

   For example:

    ```bash
    sudo ./imagecustomizer \
      --build-dir ./build \
      --image-file <base-image.vhdx> \
      --output-image-file ./out/image.vhdx \
      --output-image-format vhdx \
      --config-file <config-file.yaml>
    ```

   Where:

   - `<base-image.vhdx>`: The image file downloaded in Step 1.
   - `<config-file.yaml>`: The configuration file created in Step 2.

   For a description of all the command line options, see:
   [Mariner Image Customizer command line](./docs/cli.md)

4. Use the customized image.

   The customized image is placed in the file that you specified with the
   `--output-image-file` parameter. You can now use this image as you see fit.
   (For example, boot it in a Hyper-V VM.)

## Generating ISO Images

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

The current implementation for the LiveOS ISO does not support persistent
storage. This means that the machine loses all its state on reboot or
shutdown.