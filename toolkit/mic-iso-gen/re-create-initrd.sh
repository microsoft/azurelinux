#!/bin/bash

set -x
set -e

WORK_DIR=~/temp/experiment

WORK_DIR_IN=$WORK_DIR/in
WORK_DIR_OUT=$WORK_DIR/out

pushd $WORK_DIR

function extract () {
    echo "---- extract ----"
    local sourceInitrd=$1
    local targetDir=$2

    cp $sourceInitrd $WORK_DIR_IN/initrd.img.gz
    pigz -d $WORK_DIR_IN/initrd.img.gz

    mkdir -p $targetDir
    pushd $targetDir
    cpio -i --make-directories < $WORK_DIR_IN/initrd.img
    popd
}

function recreate () {
    echo "---- recreate ----"
    local sourceDir=$1
    local modifiedInitrd=$2

    pushd $sourceDir
    find . -depth | cpio -o > $modifiedInitrd
    pigz -c $modifiedInitrd > ${modifiedInitrd}.gz
    mv $modifiedInitrd ${modifiedInitrd}.uncompressed
    mv ${modifiedInitrd}.gz ${modifiedInitrd}
    popd
}

# ---- main ----

sudo rm -rf $WORK_DIR
mkdir -p $WORK_DIR_IN/extracted
mkdir -p $WORK_DIR_OUT/extracted

SOURCE_INIT_RD=/mnt/full-initrd-iso/isolinux/initrd.img
NEW_INIT_RD=$WORK_DIR_OUT/initrd.img

extract $SOURCE_INIT_RD $WORK_DIR_IN/extracted
# recreate $WORK_DIR_IN/extracted $NEW_INIT_RD

ls -la $SOURCE_INIT_RD
ls -la $NEW_INIT_RD

popd