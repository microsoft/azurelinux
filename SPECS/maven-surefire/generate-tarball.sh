#!/bin/bash
set -e

name=maven-surefire
version="$(sed -n 's/Version:\s*//p' *.spec)"
upstream_version="${version/'~'/'-'}"

# RETRIEVE
wget "https://repo1.maven.org/maven2/org/apache/maven/surefire/surefire/${upstream_version}/surefire-${upstream_version}-source-release.zip" -O "${name}-${version}.orig.zip"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
unzip "../${name}-${version}.orig.zip"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete

tar czf "../${name}-${version}.tar.gz" *
cd ..
rm -r tarball-tmp "${name}-${version}.orig.zip"
