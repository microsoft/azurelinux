#!/bin/bash

set -e
set -x

CONFIG_FILE=$1
OUTPUT_FILE=$2

function build_full_image () {
    local configFile=$1
    local outputFile=$2

    sudo rm -rf ./build/imagegen/baremetal
    sudo rm -rf ./out/images/baremetal

    pushd toolkit
    sudo make image \
        -j$(nproc) \
        REBUILD_TOOLS=y \
        REBUILD_TOOLCHAIN=n \
        REBUILD_PACKAGES=n \
        CONFIG_FILE=$configFile

    mkdir -p $(dirname "$outputFile")
    cp ../build/imagegen/baremetal/imager_output/disk0.raw $outputFile

    popd
}

build_full_image $CONFIG_FILE $OUTPUT_FILE