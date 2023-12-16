#!/bin/bash

set -x
set -e

script_dir=$(dirname "$BASH_SOURCE")
source $script_dir/logger.sh

BUILD_DIR=$1
BUILD_CLEAN=$2

NONE_VALUE="none"

if [[ -z $BUILD_DIR ]]; then
    echo "Specify output build directory."
    exit 1
fi

#------------------------------------------------------------------------------
function create_full_image() {
    mic_poc_log "---------------- create_full_image [enter] --------"
    local fullImageConfigFile=$1
    local outFullImageRawDisk=$2
    local outRootfsRawFile=$3
    local outRootfsRawGzFile=$4
    local outRootfsSquashFile=$5
    local outRootfsSquashGzFile=$6

    # outputs:
    #
    #  full disk:
    #   ./out/images/disk0.raw
    #   ./build/imagegen/disk0.raw
    #   ./build/imagegen/baremetal/imager_output/disk0.raw
    #   ./out/images/baremetal/core-2.0.20231206.1707.vhdx
    #
    #  rootfs partition:
    #
    #   ./out/images/baremetal/mariner-rootfs-ext4-2.0.20231206.1707.ext4.gz
    #   ./out/images/baremetal/mariner-rootfs-ext4-2.0.20231206.1707.ext4
    #
    #   ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw
    #   ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw.gz
    #
    #   ./out/images/baremetal/mariner-rootfs-squashfs-2.0.20231206.1707.squashfs
    #   ./out/images/baremetal/mariner-rootfs-squashfs-2.0.20231206.1707.squashfs.gz    
    #
    ./toolkit/mic-iso-gen/build-rootfs.sh \
        $fullImageConfigFile \
        $outFullImageRawDisk \
        $outRootfsRawFile \
        $outRootfsRawGzFile \
        $outRootfsSquashFile \
        $outRootfsSquashGzFile

    mic_poc_log "---------------- create_full_image [exit] --------"
}

#------------------------------------------------------------------------------
function extract_artifacts_from_full_image() {
    mic_poc_log "---------------- extract_artifacts_from_full_image [enter] --------"
    local outFullImageRawDisk=$1
    local tmpDir=$2
    local outDir=$3

    # outputs:
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-rootfs
    #   $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file
    #

    ./toolkit/mic-iso-gen/extract-artifacts-from-rootfs.sh \
        $outFullImageRawDisk \
        /mnt/full-disk-rootfs-mount \
        $tmpDir \
        $outDir

    sudo chown george:george -R $EXTRACT_ARTIFACTS_OUT_DIR
    mic_poc_log "---------------- extract_artifacts_from_full_image [exit] --------"
}

#------------------------------------------------------------------------------
function create_iso_with_reduced_rootfs_initrd () {
    mic_poc_log "---------------- create_iso_with_reduced_rootfs_initrd [enter] --------"
    local extractedRootFS=$1
    local initrdDir=$2
    local initrdTmpDir=$3
    local initrdOutDir=$4
    local fullImageRawDisk=$5
    local rootfsRawFile=$6
    local outDir=$7

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
        $rootfsRawFile \
        $outDir
    mic_poc_log "---------------- create_iso_with_reduced_rootfs_initrd [exit] --------"
}

#------------------------------------------------------------------------------
create_iso_with_rootfs_initrd () {
    mic_poc_log "---------------- create_iso_with_rootfs_initrd [enter] --------"
    local initrdFile=$1
    local vmlinuzFile=$2
    local grubCfg=$3
    local initrdDir=$4
    local sourceFullImageRawDisk=$5
    local sourceRootfsFile=$6
    local targetRootfsFile=$7
    local outDir=$8

    # outputs:
    #   /home/george/temp/iso-output/iso/baremetal-20231129-200226.iso
    #
    ./toolkit/mic-iso-gen/create-iso-from-initrd-vmlinuz.sh \
        $initrdFile \
        $vmlinuzFile \
        $grubCfg \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
        $sourceFullImageRawDisk \
        $sourceRootfsFile \
        $targetRootfsFile \
        $outDir

    mic_poc_log "---------------- create_iso_with_rootfs_initrd [exit] --------"
}

create_iso_with_rootfs_initrd_dir () {
    mic_poc_log "---------------- create_iso_with_rootfs_initrd_dir [enter] --------"
    local initrdOriDir=$1
    local initrdModDir=$2
    local initrdTmpDir=$3
    local initrdOutDir=$4
    local vmlinuzFile=$5
    local grubCfg=$6
    local fullImageRawDisk=$7
    local rootfsRawFile=$8
    local outDir=$9

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
        $grubCfg \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
        ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
        $fullImageRawDisk \
        $rootfsRawFile \
        $outDir

    mic_poc_log "---------------- create_iso_with_rootfs_initrd_dir [exit] --------"
}

