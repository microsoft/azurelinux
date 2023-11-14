#!/bin/bash

set -x
set -e

SRC_ROOT_FS=$1
DST_DIR=$3

mkdir -p $DST_DIR
cp $SRC_ROOT_FS $DST_DIR