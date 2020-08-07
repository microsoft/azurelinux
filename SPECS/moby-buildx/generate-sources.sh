#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-buildx package.
# Git clone is a standard practice of producing source files for moby-* packages.

BUILDX_REPO=https://github.com/docker/buildx.git
BUILDX_COMMIT=bda4882a65349ca359216b135896bddc1d92461c
VERSION=0.4.1+azure

mkdir -p /build/buildx-src
cd /build/buildx-src
git clone ${BUILDX_REPO} .
git fetch --tags origin ${BUILDX_COMMIT}
git checkout ${BUILDX_COMMIT}
cd /build/
tar -C /build/buildx-src -czf ./moby-buildx-${VERSION}.tar.gz .
rm -rf /build/buildx-src

echo "sources generated successfully @ /build/moby-buildx-${VERSION}.tar.gz"
