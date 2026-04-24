#!/bin/bash
set -e

name=junit
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/junit-team/junit/archive/r${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete
rm -r "junit4-r${version}/src/site"

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
