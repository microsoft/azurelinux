#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ROOT_FOLDER=$(git rev-parse --show-toplevel)
ARCHITECTURE=$(uname -m)
BUILD_LOG_DIR=$ROOT_FOLDER/build/logs/toolchain
TOOLCHAIN_FROM_CONTAINER_TARBALL="$ROOT_FOLDER/build/toolchain/toolchain_from_container.tar.gz"
TOOLKIT_DIR="$ROOT_FOLDER/toolkit"

echo "-- Toolchain build for the $ARCHITECTURE architecture."

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

# ARM64 hash.
EXPECTED_RAW_TOOLCHAIN_HASH="65de43b3bdcfdaac71df1f11fd1f830a8109b1eb9d7cb6cbc2e2d0e929d0ef76"
if [[ $ARCHITECTURE == "x86_64" ]]; then
    EXPECTED_RAW_TOOLCHAIN_HASH="f56df34b90915c93f772d3961bf5e9eeb8c1233db43dd92070214e4ce6b72894"
fi
RAW_TOOLCHAIN_CACHE_URL="https://cblmarinerstorage.blob.core.windows.net/rawtoolchaincache/toolchain_from_container_2.0.20220709_$ARCHITECTURE.tar.gz"
RAW_TOOLCHAIN_CACHE_LOCALFILE=$ROOT_FOLDER/build/toolchain/toolchain_from_container.tar.gz

echo "-- Downloading cached raw toolchain from '$RAW_TOOLCHAIN_CACHE_URL'."

sudo mkdir -pv "$ROOT_FOLDER/build/toolchain"
sudo wget -nv --timeout=30 --continue "$RAW_TOOLCHAIN_CACHE_URL" -o "$RAW_TOOLCHAIN_CACHE_LOCALFILE"
if [[ ! -f "$RAW_TOOLCHAIN_CACHE_LOCALFILE" ]]; then
    echo "-- ERROR: failed to download raw toolchain cache." >&2
    exit 1
fi

touch "$RAW_TOOLCHAIN_CACHE_LOCALFILE"

# Verifying toolchains SHA-256 hash.
CACHE_SHA256=$(sha256sum "$RAW_TOOLCHAIN_CACHE_LOCALFILE" | cut -d' ' -f1)
echo "-- Raw toolchain hash: $CACHE_SHA256"
if [[ "$CACHE_SHA256" != "$EXPECTED_RAW_TOOLCHAIN_HASH" ]]; then
    echo "-- ERROR: raw toolchain hash verification failed. Expected ($EXPECTED_RAW_TOOLCHAIN_HASH). Got ($CACHE_SHA256)." >&2
    exit 1
fi

if sudo make -C "$TOOLKIT_DIR" toolchain QUICK_REBUILD=y
then
    BUILD_SUCCEEDED=true
    echo =========================
    echo Toolchain built correctly
    echo =========================
else
    BUILD_SUCCEEDED=false
    if [[ -f "$BUILD_LOG_DIR/failures.txt" ]]; then
        echo =================================
        echo List of RPMs that failed to build
        echo =================================
        sudo cat "$BUILD_LOG_DIR/failures.txt"
    else
        echo ==============================
        echo Build failed - no specific RPM
        echo ==============================
    fi
fi

# Always publish logs
tar -C "$BUILD_LOG_DIR" -czf "$BUILD_ARTIFACT_FOLDER/toolchain.logs.tar.gz" .

# Always attempt to publish toolchain_from_container and manifests
if [[ -f "$TOOLCHAIN_FROM_CONTAINER_TARBALL" ]]
then
    cp "$TOOLCHAIN_FROM_CONTAINER_TARBALL" "$BUILD_ARTIFACT_FOLDER"
fi

MANIFESTS_OUTPUT_DIR="$BUILD_ARTIFACT_FOLDER/manifests"
mkdir -p "$MANIFESTS_OUTPUT_DIR"
cp ./toolkit/resources/manifests/package/{pkggen_core,toolchain}_"$ARCHITECTURE".txt "$MANIFESTS_OUTPUT_DIR"
if [[ -f ./build/logs/toolchain/downloads/download_manifest.txt ]]; then
    cp ./build/logs/toolchain/downloads/download_manifest.txt "$MANIFESTS_OUTPUT_DIR"
fi

if $BUILD_SUCCEEDED
then
    cp "$ROOT_FOLDER/build/toolchain/toolchain_built_{,s}rpms_all.tar.gz" "$BUILD_ARTIFACT_FOLDER"
fi

$BUILD_SUCCEEDED
