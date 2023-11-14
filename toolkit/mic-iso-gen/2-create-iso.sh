#!/bin/bash

sudo apt-get install -y mtools dosfstools grub-pc-bin grub2-pc xorriso glibc-iconv

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

export INPUT_INTRD=./out/images/iso_initrd/iso-initrd.img
export INPUT_VMLINUZ=./build/imagegen/iso_initrd/imager_output/rootfs/boot/vmlinuz-*
export INPUT_GRUB_CFG=./grub.cfg
export INPUT_ROOT_FS=./test-rootfs.img

export INTERMEDIATE_OUTPUT=./iso-intermediate-artifacts

export STAGED_ISO_ARTIFACTS_DIR=./iso-staged-layout

export OUTPUT_ISO_DIR=./iso-output
export OUTPUT_ISO_IMAGE_NAME=$OUTPUT_ISO_DIR/baremetal-$(printf "%(%Y%m%d-%H%M%S)T").iso
export OUTPUT_ISO_LABEL="baremetal-iso"

./steps/0-stage-initrd.sh \
    $INPUT_INTRD \
    $STAGED_ISO_ARTIFACTS_DIR/boot

./steps/1-stage-vm-linuz.sh \
    $INPUT_VMLINUZ \
    $STAGED_ISO_ARTIFACTS_DIR/boot

./steps/2-create-efiboot-img.sh \
    $INPUT_GRUB_CFG \
    $INTERMEDIATE_OUTPUT \
    $STAGED_ISO_ARTIFACTS_DIR/boot/grub

./steps/3-create-bios-img.sh \
    $INPUT_GRUB_CFG \
    $INTERMEDIATE_OUTPUT \
    $STAGED_ISO_ARTIFACTS_DIR/boot/grub

./steps/4-stage-rootfs.sh \
    $INPUT_ROOT_FS \
    $STAGED_ISO_ARTIFACTS_DIR/rootfs

# -----------------------------------------------------------------------------
# Generate the iso

xorriso \
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
