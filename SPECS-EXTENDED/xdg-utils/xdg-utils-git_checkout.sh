#!/bin/bash


MODULE=xdg-utils
VERSION=1.1.0
DATE=$(date +%Y%m%d)git

set -x

rm -rf $MODULE

git clone git://anongit.freedesktop.org/git/xdg/xdg-utils $MODULE/
pushd $MODULE
git archive master --format tar --prefix=${MODULE}-${VERSION}/ | gzip -9 > ../${MODULE}-${VERSION}-${DATE}.tar.gz
popd

rm -rf $MODULE 
