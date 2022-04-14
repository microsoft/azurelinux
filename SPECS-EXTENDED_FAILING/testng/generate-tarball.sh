#!/bin/bash
set -e

name=testng
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/cbeust/testng/archive/${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
tar xzf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
rm -r */gradle* */kobalt*
rm */src/main/resources/org/testng/jquery-*.js

tar cJf "../${name}-${version}.tar.xz" *
cd ..
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
