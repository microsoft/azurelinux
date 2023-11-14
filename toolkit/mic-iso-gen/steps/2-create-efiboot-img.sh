#!/bin/bash

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
    --verbose \
    --output=$INTERMEDIATE_OUTPUT/bootx64.efi \
    boot/grub/grub.cfg=$SRC_GRUB_CFG

# Generate the fs to hold the bootx64.efi - i.e. out/efiboot.img
rm -f $INTERMEDIATE_OUTPUT/efiboot.img

dd if=/dev/zero of=$DST_DIR/efiboot.img bs=1M count=3
mkfs.vfat $DST_DIR/efiboot.img

LC_CTYPE=C mmd -i $DST_DIR/efiboot.img efi efi/boot
LC_CTYPE=C mcopy -i $DST_DIR/efiboot.img ./$INTERMEDIATE_OUTPUT/bootx64.efi ::efi/boot/

echo "Created ---- " $DST_DIR/efiboot.img