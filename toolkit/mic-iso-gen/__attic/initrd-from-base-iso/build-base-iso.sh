#!/bin/bash

set -x
set -e

CONFIG_FILE=$1
INITRD_CONFIG_FILE=$2
OUTPUT_FILE=$3

function build_iso_image () {
    local configFile=$1
    local initrdConfigFile=$2
    local outputFile=$3

    sudo rm -rf ./build/imagegen/baremetal-initrd
    sudo rm -rf ./build/imagegen/baremetal-iso
    sudo rm -rf ./build/imagegen/iso-initrd
    sudo rm -rf ./build/imagegen/iso_initrd

    sudo rm -rf ./out/images/baremetal-initrd
    sudo rm -rf ./out/images/baremetal-iso
    sudo rm -rf ./out/images/iso-initrd
    sudo rm -rf ./out/images/iso_initrd

    pushd toolkit

    mkdir -p ./tmp
    cp $initrdConfigFile ./tmp/iso_initrd.json

    sudo make iso \
        -j$(nproc) \
        REBUILD_TOOLS=y \
        REBUILD_PACKAGES=n \
        CONFIG_FILE=$configFile \
        initrd_config_json=./tmp/iso_initrd.json

    sudo rm -r ./tmp

    mkdir -p $(dirname "$outputFile")

    generatedIsoFile=$(find ../out/images/baremetal-iso -name "baremetal-iso-*.iso")
    cp $generatedIsoFile $outputFile

    popd
}

# -----------------------------------------------------------------------------
# main()
#

build_iso_image \
  $CONFIG_FILE \
  $INITRD_CONFIG_FILE \
  $OUTPUT_FILE
