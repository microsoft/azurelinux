#!/bin/bash

set -x
set -e

SRC_VMLINUZ=$1
DST_DIR=$2

mkdir -p $DST_DIR
cp $SRC_VMLINUZ $DST_DIR/vmlinuz
