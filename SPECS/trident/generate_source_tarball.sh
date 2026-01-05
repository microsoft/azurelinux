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
# --srcTarball    : src tarball file
#                   this file contains the 'initial' source code of the component
#                   and should be replaced with the new/modified src code
# --outFolder     : folder where to copy the new tarball(s)
# --pkgVersion    : package version
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

echo "--srcTarball      -> $SRC_TARBALL"
echo "--outFolder       -> $OUT_FOLDER"
echo "--pkgVersion      -> $PKG_VERSION"

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

pushd $tmpdir > /dev/null

PKG_NAME="trident"
NAME_VER="$PKG_NAME-$PKG_VERSION"
VENDOR_PKG_NAME="trident"
VENDOR_NAME_VER="$VENDOR_PKG_NAME-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$VENDOR_NAME_VER-vendor.tar.gz"

# If source tarball is provided, use it; otherwise download it
if [ -n "$SRC_TARBALL" ]; then
    echo "Using provided source tarball: $SRC_TARBALL"
    cp "$SRC_TARBALL" .
    SOURCE_FILE=$(basename "$SRC_TARBALL")
else
    echo "Downloading source tarball..."
    SOURCE_FILE="$NAME_VER.tar.gz"
    wget https://github.com/microsoft/trident/archive/refs/tags/v$PKG_VERSION.tar.gz -O "$SOURCE_FILE"
fi

echo "Unpacking source tarball..."
tar -xf "$SOURCE_FILE"
cd "$NAME_VER"

echo "Generate vendored modules tarball"
cargo vendor

echo "Tar vendored modules"
tar  --sort=name \
     --mtime="2026-01-05 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "$VENDOR_TARBALL" vendor

popd > /dev/null
echo "$VENDOR_PKG_NAME vendored modules are available at $VENDOR_TARBALL"
