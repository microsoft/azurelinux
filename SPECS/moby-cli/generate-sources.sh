#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-cli package.
# Git clone is a standard practice of producing source files for moby-* packages.

CLI_REPO=https://github.com/docker/cli.git
CLI_COMMIT=dd360c7c0de8d9132a3965db6a59d3ae74f43ba7
VERSION=19.03.11+azure

mkdir -p /build/cli-src
cd /build/cli-src
git clone ${CLI_REPO} .
git fetch --tags origin ${CLI_COMMIT}
git checkout ${CLI_COMMIT}
cd /build/
tar -C /build/cli-src -czf ./moby-cli-${VERSION}.tar.gz .
rm -rf /build/cli-src

echo "sources generated successfully @ /build/moby-cli-${VERSION}.tar.gz"
