#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

MARINER_BUILD_DIR=$1
MARINER_SPECS_DIR=$2
MARINER_SOURCE_URL=$3
INCREMENTAL_TOOLCHAIN=$4
ARCHIVE_TOOL=$5

# Grab an identity for the raw toolchain components so we can avoid rebuilding it if it hasn't changed
sha_component_tag=$(sha256sum ./container/toolchain-sha256sums ./container/toolchain_build_in_chroot.sh ./create_toolchain_in_container.sh | sha256sum | cut -d' ' -f1 )

# Check if we already have a committed container with the same sha_component_tag
if [ "$INCREMENTAL_TOOLCHAIN" != "y" ] || [ -z "$(docker images -q marinertoolchain_populated:${sha_component_tag} 2>/dev/null)" ]; then
    echo "No existing container with tag ${sha_component_tag}, building..."

    ./toolchain_verify.sh $MARINER_BUILD_DIR

    # Cleanup
    docker images -a
    docker ps -a
    # docker system prune -f
    # docker rmi $(docker images -a -q)
    # docker rmi $(docker history marinertoolchain -q)

    # CPIO patch
    cp -v $MARINER_SPECS_DIR/cpio/cpio_extern_nocommon.patch ./container
    cp -v $MARINER_SPECS_DIR/cpio/CVE-2021-38185.patch ./container
    # Coreutils aarch64 patch
    cp -v $MARINER_SPECS_DIR/coreutils/coreutils-fix-get-sys_getdents-aarch64.patch ./container
    # Binutils readonly patch
    cp -v $MARINER_SPECS_DIR/binutils/linker-script-readonly-keyword-support.patch ./container
    # RPM LD_FLAGS patch
    cp -v $MARINER_SPECS_DIR/rpm/define-RPM_LD_FLAGS.patch ./container/rpm-define-RPM-LD-FLAGS.patch
    # GCC patch
    cp -v $MARINER_SPECS_DIR/gcc/CVE-2023-4039.patch ./container

    # Create .bashrc file for lfs user in the container
    cat > ./container/.bashrc << EOF
set +h
umask 022
LFS=/temptoolchain/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu
PATH=/usr/bin
if [ ! -L /bin ]; then PATH=/bin:$PATH; fi
PATH=$LFS/tools/bin:$PATH
CONFIG_SITE=$LFS/usr/share/config.site
export LFS LC_ALL LFS_TGT PATH CONFIG_SITE
EOF

    # Generate toolchain-local-wget-list
    cat ./container/toolchain-sha256sums | awk -v env_src=${MARINER_SOURCE_URL} '{print env_src"/"$2}' > ./container/toolchain-local-wget-list

    echo Building temp toolchain in container
    export tag=$(date +'%y%m%d.%H%M')
    docker build --tag marinertoolchain:${tag} --build-arg MARINER_BUILD_DIR="${MARINER_BUILD_DIR}" ./container
    docker tag marinertoolchain:${tag} marinertoolchain:latest

    # Now build final raw toolchain as root, which requires --privileged for the chroot
    echo Building raw toolchain in container
    set +e
    docker stop marinertoolchain-container
    docker rm marinertoolchain-container
    set -e
    docker run -t --privileged --name marinertoolchain-container marinertoolchain:latest

    echo Committing built toolchain to marinertoolchain_populated:${sha_component_tag}
    docker commit marinertoolchain-container marinertoolchain_populated:${sha_component_tag}
else
    echo "Found existing container with tag ${sha_component_tag}, skipping build..."
fi

echo Finished building toolchain, extracting from container...
pushd $MARINER_BUILD_DIR/toolchain

# Pull out the populated toolchain from the container
docker rm -f marinertoolchain-container-temp 2>/dev/null || true
temporary_toolchain_container=$(docker create --name marinertoolchain-container-temp marinertoolchain_populated:${sha_component_tag})
docker cp "${temporary_toolchain_container}":/temptoolchain/lfs .
docker rm marinertoolchain-container-temp

rm -rf ./populated_toolchain
mv ./lfs ./populated_toolchain
rm -rf ./populated_toolchain/.dockerenv
rm -rf ./populated_toolchain/sources
rm -rf ./populated_toolchain/tools/libexec/gcc

echo "Compressing toolchain_from_container.tar.gz"
tar -I "$ARCHIVE_TOOL" -cf toolchain_from_container.tar.gz populated_toolchain
ls -la ./
ls -la ./populated_toolchain
popd

# Cleanup patch files used in container
rm -vf ./container/*.patch
rm -vf ./container/.bashrc
rm -vf ./container/toolchain-local-wget-list

echo Raw toolchain build complete
