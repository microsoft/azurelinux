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
    # rm -rf $tmpdir
}
trap cleanup EXIT

tarball_folder="$tmpdir/tarballFolder"
mkdir -p $tarball_folder

pushd $tmpdir > /dev/null

PKG_NAME="etcd"
NAME_VER="$PKG_NAME-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-vendor.tar.gz"

echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL

cd "$NAME_VER"
echo "Get vendored modules"
for component in server etcdctl etcdutl; do
    pushd $component
    echo "==================================="
    echo "Get vendored modules for $component"
    go mod vendor

    component_tarball="$tarball_folder/vendor-$component.tar.gz"
    echo ""
    echo "Tar vendored modules in $component_tarball"
    tar  --sort=name \
        --mtime="2021-04-26 00:00Z" \
        --owner=0 --group=0 --numeric-owner \
        --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
        -cf "$component_tarball" vendor
    popd
done

for component in etcd-dump-db etcd-dump-logs; do
    pushd tools/$component
    echo "==================================="
    echo "Get vendored modules for $component"
    go mod init go.etcd.io/etcd/tools/$component/v3
    go mod tidy
    go mod vendor

    echo ""
    echo "Prepare files to tar"
    tmp_tarball_dir="$tmpdir/$component"
    mkdir -p $tmp_tarball_dir
    cp go.mod $tmp_tarball_dir
    cp go.sum $tmp_tarball_dir
    cp -r vendor $tmp_tarball_dir

    component_tarball="$tarball_folder/vendor-$component.tar.gz"
    cd $tmp_tarball_dir
    echo "Tar vendored modules in $component_tarball"
    tar  --sort=name \
        --mtime="2021-04-26 00:00Z" \
        --owner=0 --group=0 --numeric-owner \
        --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
        -cf "$component_tarball" .
    popd
done

echo ""
echo "========================="
echo "Tar all vendored tarballs"
cd $tarball_folder
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "$VENDOR_TARBALL" .

popd > /dev/null
echo "Etcd vendored modules are available at $VENDOR_TARBALL"
