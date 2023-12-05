#!/bin/bash

set -x
set -e

BUILD_DIR=$1
BUILD_CLEAN=$2

if [[ -z $BUILD_DIR ]]; then
    echo "Specify output build directory."
    exit 1
fi

#------------------------------------------------------------------------------
function create_and_expand_full_image() {
    local fullImageConfigFile=$1
    local fullImageRawDisk=$2
    local tmpDir=$3
    local outDir=$4

    # outputs:
    #   disk0.raw
    #
    ./toolkit/mic-iso-gen/build-rootfs.sh \
        $fullImageConfigFile \
        $fullImageRawDisk

    # outputs:
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-rootfs
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file
    #

    ./toolkit/mic-iso-gen/extract-artifacts-from-rootfs.sh \
        $fullImageRawDisk \
        /mnt/full-disk-rootfs-mount \
        $tmpDir \
        $outDir

    sudo chown george:george -R $EXTRACT_ARTIFACTS_OUT_DIR
}

#------------------------------------------------------------------------------
function create_iso_with_reduced_rootfs_initrd () {
    local extractedRootFS=$1
    local initrdDir=$2
    local initrdTmpDir=$3
    local initrdOutDir=$4
    local fullImageRawDisk=$5
    local outDir=$6

    # Modify the rootfs folder to become an initrd folder.
    #
    # outputs:
    #   $BUILD_WORKING_DIR/initrd-dir
    #
    ./toolkit/mic-iso-gen/convert-rootfs-folder-to-initrd-folder.sh \
        $extractedRootFS/extracted-rootfs \
        $initrdDir

    # outputs:
    #   /home/george/temp/generated-initrd-dir/initrd.img
    #
    ./toolkit/mic-iso-gen/create-initrd-image-from-folder.sh \
        $initrdDir \
        $initrdTmpDir \
        $initrdOutDir

    # outputs:
    #   /home/george/temp/iso-output/iso/baremetal-20231129-200226.iso
    #
    ./toolkit/mic-iso-gen/create-iso-from-initrd-vmlinuz.sh \
        $initrdOutDir/initrd.img \
        $extractedRootFS/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
        $fullImageRawDisk \
        $outDir
}

#------------------------------------------------------------------------------
create_iso_with_rootfs_initrd () {
    local initrdFile=$1
    local vmlinuzFile=$2
    local fullImageRawDisk=$3
    local outDir=$4

    # outputs:
    #   /home/george/temp/iso-output/iso/baremetal-20231129-200226.iso
    #
    ./toolkit/mic-iso-gen/create-iso-from-initrd-vmlinuz.sh \
        $initrdFile \
        $vmlinuzFile \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
        $fullImageRawDisk \
        $outDir
}

create_iso_with_rootfs_initrd_dir () {
    local initrdOriDir=$1
    local initrdModDir=$2
    local initrdTmpDir=$3
    local initrdOutDir=$4
    local vmlinuzFile=$5
    local fullImageRawDisk=$6
    local outDir=$7

    ./toolkit/mic-iso-gen/convert-rootfs-initrd-folder-to-initrd-folder.sh \
        $initrdOriDir \
        $initrdModDir

    ./toolkit/mic-iso-gen/create-initrd-image-from-folder.sh \
        $initrdModDir \
        $initrdTmpDir \
        $initrdOutDir

    ./toolkit/mic-iso-gen/create-iso-from-initrd-vmlinuz.sh \
        $initrdOutDir/initrd.img \
        $vmlinuzFile \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
        $fullImageRawDisk \
        $outDir
}

#-- main ----------------------------------------------------------------------
FULL_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json

if [[ ! -z $BUILD_CLEAN ]]; then
  sudo rm -rf $BUILD_DIR
fi
mkdir -p $BUILD_DIR

BUILD_WORKING_DIR=$BUILD_DIR/intermediates
mkdir -p $BUILD_WORKING_DIR

BUILD_OUT_DIR=$BUILD_DIR/out
mkdir -p $BUILD_OUT_DIR

#------------------------------------------------------------------------------
cd ~/git/CBL-Mariner/

FULL_IMAGE_RAW_DISK=$BUILD_WORKING_DIR/raw-disk-output/disk0.raw
EXTRACT_ARTIFACTS_TMP_DIR=$BUILD_WORKING_DIR/extract-artifacts-from-rootfs-tmp-dir
EXTRACT_ARTIFACTS_OUT_DIR=$BUILD_WORKING_DIR/extract-artifacts-from-rootfs-out-dir

if [[ ! -z $BUILD_CLEAN ]]; then
    create_and_expand_full_image \
        $FULL_IMAGE_CONFIG_FILE \
        $FULL_IMAGE_RAW_DISK \
        $EXTRACT_ARTIFACTS_TMP_DIR \
        $EXTRACT_ARTIFACTS_OUT_DIR
fi

INITRD_DIR=$BUILD_WORKING_DIR/initrd-dir
CREATE_INITRD_TMP_DIR=$BUILD_WORKING_DIR/create-initrd-from-folder-tmp-dir
CREATE_INITRD_OUT_DIR=$BUILD_WORKING_DIR/create-initrd-from-folder-out-dir

#
# Option 1. rootfs reduce to initrd.
#
# create_iso_with_reduced_rootfs_initrd \
#   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-rootfs \
#   $INITRD_DIR \
#   $CREATE_INITRD_TMP_DIR \
#   $CREATE_INITRD_OUT_DIR
#   $FULL_IMAGE_RAW_DISK \
#   $BUILD_OUT_DIR

#
# Option 2.a. rootfs initrd + no modifications
#
# create_iso_with_rootfs_initrd \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file/initrd.img-5.15.138.1-1.cm2 \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
#     $CREATE_INITRD_OUT_DIR \
#     $FULL_IMAGE_RAW_DISK\
#     $BUILD_OUT_DIR

#
# Option 2.b. rootfs initrd + modifications
#
create_iso_with_rootfs_initrd_dir \
    $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd \
    $BUILD_WORKING_DIR/modified-initrd-dir \
    $BUILD_WORKING_DIR/tmp-initrd-dir \
    $BUILD_WORKING_DIR/out-initrd-dir \
    $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
    $FULL_IMAGE_RAW_DISK\
    $BUILD_OUT_DIR
