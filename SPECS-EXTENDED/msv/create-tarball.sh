#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-tarball VERSION"
    exit 1
fi

VERSION=${1}
NAME="msv"

# Generate tarball from upstream source control:
svn co https://svn.java.net/svn/${NAME}~svn/tags/${NAME}-${VERSION}/ ${NAME}-${VERSION}

# Remove things that we don't need
(
  cd ${NAME}-${VERSION}
  rm -Rf www/ relames/ .svn/
  rm -Rf schmit/  shared/  tahiti/
)

tar zcf ${NAME}-${VERSION}-clean.tar.gz ${NAME}-${VERSION}

