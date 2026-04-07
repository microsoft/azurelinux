#!/bin/bash

# This script is intended to make a xine-lib snapshot.
# If no argument is provided, it will make a snapshot of HEAD.
# If the svn revision is provided as an argument, it will make a snapshot of
# this revision.

TMPDIR=$(mktemp -d)
pushd "$TMPDIR" || exit
echo -n "Cloning xine-lib-1.2 "
[ -n "$1" ] && echo "revision $1" || echo "HEAD"
[ -n "$1" ] && OPT="-u $1 " || OPT=""
hg clone $OPT http://hg.code.sf.net/p/xine/xine-lib-1.2 xine-lib-1.2
cd xine-lib-1.2 || exit
autoreconf -vif
./configure
make dist
popd || exit
cp -p "$TMPDIR"/xine-lib-1.2/xine-lib-1.2*.tar.xz .
rm -rf "$TMPDIR"
