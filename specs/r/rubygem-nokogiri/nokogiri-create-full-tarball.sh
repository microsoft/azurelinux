#!/bin/bash

git_restore_timestamp()
{
	set +x
	echo "Restore timestamps"
	git ls-tree -r --name-only HEAD | while read f
	do
		  unixtime=$(git log -n 1 --pretty='%ct' -- $f)
		  touch -d "@${unixtime}" $f
	done
	set -x
}

if [ $# -lt 2 ]
then
  echo "$0 <name> <version>"
  exit 1
fi

set -x
set -e

CURRDIR=$(pwd)

TMPDIRPATH=$(mktemp -d /var/tmp/$1-tar-XXXXXX)
pushd $TMPDIRPATH

git clone https://github.com/sparklemotion/$1.git
pushd $1
git reset --hard v$2
git_restore_timestamp
popd

ln -sf $1 $1-$2
tar czf \
	${CURRDIR}/rubygem-$1-$2-full.tar.gz \
	"--exclude=nokogiri-$2/./.git" \
	$1-$2/./

popd

rm -rf $TMPDIRPATH
