#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Creates the vendored Rust crates tarball (Source1) of kata-nvrc from its
# source tarball (Source0). The output is reproducible: rerunning this script
# on the same source tarball produces the same file, whose sha256 is the one in
# kata-nvrc.signatures.json.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --srcTarball    : src tarball file (Source0)
# --outFolder     : folder where to copy the new tarball
# --pkgVersion    : <upstream version>-<short commit>, e.g. 0.1.7-77ce29c
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

SRC_TARBALL=$(readlink -f "$SRC_TARBALL")
OUT_FOLDER=$(readlink -f "$OUT_FOLDER")

PKG_NAME="kata-nvrc"
VENDOR_TARBALL="$OUT_FOLDER/$PKG_NAME-$PKG_VERSION-vendor.tar.gz"

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf "$tmpdir"
}
trap cleanup EXIT

pushd "$tmpdir" > /dev/null

echo "Unpacking source tarball..."
tar -xf "$SRC_TARBALL"
cd nvrc-*

echo "Vendor rust crates..."
cargo vendor --locked vendor > /dev/null

echo "Tar vendored tarball"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf - vendor | gzip -9 -n > "$VENDOR_TARBALL"

popd > /dev/null
echo "$PKG_NAME vendored crates are available at $VENDOR_TARBALL"
