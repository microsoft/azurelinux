#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-containerd package.
# Git clone is a standard practice of producing source files for moby-* packages.

CONTAINERD_REPO=https://github.com/containerd/containerd.git
CONTAINERD_COMMIT=1407cab509ff0d96baa4f0eb6ff9980270e6e620
VERSION=1.5.9+azure

mkdir -pv /build/containerd-src/containerd-${VERSION}
cd /build/containerd-src/containerd-${VERSION}
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