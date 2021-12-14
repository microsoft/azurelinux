#!/bin/sh

#if [ -d taglib ]; then
#  echo "Remove the \"taglib\" directory first !"
#  exit 1
#fi

SNAP="$(date +%Y%m%d)git"
VERSION=1.8

git clone https://github.com/taglib/taglib.git
pushd taglib >& /dev/null
git archive --prefix=taglib-${VERSION}/ master | gzip -9 > ../taglib-${VERSION}-${SNAP}.tar.gz
popd >& /dev/null
