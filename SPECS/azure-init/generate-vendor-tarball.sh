#!/bin/bash -e

# This script is used to generate the vendor tarball for libazureinit

SOURCE_VERSION="0.1.1"
SOURCE_URL="https://github.com/Azure/azure-init/archive/refs/tags/v${SOURCE_VERSION}.tar.gz"

workdir=$(mktemp -d)
cp 0001-add-Azure-Linux-support.patch $workdir/

pushd $workdir
wget $SOURCE_URL
tar -xzvf "v${SOURCE_VERSION}.tar.gz"
pushd "azure-init-${SOURCE_VERSION}"
patch -p1 < ../0001-add-Azure-Linux-support.patch
cargo vendor >> cargo-config
tar -czvf azure-init-${SOURCE_VERSION}-vendor.tar.gz vendor
popd
popd
mv $workdir/azure-init-${SOURCE_VERSION}/azure-init-${SOURCE_VERSION}-vendor.tar.gz .
mv $workdir/azure-init-${SOURCE_VERSION}/cargo-config .
rm -rf $workdir
