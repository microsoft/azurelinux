#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

source ../common/libs/rpm_tools.sh

set -e

# Enables extended globbing patterns like '+([0-9])'.
shopt -s extglob

# Enables the '**' recursive globbing pattern.
shopt -s globstar

# Script parameters:
#
# -a -> artifacts directory where the RPMs archive is located
while getopts "a:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

rpms_archive="$(find "$ARTIFACTS_DIR" -name '*rpms.tar.gz' -type f -print -quit)"
if [[ ! -f "$rpms_archive" ]]
then
    echo "ERROR: No RPMs archive found in '$ARTIFACTS_DIR'." >&2
    exit 1
fi

tmpdir=$(mktemp -d)
function cleanup {
    echo " Cleaning up '$tmpdir'."
    rm -rf "$tmpdir"
}
trap cleanup EXIT

tar -C "$tmpdir" -xf "$rpms_archive"

for livepatch_rpm in "$tmpdir"/**/livepatch-*cm2-+([0-9])*.rpm
do
    rpm_extract_files "$livepatch_rpm" "*.ko" "$tmpdir"
done
