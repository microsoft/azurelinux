#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ROOT_FOLDER=$(git rev-parse --show-toplevel)
ARCHITECTURE=$(uname -m)

trap cleanup EXIT

usage() {
    echo "./setuplkgtoolchain.sh"
    echo " Syncs toolchain manifests to match LKG build"
    echo " Optional daily build id in the form 'YYYY-MM-DD-<branch>' (like 2024-05-28-3.0-dev), which will use that daily build instead of LKG"
    echo " WARNING: can overwrite local changes to 'toolkit/resources/manifests/package/pkggen_core_${ARCHITECTURE}.txt' or 'toolchain_${ARCHITECTURE}.txt'"
    exit 1
}

get_lkg() {
    wget -O $BUILD_FILENAME -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/$BUILD_FILENAME
    DAILY_BUILD_ID=$(jq -r .dailybuildid $BUILD_FILENAME | tr . -)
    GIT_COMMIT=$(jq -r .commit $BUILD_FILENAME)
}

check_for_modified_manifests() {
    if git status --porcelain | grep -qP "(pkggen_core|toolchain)_${ARCHITECTURE}.txt"; then
        echo "Local modifications to 'pkggen_core_${ARCHITECTURE}.txt' or 'toolchain_${ARCHITECTURE}.txt' detected."
        echo -e "\nNOTE: Changes to manifests were detected, and these will be overwritten. Hit Ctrl+C within 10 seconds to cancel...\n"
        sleep 10s
    fi
}

update_manifests() {
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/toolchain_${ARCHITECTURE}.txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/toolchain_${ARCHITECTURE}.txt
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/pkggen_core_${ARCHITECTURE}.txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/pkggen_core_${ARCHITECTURE}.txt
}

cleanup() {
    rm -f $BUILD_FILENAME
}

[[ "$1" == "--help" || "$1" == "help" ]] && usage

BUILD_ID="${1:-lkg-3.0-dev}"
BUILD_FILENAME="${BUILD_ID}.json"

get_lkg

check_for_modified_manifests

update_manifests

cat << EOF
===
=== Build Info for '$BUILD_ID':
=== DAILY_BUILD_ID='$DAILY_BUILD_ID'
=== Commit='$GIT_COMMIT'
===
EOF

echo -e "Finished syncing toolchain to LKG ('$DAILY_BUILD_ID' - '$GIT_COMMIT')"
echo -e "To download LKG toolchain, run:\n\tsudo make toolchain -j$(nproc) REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=$DAILY_BUILD_ID"

exit 0
