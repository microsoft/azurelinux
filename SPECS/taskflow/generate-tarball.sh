#!/bin/sh -x

VERSION=$1

rm -fr taskflow-$VERSION
tar -xzvf taskflow-$VERSION.tar.gz
echo "Removing copyrighted PDFs"
find taskflow-$VERSION -name "*.pdf" -print -delete

tar -czvf taskflow-$VERSION-norefpdfs.tar.gz taskflow-$VERSION
