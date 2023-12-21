#!/bin/bash

set -x
set -e

pushd ~/git/CBL-Mariner-POC/toolkit/tools/isomaker
go build
sudo mkdir -p /home/george/temp/mic-iso/dummy
sudo ./isomaker \
    --input /home/george/git/CBL-Mariner-POC/toolkit/imageconfigs/mic-test-iso.json \
    --initrd-path /home/george/temp/mic-iso/rootfs-extracted/initrd.img \
    --release-version 2.0.20240112.1740 \
    --image-tag $(printf "%(%Y%m%d-%H%M%S)T") \
    --base-dir /home/george/git/CBL-Mariner-POC/toolkit/imageconfigs \
    --build-dir /home/george/git/CBL-Mariner-POC/build/imagegen/mic-test-iso/workspace \
    --resources /home/george/git/CBL-Mariner-POC/toolkit/resources \
    --iso-repo /home/george/temp/mic-iso/dummy \
    --log-level debug \
    --log-file /home/george/git/CBL-Mariner-POC/isomaker.log \
    --output-dir /home/george/temp/iso-build-poc/iso-out/iso/
popd