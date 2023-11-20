#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

echo "--srcTarball   -> $SRC_TARBALL"
echo "--outFolder    -> $OUT_FOLDER"
echo "--pkgVersion   -> $PKG_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT

src_folder="$tmpdir/srcFolder"
src_root="$src_folder/rustc-$PKG_VERSION-src"
temp_cache="$tmpdir/cacheFolder"
mkdir -p $src_folder
mkdir -p $temp_cache

pushd $src_folder > /dev/null
echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL
popd > /dev/null

pushd $src_root > /dev/null
echo "Fetching dependencies to a temporary cache"
# The build environment's rust may not have all the features required to run
# cargo fetch, so we need to use the bootstrap mode that disables some features.
export RUSTC_BOOTSTRAP=1
CARGO_HOME=$src_root/.cargo cargo fetch
echo "Compressing the cache."
tar --sort=name --mtime="2021-04-26 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime -cf \
    "$OUT_FOLDER/rustc-$PKG_VERSION-src-cargo.tar.gz" .cargo
popd > /dev/null

pushd $OUT_FOLDER > /dev/null
echo "get additional src tarballs"
CONFIG_FILE="$src_root/src/stage0.json"
RUST_RELEASE_DATE=$(cat $CONFIG_FILE | jq -r '.compiler.date')
RUST_STAGE0_VERSION=$(cat $CONFIG_FILE | jq -r '.compiler.version')
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/cargo-$RUST_STAGE0_VERSION-x86_64-unknown-linux-gnu.tar.xz
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/rustc-$RUST_STAGE0_VERSION-x86_64-unknown-linux-gnu.tar.xz
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/rust-std-$RUST_STAGE0_VERSION-x86_64-unknown-linux-gnu.tar.xz
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/cargo-$RUST_STAGE0_VERSION-aarch64-unknown-linux-gnu.tar.xz
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/rustc-$RUST_STAGE0_VERSION-aarch64-unknown-linux-gnu.tar.xz
wget https://static.rust-lang.org/dist/$RUST_RELEASE_DATE/rust-std-$RUST_STAGE0_VERSION-aarch64-unknown-linux-gnu.tar.xz


popd > /dev/null
echo "=========================="
echo "release date:   $RUST_RELEASE_DATE"
echo "stage0 version: $RUST_STAGE0_VERSION"
echo " "
echo "Rust additional src tarballs are available at $OUT_FOLDER"
ls -ls $OUT_FOLDER
