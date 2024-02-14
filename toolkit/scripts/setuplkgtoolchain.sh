#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ROOT_FOLDER=$(git rev-parse --show-toplevel)
LKG_FILENAME="lkg-3.0-dev.json"

trap cleanup EXIT

usage() {
    echo "./setuplkgtoolchain.sh [--auto-id] [--force]"
    echo " Syncs toolchain manifests to match LKG build"
    echo " WARNING: can overwrite local changes to 'toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt'"
    echo "    --auto-id: Just prints the latest LKG build ID and commit hash but makes no changes to the local manifests"
    echo "    --force: Overwrite local changes to manifests without prompting"
    exit 1
}

get_lkg() {
    wget -O $LKG_FILENAME -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/$LKG_FILENAME
    DAILY_BUILD_ID=$(jq -r .dailybuildid $LKG_FILENAME | tr . -)
    GIT_COMMIT=$(jq -r .commit $LKG_FILENAME)
}

check_for_modified_manifests() {
    auto=$1
    force=$2
    if git status --porcelain | grep -qP "(pkggen_core|toolchain)_$(uname -p).txt"; then
        if $force; then
            echo "Forcing overwrite of local changes to 'pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt'" 1>&2
        else
            if $auto; then
                echo "Local modifications to 'pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt' detected, will not auto update without --force" 1>&2
                exit 1
            else
                echo "Local modifications to 'pkggen_core_$(uname -p).txt' or 'toolchain_$(uname -p).txt' detected." 1>&2
                echo -e "\nNOTE: Changes to manifests were detected, and these will be overwritten. Hit Ctrl+C within 10 seconds to cancel...\n" 1>&2
                sleep 10s
            fi
        fi
    fi
}

update_manifests() {
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/toolchain_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/toolchain_$(uname -p).txt 1>&2
    wget -nv https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt -O $ROOT_FOLDER/toolkit/resources/manifests/package/pkggen_core_$(uname -p).txt 1>&2
}

cleanup() {
    rm -f $LKG_FILENAME
}

auto_id=false
force_manifests=false
while [[ $# -gt 0 ]]; do
    case $1 in
        *auto-id)
            auto_id=true
            shift
            ;;
        *force)
            force_manifests=true
            shift
            ;;
        *help | *)
            usage
            ;;
    esac
done

get_lkg

check_for_modified_manifests $auto_id $force_manifests

update_manifests

if ! $auto_id; then
cat << EOF
===
=== Current LKG:
=== DAILY_BUILD_ID='$DAILY_BUILD_ID'
=== Commit='$GIT_COMMIT'
===
EOF
    echo -e "Finished syncing toolchain to LKG ('$DAILY_BUILD_ID' - '$GIT_COMMIT')"
    echo -e "To download LKG toolchain, run:\n\tsudo make toolchain -j$(nproc) REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=$DAILY_BUILD_ID"
else
    # In auto mode, just print the LKG build ID so we can use it in the calling script
    echo $DAILY_BUILD_ID
fi

exit 0
