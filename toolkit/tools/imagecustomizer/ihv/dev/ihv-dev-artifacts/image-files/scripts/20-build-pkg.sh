#!/bin/bash

set -e
set -x

packageName=${1:-kernel}
enlistmentFolder=${2:-/home/$USER/git/azurelinux}
specsFolder=$enlistmentFolder/SPECS

pushd $enlistmentFolder/toolkit

sudo make \
    package-toolkit \
    REBUILD_TOOLS=y

# 6GB used by here.

sudo make \
    build-packages \
    PACKAGE_BUILD_LIST="$packageName" \
    PACKAGE_REBUILD_LIST="$packageName" \
    REFRESH_WORKER_CHROOT=n \
    REBUILD_TOOLS=n \
    USE_CCACHE=y \
    SPECS_DIR=$specsFolder

# 34GB used by here.

popd

