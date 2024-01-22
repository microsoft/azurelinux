#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

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

echo 'Starting maven cache tarball creation'
cp maven_build_caches.sh $TEMPDIR
cd $TEMPDIR
echo $PWD
sh ./maven_build_caches.sh -v $PKG_VERSION

TARBALL_NAME="maven-$PKG_VERSION-caches.tar.gz"

NEW_TARBALL="$OUT_FOLDER/$TARBALL_NAME"

# Create a reproducible tarball
# Credit to https://reproducible-builds.org/docs/archives/ for instructions
# Do not update mtime value for new versions- keep the same value for ease of
# reproducing old tarball versions in the future if necessary

# script outputs caches in HOME
cd $HOME/

tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -zcf $NEW_TARBALL mavenCaches

popd

echo "Source tarball $NEW_TARBALL successfully created!"
