#!/bin/bash

set -x
set -e

if [ $# -lt 1 ]
then
  echo "$0 <version>"
  exit 1
fi

NAME=json

CURRDIR=$(pwd)

TMPDIRPATH=$(mktemp -d /var/tmp/${NAME}-tar-XXXXXX)
pushd $TMPDIRPATH

VERSION=$1

git clone https://github.com/flori/${NAME}.git
pushd json
git reset --hard v${VERSION} || false
popd

ln -sf ${NAME} ${NAME}-${VERSION}
tar czf ${CURRDIR}/rubygem-${NAME}-${VERSION}-missing-files.tar.gz \
	${NAME}-${VERSION}/./test/

popd

rm -rf $TMPDIRPATH

