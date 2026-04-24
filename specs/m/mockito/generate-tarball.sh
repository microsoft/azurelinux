#!/bin/bash
set -e

name=mockito
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/mockito/mockito/archive/v${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
pushd "mockito-${version}"
find -name '*.jar' -delete
find -name '*.class' -delete
rm -rf gradlew gradlew.bat src/javadoc
popd

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