#
# Create the following:
# wrapper.img [raw file system]
#  |- LiveOS
#      |- rootfs.img [raw file system]
#
function create_uncompressed_wrapper_un_compressed_rootfs() {
    local rootfsRawFile=$1
    local fedoraLiveIsoDir=$2
    local fedoraLiveIsoWrapperRawFile=$3
    local wrapperSizeInMBs=$4

    mkdir -p $fedoraLiveIsoDir
    sudo rm -f $fedoraLiveIsoWrapperRawFile

    dd if=/dev/zero \
       of=$fedoraLiveIsoWrapperRawFile \
       bs=1M \
       count=$wrapperSizeInMBs

    mkfs.ext4 $fedoraLiveIsoWrapperRawFile

    newDevice=$(sudo losetup -f -P --show $fedoraLiveIsoWrapperRawFile)
    sudo mkdir -p /mnt/wrapper
    sudo mount $newDevice /mnt/wrapper
    sudo mkdir -p /mnt/wrapper/LiveOS
    sudo cp $rootfsRawFile /mnt/wrapper/LiveOS/rootfs.img
    echo "---------------------------------------------------------------------"
    echo "New Device: $newDevice"
    set +e
    lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID,PARTLABEL,PARTUUID
    set -e
    echo "---------------------------------------------------------------------"
    sudo umount /mnt/wrapper
    sleep 5s
    # The following command fails with a device still in use error.
    # sudo rm -r /mnt/wrapper
    sudo losetup -d $newDevice
}

#
# Create the following:
# squashfs.img [squash file system]
#  |- LiveOS
#      |- rootfs.img [raw file system]
#
function create_squashfs_wrapper_uncompressed_rootfs () {
    local rootfsRawFile=$1
    local fedoraLiveIsoStagingDir=$2
    local fedoraLiveIsoWrapperSquashfsFile=$3
    local liveOSDir=$fedoraLiveIsoStagingDir/LiveOS

    mkdir -p $liveOSDir
    cp $rootfsRawFile \
        $liveOSDir
    sudo rm -f $fedoraLiveIsoWrapperSquashfsFile
    mksquashfs \
        $fedoraLiveIsoStagingDir \
        $fedoraLiveIsoWrapperSquashfsFile
}

#
# Create the following
# squashfs.iso [iso file system - label=WRAPISO]
#  |- LiveOS
#      |- squashfs.img
#
function create_iso_wrapper_squashfs_rootfs() {
    local rootfsSquashfsFile=$1
    local fedoraLiveIsoStagingDir=$2
    local isoLabel=$3
    local fedoraLiveIsoWrapperIsofsFile=$5

    local liveOSDir=$fedoraLiveIsoStagingDir/LiveOS

    mkdir -p $liveOSDir
    cp $rootfsSquashfsFile \
        $liveOSDir
    sudo rm -f $fedoraLiveIsoWrapperIsofsFile
    sudo xorriso \
        -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid $isoLabel \
        -graft-points $liveOSDir \
        -output $fedoraLiveIsoWrapperIsofsFile
}


function prepare_root_partition() {
    rootfsRawFile=$1
    modifiedRootfsRawFile=$2

    cp $rootfsRawFile \
        $modifiedRootfsRawFile

    sudo mkdir -p /mnt/hack
    loDevice=$(sudo losetup -f -P --show $modifiedRootfsRawFile)
    sudo mount $loDevice /mnt/hack
    sudo ls -la /mnt/hack/etc/fstab
    sudo rm /mnt/hack/etc/fstab
    sudo umount /mnt/hack
    sudo rm -f /mnt/hack
    sudo losetup -d loDevice
}

#-- main ----------------------------------------------------------------------
FULL_IMAGE_CONFIG_FILE=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json

mkdir -p $BUILD_DIR

BUILD_WORKING_DIR=$BUILD_DIR/intermediates
mkdir -p $BUILD_WORKING_DIR

BUILD_OUT_DIR=$BUILD_DIR/out
mkdir -p $BUILD_OUT_DIR

#------------------------------------------------------------------------------
cd ~/git/CBL-Mariner/

FULL_IMAGE_RAW_DISK=$BUILD_WORKING_DIR/raw-disk-output/disk0.raw

