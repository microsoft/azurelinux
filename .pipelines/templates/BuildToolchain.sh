#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

function populate_raw_toolchain {
    local architecture
    local cache_sha256
    local expected_raw_toolchain_hash
    local raw_toolchain_cache_url
    local raw_toolchain_file_path
    local root_folder

    root_folder="$1"

    architecture=$(uname -m)
    raw_toolchain_cache_url="https://cblmarinerstorage.blob.core.windows.net/rawtoolchaincache/toolchain_from_container_2.0.20220709_$architecture.tar.gz"
    raw_toolchain_file_path="$root_folder/build/toolchain/toolchain_from_container.tar.gz"

    # ARM64 hash.
    expected_raw_toolchain_hash="65de43b3bdcfdaac71df1f11fd1f830a8109b1eb9d7cb6cbc2e2d0e929d0ef76"
    if [[ $architecture == "x86_64" ]]; then
        expected_raw_toolchain_hash="f56df34b90915c93f772d3961bf5e9eeb8c1233db43dd92070214e4ce6b72894"
    fi

    echo "-- Downloading cached raw toolchain from '$raw_toolchain_cache_url'."

    mkdir -p "$(dirname "$raw_toolchain_file_path")"
    wget --quiet --timeout=30 --continue "$raw_toolchain_cache_url" -O "$raw_toolchain_file_path"
    if [[ ! -f "$raw_toolchain_file_path" ]]; then
        echo "-- ERROR: failed to download raw toolchain cache." >&2
        return 1
    fi

    # Verifying toolchains SHA-256 hash.
    cache_sha256=$(sha256sum "$raw_toolchain_file_path" | cut -d' ' -f1)
    echo "-- Raw toolchain hash: $cache_sha256"
    if [[ "$cache_sha256" != "$expected_raw_toolchain_hash" ]]; then
        echo "-- ERROR: raw toolchain hash verification failed. Expected ($expected_raw_toolchain_hash). Got ($cache_sha256)." >&2
        return 1
    fi

    touch "$raw_toolchain_file_path"
}

ROOT_FOLDER=$(git rev-parse --show-toplevel)
BUILD_LOG_DIR=$ROOT_FOLDER/build/logs/toolchain
TOOLKIT_DIR="$ROOT_FOLDER/toolkit"

# Parameters:
#
# -b -> build artifacts directory

while getopts "b:" OPTIONS; do
    case "${OPTIONS}" in
    b) BUILD_ARTIFACT_FOLDER=$OPTARG ;;

    *)
        echo "-- ERROR: invalid option '$OPTARG'" >&2
        exit 1
        ;;
    esac
done

echo "-- BUILD_ARTIFACT_FOLDER      -> $BUILD_ARTIFACT_FOLDER"
echo

if ! populate_raw_toolchain "$ROOT_FOLDER"; then
    echo "-- ERROR: failed to populate the cached raw toolchain." >&2
    exit 1
fi

if sudo make -C "$TOOLKIT_DIR" "-j$(nproc)" toolchain QUICK_REBUILD=y; then
    BUILD_SUCCEEDED=true

    echo =========================
    echo Toolchain built correctly
    echo =========================

    cp "$ROOT_FOLDER"/build/toolchain/toolchain_built_{,s}rpms_all.tar.gz "$BUILD_ARTIFACT_FOLDER"
else
    BUILD_SUCCEEDED=false

    if [[ -f "$BUILD_LOG_DIR/failures.txt" ]]; then
        echo =================================
        echo List of RPMs that failed to build
        echo =================================
        cat "$BUILD_LOG_DIR/failures.txt"
    else
        echo ==============================
        echo Build failed - no specific RPM
        echo ==============================
    fi
fi

# Always publish logs
tar -C "$BUILD_LOG_DIR" -czf "$BUILD_ARTIFACT_FOLDER/toolchain.logs.tar.gz" .

$BUILD_SUCCEEDED
