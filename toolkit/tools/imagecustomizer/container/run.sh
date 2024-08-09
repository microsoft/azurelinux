#!/bin/bash

set -e

# The first argument is expected to be a version tag like '2.0.20240615',
# '2.0.latest', '3.0.20240615-rc', etc.
VERSION_TAG=$1

# Construct the full OCI artifact path based on the provided version tag. Below
# splits the VERSION_TAG into major version (e.g., '2.0') and the specific tag
# (e.g., '20240615' or 'latest').
MAJOR_VERSION=$(echo $VERSION_TAG | cut -d'.' -f1-2)
SPECIFIC_TAG=$(echo $VERSION_TAG | cut -d'.' -f3-)

# Check if the specific tag is 'latest'. If not, prepend the MAJOR_VERSION to
# it.
if [ "$SPECIFIC_TAG" != "latest" ]; then
    SPECIFIC_TAG="${MAJOR_VERSION}.${SPECIFIC_TAG}"
fi

# Construct the OCI Artifact full path.
OCI_ARTIFACT_PATH="mcr.microsoft.com/azurelinux/${MAJOR_VERSION}/image/minimal-os:${SPECIFIC_TAG}"

ARTIFACT_DIR="/oci/artifact"
mkdir -p $ARTIFACT_DIR

# Pull the OCI artifact, and check if the pull was successful.
oras pull $OCI_ARTIFACT_PATH -o $ARTIFACT_DIR
if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch image with the provided version $version"
    exit 1
fi

# Find the VHDX file matching the pattern 'image.vhdx'.
VHDX_PATH=$(find $ARTIFACT_DIR -type f -name 'image.vhdx' -print -quit)

# Check if the VHDX base image file exists. 
if [ ! -f $VHDX_PATH ]; then
    echo "Error: VHDX file not found at $VHDX_PATH"
    exit 1
fi

# Remove the first argument (VERSION_TAG) and pass the rest to the MIC binary.
shift
imagecustomizer --image-file $VHDX_PATH "$@"