ROOTFS_RAW_FILE=$BUILD_WORKING_DIR/raw-disk-output/rootfs.img
ROOTFS_RAW_GZ_FILE=$BUILD_WORKING_DIR/raw-disk-output/rootfs.img.tgz

MODIFIED_ROOTFS_DIR=$BUILD_WORKING_DIR/raw-disk-output-modified
MODIFIED_ROOTFS_RAW_FILE=$MODIFIED_ROOTFS_DIR/rootfs.img
MODIFIED_ROOTFS_RAW_FILE_COMPRESSED=${MODIFIED_ROOTFS_RAW_FILE}.tar.gz

UNWRAPPED_ROOTFS_SQUASH_FILE=$BUILD_WORKING_DIR/raw-disk-output/squashfs.img
ROOTFS_SQUASH_GZ_FILE=$BUILD_WORKING_DIR/raw-disk-output/squashfs.img.tgz

EXTRACT_ARTIFACTS_TMP_DIR=$BUILD_WORKING_DIR/extract-artifacts-from-rootfs-tmp-dir
EXTRACT_ARTIFACTS_OUT_DIR=$BUILD_WORKING_DIR/extract-artifacts-from-rootfs-out-dir

FEDORA_LIVE_ISO_DIR_0=$BUILD_WORKING_DIR/fedora-working-dir-0
FEDORA_LIVE_ISO_WRAPPER_RAW_FILE_0=$FEDORA_LIVE_ISO_DIR_0/wrapper.img
FEDORA_LIVE_ISO_WRAPPER_SIZE_IN_MBS_0=2176
FEDORA_LIVE_ISO_WRAPPER_SIZE_IN_MBS_0_COMPRESSED=256

FEDORA_LIVE_ISO_DIR_1=$BUILD_WORKING_DIR/fedora-working-dir-1
FEDORA_LIVE_ISO_STAGING_DIR_1=$FEDORA_LIVE_ISO_DIR_1/input
FEDORA_LIVE_ISO_SQUASHFS_FILE_1=$FEDORA_LIVE_ISO_DIR_1/squashfs.img

FEDORA_LIVE_ISO_DIR_2=$BUILD_WORKING_DIR/fedora-working-dir-2
FEDORA_LIVE_ISO_STAGING_DIR_2=$FEDORA_LIVE_ISO_DIR_2/input
FEDORA_LIVE_ISO_WRAPPER_ISO_FILE=$FEDORA_LIVE_ISO_DIR_2/squashfs.iso

if [[ ! -z $BUILD_CLEAN ]]; then
    # create_full_image  \
    #     $FULL_IMAGE_CONFIG_FILE \
    #     $FULL_IMAGE_RAW_DISK \
    #     $ROOTFS_RAW_FILE \
    #     $ROOTFS_RAW_GZ_FILE \
    #     $UNWRAPPED_ROOTFS_SQUASH_FILE \
    #     $ROOTFS_SQUASH_GZ_FILE

    # extract_artifacts_from_full_image \
    #     $FULL_IMAGE_RAW_DISK \
    #     $EXTRACT_ARTIFACTS_TMP_DIR \
    #     $EXTRACT_ARTIFACTS_OUT_DIR

    # remove fstab...
    #
    # mkdir -p $MODIFIED_ROOTFS_DIR
    # prepare_root_partition \
    #     $ROOTFS_RAW_FILE \
    #     $MODIFIED_ROOTFS_RAW_FILE

    # -------------------------------------------
    # Cfg1
    #
    # Create the following:
    #
    # wrapper.img [raw file system - uncompressed]
    #  |- LiveOS
    #      |- rootfs.img [raw file system - uncompressed]
    #
    # create_uncompressed_wrapper_un_compressed_rootfs \
    #     $MODIFIED_ROOTFS_RAW_FILE \
    #     $FEDORA_LIVE_ISO_DIR_0 \
    #     $FEDORA_LIVE_ISO_WRAPPER_RAW_FILE_0 \
    #     $FEDORA_LIVE_ISO_WRAPPER_SIZE_IN_MBS_0
 
    # -------------------------------------------
    # Cfg2
    #
    # Create the following:
    #
    # squashfs.img [squash file system]
    #  |- LiveOS
    #      |- rootfs.img [raw file system]
    #
    # create_squashfs_wrapper_uncompressed_rootfs \
    #     $MODIFIED_ROOTFS_RAW_FILE \
    #     $FEDORA_LIVE_ISO_STAGING_DIR_1 \
    #     $FEDORA_LIVE_ISO_SQUASHFS_FILE_1

    # -------------------------------------------
    # Cfg3, Cfg4
    #
    # Create the following:
    #
    # wrapper.img [squash file system]
    #  |- LiveOS
    #      |- rootfs.img [raw file system - compressed]
    #
    sudo rm -f $MODIFIED_ROOTFS_RAW_FILE_COMPRESSED

    # compress
    rawFilePath=$(dirname $MODIFIED_ROOTFS_RAW_FILE)
    rawFileName=$(basename $MODIFIED_ROOTFS_RAW_FILE)
    pushd $rawFilePath
    tar -czvf $MODIFIED_ROOTFS_RAW_FILE_COMPRESSED $rawFileName
    popd

    create_uncompressed_wrapper_un_compressed_rootfs \
        $MODIFIED_ROOTFS_RAW_FILE_COMPRESSED \
        $FEDORA_LIVE_ISO_DIR_0 \
        $FEDORA_LIVE_ISO_WRAPPER_RAW_FILE_0 \
        $FEDORA_LIVE_ISO_WRAPPER_SIZE_IN_MBS_0_COMPRESSED

    # -------------------------------------------
    # CfgX
    #
    # Create the following
    # squashfs.iso [iso file system - label=WRAPISO]
    #  |- LiveOS
    #      |- squashfs.img
    #
    # create_iso_wrapper_squashfs_rootfs \
    #     $FEDORA_LIVE_ISO_SQUASHFS_FILE_1 \
    #     $FEDORA_LIVE_ISO_STAGING_DIR_2 \
    #     "WRAPISO" \
    #     $FEDORA_LIVE_ISO_WRAPPER_ISO_FILE
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
#   $NONE_VALUE \
#   $BUILD_OUT_DIR

