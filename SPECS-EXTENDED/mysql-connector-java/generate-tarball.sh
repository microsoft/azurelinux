#!/bin/sh

VERSION=$1

if [ -z "$VERSION" ]; then
    echo >&2 "Usage:"
    echo >&2 "    $0 <version>"
    exit 1
fi

rm -rf mysql-connector-j-$VERSION
wget https://github.com/mysql/mysql-connector-j/archive/$VERSION.tar.gz
tar xfz $VERSION.tar.gz || exit 1

find mysql-connector-j-$VERSION -name "*.class" -print -delete
find mysql-connector-j-$VERSION -name '*.jar' -print -delete
find mysql-connector-j-$VERSION -name '*.zip' -print -delete

tar cfJ mysql-connector-java-$VERSION-nojars.tar.xz mysql-connector-j-$VERSION || exit 1

rm -rf mysql-connector-j-$VERSION $VERSION.tar.gz

exit 0

