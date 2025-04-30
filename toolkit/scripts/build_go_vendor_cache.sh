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
# --vendorVersion : vendor version
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
        --vendorVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            VENDOR_VERSION=$2
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

if [ -z "$SRC_TARBALL" ]; then
    echo "--srcTarball parameter cannot be empty"
    exit 1
fi

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

if [ -z "$VENDOR_VERSION" ]; then
    echo "--vendorVersion parameter cannot be empty"
    exit 1
fi

echo "--srcTarball      -> $SRC_TARBALL"
echo "--outFolder       -> $OUT_FOLDER"
echo "--pkgVersion      -> $PKG_VERSION"
echo "--vendorVersion   -> $VENDOR_VERSION"

temp_dir=$(mktemp -d)
echo "Working in temporary directory '$temp_dir'."
function clean-up {
    echo "Cleaning up temporary directory '$temp_dir'."
    rm -rf "$temp_dir"
}
trap clean-up EXIT

tarball_name=$(basename "$SRC_TARBALL")

cache_name=${tarball_name%.*}
if [[ "$cache_name" =~ \.tar$ ]]
then
    cache_name=${cache_name%.*}
fi

cache_tarball_name="$cache_name-$PKG_VERSION-govendor-v$VENDOR_VERSION.tar.gz"

if [[ -f "$tarball_name" ]]
then
    cp "$SRC_TARBALL" "$temp_dir"
else
    echo "Tarball '$tarball_name' doesn't exist. Will attempt to download from blobstorage."
    if ! wget -q "https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/$tarball_name" -O "$temp_dir/$tarball_name"
    then
        echo "ERROR: failed to download the source tarball."
        exit 1
    fi
    echo "Download successful."
fi

pushd "$temp_dir" &> /dev/null
    echo "Extracting $tarball_name."

    tar -xf "$tarball_name"

    directory_name=($(ls -d */))

    # assume there is only one directory in the tarball
    directory_name=${directory_name[0]%//}

    pushd "$directory_name" &> /dev/null
        echo "Fetching dependencies to a temporary cache in $directory_name."
        go mod vendor

        echo "Compressing the cache."
        tar  --sort=name \
            --mtime="2021-04-26 00:00Z" \
            --owner=0 --group=0 --numeric-owner \
            --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
            -czf "$cache_tarball_name" vendor
    popd &> /dev/null
popd &> /dev/null

mv "$temp_dir/$directory_name/$cache_tarball_name" "$OUT_FOLDER"

echo "Done:"
sha256sum "$OUT_FOLDER"/"$cache_tarball_name"
