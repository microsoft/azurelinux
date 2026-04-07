#!/bin/bash
set -e

name=bsh
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/beanshell/beanshell/archive/${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
tar xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
rm -r */lib
find -name '*.jar' -print -delete
find -name '*.class' -print -delete
# Files marked as SUN PROPRIETARY/CONFIDENTAIL
rm -rv */engine/javax-src

tar cf "../${name}-${version}.tar.gz" *
cd ..
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
