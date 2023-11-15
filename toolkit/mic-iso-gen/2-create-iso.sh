#!/bin/bash

set -x
set -e

sudo apt-get install -y mtools dosfstools grub-pc-bin grub-pc xorriso

function CreateEfibootImage () {
    SRC_GRUB_CFG=$1
    INTERMEDIATE_OUTPUT=$2
    DST_DIR=$3

    mkdir -p $INTERMEDIATE_OUTPUT

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
    LC_CTYPE=C mcopy -i $DST_DIR/efiboot.img ./$INTERMEDIATE_OUTPUT/bootx64.efi ::efi/boot/

    echo "Created ---- " $DST_DIR/efiboot.img
}

function CreateBiosImage () {
    SRC_GRUB_CFG=$1
    INTERMEDIATE_OUTPUT=$2
    DST_DIR=$3

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

export INPUT_INTRD=$1
export INPUT_VMLINUZ=$2
export INPUT_GRUB_CFG=$3
export INPUT_ROOT_FS=$4
export INPUT_HOST_CONFIGURATION=$5
export OUTPUT_ISO_DIR=$6

export INTERMEDIATE_OUTPUT_DIR=./iso-intermediate-artifacts

export STAGED_ISO_ARTIFACTS_DIR=./iso-staged-layout

export OUTPUT_ISO_IMAGE_NAME=$OUTPUT_ISO_DIR/baremetal-$(printf "%(%Y%m%d-%H%M%S)T").iso
export OUTPUT_ISO_LABEL="baremetal-iso"

cd ~/git/CBL-Mariner/toolkit/mic-iso-gen

mkdir -p $STAGED_ISO_ARTIFACTS_DIR/boot
cp $INPUT_INTRD $STAGED_ISO_ARTIFACTS_DIR/boot/initrd.img
cp $INPUT_VMLINUZ $STAGED_ISO_ARTIFACTS_DIR/boot/vmlinuz

mkdir -p $STAGED_ISO_ARTIFACTS_DIR/artifacts
cp $INPUT_ROOT_FS $STAGED_ISO_ARTIFACTS_DIR/artifacts/
cp $INPUT_HOST_CONFIGURATION $STAGED_ISO_ARTIFACTS_DIR/artifacts/

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
