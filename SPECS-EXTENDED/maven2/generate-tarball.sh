#!/bin/bash
set -e

name=maven2
version="$(sed -n 's/Version:\s*//p' *.spec)"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp

# RETRIEVE
svn export "https://svn.apache.org/repos/asf/maven/maven-2/tags/maven-${version}/" "${name}-${version}"

# CLEAN TARBALL
rm */*.jar

tar czf "../${name}-${version}.tar.gz" *
