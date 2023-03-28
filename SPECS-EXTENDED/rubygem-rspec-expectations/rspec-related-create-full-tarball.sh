#!/bin/bash

if [ $# -lt 2 ]
then
  echo "$0 <name> <version>"
  exit 1
fi

set -x
set -e

CURRDIR=$(pwd)

TMPDIRPATH=$(mktemp -d /var/tmp/rspec-tar-XXXXXX)
pushd $TMPDIRPATH

git clone https://github.com/rspec/$1.git
pushd $1
git reset --hard v$2
popd

ln -sf $1 $1-$2
tar czf ${CURRDIR}/rubygem-$1-$2-full.tar.gz $1-$2/./

popd

rm -rf $TMPDIRPATH
