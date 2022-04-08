#!/bin/bash
set -e

name=objectweb-asm
version="$(sed -n 's/Version:\s*//p' *.spec)"
gittag="ASM_${version//./_}"

# RETRIEVE
wget "https://gitlab.ow2.org/asm/asm/repository/${gittag}/archive.tar.gz#/${name}-${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
tar xf "../${name}-${version}.orig.tar.gz"

# Rename dir not to contain commit
mv asm-${gittag}-* ${name}-${version}

# CLEAN TARBALL
# Remove all jar files
find -name '*.jar' -delete

tar cJf "../${name}-${version}.tar.xz" *
cd ..
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
