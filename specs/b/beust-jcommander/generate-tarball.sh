#!/bin/bash

set -e

# This commit refers to the state of the sources when they were published to
# Maven Central
git_tag='dcf154b6d40dd3865e317de7250b7019044543a9'
version="$(sed -n 's/Version:\s*//p' *.spec)"

# Retrieve and set version
git clone https://github.com/cbeust/jcommander.git

pushd jcommander
git reset --hard "${git_tag}"

# Clean
find -name '*.jar' -delete
find -name '*.class' -delete
rm -rf gradle* kobalt* lib
rm -rf .git
popd

# Pack into tarball
mv jcommander beust-jcommander-"${version}"
tar -cvf beust-jcommander-"${version}".tar.gz beust-jcommander-"${version}"/
rm -rf beust-jcommander-"${version}"
