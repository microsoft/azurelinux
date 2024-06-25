#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

EFIDIR="BOOT"
KERNEL_VERSION=""

# Image generation is done in a chroot environment, so running `uname -r`
# will return the version of the host running kernel. This function works
# under the assumption that exactly one kernel is installed in the end image.
get_kernel_version() {
    kernel_modules_dir="/usr/lib/modules"
    KERNEL_VERSION="$(ls $kernel_modules_dir)"
}

# symlink /boot/efi to ../efi
cp -a /boot/efi/. /efi
rm -rf /boot/efi
ln -s ../efi /boot/efi

# The shim has its default boot-loader filename built in as grubx64.efi.
# To switch to systemd-boot, we overwrite that file location with the
# sd-boot EFI binary as a workaround.
cp /lib/systemd/boot/efi/systemd-bootx64.efi /efi/EFI/$EFIDIR/grubx64.efi

# empty /etc/fstab file
echo > /etc/fstab

# copy UKI into the ESP
mkdir -p /efi/EFI/Linux
get_kernel_version
echo "Kernel version = $KERNEL_VERSION"
cp /lib/modules/$KERNEL_VERSION/vmlinuz-uki.efi /efi/EFI/Linux/vmlinuz-uki-$KERNEL_VERSION.efi
