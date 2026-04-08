#!/bin/bash
#
# This script removes non-linux dialects from upstream source package before
# release.  There is a problem with copyrights for some UN*Xes ... also .. this
# script merges all to the one normal tarball and rename all to lsof_X.XX-rh.
#
# Usage:  ./upstream2downstream  <usptream-tarball>
# 
# This code is in the public domain; do with it what you wish.
#
# Copyright (C) 2007 Karel Zak <kzak@redhat.com>
#

UPSTREAM="$1"
NAME=$(basename $UPSTREAM .tar.gz)
MYPWD=$(pwd)
TMP=$(mktemp -d)

echo
echo -n "Extracting upstream code..."
tar -xf $UPSTREAM  -C $TMP
cd $TMP/$NAME
echo " done."

echo -n "Removing non-Linux dialects..."
rm -rf ./dialects/{aix,darwin,du,freebsd,hpux,n+obsd,n+os,osr,sun,uw}
echo " done."

echo -n "Removing unused distribution scripts..."
rm -rf ./support
echo " done."

echo -n "Creating final downstream tarball..."
cd ..
mv $NAME $NAME-rh
tar Jcf $MYPWD/"$NAME"-rh.tar.xz "$NAME"-rh
echo " done."

rm -rf $TMP
cd $MYPWD

echo
echo "Linux-only tarball: $MYPWD/"$NAME"-rh.tar.xz"
echo

