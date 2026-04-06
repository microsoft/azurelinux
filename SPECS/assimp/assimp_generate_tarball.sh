#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 version"
    exit 1
fi

RELEASE=$1

if [ ! -f assimp-$RELEASE.tar.gz ]; then
    wget https://github.com/assimp/assimp/archive/v$RELEASE/assimp-$RELEASE.tar.gz
fi

if [ -d assimp-$RELEASE ]; then
    rm -fr assimp-$RELEASE
fi

tar xvf assimp-$RELEASE.tar.gz
cd assimp-$RELEASE
find ./ -name "*.dll" -exec git rm -r {} \;
rm -r test/models-nonbsd
cd ..

tar czf assimp-$RELEASE-free.tar.xz assimp-$RELEASE
