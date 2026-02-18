#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

#
# The nodejs source tarball contains a copy of the OpenSSL source tree.
# OpenSSL contains patented algorithms that should not be distributed
# as part of the SRPM. Since we use the shared OpenSSL libraries, we 
# can just remove the entire OpenSSL source tree from the tarball.

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

pushd $tmpdir > /dev/null

namever="node-v${PKG_VERSION}"

if [[ -n $SRC_TARBALL ]]; then
    upstream_tarball_name="$SRC_TARBALL"
    clean_tarball_name="$OUT_FOLDER/$(basename $SRC_TARBALL)"
else
    upstream_tarball_name="${namever}.tar.xz"
    clean_tarball_name="$OUT_FOLDER/${namever}-clean.tar.xz"
    download_url="https://nodejs.org/download/release/v${PKG_VERSION}/${upstream_tarball_name}"

    echo "Downloading upstream source tarball..."
    curl -s -O $download_url
fi

echo "Unpacking upstream source tarball..."
tar -xf $upstream_tarball_name

echo "Removing bad vendored dependencies from source tree..."
rm -rf ./$namever/deps/openssl/openssl

# Create a reproducible tarball
# Credit to https://reproducible-builds.org/docs/archives/ for instructions
# Do not update mtime value for new versions- keep the same value for ease of
# reproducing old tarball versions in the future if necessary
echo "Repacking source tarball..."
tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -cJf $clean_tarball_name ./$namever

popd > /dev/null
echo "Clean nodejs source tarball available at $clean_tarball_name"
