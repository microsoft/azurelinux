#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/libs/file_tools.sh
source "$ROOT_DIR"/pipelines/common/libs/file_tools.sh

# shellcheck source=../common/libs/rpm_tools.sh
source "$ROOT_DIR"/pipelines/common/libs/rpm_tools.sh

set -e

# Script parameters:
#
# -a -> artifacts directory where the RPMs archive is located.
# -o -> output directory where the RPMs will be extracted.
while getopts "a:o:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    o ) OUTPUT_DIR=$OPTARG ;;

    \? )
        echo "ERROR: Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "ERROR: Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

rpms_archive="$(find_file_fullpath "$ARTIFACTS_DIR" "rpms.tar.gz")"
if [[ ! -f "$rpms_archive" ]]
then
    echo "ERROR: No RPMs archive found in '$ARTIFACTS_DIR'." >&2
    exit 1
fi

TEMP_DIR="$(mktemp -d)"
trap temp_dir_cleanup EXIT

tar -C "$TEMP_DIR" -xf "$rpms_archive"

rpm_extract_files -f -i "$TEMP_DIR" -p "*.ko" -o "$OUTPUT_DIR" -w "$TEMP_DIR"
