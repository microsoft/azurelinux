#!/bin/bash

echo "-------- create-iso-from-initrd-vmlinuz.sh [enter] --------"

set -x
set -e

INPUT_INTRD=$1
INPUT_VMLINUZ=$2
INPUT_GRUB_CFG=$3
INPUT_STARTUP_SCRIPT=$4
INPUT_STARTUP_SCRIPT_CONFIGURATION=$5
INPUT_FULL_IMAGE=$6
INPUT_ROOTFS_FILE=$7
OUTPUT_ROOTFS_FILE=$8
OUTPUT_ISO_DIR=$9

function CreateEfibootImage () {
    SRC_GRUB_CFG=$1
    INTERMEDIATE_OUTPUT=$2
    DST_DIR=$3

    mkdir -p $INTERMEDIATE_OUTPUT
    mkdir -p $DST_DIR

    rm -f $INTERMEDIATE_OUTPUT/bootx64.efi

    # create bootx64.efi with the our custom grub
    grub-mkstandalone \
        --format=x86_64-efi \
        --locales="" \
        --fonts="" \
        --output=$INTERMEDIATE_OUTPUT/bootx64.efi \
        boot/grub/grub.cfg=$SRC_GRUB_CFG

    #    --verbose \

    # Generate the fs to hold the bootx64.efi - i.e. out/efiboot.img
    rm -f $INTERMEDIATE_OUTPUT/efiboot.img

    dd if=/dev/zero of=$DST_DIR/efiboot.img bs=1M count=3
    mkfs.vfat $DST_DIR/efiboot.img

    LC_CTYPE=C mmd -i $DST_DIR/efiboot.img efi efi/boot
    LC_CTYPE=C mcopy -i $DST_DIR/efiboot.img $INTERMEDIATE_OUTPUT/bootx64.efi ::efi/boot/

    echo "Created -------- " $DST_DIR/efiboot.img
}

function CreateBiosImage () {
    SRC_GRUB_CFG=$1
    INTERMEDIATE_OUTPUT=$2
    DST_DIR=$3

    mkdir -p $INTERMEDIATE_OUTPUT
    mkdir -p $DST_DIR

    rm -f $INTERMEDIATE_OUTPUT/core.img

    grub-mkstandalone \
        --format=i386-pc \
        --install-modules="linux normal iso9660 biosdisk memdisk search tar ls all_video" \
        --modules="linux normal iso9660 biosdisk search" \
        --locales="" \
        --fonts="" \
        --output=$INTERMEDIATE_OUTPUT/core.img \
        boot/grub/grub.cfg=$SRC_GRUB_CFG

    # Generate the fs to hold the bios.img - i.e. out/core.img
    if [[ -f $INTERMEDIATE_OUTPUT/bios.img ]]; then
        rm $INTERMEDIATE_OUTPUT/bios.img
    fi

    cat /usr/lib/grub/i386-pc/cdboot.img $INTERMEDIATE_OUTPUT/core.img > $DST_DIR/bios.img

    echo "Created -------- " $DST_DIR/bios.img
}

# -----------------------------------------------------------------------------
# prepare iso artifacts
#
#
# This script generates the following layout:
#
#     ./intermediate-iso-artifacts
#         ./bootx64.efi
#         ./core.img
#     ./staged-iso-layout
#         ./boot/
#               ./vmlinuz
#               ./initrd.img
#               ./grub
#                   ./efiboot.img
#                   ./bios.img
#         ./rootfs
#               ./rootfs.img
#
# Originally: ./prepare-iso-artifacts.sh
#
sudo apt-get install -y mtools dosfstools grub-pc-bin grub-pc xorriso

INTERMEDIATE_OUTPUT_DIR=$OUTPUT_ISO_DIR/iso-intermediate-artifacts
mkdir -p $INTERMEDIATE_OUTPUT_DIR

STAGED_ISO_ARTIFACTS_DIR=$OUTPUT_ISO_DIR/iso-staged-layout
mkdir -p $STAGED_ISO_ARTIFACTS_DIR

FINAL_ISO_DIR=$OUTPUT_ISO_DIR/iso
mkdir -p $FINAL_ISO_DIR

OUTPUT_ISO_IMAGE_NAME=$FINAL_ISO_DIR/baremetal-$(printf "%(%Y%m%d-%H%M%S)T").iso
OUTPUT_ISO_LABEL="baremetal-iso"

cd ~/git/CBL-Mariner/toolkit/mic-iso-gen

mkdir -p $STAGED_ISO_ARTIFACTS_DIR/boot
cp $INPUT_INTRD $STAGED_ISO_ARTIFACTS_DIR/boot/initrd.img
cp $INPUT_VMLINUZ $STAGED_ISO_ARTIFACTS_DIR/boot/vmlinuz
if [[ ! -z $INPUT_ROOTFS_FILE ]] && [[ $INPUT_ROOTFS_FILE != "none" ]]; then
    TARGET_ROOTFS_FILE=${STAGED_ISO_ARTIFACTS_DIR}${OUTPUT_ROOTFS_FILE}
    mkdir -p $(dirname $TARGET_ROOTFS_FILE)
    cp $INPUT_ROOTFS_FILE $TARGET_ROOTFS_FILE
fi

mkdir -p $STAGED_ISO_ARTIFACTS_DIR/artifacts
cp $INPUT_STARTUP_SCRIPT $STAGED_ISO_ARTIFACTS_DIR/artifacts/
cp $INPUT_STARTUP_SCRIPT_CONFIGURATION $STAGED_ISO_ARTIFACTS_DIR/artifacts/
if [[ ! -z $INPUT_FULL_IMAGE ]] && [[ ! $INPUT_FULL_IMAGE == "none" ]]; then
    cp $INPUT_FULL_IMAGE $STAGED_ISO_ARTIFACTS_DIR/artifacts/
fi

CreateEfibootImage \
    $INPUT_GRUB_CFG \
    $INTERMEDIATE_OUTPUT_DIR \
    $STAGED_ISO_ARTIFACTS_DIR/boot/grub

CreateBiosImage \
    $INPUT_GRUB_CFG \
    $INTERMEDIATE_OUTPUT_DIR \
    $STAGED_ISO_ARTIFACTS_DIR/boot/grub

# -----------------------------------------------------------------------------
# Generate the iso

echo
pwd
find $STAGED_ISO_ARTIFACTS_DIR
echo

mkdir -p $OUTPUT_ISO_DIR

sudo xorriso \
    -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid $OUTPUT_ISO_LABEL \
    -eltorito-boot boot/grub/bios.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --eltorito-catalog boot/grub/boot.cat \
    --grub2-boot-info \
    --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
    -eltorito-alt-boot \
    -e boot/grub/efiboot.img \
    -no-emul-boot \
    -append_partition 2 0xef $STAGED_ISO_ARTIFACTS_DIR/boot/grub/efiboot.img \
    -graft-points \
        $STAGED_ISO_ARTIFACTS_DIR \
        /boot/grub/bios.img=$STAGED_ISO_ARTIFACTS_DIR/boot/grub/bios.img \
        /EFI/efiboot.img=$STAGED_ISO_ARTIFACTS_DIR/boot/grub/efiboot.img \
    -output $OUTPUT_ISO_IMAGE_NAME

echo $OUTPUT_ISO_IMAGE_NAME

set +x
echo "-------- create-iso-from-initrd-vmlinuz.sh [exit] --------"
