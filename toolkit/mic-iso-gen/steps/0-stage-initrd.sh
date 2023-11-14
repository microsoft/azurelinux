#!/bin/bash

set -x
set -e

SRC_INTRD=$1
DST_DIR=$2

mkdir -p $DST_DIR
cp $SRC_INTRD $DST_DIR/initrd.img
