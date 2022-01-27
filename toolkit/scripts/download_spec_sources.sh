#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 - Path to 'cgmanifest.json'.
# ${@:2} - Spec names.

cgmanifest_path="$1"

if [[ $# -lt 2 ]]
then
    echo "ERROR: must provide at least two arguments: 'cgmanifest.json' path and the spec name(s)." >&2
    exit 1
fi

TEMP_DIR=$(mktemp -d)
function clean_up {
    rm -rf "$TEMP_DIR"
}
trap clean_up EXIT SIGINT SIGTERM

OUTPUT_DIR="$(pwd)/downloaded_sources"

for spec in "${@:2}"
do
    if ! grep -q -P "\"name\":\s+\"$spec\"" "$cgmanifest_path"
    then
        echo "WARNING: spec '$spec' not found inside '$cgmanifest_path', cannot download sources." >&2
        continue
    fi

    echo "Downloading sources for '$spec'."
    wget -q -P "$TEMP_DIR" $(jq ".Registrations[].component | select(.other != null).other | select(.name == \"$spec\") | .downloadUrl" -r "$cgmanifest_path")
done

mkdir -p "$OUTPUT_DIR"
for archive in "$TEMP_DIR"/*
do
    echo "Extracting '$archive' into '$OUTPUT_DIR'."
    tar -xf "$archive" -C "$OUTPUT_DIR"
done
