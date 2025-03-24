#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENDOR_VERSION="1"

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
# --vendorVersion : vendor version

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

echo "--srcTarball      -> $SRC_TARBALL"
echo "--outFolder       -> $OUT_FOLDER"
echo "--pkgVersion      -> $PKG_VERSION"
echo "--vendorVersion   -> $VENDOR_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

if [ -z "$VENDOR_VERSION" ]; then
    echo "--vendorVersion parameter cannot be empty"
    exit 1
fi

function generate_vendor {
    local pkg_name=$1
    local pkg_version=$2
    local checkout_tags=$3
    local folder_name=$4
    local git_url=$5

    # makesure we get the correct git url
    local git_url_clone
    git_url_clone=$(echo "$git_url" | grep -oP '^https://github\.com/[^/]+/[^/]+')

    local branch_name="$pkg_name-$pkg_version"

    echo "cloning $git_url_clone"

    git clone --depth 1 "$git_url_clone" -b "$pkg_name-$pkg_version"

    pushd $folder_name &> /dev/null

    if [[ "$checkout_tags" = "true" ]]; then
        git fetch --all --tags

        echo "checkout tags $branch_name and make branch $branch_name"
        git checkout tags/v"$pkg_version" -b "$branch_name"
    fi

    echo "fetching submodules with depth 1, recursive"
    git submodule update --depth 1 --init --recursive
    popd

    echo "move $folder_name to $branch_name"
    # move the vendored files to the correct location
    mv $folder_name $branch_name
}

echo "-- create temp folder"
TEMP_DIR=$(mktemp -d)
function cleanup {
    echo "cleanup -> remove $TEMP_DIR"
    rm -rf $TEMP_DIR
}
trap cleanup EXIT

pushd $TEMP_DIR > /dev/null

TARBALL_NAME=$(basename "$SRC_TARBALL")

NAME_VER=${TARBALL_NAME%.*}
if [[ "$NAME_VER" =~ \.tar$ ]]
then
    NAME_VER=${NAME_VER%.*}
fi

VENDOR_TARBALL="$NAME_VER-cargovendor-v$VENDOR_VERSION.tar.gz"

if [[ -f "$TARBALL_NAME" ]]
then
    cp "$SRC_TARBALL" "$TEMP_DIR"
else
    echo "Tarball '$TARBALL_NAME' doesn't exist. Will attempt to download from blobstorage."
    if ! wget -q "https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/$TARBALL_NAME" -O "$TEMP_DIR/$TARBALL_NAME"
    then
        echo "ERROR: failed to download the source tarball."
        exit 1
    fi
    echo "Download successful."
fi

echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL

echo "Vendor cargo ..."
DIRECTORY_NAME=($(ls -d */))

# assume there is only one directory in the tarball
DIRECTORY_NAME=${DIRECTORY_NAME[0]%//}

pushd "$DIRECTORY_NAME" &> /dev/null
echo "Fetching dependencies to a temporary cache in $DIRECTORY_NAME."
generate_vendor $PKG_NAME $PKG_VERSION $CHECKOUT_TAGS $SUBMODULE_DIRECTORY_NAME

echo ""
echo "========================="
echo "Tar vendored tarball"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -I pigz -cf "$VENDOR_TARBALL" $SUBMODULE_DIRECTORY_NAME

cp $VENDOR_TARBALL $OUT_FOLDER
popd > /dev/null
echo "$NAME_VER vendored modules are available at $VENDOR_TARBALL"
