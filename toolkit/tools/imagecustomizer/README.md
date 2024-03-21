# Azure Linux Image Customizer

The Azure Linux Image Customizer is a tool that can take an existing generic Azure Linux
image and modify it to be suited for particular scenario.

MIC uses [chroot](https://en.wikipedia.org/wiki/Chroot) (and loopback block devices) to
customize the image.
This is the same technology used to build the Azure Linux images (along with most other
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

1. Download an Azure Linux core image.

2. Create a customization config file.

   For example:

    ```yaml
    os:
      packagesInstall:
      - dnf
    ```

   For documentation on the supported configuration options, see:
   [Azure Linux Image Customizer configuration](./docs/configuration.md)

3. Install prerequisites: `qemu-img`, `rpm`, `dd`, `lsblk`, `losetup`, `sfdisk`,
   `udevadm`, `flock`, `blkid`, `openssl`, `sed`, `createrepo`, `mksquashfs`,
   `genisoimage`, `mkfs`, `mkfs.ext4`, `mkfs.vfat`, `mkfs.xfs`, `fsck`, `e2fsck`,
   `xfs_repair`, `zstd`.

   - For Ubuntu 22.04 images, run:

     ```bash
     sudo apt -y install qemu-utils rpm coreutils util-linux mount fdisk udev openssl sed createrepo-c squashfs-tools genisoimage e2fsprogs dosfstools xfsprogs zstd
     ```

4. Run the Azure Linux Image Customizer tool.

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
   [Azure Linux Image Customizer command line](./docs/cli.md)

5. Use the customized image.

   The customized image is placed in the file that you specified with the
   `--output-image-file` parameter. You can now use this image as you see fit.
   (For example, boot it in a Hyper-V VM.)
