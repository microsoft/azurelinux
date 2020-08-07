#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources moby-runc dependent packages.

# golang sys sources are git cloned to latest commit.
GOLANG_SYS=https://github.com/golang/sys.git
GOLANG_SYS_COMMIT=669c56c373c468cbe0f0c12b7939832b26088d33

mkdir -p /build/work/sys-master
cd /build/work/sys-master
git clone ${GOLANG_SYS} .
git fetch --tags origin ${GOLANG_SYS_COMMIT}
git checkout ${GOLANG_SYS_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-sys-${GOLANG_SYS_COMMIT}.tar.gz sys-master
rm -rf /build/work

# golang crypto sources are git cloned to latest commit.
GOLANG_CRYPO=https://github.com/golang/crypto.git
GOLANG_CRYPTO_COMMIT=0848c9571904fcbcb24543358ca8b5a7dbfde875

mkdir -p /build/work/crypto-master
cd /build/work/crypto-master
git clone ${GOLANG_CRYPO} .
git fetch --tags origin ${GOLANG_CRYPTO_COMMIT}
git checkout ${GOLANG_CRYPTO_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-crypto-${GOLANG_CRYPTO_COMMIT}.tar.gz crypto-master
rm -rf /build/work
