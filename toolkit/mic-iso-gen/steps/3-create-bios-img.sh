#!/bin/bash

set -x
set -e

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