#!/bin/bash
set -e

name=testng
version="$(sed -n 's/Version:\s*//p' *.spec)"
upstream_version="$(echo ${version} | tr '~' '-')"

# RETRIEVE
wget "https://github.com/cbeust/testng/archive/${upstream_version}.tar.gz" -O "${name}-${upstream_version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${upstream_version}.orig.tar.gz"

# CLEAN TARBALL
rm -r */bin*
rm -r */gradle*
find -name 'jquery-*.min.js' -delete

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${upstream_version}.orig.tar.gz"
