#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Clean up any containers used during Azure Linux builds. These containers will
# be rooted in a container called 'marinertoolchain:*', with committed children
# called marinertoolchain_populated:*.
# We use a tag 'marinertoolchain'=MARINER_BUILD_DIR to identify containers, where
# MARINER_BUILD_DIR is the absolute path to the Azure Linux build directory.

set -e

# Used to tag our container layers
MARINER_BUILD_DIR=$1

# Only remove our tagged containers, as we may have running containers in another build
containers=$(docker ps -aq --filter label="marinertoolchain"="${MARINER_BUILD_DIR}" | sort -u)
if [ -n "${containers}" ]; then
    echo "Removing toolchain containers: '${containers}'"
    docker rm --force ${containers} 2>&1 || true
else
    echo "No containers found for 'marinertoolchain=${MARINER_BUILD_DIR}'"
fi

containers=$(docker ps -aq --filter label="containerized-rpmbuild"="${MARINER_BUILD_DIR}" | sort -u)
if [ -n "${containers}" ]; then
    echo "Removing containerized-rpmbuild containers: '${containers}'"
    docker rm --force ${containers} 2>&1 || true
else
    echo "No containers found for 'containerized-rpmbuild=${MARINER_BUILD_DIR}'"
fi

images="$(docker images -aq --filter label="marinertoolchain"="${MARINER_BUILD_DIR}" | sort -u)"
if [ -n "${images}" ]; then
    echo "Removing toolchain images: '${images}'"
    docker image rm --force ${images} 2>&1 || true
else
    echo "No images found for 'marinertoolchain=${MARINER_BUILD_DIR}'"
fi

images="$(docker images -aq --filter label="containerized-rpmbuild"="${MARINER_BUILD_DIR}" | sort -u)"
if [ -n "${images}" ]; then
    echo "Removing containerized-rpmbuild images: '${images}'"
    docker image rm --force ${images} 2>&1 || true
else
    echo "No images found for 'containerized-rpmbuild=${MARINER_BUILD_DIR}'"
fi