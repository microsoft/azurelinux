# Azure Linux Image Customizer

The Azure Linux Image Customizer is a tool that can take an existing generic Azure Linux
image and modify it to be suited for particular scenario.

The Image Customizer uses [chroot](https://en.wikipedia.org/wiki/Chroot) (and loopback
block devices) to customize the image.
This is the same technology used to build the Azure Linux images, along with most other
Linux distros.
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

- Not all Linux tools play nicely when run under chroot.
  So, some customizations aren't possible using the Image Customizer.
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
   `genisoimage`, `parted`, `mkfs`, `mkfs.ext4`, `mkfs.vfat`, `mkfs.xfs`, `fsck`,
   `e2fsck`, `xfs_repair`, `resize2fs`, `zstd`, `veritysetup`.

   - For Ubuntu 22.04 images, run:

     ```bash
     sudo apt -y install qemu-utils rpm coreutils util-linux mount fdisk udev openssl \
        sed createrepo-c squashfs-tools genisoimage parted e2fsprogs dosfstools \
        xfsprogs zstd cryptsetup-bin
     ```

   - For Mariner 2.0, run:

     ```bash
     sudo tdnf install -y qemu-img rpm coreutils util-linux systemd openssl \
        sed createrepo_c squashfs-tools cdrkit parted e2fsprogs dosfstools \
        xfsprogs zstd veritysetup
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

## Things to avoid

The Image Customizer tool provides the option to run custom scripts as part of the
customization process.
These can be used to handle scenarios not covered by the Image Customizer tool.
However, these scripts are only run within a chroot environment, which while it is kind
of similar to containers, is very explicitly not a sandbox environment.
So, such scripts have the ability to modify the host build system.

In particular, you should be very wary of commands that have the ability to change the
runtime kernel settings.
And even commands that only read runtime kernel settings are probably doing the wrong
thing, since the host build system's kernel is likely entirely unrelated to the
customized OS's kernel.

Examples of commands to avoid:

- `ip`
- `iptables`
- `iptables-save`
- `ip6tables-save`
- `modprobe`
- `sysctl`

Instead, you should you make use of config files that set the runtime kernel settings
during OS boot.

Example config directories to use instead:

- `/etc/sysctl.d` (`systemd-sysctl.service`)
