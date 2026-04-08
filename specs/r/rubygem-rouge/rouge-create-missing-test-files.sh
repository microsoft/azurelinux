#!/bin/bash

usage() {
	echo "$0 <VERSION>"
}

set -e
set -x

if [ $# -lt 1 ] ; then
	usage
	exit 1
fi

VERSION=$1
REPONAME=rouge

TMPDIR=$(mktemp -d /tmp/rouge-XXXXXX)
CURDIR=$(pwd)

pushd $TMPDIR

git clone https://github.com/rouge-ruby/${REPONAME}.git
cd rouge/

git reset --hard v$VERSION
cd ..
ln -sf ${REPONAME} ${REPONAME}-${VERSION}
tar czf $CURDIR/rouge-${VERSION}-test-missing-files.tar.gz ${REPONAME}-${VERSION}/spec/

popd
rm -rf $TMPDIR

