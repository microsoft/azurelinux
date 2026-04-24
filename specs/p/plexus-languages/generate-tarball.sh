#!/bin/bash
set -e

name=plexus-languages
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/codehaus-plexus/plexus-languages/archive/plexus-languages-${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
