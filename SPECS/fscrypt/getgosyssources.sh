#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources moby-runc dependent packages.

# golang crypto sources are git cloned to latest commit.
GOLANG_CRYPO=https://github.com/golang/crypto.git
GOLANG_CRYPTO_COMMIT=cbcb750295291b33242907a04be40e80801d0cfc

mkdir -p /build/work/crypto-master
cd /build/work/crypto-master
git clone ${GOLANG_CRYPO} .
git fetch --tags origin ${GOLANG_CRYPTO_COMMIT}
git checkout ${GOLANG_CRYPTO_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-crypto-${GOLANG_CRYPTO_COMMIT}.tar.gz crypto-master
rm -rf /build/work

# golang lint sources are git cloned to latest commit.
GOLANG_LINT=https://github.com/golang/lint.git
GOLANG_LINT_COMMIT=16217165b5de779cb6a5e4fc81fa9c1166fda457

mkdir -p /build/work/lint-master
cd /build/work/lint-master
git clone ${GOLANG_LINT} .
git fetch --tags origin ${GOLANG_LINT_COMMIT}
git checkout ${GOLANG_LINT_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-lint-${GOLANG_LINT_COMMIT}.tar.gz lint-master
rm -rf /build/work

# golang sys sources are git cloned to latest commit.
GOLANG_SYS=https://github.com/golang/sys.git
GOLANG_SYS_COMMIT=63cb32ae39b28d6bb8e7e215c1fc39dd80dcdb02

mkdir -p /build/work/sys-master
cd /build/work/sys-master
git clone ${GOLANG_SYS} .
git fetch --tags origin ${GOLANG_SYS_COMMIT}
git checkout ${GOLANG_SYS_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-sys-${GOLANG_SYS_COMMIT}.tar.gz sys-master
rm -rf /build/work

# golang tools sources are git cloned to latest commit.
GOLANG_TOOLS=https://github.com/golang/tools.git
GOLANG_TOOLS_COMMIT=2077df36852e9a22c3b78f535833d3e54e9fcc8a

mkdir -p /build/work/tools-master
cd /build/work/tools-master
git clone ${GOLANG_TOOLS} .
git fetch --tags origin ${GOLANG_TOOLS_COMMIT}
git checkout ${GOLANG_TOOLS_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-tools-${GOLANG_TOOLS_COMMIT}.tar.gz tools-master
rm -rf /build/work