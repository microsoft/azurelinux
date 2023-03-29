#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

get_param() {
    if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        echo "$2"
    else
        echo "Error: argument for ($1) is missing." >&2
        return 1
    fi
}

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --srcTarball  : src tarball file
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
#
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        SRC_TARBALL="$(get_param "$1" "$2")"
        shift 2
        ;;
        --outFolder)
        OUT_FOLDER="$(get_param "$1" "$2")"
        shift 2
        ;;
        --pkgVersion)
        PKG_VERSION="$(get_param "$1" "$2")"
        shift 2
        ;;
        -*)
        echo "Error: unsupported flag $1." >&2
        exit 1
        ;;
  esac
done

echo "--srcTarball   -> $SRC_TARBALL"
echo "--outFolder    -> $OUT_FOLDER"
echo "--pkgVersion   -> $PKG_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "Error: --pkgVersion parameter cannot be empty." >&2
    exit 1
fi

if [ ! -f "$SRC_TARBALL" ]; then
    echo "Error: --srcTarball is not a file." >&2
    exit 1
fi

SRC_TARBALL="$(realpath "$SRC_TARBALL")"
OUT_FOLDER="$(realpath "$OUT_FOLDER")"

echo "Creating a tempdir."
tmpdir=$(mktemp -d)
function cleanup {
    echo "Clean-up: removing tempdir ($tmpdir)."
    rm -rf "$tmpdir"
}
trap cleanup EXIT

pushd "$tmpdir" > /dev/null

NAME_VER="telegraf-$PKG_VERSION"
VENDOR_TARBALL="$(realpath "$OUT_FOLDER/$NAME_VER-vendor.tar.gz")"

echo "Unpacking the source tarball."
tar -xf "$SRC_TARBALL"

cd "$NAME_VER"
echo "Getting the vendored modules."
go mod vendor

mkdir -p "$OUT_FOLDER"

echo "Tar vendored modules."
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "$VENDOR_TARBALL" vendor

echo "Telegraf vendored modules are available at ($VENDOR_TARBALL)."
echo "SHA256: $(sha256sum "$VENDOR_TARBALL")."
