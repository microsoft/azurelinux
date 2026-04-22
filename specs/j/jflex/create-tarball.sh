#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-tarball.sh VERSION"
    exit 1
fi

VERSION=${1}
NAME="jflex"

wget http://jflex.de/release/${NAME}-${VERSION}.tar.gz
tar xvf ${NAME}-${VERSION}.tar.gz

(
  cd ${NAME}-${VERSION}
  find . -name "*.jar" -delete
  rm -Rf src/main/java/java_cup/ examples/
)

tar czvf ${NAME}-${VERSION}-clean.tar.gz ${NAME}-${VERSION}
rm -Rf ${NAME}-${VERSION}.tar.gz ${NAME}-${VERSION}

