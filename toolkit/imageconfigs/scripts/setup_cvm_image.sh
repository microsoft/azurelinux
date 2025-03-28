#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# set up ESP under /efi
# symlink /boot/efi to ../efi
cp -a /boot/efi/. /efi
rm -rf /boot/efi
ln -s ../efi /boot/efi

# empty /etc/fstab file
echo > /etc/fstab

