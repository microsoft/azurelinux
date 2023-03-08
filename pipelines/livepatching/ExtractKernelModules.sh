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
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

if [[ -f "$OUTPUT_DIR" ]]
then
    echo "ERROR: output path ($OUTPUT_DIR) is a file. Expected a directory." >&2
    exit 1
fi

if [[ -z "$OUTPUT_DIR" ]]
then
    echo "ERROR: output directory not specified." >&2
    exit 1
fi

rpms_archive="$(find "$ARTIFACTS_DIR" -name '*rpms.tar.gz' -type f -print -quit)"
if [[ ! -f "$rpms_archive" ]]
then
    echo "ERROR: No RPMs archive found in '$ARTIFACTS_DIR'." >&2
    exit 1
fi

tmpdir="$(prepare_temp_dir)"

tar -C "$tmpdir" -xf "$rpms_archive"

rpm_extract_files -f -i "$tmpdir" -p "*.ko" -o "$OUTPUT_DIR" -w "$tmpdir"
