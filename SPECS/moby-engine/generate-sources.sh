#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-engine package.
# Git clone is a standard practice of producing source files for moby-* packages.

ENGINE_REPO=https://github.com/moby/moby.git
ENGINE_COMMIT=77e06fda0c9457c99a210e9648c064b44805fa2d
VERSION=19.03.11+azure

# docker-proxy binary comes from libnetwork
# The proxy code rarely sees any changes
# The default value for the commit is taken from the engine repo
#   see "hack/dockerfile/install/proxy.installer" in that repo
PROXY_REPO=https://github.com/docker/libnetwork.git
PROXY_COMMIT=153d0769a1181bf591a9637fd487a541ec7db1e6

# Tini is a tiny container init, it's used as the binary for "docker-init"
# tini sources are git cloned to tag v0.18.0
#   see "hack/dockerfile/install/tini.installer" in moby engine repo for matching commit
TINI_REPO=https://github.com/krallin/tini.git
TINI_COMMIT=fec3683b971d9c3ef73f284f176672c44b448662

mkdir -p /build/engine-src
cd /build/engine-src
git clone ${ENGINE_REPO} .
git fetch --tags origin ${ENGINE_COMMIT}
git checkout ${ENGINE_COMMIT}
git archive HEAD  > /build/engine-src.tar
cd /build/
rm -rf /build/engine-src

mkdir -p /build/proxy-src
cd /build/proxy-src
git clone ${PROXY_REPO} .
git fetch --tags origin ${PROXY_COMMIT}
git checkout  ${PROXY_COMMIT}
git archive HEAD  > /build/proxy-src.tar
cd /build/
rm -rf /build/proxy-src

mkdir -p /build/tini-src
cd /build/tini-src
git clone ${TINI_REPO} .
git fetch --tags origin ${TINI_COMMIT}
git checkout ${TINI_COMMIT}
git archive HEAD > /build/tini-src.tar
cd /build/
rm -rf /build/tiny-src

mkdir -p /build/work/tini
mkdir -p /build/work/libnetwork 
tar -C /build/work -xf /build/engine-src.tar
tar -C /build/work/tini -xvf /build/tini-src.tar
tar -C /build/work/libnetwork -xvf /build/proxy-src.tar

tar -C /build/work -czf ./moby-engine-${VERSION}.tar.gz .
rm -rf /build/work

echo "sources generated successfully @ /build/moby-engine-${VERSION}.tar.gz"