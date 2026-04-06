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

GEMNAME=redcarpet
TMPDIR=$(mktemp -d /var/tmp/${GEMNAME}-XXXXXX)
CURDIR=$(pwd)
GITTOPDIR=${GEMNAME}-${VERSION}

pushd $TMPDIR

git clone http://github.com/vmg/${GEMNAME} ${GITTOPDIR}
cd ${GEMNAME}-$VERSION

git checkout -b fedora-$VERSION v$VERSION || true
cd ..

tar czf $CURDIR/${GEMNAME}-${VERSION}-test-missing-files.tar.gz \
	${GITTOPDIR}/test/ \

popd
rm -rf $TMPDIR

