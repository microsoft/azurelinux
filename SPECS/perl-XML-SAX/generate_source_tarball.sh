#!/bin/bash

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

echo '-- Perl-XML-SAX source tarball creation'
cd $TEMPDIR
if [ -z "$SRC_TARBALL" ]; then
    echo "download source tarball"
    TARBALL_NAME="XML-SAX-$PKG_VERSION.tar.gz"
    wget "http://www.cpan.org/authors/id/G/GR/GRANTM/$TARBALL_NAME"
    SRC_TARBALL="$TEMPDIR/$TARBALL_NAME"
fi
tar -xzf $SRC_TARBALL

# xmltest.xml could not be distributed due to copyright
rm XML-SAX-$PKG_VERSION/testfiles/xmltest.xml
rm XML-SAX-$PKG_VERSION/t/16large.t
sed -i -e '/testfiles\/xmltest.xml/ d' XML-SAX-$PKG_VERSION/MANIFEST
sed -i -e '/t\/16large.t/ d' XML-SAX-$PKG_VERSION/MANIFEST

# make sure new tarball file does not exist and create new tarball
NEW_TARBALL="$OUT_FOLDER/$(basename $SRC_TARBALL)"
rm -f $NEW_TARBALL
# Create a reproducible tarball
# Credit to https://reproducible-builds.org/docs/archives/ for instructions
# Do not update mtime value for new versions- keep the same value for ease of
# reproducing old tarball versions in the future if necessary
echo "Create $NEW_TARBALL tarball"
tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -zcf $NEW_TARBALL  XML-SAX-$PKG_VERSION

