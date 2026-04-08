#!/bin/bash

if [ $# -lt 1 ]
then
  echo "$0 <version>"
  exit 1
fi

set -x
set -e

GEMNAME=aruba
CURRDIR=$(pwd)
VERSION=$1

TMPDIRPATH=$(mktemp -d /var/tmp/${GEMNAME}-tar-XXXXXX)
pushd $TMPDIRPATH

git clone https://github.com/cucumber/${GEMNAME}.git
pushd ${GEMNAME}
git reset --hard v${VERSION}
popd

ln -sf ${GEMNAME} ${GEMNAME}-${VERSION}
tar czf ${CURRDIR}/rubygem-${GEMNAME}-${VERSION}-testsuite.tar.gz \
    ${GEMNAME}-${VERSION}/{features,fixtures,spec}

popd

rm -rf $TMPDIRPATH
