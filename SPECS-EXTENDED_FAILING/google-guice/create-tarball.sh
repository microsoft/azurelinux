#!/bin/sh
set -e -x
test $# -eq 1
test ! -d guice
git clone git://github.com/google/guice.git
cd ./guice
git checkout ${1}
git branch unbundled-${1}
git checkout unbundled-${1}
rm -rf $(ls . | grep -E -v 'core|extensions|pom|bom|jdk8-tests|COPYING|common.xml|build.xml|build.properties|lib')
find . -name "*.jar" -and ! -name munge.jar -delete
find . -name "*.class" -delete
find lib -type f -and ! -name munge.jar -delete
git commit -a -m "Remove unneeded stuff"
git tag unbundled-${1}
git archive --format=tar --prefix=google-guice-${1}/ unbundled-${1} \
    | xz >../google-guice-${1}.tar.xz
