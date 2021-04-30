#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-cli package.
# Git clone is a standard practice of producing source files for moby-* packages.

CLI_REPO=https://github.com/docker/cli.git
CLI_COMMIT=48d30b5b32e99c932b4ea3edca74353feddd83ff
VERSION=19.03.15+azure

mkdir -p /build/cli-src
cd /build/cli-src
git clone ${CLI_REPO} .
git fetch --tags origin ${CLI_COMMIT}
git checkout ${CLI_COMMIT}
cd /build/
tar -C /build/cli-src -czf ./moby-cli-${VERSION}.tar.gz .
rm -rf /build/cli-src

echo "sources generated successfully @ /build/moby-cli-${VERSION}.tar.gz"
