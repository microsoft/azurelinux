#!/bin/bash
set -euxo pipefail
TARGET_DIR="/var/tmp/azl-vm-images"

# remove the target dir if it exists
if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"
fi

sudo rm -rf ./base/out/images/*
sudo rm -rf ./base/build/work/vm-base/*
# # Build the VM image using KIWI
# sudo kiwi --loglevel 10 \
#     --kiwi-file vm-base.kiwi \
#     system build  \
#     --description ./base/images/vm-base \
#     --target-dir "$TARGET_DIR" \
#     --add-repo="http://4.249.86.161/kojifiles/repos/azl4-bootstrap-rpms-build-tag/latest/x86_64/,rpm-md,azl,1"

# Build vm-base image using azldev
azldev image build vm-base --local-repo ./base/out --remote-repo http://4.249.86.161/kojifiles/repos/azl4-bootstrap-rpms-build-tag/latest/x86_64/

# Convert VHDX to VPC fixed size
qemu-img convert -f vhdx -O vpc -o subformat=fixed,force_size \
    ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhdx \
    ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhd

# Copy the resulting VHD to Windows Downloads folder
cp ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhd /mnt/c/Users/liunan/Downloads/azl4-vm-base.x86_64-0.1.vhd