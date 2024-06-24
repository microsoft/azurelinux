#!/bin/bash
# entrypoint.sh

# The first argument is expected to be the OCI artifact path.
OCI_ARTIFACT_PATH=$1

# Validate that the OCI artifact path is from MCR.
if [[ $OCI_ARTIFACT_PATH != mcr.microsoft.com/*:* ]]; then
    echo "Error: Provided path '$OCI_ARTIFACT_PATH' is not a valid MCR OCI artifact path."
    echo "Expected format: 'mcr.microsoft.com/path/to/oci/artifact:tag'"
    exit 1
fi

ARTIFACT_DIR="/image/artifact"
mkdir -p $ARTIFACT_DIR
oras pull -a $OCI_ARTIFACT_PATH -o $ARTIFACT_DIR

# Find the VHDX file matching the pattern 'core-*.vhdx'.
VHDX_PATH=$(find $ARTIFACT_DIR -type f -name 'core-*.vhdx' -print -quit)

# Check if the VHDX file exists and confirm it's an expected file from an OCI
# artifact. This check acts as a validation of both the presence of the VHDX
# file and the correct OCI artifact type.
if [ ! -f $VHDX_PATH ]; then
    echo "Error: VHDX file not found at $VHDX_PATH"
    exit 1
fi

# Remove the first argument (OCI_ARTIFACT_PATH) and pass the rest to MIC binary.
shift
imagecustomizer --image-file $VHDX_PATH "$@"
