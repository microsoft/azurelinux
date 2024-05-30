#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
uname_r="6.6.29.1-4.azl3"

# symlink /boot/efi to ../efi
cp -a /boot/efi/. /efi
rm -rf /boot/efi
ln -s ../efi /boot/efi

# copy grub to a backup
cp /efi/EFI/BOOT/grubx64.efi /efi/EFI/BOOT/backupgrubx64.efi

# empty /etc/fstab file
echo > /etc/fstab

# copy sd-boot EFI binary over the grub EFI binary
cp /lib/systemd/boot/efi/systemd-bootx64.efi /efi/EFI/BOOT/grubx64.efi

# copy UKI into the ESP
mkdir -p /efi/EFI/Linux
cp /lib/modules/$uname_r/vmlinuz-uki.efi /efi/EFI/Linux/vmlinuz-uki-$uname_r.efi

# create sd-boot loader config file with timeout value
mkdir -p /efi/loader
echo "timeout 3" > /efi/loader/loader.conf
