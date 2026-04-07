#!/bin/sh

if [[ -z "$1" ]]; then
    echo "Usage: $0 <version>" 1>&2
    exit 1
fi

VERSION=$1
NAME=AMF

wget -q -c https://github.com/GPUOpen-LibrariesAndSDKs/AMF/archive/v$VERSION/$NAME-$VERSION.tar.gz

tar -xzf $NAME-$VERSION.tar.gz
rm -f $NAME-$VERSION.tar.gz
rm -fr $NAME-$VERSION/Thirdparty

tar -czf $NAME-cleaned-$VERSION.tar.gz --remove-files $NAME-$VERSION
