#!/bin/bash
# Get upstream zip and make source tar.gz

ARCHIVE="open-sans-fonts-1.10"
TMPDIR=$(mktemp -d --tmpdir=/var/tmp getopensans-XXXXXXXXXX)
[ $? != 0 ] && exit 1
umask 022
pushd "$TMPDIR"

wget -N -O $ARCHIVE.zip http://www.google.com/fonts/download?kit=3hvsV99qyKCBS55e5pvb3ltkqrIMaAZWyLYEoB48lSQ
unzip $ARCHIVE.zip -d $ARCHIVE
tar -cvJf "$ARCHIVE.tar.xz" $ARCHIVE

popd
mv "$TMPDIR/$ARCHIVE.tar.xz" .
rm -fr "$TMPDIR"