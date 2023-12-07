#!/bin/bash

echo "-------- create-initrd-image-from-folder.sh [enter] --------"

set -x
set -e

SOURCE_DIR=$1
WORKING_DIR=$2
OUTPUT_DIR=$3

build_and_run_roast() {

    pushd ~/git/CBL-Mariner/toolkit

    sudo rm -rf $OUTPUT_DIR
    mkdir -p $OUTPUT_DIR

    sudo rm -rf $WORKING_DIR
    mkdir -p $WORKING_DIR

    sudo make go-tools REBUILD_TOOLS=y

    sudo ./out/tools/roast \
    --dir $SOURCE_DIR \
    --output-dir $OUTPUT_DIR \
    --tmp-dir $WORKING_DIR

    popd
}

# -------- main --------

pushd ~/git/CBL-Mariner

patch -p1 -i /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/roast.patch

build_and_run_roast

git checkout -- toolkit/tools/roast/roast.go

popd

set +x
echo "-------- create-initrd-image-from-folder.sh [exit] --------"
