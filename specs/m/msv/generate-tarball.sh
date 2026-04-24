#!/bin/bash
set -e

name=msv
version="$(sed -n 's/Version:\s*//p' ./*.spec)"

# RETRIEVE
wget "https://github.com/xmlark/msv/archive/${name}-${version}/${name}-${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"
mv "msv-msv-${version}" "${name}-${version}"

pushd "${name}-${version}"
mv docs/xsdlib/Apache-LICENSE-1.1.txt .
mv docs/xsdlib/license.txt .
mv docs/xsdlib/README.md README-xsdlib.md

# CLEAN TARBALL
find . -mindepth 1 -maxdepth 1 -type d ! -name 'xsdlib' -exec rm -rf {} +
rm -rf xsdlib/src/test

popd

tar -czf "../${name}-${version}.tar.gz" ./*
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
