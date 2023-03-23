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

TMPDIR=$(mktemp -d /var/tmp/flexmock-XXXXXX)
CURDIR=$(pwd)

pushd $TMPDIR

git clone https://github.com/doudou/flexmock.git

cd flexmock
git reset --hard $VERSION
cd ..

tar czf $CURDIR/flexmock-${VERSION}-test-missing-files.tar.gz flexmock/test/

popd
rm -rf $TMPDIR

