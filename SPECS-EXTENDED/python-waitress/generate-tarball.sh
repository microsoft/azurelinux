#!/bin/sh

VERSION=$1

tar -xzvf v$VERSION.tar.gz
rm -rf waitress-$VERSION/docs
mv waitress-$VERSION waitress-$VERSION-nodocs
tar -czvf v$VERSION-nodocs.tar.gz waitress-$VERSION-nodocs
