#!/bin/bash

set -x
set -e

FULL_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json
ISO_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal-iso.json

#------------------------------------------------------------------------------

BUILD_DIR=~/temp/iso-build
sudo rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

BUILD_WORKING_DIR=$BUILD_DIR/intermediates
mkdir -p $BUILD_WORKING_DIR

BUILD_OUT_DIR=$BUILD_DIR/out
mkdir -p $BUILD_OUT_DIR

#------------------------------------------------------------------------------
cd ~/git/CBL-Mariner/

FULL_IMAGE_RAW_DISK=$BUILD_WORKING_DIR/raw-disk-output/disk0.raw

# outputs:
#   disk0.raw
#
./toolkit/mic-iso-gen/build-rootfs.sh \
    $FULL_IMAGE_CONFIG_FILE \
    $FULL_IMAGE_RAW_DISK

# outputs:
#   baremetal.iso
#
ISO_IMAGE_RAW_DISK=$BUILD_WORKING_DIR/iso-image-output/baremetal.iso

./toolkit/mic-iso-gen/__attic/initrd-from-base-iso/build-base-iso.sh \
    $ISO_IMAGE_CONFIG_FILE \
    $ISO_IMAGE_RAW_DISK




#----
OUTPUT_DIR=~/temp/iso-output
sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

INTERMEDIATE_ARTIFACTS_DIR=$OUTPUT_DIR/iso-intermediates
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

cd ~/git/CBL-Mariner/

# ~/temp/iso-intermediates/iso-initrd.img
# ~/temp/iso-intermediates/vmlinuz
# ~/temp/iso-intermediates/baremetal.iso
./toolkit/mic-iso-gen/0-build-baremetal-iso.sh gmileka/assemble-iso $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso-2.sh \
    $INTERMEDIATE_ARTIFACTS_DIR/baremetal.iso \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    $INTERMEDIATE_ARTIFACTS_DIR/disk0.raw \
    $OUTPUT_DIR