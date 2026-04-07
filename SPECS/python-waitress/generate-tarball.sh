#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $(basename $0) <VERSION>"
    exit 1
fi

VERSION=$1

wget https://github.com/Pylons/waitress/archive/v$VERSION/waitress-$VERSION.tar.gz
tar -xzvf waitress-$VERSION.tar.gz
rm -rf waitress-$VERSION/docs
mv waitress-$VERSION waitress-$VERSION-nodocs
tar -czvf waitress-$VERSION-nodocs.tar.gz waitress-$VERSION-nodocs
