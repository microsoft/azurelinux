#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
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

echo "Copying golang-version-upgrade.patch to $tmpdir"
cp golang-version-upgrade.patch $tmpdir/

pushd $tmpdir > /dev/null

NAME_VER="cluster-api-provider-kubevirt-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-vendor.tar.gz"

echo "Downloading source tarball..."
wget https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt/archive/refs/tags/v$PKG_VERSION.tar.gz -O $NAME_VER.tar.gz

echo "Unpacking source tarball..."
tar -xf $NAME_VER.tar.gz

cp golang-version-upgrade.patch $NAME_VER/
cd "$NAME_VER"

echo "Applying Golang versioning patch"
git apply golang-version-upgrade.patch
go mod tidy

echo "Get vendored modules"
go mod vendor

echo "Tar vendored modules"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "$VENDOR_TARBALL" vendor

popd > /dev/null
echo "cloud-provider-kubevirt vendored modules are available at $VENDOR_TARBALL"