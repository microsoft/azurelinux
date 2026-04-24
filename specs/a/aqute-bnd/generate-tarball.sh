#!/bin/bash
set -e

name=aqute-bnd
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/bndtools/bnd/archive/${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"
mv "bnd-${version}" "${name}-${version}"

# CLEAN TARBALL
rm -rf "${name}-${version}/docs"
find -name '*.jar' -delete
find -name '*.class' -delete
find -name '*.ar' -delete
find -name '*.tar' -delete
find -name '*.gz' -delete
find -name '*.bz2' -delete
find -name '*.xz' -delete
find -name '*.zip' -delete
find -name '*.exe' -delete
find -name '*.dll' -delete

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
