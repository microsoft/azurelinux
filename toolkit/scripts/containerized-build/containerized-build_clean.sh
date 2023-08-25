#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Clean up any containers used during Mariner containerized-rpmbuild. These containers will
# be rooted in a container called 'mariner-container-build:*'
# We use a tag 'containerized-rpmbuild'=MARINER_BUILD_DIR to identify containers, where
# MARINER_BUILD_DIR is the absolute path to the Mariner build directory.

set -e

# Used to tag our container layers
MARINER_BUILD_DIR=$1

# Only remove our tagged containers, as we may have running containers in another build
containers=$(docker ps -aq --filter label="containerized-rpmbuild"="${MARINER_BUILD_DIR}" | sort -u)
if [ -n "${containers}" ]; then
    echo "Removing containerized-rpmbuild containers: '${containers}'"
    docker rm --force ${containers} 2>&1 || true
else
    echo "No containers found for 'containerized-rpmbuild=${MARINER_BUILD_DIR}'"
fi

images="$(docker images -aq --filter label="containerized-rpmbuild"="${MARINER_BUILD_DIR}" | sort -u)"
if [ -n "${images}" ]; then
    echo "Removing containerized-rpmbuild images: '${images}'"
    docker image rm --force ${images} 2>&1 || true
else
    echo "No images found for 'containerized-rpmbuild=${MARINER_BUILD_DIR}'"
fi
