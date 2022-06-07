#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-containerd package.
# Git clone is a standard practice of producing source files for moby-* packages.

CONTAINERD_REPO=https://github.com/containerd/containerd.git
CONTAINERD_COMMIT=10c12954828e7c7c9b6e0ea9b0c02b01407d3ae1
VERSION=1.6.6+azure

mkdir -p /build/containerd-src
cd /build/containerd-src
git clone ${CONTAINERD_REPO} .
git fetch --tags origin ${CONTAINERD_COMMIT}
git checkout ${CONTAINERD_COMMIT}
cd /build/

tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -C /build/containerd-src -czf ./moby-containerd-${VERSION}.tar.gz .
rm -rf /build/containerd-src

echo "sources generated successfully @ /build/moby-containerd-${VERSION}.tar.gz"