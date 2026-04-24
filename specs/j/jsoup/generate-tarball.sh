#!/bin/bash
set -e

name=jsoup
version="$(sed -n 's/Version:\s*//p' *.spec)"

# RETRIEVE
wget "https://github.com/jhy/${name}/archive/${name}-${version}.tar.gz" -O "${name}-${version}.orig.tar.gz"

rm -rf tarball-tmp
mkdir tarball-tmp
pushd tarball-tmp
tar -xf "../${name}-${version}.orig.tar.gz"

# CLEAN TARBALL
# contains scraped news articles (non-free)
rm -r "${name}-${name}-${version}/src/test/resources"

tar -czf "../${name}-${version}.tar.gz" *
popd
rm -r tarball-tmp "${name}-${version}.orig.tar.gz"
