#!/bin/bash

set -x
set -e

SOURCE_DIR=$1
WORKING_DIR=$2
OUTPUT_DIR=$3

chmod 755 /home/george/temp/experiment/in/extracted/etc/shadow

sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

sudo rm -rf $WORKING_DIR
mkdir -p $WORKING_DIR

pushd ~/git/CBL-Mariner/toolkit

sudo make go-tools REBUILD_TOOLS=y

sudo ./out/tools/roast \
 --dir $SOURCE_DIR \
 --output-dir $OUTPUT_DIR \
 --tmp-dir $WORKING_DIR

popd

