#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# The nodejs source tarball contains a copy of the OpenSSL source tree.
# OpenSSL contains patented algorithms that should not be distributed
# as part of the SRPM. Since we use the shared OpenSSL libraries, we 
# can just remove the entire OpenSSL source tree from the tarball.

print_usage() {
    echo "Usage:"
    echo "clean-source-tarball.sh {version}"
    echo "Example: clean-source-tarball.sh 14.18.1"
    echo
    exit
}

VERSION=$1

if [ -z "$1" ]; then
    print_usage
fi


# Quit on failure
set -e

namever="node-v${VERSION}"
upstream_tarball_name="${namever}.tar.xz"
clean_tarball_name="${namever}-clean.tar.xz"
download_url="https://nodejs.org/download/release/v${VERSION}/${upstream_tarball_name}"

tmpdir=$(mktemp -d)
echo "Using temporary directory: $tmpdir"
pushd $tmpdir > /dev/null

echo "Downloading upstream source tarball..."
curl -s -O $download_url

echo "Unpacking upstream source tarball..."
tar -xf $upstream_tarball_name

echo "Removing bad vendored dependencies from source tree..."
rm -rf ./$namever/deps/openssl/openssl

# Create a reproducible tarball
# Credit to https://reproducible-builds.org/docs/archives/ for instructions
# Do not update mtime value for new versions- keep the same value for ease of
# reproducing old tarball versions in the future if necessary
echo "Repacking source tarball..."
tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -cJf $clean_tarball_name ./$namever

popd > /dev/null
cp "${tmpdir}/${clean_tarball_name}" .
echo "Clean nodejs source tarball available at $PWD/$clean_tarball_name"
rm -rf $tmpdir
