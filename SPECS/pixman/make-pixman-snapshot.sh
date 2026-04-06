#!/bin/sh

DIRNAME=pixman-$( date +%Y%m%d )

rm -rf $DIRNAME
git clone git://git.freedesktop.org/git/pixman $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git log | head -1
else
    git checkout $1
fi
rm -rf .git
cd ..
tar jcf $DIRNAME.tar.bz2 $DIRNAME
rm -rf $DIRNAME
