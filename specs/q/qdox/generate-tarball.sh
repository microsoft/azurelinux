#!/bin/bash
set -e

name=qdox
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://repo1.maven.org/maven2/com/thoughtworks/qdox/qdox/${version/'~'/'-'}/${name}-${version/'~'/'-'}-project.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete
# contains possibly proprietary binaries of YACC
rm -r */bootstrap

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
