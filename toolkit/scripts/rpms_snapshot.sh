#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e -o pipefail

SCRIPT_FOLDER="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
OUTPUT_FILE_PATH="$SCRIPT_FOLDER/rpms.snapshot"

while getopts c:o:s:t: flag
do
    case "${flag}" in
        c) CHROOT_TAR="${OPTARG}";;
        o) OUTPUT_FILE_PATH="${OPTARG}";;
        s) SPECS_DIR="${OPTARG}";;
        t) DIST_TAG="${OPTARG}";;
        *)
            echo "ERROR: invalid flag '$flag'!" 1>&2
            exit 1
            ;;
    esac
done

if [[ ! -f "$CHROOT_TAR" ]]
then
    echo "Must pass a path to the worker chroot tarball."
    exit 1
fi

if [[ ! -d "$SPECS_DIR" ]]
then
    echo "Must pass a path to the specs directory."
    exit 1
fi

if [[ -z "$DIST_TAG" ]]
then
    echo "Must pass a distribution tag."
    exit 1
fi

if [[ -f "$OUTPUT_FILE_PATH" ]]
then
    echo "Will overwrite existing output file '$OUTPUT_FILE_PATH'."
fi

TEMP_DIR=$(mktemp -d)
function cleanup {
    echo "Cleaning up."

    if mount -v | grep -q "$TEMP_CHROOT_SPECS_DIR"
    then
        sudo umount -q "$TEMP_CHROOT_SPECS_DIR"
    fi

    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT SIGINT SIGTERM

TEMP_CHROOT_SPECS_DIR="$TEMP_DIR/SPECS"

ARCHIVE_TOOL=gzip
if command -v pigz &>/dev/null
then
    ARCHIVE_TOOL=pigz
fi

echo "Building RPMs snapshot inside '$TEMP_DIR'."

tar -I $ARCHIVE_TOOL -xf "$CHROOT_TAR" -C "$TEMP_DIR"
cp "$SCRIPT_FOLDER/rpms_snapshot_chroot.sh" "$TEMP_DIR"

mkdir -p "$(dirname "$OUTPUT_FILE_PATH")"

mkdir "$TEMP_CHROOT_SPECS_DIR"
sudo mount --bind "$SPECS_DIR" "$TEMP_CHROOT_SPECS_DIR"

chroot "$TEMP_DIR" ./rpms_snapshot_chroot.sh -s "SPECS" -t "$DIST_TAG" -o rpms.snapshot

mv "$TEMP_DIR/rpms.snapshot" "$OUTPUT_FILE_PATH"
