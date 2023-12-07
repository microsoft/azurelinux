#!/bin/bash

set -x
set -e

FULL_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json
ISO_INITRD_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal-initrd.json
# ISO_INITRD_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal-initrd-minimal.json
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

# FULL_IMAGE_RAW_DISK=$BUILD_WORKING_DIR/raw-disk-output/disk0.raw
# FULL_IMAGE_RAW_DISK=~/temp/control-plane.zst
# FULL_IMAGE_RAW_DISK=~/temp/control-plane-20231201.9.zst
FULL_IMAGE_RAW_DISK=~/temp/worker-20231201.9.zst

# outputs:
#   disk0.raw
#
# ./toolkit/mic-iso-gen/build-rootfs.sh \
#     $FULL_IMAGE_CONFIG_FILE \
#     $FULL_IMAGE_RAW_DISK

# outputs:
#   $BUILD_WORKING_DIR/iso-image-output/baremetal.iso
#
ISO_IMAGE=$BUILD_WORKING_DIR/iso-image-output/baremetal.iso

./toolkit/mic-iso-gen/__attic/initrd-from-base-iso/build-base-iso.sh \
    $ISO_IMAGE_CONFIG_FILE \
    $ISO_INITRD_CONFIG_FILE \
    $ISO_IMAGE

# outputs:
#    $EXTRACT_ARTIFACTS_OUT_DIR
#
EXTRACT_ARTIFACTS_OUT_DIR=$BUILD_WORKING_DIR/extract-artifacts-from-iso-out-dir

./toolkit/mic-iso-gen/__attic/initrd-from-base-iso/extract-artifacts-from-iso.sh \
    $ISO_IMAGE \
    /mnt/iso-mount \
    $EXTRACT_ARTIFACTS_OUT_DIR

# outputs:
# $OUTPUT_DIR
#
./toolkit/mic-iso-gen/__attic/initrd-from-base-iso/create-iso-from-initrd-and-vmlinuz.sh \
    $EXTRACT_ARTIFACTS_OUT_DIR/initrd.img \
    $EXTRACT_ARTIFACTS_OUT_DIR/vmlinuz \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    $FULL_IMAGE_RAW_DISK \
    $BUILD_OUT_DIR