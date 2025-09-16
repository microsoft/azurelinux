#!/bin/bash

if [ $# -lt 1 ]
then
  echo "$0 <version>"
  exit 1
fi

set -x
set -e

VERSION=$1

REPOURL=https://github.com/ruby/
REPONAME=test-unit-ruby-core

TARBALLNAME=${REPONAME}-${VERSION}-additional.tar.gz

CURRDIR=$(pwd)
TMPDIRPATH=$(mktemp -d /var/tmp/${REPONAME}-tar-XXXXXX)
pushd $TMPDIRPATH

git clone ${REPOURL}/${REPONAME}.git
ln -sf ${REPONAME} ${REPONAME}-${VERSION}
cd ${REPONAME}

git checkout -b fedora-${VERSION} v${VERSION} || true
cd ..
tar czf $TARBALLNAME \
	${REPONAME}-${VERSION}/BSDL \
	${REPONAME}-${VERSION}/COPYING \
	${REPONAME}-${VERSION}/README.md \

mv $TARBALLNAME $CURRDIR

popd
rm -rf $TMPDIRPATH


