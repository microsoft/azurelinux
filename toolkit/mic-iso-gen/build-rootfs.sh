#!/bin/bash

set -e
set -x

CONFIG_FILE=$1
OUTPUT_DISK_RAW_FILE=$2
OUTPUT_ROOTFS_RAW_FILE=$3
OUTPUT_ROOTFS_RAW_GZ_FILE=$4
OUTPUT_ROOTFS_SQUASH_FILE=$5
OUTPUT_ROOTFS_SQUASH_GZ_FILE=$6

function build_full_image () {
    local configFile=$1
    local outputDiskRawFile=$2
    local outputRootfsRawFile=$3
    local outputRootfsRawGzFile=$4
    local outputRootfsSquashFile=$5
    local outputRootfsSquashGzFile=$6

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

    # ./out/images/baremetal/mariner-rootfs-raw-2.0.20231208.1322.raw.gz
    sourceRootfsRawGzFile=$(find ../out/images/baremetal -name "mariner-rootfs-raw*.raw.gz")
    cp $sourceRootfsRawGzFile $outputRootfsRawGzFile

    # ./out/images/baremetal/mariner-rootfs-squashfs-2.0.20231208.1322.squashfs
    sourceRootfsSquashFile=$(find ../out/images/baremetal -name "mariner-rootfs-squash*.squashfs")
    cp $sourceRootfsSquashFile $outputRootfsSquashFile

    # ./out/images/baremetal/mariner-rootfs-squashfs-2.0.20231208.1322.squashfs.gz
    sourceRootfsSquashGzFile=$(find ../out/images/baremetal -name "mariner-rootfs-squash*.squashfs.gz")
    cp $sourceRootfsSquashGzFile $outputRootfsSquashGzFile

    popd
}

build_full_image \
    $CONFIG_FILE \
    $OUTPUT_DISK_RAW_FILE \
    $OUTPUT_ROOTFS_RAW_FILE \
    $OUTPUT_ROOTFS_RAW_GZ_FILE \
    $OUTPUT_ROOTFS_SQUASH_FILE \
    $OUTPUT_ROOTFS_SQUASH_GZ_FILE