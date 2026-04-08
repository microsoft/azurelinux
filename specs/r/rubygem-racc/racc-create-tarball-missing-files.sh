#!/bin/bash

set -x
set -e

if [ $# -lt 1 ]
then
  echo "$0 <version>"
  exit 1
fi

CURRDIR=$(pwd)

TMPDIRPATH=$(mktemp -d /var/tmp/racc-tar-XXXXXX)
pushd $TMPDIRPATH

NAME=racc
VERSION=$1

git clone https://github.com/ruby/racc.git
pushd racc
git reset --hard v${VERSION}
popd

ln -sf ${NAME} ${NAME}-${VERSION}
tar czf ${CURRDIR}/rubygem-${NAME}-${VERSION}-missing-files.tar.gz \
	${NAME}-${VERSION}/./{test/,sample/}

popd

rm -rf $TMPDIRPATH

