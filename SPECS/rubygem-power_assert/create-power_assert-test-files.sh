#!/bin/bash

if [ $# -lt 1 ]
then
  echo "$0  v<version>"
  exit 1
fi


set -x
set -e

VERSION=$1
TARBALL=power_assert-tests-${VERSION}.tar.gz
CURDIR=$(pwd)

WORKDIR=$(mktemp -d /var/tmp/power_assert-XXXXXX)
pushd $WORKDIR

git clone https://github.com/ruby/power_assert.git
cd power_assert
git reset --hard v${VERSION}
tar czf ${TARBALL} test/
mv ${TARBALL} ${CURDIR}/

popd
rm -rf $WORKDIR
