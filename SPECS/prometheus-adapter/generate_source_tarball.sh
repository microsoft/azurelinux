#!/bin/bash

# The flow of this script is as such:
# 1. Download prometheus-adapter tarball to a temp working directory and extract it.
# 2. Then we run go mod vendor.
# 3. We tar the updated prometheus-adapter

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
go mod vendor

cd "$TEMPDIR"
tar -czf "$OUT_FOLDER/prometheus-adapter-$PKG_VERSION.tar.gz" "prometheus-adapter-$PKG_VERSION"
cd "$START_DIR"
rm -rf "$TEMPDIR"
echo "Source tarball $OUT_FOLDER/prometheus-adapter-$PKG_VERSION.tar.gz successfully created!"