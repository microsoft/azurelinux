#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

root_folder=$(git rev-parse --show-toplevel)
build_log_dir=$root_folder/build/logs/toolchain
toolkit_dir="$root_folder/toolkit"

# Parameters:
#
# -b -> build artifacts directory

while getopts "b:" OPTIONS; do
    case "${OPTIONS}" in
    b) build_artifact_dir=$OPTARG ;;

    *)
        echo "-- ERROR: invalid option '$OPTARG'" >&2
        exit 1
        ;;
    esac
done

echo "-- build_artifact_dir      -> $build_artifact_dir"
echo

if sudo make -C "$toolkit_dir" "-j$(nproc)" toolchain QUICK_REBUILD=y; then
    BUILD_SUCCEEDED=true

    echo =========================
    echo Toolchain built correctly
    echo =========================

    cp "$root_folder"/build/toolchain/toolchain_built_{,s}rpms_all.tar.gz "$build_artifact_dir"
else
    BUILD_SUCCEEDED=false

    if [[ -f "$build_log_dir/failures.txt" ]]; then
        echo =================================
        echo List of RPMs that failed to build
        echo =================================
        cat "$build_log_dir/failures.txt"
    else
        echo ==============================
        echo Build failed - no specific RPM
        echo ==============================
    fi
fi

# Always publish logs
tar -C "$build_log_dir" -czf "$build_artifact_dir/toolchain.logs.tar.gz" .

$BUILD_SUCCEEDED
