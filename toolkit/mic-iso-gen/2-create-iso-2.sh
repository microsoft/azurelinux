#!/bin/bash

set -x
set -e

INPUT_BASE_ISO=$1
INPUT_GRUB_CFG=$2
INPUT_STARTUP_SCRIPT=$3
INPUT_STARTUP_SCRIPT_CONFIGURATION=$4
INPUT_ROOT_FS=$5
OUTPUT_ISO_DIR=$6

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

    echo "Created ---- " $DST_DIR/efiboot.img
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

    echo "Created ---- " $DST_DIR/bios.img
}

function ExtractInitrdAndVmlinuz () {
    local INPUT_ISO=$1
    local OUTPUT_DIR=$2

    BASE_ISO_MOUNT_DIR=/mnt/isomount
    INPUT_INTRD=$BASE_ISO_MOUNT_DIR/isolinux/initrd.img
    INPUT_VMLINUZ=$BASE_ISO_MOUNT_DIR/isolinux/vmlinuz

    sudo mkdir -p $BASE_ISO_MOUNT_DIR
    # sudo umount $BASE_ISO_MOUNT_DIR
    sudo mount -o loop $INPUT_BASE_ISO $BASE_ISO_MOUNT_DIR

    mkdir -p $OUTPUT_DIR
    sudo cp $INPUT_INTRD $OUTPUT_DIR/initrd.img
    sudo cp $INPUT_VMLINUZ $OUTPUT_DIR/vmlinuz

    sudo umount $BASE_ISO_MOUNT_DIR
    sudo rm -r $BASE_ISO_MOUNT_DIR
}

function CreateBootloadImages() {
    local INPUT_GRUB_CFG=$1
    local INTERMEDIATE_OUTPUT_DIR=$2
    local OUT_DIR=$3

    mkdir -p INTERMEDIATE_OUTPUT_DIR

    CreateEfibootImage \
        $INPUT_GRUB_CFG \
        $INTERMEDIATE_OUTPUT_DIR \
        $OUT_DIR

    CreateBiosImage \
        $INPUT_GRUB_CFG \
        $INTERMEDIATE_OUTPUT_DIR \
        $OUT_DIR
}

# -----------------------------------------------------------------------------
# main()
#
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

STAGED_ISO_ARTIFACTS_DIR=$OUTPUT_ISO_DIR/iso-staged-layout
mkdir -p $STAGED_ISO_ARTIFACTS_DIR

pushd ~/git/CBL-Mariner/toolkit/mic-iso-gen

ExtractInitrdAndVmlinuz \
    $INPUT_BASE_ISO \
    $STAGED_ISO_ARTIFACTS_DIR/boot

CreateBootloadImages \
    $INPUT_GRUB_CFG \
    $OUTPUT_ISO_DIR/iso-intermediate-artifacts \
    $STAGED_ISO_ARTIFACTS_DIR/boot/grub

mkdir -p $STAGED_ISO_ARTIFACTS_DIR/artifacts
cp $INPUT_STARTUP_SCRIPT $STAGED_ISO_ARTIFACTS_DIR/artifacts/
cp $INPUT_STARTUP_SCRIPT_CONFIGURATION $STAGED_ISO_ARTIFACTS_DIR/artifacts/
cp $INPUT_ROOT_FS $STAGED_ISO_ARTIFACTS_DIR/artifacts/

# -----------------------------------------------------------------------------
# Generate the iso

FINAL_ISO_DIR=$OUTPUT_ISO_DIR/iso
mkdir -p $FINAL_ISO_DIR

OUTPUT_ISO_IMAGE_NAME=$FINAL_ISO_DIR/baremetal-$(printf "%(%Y%m%d-%H%M%S)T").iso
OUTPUT_ISO_LABEL="baremetal-iso"

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

popd

# -----------------------------------------------------------------------------
# Test iso

# sudo ./images/live-cd/test-create-vm.sh mariner13 /home/george/git/AfO-Packages/afo-host-live-cd-20211229-150826.iso

# virt-install \
#   --name $1 \
#   --memory 4096 \
#   --vcpus 2 \
#   --cdrom $2 \
#   --livecd \
#   --nodisks \
#   --cpu host \
#   --machine pc-i440fx-hirsute \
#   --os-variant linux2020 \
#   --network default \
#   --boot uefi,loader=/usr/share/OVMF/OVMF_CODE_4M.fd,loader_secure=no
