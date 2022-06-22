#!/bin/bash
set -x
set -e

# This script streamlines the cross compile build with Mariner

SOURCE_SERVER=https://cblmarinerstorage.blob.core.windows.net/sources/core
SPECS_DIR="../SPECS-CROSS"
TOOLCHAIN_FILE="../build/toolchain/toolchain_built_rpms_all.tar.gz"
LOG="debug"

# Make clean and then toolchain (stage 1 & stage 2) from scratch
make clean
docker rmi -f $(docker image ls marinertoolchain -q) || true
make toolchain \
REBUILD_TOOLCHAIN=y \
REBUILD_TOOLS=y \
SOURCE_URL=$SOURCE_SERVER

# Make cross-compiling toolchain RPMS
make build-packages -j$(nproc) \
SOURCE_URL=$SOURCE_SERVER \
REBUILD_TOOLCHAIN=n \
TOOLCHAIN_ARCHIVE=$TOOLCHAIN_FILE \
REBUILD_TOOLS=y \
SPECS_DIR=$SPECS_DIR \
CONFIG_FILE= \
DISABLE_UPSTREAM_REPOS=y \
LOG_LEVEL=$LOG
