#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

VERSION=$1
NAME=bullet3

if [ ! -f $NAME-$VERSION.tgz ]; then
    wget "https://codeload.github.com/bulletphysics/bullet3/tar.gz/$VERSION" -O ${NAME}-${VERSION}.tgz
fi

tar -xzvf $NAME-$VERSION.tgz
rm -rf $NAME-$VERSION/build3/*.{bat,exe}
rm -rf $NAME-$VERSION/build3/xcode*
rm -rf $NAME-$VERSION/build3/*osx*
rm -rf $NAME-$VERSION/build3/premake*
rm -rf $NAME-$VERSION/data
rm -rf $NAME-$VERSION/examples/ThirdPartyLibs

tar -cJvf $NAME-$VERSION-free.tar.xz $NAME-$VERSION 
