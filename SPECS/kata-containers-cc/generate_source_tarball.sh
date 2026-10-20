#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# The cargo tarball ships three trees: the Rust ".cargo"/"vendor" pair produced by
# "cargo vendor-filterer" and the Go "src/runtime/vendor" tree produced by "go mod vendor".
# cargo-vendor-filterer restricts the Rust vendor tree to the Linux targets we actually
# build, which keeps the tarball a fraction of the size of a plain "cargo vendor".
RUST_TARGETS=("x86_64-unknown-linux-gnu" "aarch64-unknown-linux-gnu")

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

SRC_TARBALL=$(readlink -f "$SRC_TARBALL")
OUT_FOLDER=$(readlink -f "$OUT_FOLDER")

PKG_NAME="kata-containers"

if ! command -v cargo-vendor-filterer > /dev/null; then
    echo "Installing cargo-vendor-filterer..."
    cargo install --locked cargo-vendor-filterer
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT

TARBALL_FOLDER="$tmpdir/tarballFolder"
mkdir -p $TARBALL_FOLDER
cp $SRC_TARBALL $tmpdir

pushd $tmpdir > /dev/null

NAME_VER="$PKG_NAME-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-cargo.tar.gz"

echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL

cd $NAME_VER

echo "Vendor rust crates..."
mkdir -p .cargo
vendor_filterer_args=()
for target in "${RUST_TARGETS[@]}"; do
    vendor_filterer_args+=(--platform "$target")
done
cargo vendor-filterer "${vendor_filterer_args[@]}" --all-features vendor > .cargo/config.toml

echo "Vendor go modules..."
cd src/runtime
# Keep the vendor tree in sync with the grpc bump applied by CVE-2026-84304.patch.
go mod edit -require=google.golang.org/grpc@v1.83.2
go mod tidy
go mod vendor
cd ../..

echo ""
echo "========================="
echo "Tar vendored tarball"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -czf "$VENDOR_TARBALL" .cargo vendor src/runtime/vendor

popd > /dev/null
echo "$PKG_NAME vendored modules are available at $VENDOR_TARBALL"
