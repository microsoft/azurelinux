#!/bin/bash

set -e
set -x

CONFIG_FILE=$1
OUTPUT_DISK_RAW_FILE=$2
OUTPUT_ROOTFS_RAW_FILE=$3

function build_full_image () {
    local configFile=$1
    local outputDiskRawFile=$2
    local outputRootfsRawFile=$3

    sudo rm -rf ./build/imagegen/baremetal
    sudo rm -rf ./out/images/baremetal

    pushd toolkit
    sudo make image \
        -j$(nproc) \
        REBUILD_TOOLS=y \
        REBUILD_TOOLCHAIN=n \
        REBUILD_PACKAGES=n \
        CONFIG_FILE=$configFile

    mkdir -p $(dirname "$outputDiskRawFile")
    cp ../build/imagegen/baremetal/imager_output/disk0.raw $outputDiskRawFile

    # ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw
    sourceRootfsRawFile=$(find ../out/images/baremetal -name "mariner-rootfs-raw*.raw")
    cp $sourceRootfsRawFile $outputRootfsRawFile

    popd
}

build_full_image $CONFIG_FILE $OUTPUT_DISK_RAW_FILE $OUTPUT_ROOTFS_RAW_FILE