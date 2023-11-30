#!/bin/bash

set -e
set -x

IMAGE_DEFINITION={$1:./imageconfigs/baremetal.json}
OUTPUT_DIR=$2

# -----------------------------------------------------------------------------
# [placeholder] build/customize rootfs
#


# -----------------------------------------------------------------------------
# Build rootfs
#

sudo rm -rf ./build/imagegen/baremetal
sudo rm -rf ./out/images/baremetal

pushd toolkit
sudo make image \
    -j$(nproc) \
    REBUILD_TOOLS=y \
    REBUILD_TOOLCHAIN=n \
    REBUILD_PACKAGES=n \
    CONFIG_FILE=./imageconfigs/baremetal.json

#   REPO_LIST="$RPM_REPO_LIST"   \

mkdir -p $OUTPUT_DIR
cp ../build/imagegen/baremetal/imager_output/disk0.raw $OUTPUT_DIR/

popd

