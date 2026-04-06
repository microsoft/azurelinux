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

git clone https://github.com/rspec/rspec.git
pushd rspec

# https://github.com/rspec/rspec/issues/220
git reset --hard $1-v$2 || \
	git reset --hard rspec-expecations-v$2

ln -sf $1 $1-$2
tar czf ${CURRDIR}/rubygem-$1-$2-full.tar.gz $1-$2/./

popd

rm -rf $TMPDIRPATH