#
# Option 2.a. rootfs initrd + NO modifications
#
# create_iso_with_rootfs_initrd \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file/initrd.img-5.15.138.1-1.cm2 \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
#     "~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg" \
#     $CREATE_INITRD_OUT_DIR \
#     $FULL_IMAGE_RAW_DISK\
#     $NONE_VALUE \
#     $NONE_VALUE \
#     $BUILD_OUT_DIR

#
# Option 2.b. rootfs initrd + NO modifications + grub configured for dracut live scenario
#
# $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd-file/initrd.img-5.15.138.1-1.cm2
#

# SOURCE_ROOTFS_FILE=$FEDORA_LIVE_ISO_WRAPPER_ISO_FILE
# TARGET_ROOTFS_FILE="/LiveOS/squashfs.iso"

# This configuration fails because dracut expects this raw images to contain
# a subfolder named LiveOS/ and in that LiveOS/ folder, there should be
# a raw file name `rootfs.img`.
# SOURCE_ROOTFS_FILE=$ROOTFS_RAW_FILE
# TARGET_ROOTFS_FILE="/artifacts/rootfs.img"

# -----------------------------------------------
# Cfg1
#
# SOURCE_ROOTFS_FILE=$FEDORA_LIVE_ISO_WRAPPER_RAW_FILE_0
# TARGET_ROOTFS_FILE="/artifacts/wrapper.img"

# -----------------------------------------------
# Cfg2
#
# SOURCE_ROOTFS_FILE=$FEDORA_LIVE_ISO_SQUASHFS_FILE_1
# TARGET_ROOTFS_FILE="/artifacts/squashfs.img"

# -----------------------------------------------
# Cfg3, Cfg4
#
SOURCE_ROOTFS_FILE=$FEDORA_LIVE_ISO_WRAPPER_RAW_FILE_0
TARGET_ROOTFS_FILE="/artifacts/wrapper.img"

create_iso_with_rootfs_initrd \
    ~/temp/initrd.img \
    $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
    "/home/george/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub-dracut-live-cd.cfg" \
    $CREATE_INITRD_OUT_DIR \
    $NONE_VALUE \
    $SOURCE_ROOTFS_FILE \
    $TARGET_ROOTFS_FILE \
    $BUILD_OUT_DIR

#
# Option 2.c. rootfs initrd + Modifications
#
# create_iso_with_rootfs_initrd_dir \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-initrd \
#     $BUILD_WORKING_DIR/modified-initrd-dir \
#     $BUILD_WORKING_DIR/tmp-initrd-dir \
#     $BUILD_WORKING_DIR/out-initrd-dir \
#     $EXTRACT_ARTIFACTS_OUT_DIR/extracted-vmlinuz-file/vmlinuz-5.15.138.1-1.cm2 \
#     "~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg" \
#     $NONE_VALUE \
#     $NONE_VALUE \
#     $BUILD_OUT_DIR
