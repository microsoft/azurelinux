#!/bin/bash

set -e
set -x

packageName=${1:-kernel}
enlistmentFolder=${2:-/home/$USER/git/azurelinux}

pushd $enlistmentFolder

isolatedSpecsFolder=$enlistmentFolder/SPECS
# isolatedSpecsFolder=$enlistmentFolder/SPECS-TEMP
# sudo rm -rf $isolatedSpecsFolder
# mkdir $isolatedSpecsFolder
# cp -r  $enlistmentFolder/SPECS/$packageName $isolatedSpecsFolder/

# ls -la $isolatedSpecsFolder/
# sleep 2s

pushd $enlistmentFolder/toolkit

sudo make \
    package-toolkit \
    REBUILD_TOOLS=y

# 6GB used by here 9 GB free.

sudo make \
    build-packages \
    PACKAGE_BUILD_LIST="$packageName" \
    PACKAGE_REBUILD_LIST="$packageName" \
    REFRESH_WORKER_CHROOT=n \
    REBUILD_TOOLS=n \
    USE_CCACHE=y \
    SPECS_DIR=$isolatedSpecsFolder

popd
popd
