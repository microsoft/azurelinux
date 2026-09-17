#!/bin/bash

# The flow of this script is as such:
# 1. Download prometheus-adapter tarball to a temp working directory and extract it.
# 2. Bump the modules carrying CVE fixes (grpc, cel-go and their transitive deps).
# 3. Then we run go mod vendor.
# 4. We tar the resulting vendor/ tree only.
#
# The upstream Source0 tarball is left untouched; this script produces the
# companion vendor tarball (Source1) that the spec unpacks over it.

set -e

SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_VERSION=""

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
TEMPDIR=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $TEMPDIR"
    rm -rf $TEMPDIR
}
trap cleanup EXIT

echo "Starting Prometheus-Adapter source tarball creation"
ADAPTER_URL="https://github.com/kubernetes-sigs/prometheus-adapter/archive/refs/tags/v$PKG_VERSION.tar.gz"

cd "$TEMPDIR"
# sudo chown -R "$USER": .
wget -c $ADAPTER_URL -O "prometheus-adapter-$PKG_VERSION.tar.gz"
tar -xzf "prometheus-adapter-$PKG_VERSION.tar.gz"
cd "prometheus-adapter-$PKG_VERSION"

# Bump the modules carrying the CVE fixes. grpc v1.83.2 requires go >= 1.25 and
# x/crypto v0.57.0 requires go >= 1.26, so raise the language level to match.
go mod edit -go=1.26.0
go mod edit \
    -require=google.golang.org/grpc@v1.83.2 \
    -require=github.com/google/cel-go@v0.31.0

go mod tidy
go mod vendor

# Ship only the vendor tree; Source0 stays pristine and the go.mod/go.sum
# changes are carried by the spec's patches.
tar -czf "$OUT_FOLDER/prometheus-adapter-$PKG_VERSION-vendor.tar.gz" vendor

cd "$START_DIR"
rm -rf "$TEMPDIR"
echo "Vendor tarball $OUT_FOLDER/prometheus-adapter-$PKG_VERSION-vendor.tar.gz successfully created!"