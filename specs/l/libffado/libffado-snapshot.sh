#!/bin/bash

# $1 - revision number to checkout.
: ${1?"You must either provide desired revision number \"X\" to checkout: `basename $0` X
                                or fetch the latest revision by: `basename $0` HEAD"}

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
unset GREP_OPTIONS
pwd=$(pwd)
name=libffado
version=2.1.0

revision=$1

pushd "$tmp" >/dev/null
echo "Fetching SVN revision: $1"
svn export -r$revision http://subversion.ffado.org/ffado/trunk/$name $name-$version |tee $name.stdout
revision=$(cat $name.stdout|grep "Exported revision"|sed 's|[^0-9]*||g')
echo "Fetched SVN revision: $revision"
rm -f $name.stdout

tar jcf "$pwd"/$name-$version-svn$revision.tar.bz2 $name-$version
echo "Written: $name-$version-svn$revision.tar.bz2"
popd >/dev/null
