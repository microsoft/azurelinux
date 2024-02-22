#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Updates the requested manifest file based on the contents of the LKG json.

set -e

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <manifest_file> <arch> <temp_dir> <force_update>"
    exit 1
fi

manifest_file="$1"
arch="$2"
temp_dir="$3"
force_update="$4"

# Get SUDO_USER if set, USER otherwise
CALLING_USER=${SUDO_USER:-$USER}
echo "Running update_manifest.sh as $CALLING_USER"
LKG_FILENAME="lkg-3.0-dev.json"
LKG_TEMP_FILENAME="$(mktemp -p "$temp_dir" "${LKG_FILENAME}.XXXXXX" )"
LKG_TEMP_MANIFEST_FILENAME="$(mktemp -p "$temp_dir" "$(basename "$manifest_file").XXXXXX" )"

cleanup() {
    rm -f "$LKG_TEMP_FILENAME"
    rm -f "$LKG_TEMP_MANIFEST_FILENAME"
}
trap cleanup EXIT

usage() {
    echo "$0 <manifest_file> <arch> <temp_dir>"
    exit 1
}

get_lkg() {
    wget -O $LKG_TEMP_FILENAME -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/$LKG_FILENAME
    GIT_COMMIT=$(jq -r .commit $LKG_TEMP_FILENAME)
}

check_for_modified_manifests() {
    if git status --porcelain | grep -qP "$(basename $manifest_file)"; then
        echo "    #### Local modifications to '$manifest_file' detected."
        echo "           Use 'DAILY_BUILD_ID=lkg-force' or 'PKG_MANIFEST_OVERWRITE=y' to overwrite local changes. ####" >&2
        exit 1
    fi
}

# We don't want to update the timestamps unless we actually change the file, so download to a temp file and then move it over
# if the files are different
# $1 - filename (e.g. toolchain_aarch64.txt)
update_manifest() {
    local filepath
    local arch
    local url
    filepath="$1"
    arch="$2"
    basename=$(basename $filepath)

    url="https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/${basename}"

    echo "Downloading $basename manifest from $url"

    wget -nv "${url}" -O "${LKG_TEMP_MANIFEST_FILENAME}"
    # only update if the files are different
    if ! cmp -s "${LKG_TEMP_MANIFEST_FILENAME}" "${filepath}"; then
        echo "Manifests are different, updating ${basename}"
        mv "${LKG_TEMP_MANIFEST_FILENAME}" "${filepath}"
        chown "$CALLING_USER:$CALLING_USER" "${filepath}"
    else
        echo "Manifests are the same, not updating ${basename}"
    fi
}

if ! $force_update; then
    check_for_modified_manifests
fi

get_lkg

update_manifest "${manifest_file}" "${arch}"

exit 0
