#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
# convert to using DPS
# create a directory /efi inside the image, and replace the
# /boot/efi directory with a symlink to /efi
ln -s /boot/efi /efi

# TODO: change the root partition type GUID to 4f68bce3-e8cd-4db1-96e7-fbcaf984b709

# don't put anything in the /etc/fstab file
echo >> /etc/fstab

# replace /efi/EFI/BOOT/grubx64.efi with the sd-boot efi binary
# /usr/lib/systemd/boot/efi/systemd-bootx64.efi
mv /usr/lib/systemd/boot/efi/systemd-bootx64.efi /boot/efi/EFI/BOOT/grubx64.efi

