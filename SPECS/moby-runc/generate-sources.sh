#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-buildx package.
# Git clone is a standard practice of producing source files for moby-* packages.

RUNC_REPO=https://github.com/opencontainers/runc.git
RUNC_COMMIT=f19387a6bec4944c770f7668ab51c4348d9c2f38
VERSION=v1.1.5

mkdir -p /build/runc-src
cd /build/runc-src
git clone ${RUNC_REPO}
cd runc
git fetch --tags origin ${RUNC_COMMIT}
git checkout ${RUNC_COMMIT}
cd /build/
tar -C /build/runc-src -czf ./runc-${VERSION}.tar.gz .
rm -rf /build/runc-src

echo "sources generated successfully @ /build/runc-${VERSION}.tar.gz"
