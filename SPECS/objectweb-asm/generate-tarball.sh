#!/bin/bash
set -e

name=objectweb-asm
version="$(sed -n 's/Version:\s*//p' *.spec)"
gittag="ASM_${version//./_}"

# RETRIEVE
wget "https://gitlab.ow2.org/asm/asm/-/archive/${gittag}/asm-${gittag}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xzf "../${name}-${version}.orig.tar.gz"

# Rename dir not to contain commit
mv asm-${gittag} ${name}-${version}

# CLEAN TARBALL
# Remove all jar files
find -name '*.jar' -delete
# Remove all class files except those in asm-test, which are shipped alongside appropriately licensed source
find */asm{,-analysis,-commons} -name '*.class' -delete
rm -r */gradle

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"