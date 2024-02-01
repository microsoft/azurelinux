#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ROOT_FOLDER=$(git rev-parse --show-toplevel)
LKG_FILENAME="lkg-3.0-dev.json"

usage() {
    echo "./setuplkgtoolchain.sh"
    echo " Syncs toolchain manifests to match LKG build"
    echo " WARNING: can overwrite local changes to 'toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt'"
    exit 1
}

get_lkg() {
    wget -O $LKG_FILENAME -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/$LKG_FILENAME
    DAILY_BUILD_ID=$(jq -r .dailybuildid $LKG_FILENAME | tr . -)
    GIT_COMMIT=$(jq -r .commit $LKG_FILENAME)
}

check_for_modified_manifests() {
    if git status --porcelain | grep -qP "(pkggen_core|toolchain)_$(uname -p).txt"; then
        echo "Local modifications to 'pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt' detected."
        echo -e "\nNOTE: Changes to manifests were detected, and these will be overwritten. Hit Ctrl+C within 10 seconds to cancel...\n"
        sleep 10s
    fi
}

update_manifests() {
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/toolchain_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/toolchain_$(uname -p).txt
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt
}

[[ "$1" == "--help" || "$1" == "help" ]] && usage

get_lkg

check_for_modified_manifests

update_manifests

cat << EOF
===
=== Current LKG:
=== DAILY_BUILD_ID='$DAILY_BUILD_ID'
=== Commit='$GIT_COMMIT'
===
EOF

echo -e "Finished syncing toolchain to LKG ('$DAILY_BUILD_ID' - '$GIT_COMMIT')"
echo -e "To download LKG toolchain, run:\n\tsudo make toolchain -j$(nproc) REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=$DAILY_BUILD_ID"

exit 0
