#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Prints to stdout the daily build id from the LKG file

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <temp_dir>" >&2
    exit 1
fi

temp_dir="$1"

LKG_FILENAME="lkg-3.0-dev.json"
LKG_TEMP_FILENAME="$(mktemp -p "$temp_dir" "${LKG_FILENAME}.XXXXXX" )"

# shellcheck disable=SC2317
cleanup() {
    rm -f "$LKG_TEMP_FILENAME"
}
trap cleanup EXIT

get_lkg() {
    wget -O "$LKG_TEMP_FILENAME" -nv "https://mariner3dailydevrepo.blob.core.windows.net/lkg/$LKG_FILENAME"
    DAILY_BUILD_ID=$(jq -r .dailybuildid "$LKG_TEMP_FILENAME" | tr . -)
}

get_lkg

if [ -z "$DAILY_BUILD_ID" ]; then
    echo "Failed to get DAILY_BUILD_ID from https://mariner3dailydevrepo.blob.core.windows.net/lkg/$LKG_FILENAME" >&2
    exit 1
fi

echo "$DAILY_BUILD_ID"

exit 0
