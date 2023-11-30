#!/bin/bash

set -x
set -e

FULL_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json

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
#   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd
#   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file
#   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-rootfs
#   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file
#
EXTRACT_ARTIFACTS_TMP_DIR=$BUILD_WORKING_DIR/extract-rootfs-artifacts-from-rootfs-tmp-dir
EXTRACT_ARTIFACTS_OUT_DIR=$BUILD_WORKING_DIR/extract-rootfs-artifacts-from-rootfs-out-dir

./toolkit/mic-iso-gen/extract-artifacts-from-rootfs.sh \
    $FULL_IMAGE_RAW_DISK \
    /mnt/full-disk-rootfs-mount \
    $EXTRACT_ARTIFACTS_TMP_DIR \
    $EXTRACT_ARTIFACTS_OUT_DIR

# Modify the rootfs folder to become an initrd folder.
#
# outputs:
#   $BUILD_WORKING_DIR/initrd-dir
#
INITRD_DIR=$BUILD_WORKING_DIR/initrd-dir

./toolkit/mic-iso-gen/convert-rootfs-folder-to-initrd-folder.sh \
    $EXTRACT_ARTIFACTS_OUT_DIR/extracted-rootfs \
    $INITRD_DIR

# outputs:
#   /home/george/temp/generated-initrd-dir/initrd.img
#
CREATE_INITRD_TMP_DIR=$BUILD_WORKING_DIR/create-initrd-from-folder-tmp-dir
CREATE_INITRD_OUT_DIR=$BUILD_WORKING_DIR/create-initrd-from-folder-out-dir

./toolkit/mic-iso-gen/create-initrd-image-from-folder.sh \
    $INITRD_DIR \
    $CREATE_INITRD_TMP_DIR \
    $CREATE_INITRD_OUT_DIR

# outputs:
#   /home/george/temp/iso-output/iso/baremetal-20231129-200226.iso
#
./toolkit/mic-iso-gen/create-iso-from-initrd-vmlinuz.sh \
    $CREATE_INITRD_OUT_DIR/initrd.img \
    $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.137.1-1.cm2 \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    $FULL_IMAGE_RAW_DISK \
    $BUILD_OUT_DIR
