#!/bin/bash

# buildpackage.sh - use toolkit to build one specific package

check_args() {
    if [ -z "$1" ]; then
        echo "Provide spec folder name (SPECS, SPECS-EXTENDED)"
        exit 1
    fi
    SPEC_FOLDER_NAME=$1
    if [ -z "$2" ]; then
        echo "Provide name of package to build"
        exit 1
    fi
    PKGNAME=$2
}

check_args "$@"

ROOT_FOLDER=$(git rev-parse --show-toplevel)
TEMP_SPEC_FOLDER="$ROOT_FOLDER/SPECS-build-temp"
echo "Building package $PKGNAME from $SPEC_FOLDER_NAME in $ROOT_FOLDER"

# setup 2-0-stable toolchain
wget https://raw.githubusercontent.com/microsoft/CBL-Mariner/2.0-stable/toolkit/resources/manifests/package/toolchain_x86_64.txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/toolchain_x86_64.txt
wget https://raw.githubusercontent.com/microsoft/CBL-Mariner/2.0-stable/toolkit/resources/manifests/package/pkggen_core_x86_64.txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/pkggen_core_x86_64.txt
sudo make toolchain REBUILD_TOOLCHAIN=n
sudo make copy-toolchain-rpms

# prepare for build
sudo make clean-input-srpms clean-expand-specs
rm -rf $TEMP_SPEC_FOLDER
mkdir -pv $TEMP_SPEC_FOLDER
cp -vr $ROOT_FOLDER/$SPEC_FOLDER_NAME/$PKGNAME $TEMP_SPEC_FOLDER

# build the package
time sudo make build-packages PACKAGE_BUILD_LIST="$PKGNAME" PACKAGE_REBUILD_LIST="$PKGNAME" RUN_CHECK=n REFRESH_WORKER_CHROOT=n SPECS_DIR=$TEMP_SPEC_FOLDER SOURCE_URL=https://cblmarinerstorage.blob.core.windows.net/sources/core REBUILD_TOOLS=y
