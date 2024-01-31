#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

ROOT_FOLDER=$(git rev-parse --show-toplevel)

usage() {
    echo "./setuplkgtoolchain.sh"
    echo " Syncs toolchain manifests to match LKG build"
    exit 1
}

getlkg() {
    wget -O lkg-3.0-dev.json -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/lkg-3.0-dev.json
    DAILY_BUILD_ID=$(cat lkg-3.0-dev.json | jq -r .dailybuildid | tr . -)
    GIT_COMMIT=$(cat lkg-3.0-dev.json | jq -r .commit)
}

checkformodifiedmanifests() {
    if [[ $(git status --porcelain | grep pkggen_core_$(uname -p).txt | wc -l) -ne "0" ||
          $(git status --porcelain | grep toolchain_$(uname -p).txt | wc -l) -ne "0" ]]; then
        echo "Local modifications to 'pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt' detected."
        echo -e "\nNOTE: Changes to manifests were detected, and these will be overwritten. Hit Ctrl+C within 10 seconds to cancel...\n"
        sleep 10s
    fi
}

updatemanifests() {
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/toolchain_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/toolchain_$(uname -p).txt
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt
}

[[ "$1" == "--help" ]] && usage

getlkg
echo -e "===\n=== Current LKG:\n=== DAILY_BUILD_ID=\t'$DAILY_BUILD_ID'\n=== commit=\t\t'$GIT_COMMIT'\n===\n"

checkformodifiedmanifests

updatemanifests

echo -e "\nFinished syncing toolchain to LKG ('$DAILY_BUILD_ID' - '$GIT_COMMIT')"
echo -e "To download LKG toolchain, run:\n\tsudo make toolchain -j$(nproc) REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=$DAILY_BUILD_ID"

exit 0
