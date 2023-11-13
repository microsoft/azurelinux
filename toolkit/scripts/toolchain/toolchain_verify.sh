#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

MARINER_BUILD_DIR=$1

set -e

echo toolchain_verify.sh
echo Verify machine is ready to build toolchain

# Check for mounted toolchain or stage folders
mount > output_mount
if grep toolchain output_mount; then
  echo It looks like a toolchain directory is still mounted
  echo Unmount the directory
  exit 1
else
  echo No mounted toolchain directories found
fi
if grep $MARINER_BUILD_DIR output_mount; then
  echo It looks like a stage directory is still mounted
  echo Unmount the directory
  exit 1
else
  echo No mounted stage directories found
fi
rm output_mount

# Print free space
df -h \

# Check docker container
echo Checking docker images and containers related to toolchain
if docker history marinertoolchain; then
    echo marinertoolchain container exists on this machine
    echo cleanup previous toolchain build with: docker rmi
else
    echo marinertoolchain container does not exist on this machine
    echo toolchain will build from the beginning
fi