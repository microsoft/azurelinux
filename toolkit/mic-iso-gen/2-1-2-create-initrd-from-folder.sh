#!/bin/bash

set -x
set -e

EXTRACTED_DIR=$1
OUTPUT_DIR=/home/george/temp/experiment-roast-out
WORKING_DIR=/home/george/temp/experiment-roast-tmp

chmod 755 /home/george/temp/experiment/in/extracted/etc/shadow

sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

sudo rm -rf $WORKING_DIR
mkdir -p $WORKING_DIR

pushd ~/git/CBL-Mariner/toolkit

sudo make go-tools REBUILD_TOOLS=y

sudo ./out/tools/roast \
 --dir $EXTRACTED_DIR \
 --output-dir $OUTPUT_DIR \
 --tmp-dir $WORKING_DIR

popd

