#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

EFIDIR="BOOT"
KERNEL_VERSION=""

get_kernel_version() {
    kernel_modules_dir="/usr/lib/modules"
    KERNEL_VERSION="$(ls $kernel_modules_dir)"
}

# symlink /boot/efi to ../efi
cp -a /boot/efi/. /efi
rm -rf /boot/efi
ln -s ../efi /boot/efi

# switching to systemd-boot
# copy sd-boot EFI binary over the grub EFI binary
cp /lib/systemd/boot/efi/systemd-bootx64.efi /efi/EFI/$EFIDIR/grubx64.efi

# empty /etc/fstab file
echo > /etc/fstab

# copy UKI into the ESP
mkdir -p /efi/EFI/Linux
get_kernel_version
echo "Kernel version = $KERNEL_VERSION"
cp /lib/modules/$KERNEL_VERSION/vmlinuz-uki.efi /efi/EFI/Linux/vmlinuz-uki-$KERNEL_VERSION.efi
