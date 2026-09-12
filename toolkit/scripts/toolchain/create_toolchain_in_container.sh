#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

MARINER_BUILD_DIR=$1
MARINER_SPECS_DIR=$2
MARINER_SOURCE_URL=$3
NO_TOOLCHAIN_CONTAINER=$4
INCREMENTAL_TOOLCHAIN=$5
ARCHIVE_TOOL=$6
LOG_DIR=$7

if [ -z "$MARINER_BUILD_DIR" ] || [ -z "$MARINER_SPECS_DIR" ] || [ -z "$MARINER_SOURCE_URL" ] || [ -z "$NO_TOOLCHAIN_CONTAINER" ] || [ -z "$INCREMENTAL_TOOLCHAIN" ] || [ -z "$ARCHIVE_TOOL" ] || [ -z "$LOG_DIR" ]; then
    echo "Usage: $0 <MARINER_BUILD_DIR> <MARINER_SPECS_DIR> <MARINER_SOURCE_URL> <NO_TOOLCHAIN_CONTAINER> <INCREMENTAL_TOOLCHAIN> <ARCHIVE_TOOL> <LOG_DIR>"
    exit 1
fi

# Grab an identity for the raw toolchain components so we can avoid rebuilding it if it hasn't changed
files_to_watch=(    "./create_toolchain_in_container.sh" \
                    "./container/Dockerfile" \
                    "./container/bypass_container.sh" \
                    "./container/mount_chroot_start_build.sh" \
                    "./container/sanity_check.sh" \
                    "./container/toolchain_build_in_chroot.sh" \
                    "./container/toolchain_build_temp_tools.sh" \
                    "./container/toolchain_initial_chroot_setup.sh" \
                    "./container/toolchain-remote-wget-list" \
                    "./container/toolchain-sha256sums" \
                    "./container/unmount_chroot.sh" \
                    "./container/version-check-container.sh" )
sha_component_tag=$(sha256sum "${files_to_watch[@]}" | sha256sum | cut -d' ' -f1 )

# Check if we already have a committed container with the same sha_component_tag
if [ "$NO_TOOLCHAIN_CONTAINER" = "y"  ] || [ "$INCREMENTAL_TOOLCHAIN" != "y" ] || [ -z "$(docker images -q marinertoolchain_populated:${sha_component_tag} 2>/dev/null)" ]; then
    echo "No existing container with tag ${sha_component_tag}, building..."

    ./toolchain_verify.sh $MARINER_BUILD_DIR

    # Cleanup
    if [ "$NO_TOOLCHAIN_CONTAINER" != "y" ]; then
        docker images -a
        docker ps -a
        # docker system prune -f
        # docker rmi $(docker images -a -q)
        # docker rmi $(docker history marinertoolchain -q)
    else
        export LFSROOT=$MARINER_BUILD_DIR/toolchain/lfs
    fi

    # RPM LD_FLAGS patch
    cp -v $MARINER_SPECS_DIR/rpm/define-RPM_LD_FLAGS.patch ./container/rpm-define-RPM-LD-FLAGS.patch
    # GCC patch
    cp -v $MARINER_SPECS_DIR/gcc/CVE-2023-4039.patch ./container

    # Create .bashrc file for lfs user in the container
    cat > ./container/.bashrc << EOF
set +h
umask 022
LFS=${LFSROOT:-/temptoolchain/lfs}
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

    if [ "$NO_TOOLCHAIN_CONTAINER" = "y" ]; then
        echo Building raw toolchain in chroot
        pushd container
        ./bypass_container.sh
    else
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
    fi
else
    echo "Found existing container with tag ${sha_component_tag}, skipping build..."
fi

pushd $MARINER_BUILD_DIR/toolchain
if [ "$NO_TOOLCHAIN_CONTAINER" = "y" ]; then
    echo Finished building toolchain, saving logs...
    cp -r ./lfs/logs ${LOG_DIR}
else
    echo Finished building toolchain, extracting from container...

    # Pull out the populated toolchain from the container
    docker rm -f marinertoolchain-container-temp 2>/dev/null || true
    temporary_toolchain_container=$(docker create --name marinertoolchain-container-temp marinertoolchain_populated:${sha_component_tag})
    rm -rf ${LOG_DIR}/logs
    mkdir -p ${LOG_DIR}/logs
    docker cp "${temporary_toolchain_container}":/temptoolchain/lfs .
    docker cp "${temporary_toolchain_container}":/temptoolchain/lfs/logs ${LOG_DIR}
    docker rm marinertoolchain-container-temp
fi

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

# Ensure the populated toolchain was created successfully
if [ ! -f ${LOG_DIR}/logs/status_building_in_chroot_complete ]; then
    echo "Error: Raw toolchain container build failed, check logs in ${LOG_DIR} for details"
    exit 1
fi

echo Raw toolchain build complete
