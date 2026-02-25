#!/bin/bash
set -euxo pipefail

sudo rm -rf ./base/out/images/*
sudo rm -rf ./base/build/work/vm-base/*
# Find the absolute path of the directory containing this script
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPTS_DIR/common.sh"

# Build vm-base image using azldev
azldev image build vm-base --local-repo ./base/out --remote-repo "$REMOTE_KOJI_REPO_URL"

# Convert VHDX to VPC fixed size
qemu-img convert -f vhdx -O vpc -o subformat=fixed,force_size \
    ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhdx \
    ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhd
