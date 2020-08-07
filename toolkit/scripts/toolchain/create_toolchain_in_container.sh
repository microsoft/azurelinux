#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

MARINER_BUILD_DIR=$1
MARINER_SPECS_DIR=$2
MARINER_SOURCE_URL=$3

./toolchain_verify.sh $MARINER_BUILD_DIR

# Cleanup
docker images -a
docker ps -a
# docker system prune -f
# docker rmi $(docker images -a -q)
# docker rmi $(docker history marinertoolchain -q)

# Texinfo patch file
cp -v $MARINER_SPECS_DIR/texinfo/texinfo-perl-fix.patch ./container
cp -v $MARINER_SPECS_DIR/openjdk8/Awt_build_headless_only.patch ./container
cp -v $MARINER_SPECS_DIR/openjdk8/check-system-ca-certs.patch ./container
# Create .bashrc file for lfs user in the container
cat > ./container/.bashrc << EOF
umask 022
LFS=/temptoolchain/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu
PATH=/tools/bin:/bin:/usr/bin
export LFS LC_ALL LFS_TGT PATH
EOF

# Generate toolchain-local-wget-list
cat ./container/toolchain-md5sums | awk -v env_src=${MARINER_SOURCE_URL} '{print env_src"/toolchain/"$2}' > ./container/toolchain-local-wget-list

echo Building temp toolchain in container
export tag=$(date +'%y%m%d.%H%M')
docker build --tag marinertoolchain:${tag} ./container
docker tag marinertoolchain:${tag} marinertoolchain:latest

# Now build final raw toolchain as root, which requires --privileged for the chroot
echo Building raw toolchain in container
set +e
docker stop marinertoolchain-container
docker rm marinertoolchain-container
set -e
docker run -t --privileged --name marinertoolchain-container marinertoolchain:latest

echo Finished building toolchain, extracting from container...
pushd $MARINER_BUILD_DIR/toolchain
docker cp marinertoolchain-container:/temptoolchain/lfs .
rm -rvf ./populated_toolchain
mv ./lfs ./populated_toolchain
rm -rvf ./populated_toolchain/.dockerenv
rm -rvf ./populated_toolchain/sources
tar czf toolchain_from_container.tar.gz populated_toolchain
ls -la ./
ls -la ./populated_toolchain
popd

# Cleanup patch files used in container
rm -vf ./container/texinfo-perl-fix.patch
rm -vf ./container/Awt_build_headless_only.patch
rm -vf ./container/check-system-ca-certs.patch
rm -vf ./container/.bashrc

echo Raw toolchain build complete