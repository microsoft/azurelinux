#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-containerd package.
# Git clone is a standard practice of producing source files for moby-* packages.

CONTAINERD_REPO=https://github.com/containerd/containerd.git
CONTAINERD_COMMIT=814b7956fafc7a0980ea07e950f983d0837e5578
VERSION=1.3.4+azure

mkdir -p /build/containerd-src
cd /build/containerd-src
git clone ${CONTAINERD_REPO} .
git fetch --tags origin ${CONTAINERD_COMMIT}
git checkout ${CONTAINERD_COMMIT}
cd /build/

tar -C /build/containerd-src -czf ./moby-containerd-${VERSION}.tar.gz .
rm -rf /build/containerd-src

echo "sources generated successfully @ /build/moby-containerd-${VERSION}.tar.gz"