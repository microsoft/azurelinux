#!/bin/bash

set -x
set -e

pushd /home/george/git/CBL-Mariner-POC

sudo rm -f ./mic-build/out/mic-20240124-1514.vhdx
sudo rm -rf ./out/images/baremetal
sudo rm -rf ./build/imagegen/baremetal

pushd /home/george/git/CBL-Mariner-POC/toolkit

sudo make image \
    -j$(nproc) \
    REBUILD_TOOLS=y \
    REBUILD_TOOLCHAIN=n \
    REBUILD_PACKAGES=n \
    CONFIG_FILE=/home/george/git/CBL-Mariner-POC/toolkit/imageconfigs/baremetal.json

popd