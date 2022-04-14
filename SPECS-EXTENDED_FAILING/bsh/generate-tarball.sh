#!/bin/bash
set -e

name=bsh
version="$(sed -n 's/Version:\s*//p' *.spec)"
reltag="$(sed -n 's/%global\s*reltag\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/beanshell/beanshell/archive/${version}${reltag}.tar.gz" -O "${name}-${version}-${reltag}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
tar xf "../${name}-${version}-${reltag}.orig.tar.gz"

# CLEAN TARBALL
rm -r */lib
find -name '*.jar' -delete
find -name '*.class' -delete
# Files marked as SUN PROPRIETARY/CONFIDENTAIL
rm -r */engine/javax-src

tar cf "../${name}-${version}-${reltag}.tar.gz" *
cd ..
rm -r tarball-tmp "${name}-${version}-${reltag}.orig.tar.gz"
