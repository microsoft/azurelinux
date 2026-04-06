#! /bin/sh

# This script builds the PDF version of the libconfig documentation.
# Inspired by the PostgreSQL package.

set -e

# Pass package version and name optionally as argument
VERSION=$1
PKGNAME=${2-libconfig}

test -z "$VERSION" && VERSION=`awk '/^Version:/ { print $2; }' "$PKGNAME".spec`

TARGETFILE=`readlink -f "$PKGNAME-$VERSION.pdf"`
test -f "$TARGETFILE" && echo "$TARGETFILE exists" && exit 1

echo Building $TARGETFILE ...

tar xf "$PKGNAME"-$VERSION.tar.*
cd "$PKGNAME"-$VERSION

# Apply any patches that affect the PDF documentation
# patch -p1 < ../xxx.patch

# Build the PDF docs
./configure >/dev/null
make pdf
mv -f doc/libconfig.pdf "$TARGETFILE"

exit 0
