#!/usr/bin/bash
set -e

NAME=$(basename $(pwd))
VERSION=$(rpmspec -q $NAME.spec --srpm --qf "%{version}")

if [ -z "$VERSION" ]
then
    echo "Usage: ./make_tarball.sh {version}"
    exit 1
fi

URL="https://openal-soft.org/openal-releases"
TARBALL_DIR="$NAME-$VERSION"
TARBALL_ORIG="$NAME-$VERSION.tar.bz2"
TARBALL_NEW="$NAME-$VERSION-clean.tar.xz"

echo "Downloading upstream tarball..."
curl -O "$URL/$TARBALL_ORIG"

echo "Unpacking upstream tarball..."
tar -xvf "$TARBALL_ORIG"

echo  "Removing bundled components..."
rm -rfv $NAME-$VERSION/fmt-*/

echo "Removing non-free components..."
rm -rfv $NAME-$VERSION/utils/*.def

echo "Building a new tarball..."
tar -cJvf "$TARBALL_NEW" "$TARBALL_DIR"

echo "Performing cleanup..."
rm -rfv "$TARBALL_ORIG"
rm -rfv "$TARBALL_DIR"

echo "Done."
