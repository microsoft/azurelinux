#!/bin/bash
set -e

name=easymock
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/${name}/${name}/archive/${name}-${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
tar xzf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete
# Contains minified js of uncertain origin
rm -r */website

tar cJf "../${name}-${version}.tar.xz" *
cd ..
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
