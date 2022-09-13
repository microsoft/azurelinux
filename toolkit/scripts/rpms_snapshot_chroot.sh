#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e -o pipefail

OUTPUT=rpms.snapshot

while getopts o:s:t: flag
do
    case "${flag}" in
        o) OUTPUT="${OPTARG}";;
        s) SPECS_DIR="${OPTARG}";;
        t) DIST_TAG="${OPTARG}";;
        *)
            echo "ERROR: invalid flag '$flag'!" 1>&2
            exit 1
            ;;
    esac
done

if [[ ! -d "$SPECS_DIR" ]]
then
    echo "'$SPECS_DIR' is not a path to the specs directory."
    exit 1
fi

if [[ -z "$DIST_TAG" ]]
then
    echo "Must pass a distribution tag."
    exit 1
fi

TEMP_FILE=$(mktemp)
function cleanup {
    echo "Cleaning up."
    rm -rf "$TEMP_FILE"
}
trap cleanup EXIT SIGINT SIGTERM

CURRENT_ARCH=$(rpm --eval "%{_arch}")

echo "Creating RPMs snapshot for architecture '$CURRENT_ARCH'."
echo "DIST_TAG: $DIST_TAG."
echo "SPECS_DIR: $SPECS_DIR."

grep -LP "^\s*(Exclusive|Exclude)Arch:" "$SPECS_DIR"/**/*.spec > "$TEMP_FILE"

EXCLUDE_ARCH_SPECS=$(grep -lP "^\s*ExcludeArch:" "$SPECS_DIR"/**/*.spec)
for spec in $EXCLUDE_ARCH_SPECS
do
    if ! rpmspec -q -D "_sourcedir $(dirname "$spec")" -D "dist $DIST_TAG" -D "with_check 1" --queryformat="[%{EXCLUDEARCH} ]\n" --srpm "$spec" 2>/dev/null | grep -qP "\b$CURRENT_ARCH\b"
    then
        echo "$spec" >> "$TEMP_FILE"
    fi
done

EXCLUSIVE_ARCH_SPECS=$(grep -lP "^\s*ExclusiveArch:" "$SPECS_DIR"/**/*.spec)
for spec in $EXCLUSIVE_ARCH_SPECS
do
    if rpmspec -q -D "_sourcedir $(dirname "$spec")" -D "dist $DIST_TAG" -D "with_check 1" --queryformat="[%{EXCLUSIVEARCH} ]\n" --srpm "$spec" 2>/dev/null | grep -qP "\b$CURRENT_ARCH\b"
    then
        echo "$spec" >> "$TEMP_FILE"
    fi
done

rm -f "$OUTPUT"
while read -r spec
do
    rpmspec -q -D "_sourcedir $(dirname "$spec")" -D "dist $DIST_TAG" -D "with_check 1" --builtrpms "$spec" >> "$OUTPUT" 2>/dev/null
done < "$TEMP_FILE"

echo "Finished building RPMs snapshot."
