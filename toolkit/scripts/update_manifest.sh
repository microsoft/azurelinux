#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Updates the requested manifest file based on the contents of the LKG json.

set -e

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <manifest_file> <arch> <temp_dir> <build_id>" >&2
    exit 1
fi

manifest_file="$1"
arch="$2"
temp_dir="$3"
build_id="$4"

# Get SUDO_USER if set, USER otherwise
CALLING_USER=${SUDO_USER:-$USER}
echo "Running update_manifest.sh as $CALLING_USER"

# Convert build_id to the associated filename on the LKG blob
# "3-0-YYYYMMDD" -> "YYYY-MM-DD-3.0-dev"
convert_id() {
    branch=$(echo "$1" | cut -d- -f1-2)
    date=$(echo "$1" | cut -d- -f3)

    # Ensure the parts are in the correct format
    if [[ ! "$branch" =~ ^[0-9]+-[0-9]+$ ]]; then
        echo "Invalid branch format: $branch" >&2
        echo "Expected ID format: lkg | <major>-<minor>-<YYYYMMDD>" >&2
        exit 1
    fi
    if [[ ! "$date" =~ ^[0-9]{8}$ ]]; then
        echo "Invalid date format: $date" >&2
        echo "Expected DAILY_BUILD_ID format: lkg | <major>-<minor>-<YYYYMMDD>" >&2
        exit 1
    fi
    # Check we can parse the date
    date -d "$date" >/dev/null 2>&1 || {
        echo "Invalid date: $date" >&2
        echo "Expected DAILY_BUILD_ID format: lkg | <major>-<minor>-<YYYYMMDD>" >&2
        exit 1
    }

    branch=$(echo "$branch" | tr - .)-dev
    date=$(date -d "$date" +%Y-%m-%d)

    echo "${date}-${branch}"
}

BUILD_FILENAME="$(convert_id "$build_id").json"
BUILD_TEMP_FILENAME="$(mktemp -p "$temp_dir" "${BUILD_FILENAME}.XXXXXX" )"
BUILD_TEMP_MANIFEST_FILENAME="$(mktemp -p "$temp_dir" "$(basename "$manifest_file").XXXXXX" )"

# shellcheck disable=SC2317
cleanup() {
    rm -f "$BUILD_TEMP_FILENAME"
    rm -f "$BUILD_TEMP_MANIFEST_FILENAME"
}
trap cleanup EXIT

get_commit_info() {
    wget -O "$BUILD_TEMP_FILENAME" -nv "https://mariner3dailydevrepo.blob.core.windows.net/lkg/$BUILD_FILENAME"
    GIT_COMMIT=$(jq -r .commit "$BUILD_TEMP_FILENAME")
}

# Check if the current manifest have been changed by the user
check_for_modified_manifests() {
    if git status --porcelain | grep -qP "$(basename "$manifest_file")"; then
        echo "    #### Local modifications to '$manifest_file' detected."
        echo "           Revert changes to '$manifest_file' before proceeding. ####" >&2
        exit 1
    fi
}

# We don't want to update the timestamps unless we actually change the file, so download to a temp file and then move it over
# if the files are different. Refuse to overwrite possible user changes to the manifest files.
# $1 - filename (e.g. toolchain_aarch64.txt)
update_manifest() {
    local filepath
    local arch
    local url
    filepath="$1"
    arch="$2"
    basename=$(basename "$filepath")

    url="https://raw.githubusercontent.com/microsoft/CBL-Mariner/$GIT_COMMIT/toolkit/resources/manifests/package/${basename}"

    echo "Checking for updates to $basename manifest from $url"

    wget -nv "${url}" -O "${BUILD_TEMP_MANIFEST_FILENAME}"
    # only update if the files are different
    if ! cmp -s "${BUILD_TEMP_MANIFEST_FILENAME}" "${filepath}"; then

        # Refuse to overwrite possible user changes to the manifest files. This will fail if LKG changes the manifests
        # day-to-day but is better than silently overwriting user changes.
        check_for_modified_manifests

        echo "Manifests are different, updating ${basename}"
        mv "${BUILD_TEMP_MANIFEST_FILENAME}" "${filepath}"
        chown "$CALLING_USER:" "${filepath}"
    else
        echo "Manifests are the same, not updating ${basename}"
    fi
}

get_commit_info

update_manifest "${manifest_file}" "${arch}"

exit 0
