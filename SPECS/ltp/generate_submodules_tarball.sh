#!/bin/bash

set -e

SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_VERSION=""

function arg_present_check {
    if [[ -z "$2" || "${2:0:1}" == "-" ]]; then
        echo "Error: Argument for $1 is missing" >&2
        exit 1
    fi
}

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
        arg_present_check "$1" "$2"

        SRC_TARBALL=$2
        shift 2
        ;;

        --outFolder)
        arg_present_check "$1" "$2"

        OUT_FOLDER=$2
        shift 2
        ;;

        --pkgVersion)
        arg_present_check "$1" "$2"

        PKG_VERSION=$2
        shift 2
        ;;

        -*) # unsupported flags
        echo "Error: Unsupported flag ($1)" >&2
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
    rm -rf "$TEMPDIR"
}
trap cleanup EXIT

echo 'Starting LTP submodules source tarball creation.'

git -C "$TEMPDIR" clone --depth 1 git@github.com:linux-test-project/ltp.git -b "$PKG_VERSION"
git -C "$TEMPDIR"/ltp submodule update --init

if [[ -n $SRC_TARBALL ]]; then
    TARBALL_NAME="$(basename "$SRC_TARBALL")"
else
    TARBALL_NAME="ltp_submodules-$PKG_VERSION.tar.gz"
fi

NEW_TARBALL="$OUT_FOLDER/$TARBALL_NAME"

# Create a reproducible tarball
# Credit to https://reproducible-builds.org/docs/archives/ for instructions
# Do not update mtime value for new versions- keep the same value for ease of
# reproducing old tarball versions in the future if necessary
tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -C "$TEMPDIR"/ltp -zcf "$NEW_TARBALL" testcases/kernel/mce-test tools/sparse/sparse-src

echo "Submodules source tarball ($NEW_TARBALL) successfully created!"
echo "SHA-256: $(sha256sum "$NEW_TARBALL")"
