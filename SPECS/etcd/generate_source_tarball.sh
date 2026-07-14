#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

# etcd's go.mod files pin a newer Go release via the 'toolchain' directive than
# the base system Go. Default to automatic toolchain selection so 'go' fetches
# the required version on demand. An explicit GOTOOLCHAIN set by the caller wins.
export GOTOOLCHAIN="${GOTOOLCHAIN:-auto}"

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

# The dump tools are standalone modules that depend on etcd's in-tree modules.
# Point every etcd dependency at the local source (relative to tools/<component>)
# before running 'go mod tidy'. Without these replace rules, tidy resolves the
# etcd modules from the network, pulling newer releases that require an even
# newer Go toolchain and that have relocated packages (e.g. mvcc/backend,
# mvcc/buckets), which breaks the build.
etcd_local_modules=(
    "go.etcd.io/etcd/api/v3=../../api"
    "go.etcd.io/etcd/client/pkg/v3=../../client/pkg"
    "go.etcd.io/etcd/client/v2=../../client/v2"
    "go.etcd.io/etcd/client/v3=../../client/v3"
    "go.etcd.io/etcd/pkg/v3=../../pkg"
    "go.etcd.io/etcd/raft/v3=../../raft"
    "go.etcd.io/etcd/server/v3=../../server"
)
for component in etcd-dump-db etcd-dump-logs; do
    pushd tools/$component
    echo "==================================="
    echo "Get vendored modules for $component"
    go mod init go.etcd.io/etcd/tools/$component/v3
    for replace_rule in "${etcd_local_modules[@]}"; do
        go mod edit -replace "$replace_rule"
    done
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
