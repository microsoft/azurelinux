#!/bin/bash
set -euxo pipefail
TARGET_DIR="/var/tmp/azl-vm-images"

# remove the target dir if it exists
if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"
fi

# Build the VM image using KIWI
sudo kiwi --loglevel 10 \
    --kiwi-file vm-base.kiwi \
    system build  \
    --description ./base/images/vm-base \
    --target-dir "$TARGET_DIR" \
    --add-repo="http://4.249.86.161/kojifiles/repos/azl4-bootstrap-rpms-build-tag/latest/x86_64/,rpm-md,azl,1"