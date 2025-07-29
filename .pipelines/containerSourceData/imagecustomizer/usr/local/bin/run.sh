#!/bin/bash

set -euo pipefail
shopt -s nullglob

exit_with_usage() {
    local error_msg="$1"

    echo "Usage: run.sh <VERSION> [extra imagecustomizer args]"
    echo ""
    echo "This script pulls a base image of the specified version from the Microsoft Container Registry (MCR) and runs"
    echo "imagecustomizer on it."
    echo ""
    echo "Cross-architecture builds are not available, so the architecture of the base image pulled will always match"
    echo "the architecture of the host system."
    echo ""
    echo "The base image is pulled from the MCR and stored in /container/base."
    echo ""
    echo "Arguments:"
    echo "  VERSION  The version of the image to use as the base image for the imagecustomizer run."
    echo "           * If VERSION is in the format MAJOR.MINOR.latest or MAJOR.MINOR.latest-*, the script will pull the"
    echo "             image tag that matches the latest or latest-* suffix (e.g., 3.0.latest or 3.0.latest-preview)."
    echo "           * For any other format, the script will pull the tag that matches the full version string as"
    echo "             provided (e.g., 3.0.20250701 or 3.0.20250701-preview1)."
    echo "Options:"
    echo "  -h, --help  Show this help message and exit."
    echo ""
    echo "Environment variables:"
    echo ""
    echo "  BASE_IMAGE_NAME  The name of the base image to use (default: 'minimal-os')."
    echo ""

    if [[ -n "$error_msg" ]]; then
        echo "Error: $error_msg" >&2
        exit 1
    fi

    exit 0
}

ARG_VERSION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            exit_with_usage
            ;;
        -*)
            exit_with_usage "unknown option: '$1'"
            ;;
        *)
            ARG_VERSION="$1"
            shift
            break
            ;;
    esac
done

if [[ -z "$ARG_VERSION" ]]; then
    exit_with_usage "missing required argument: 'VERSION'"
fi

PLATFORM="linux/amd64"
case "$(uname -m)" in
    aarch64|arm64)
        PLATFORM="linux/arm64"
        ;;
esac

OCI_ARTIFACT_REGISTRY="mcr.microsoft.com"

BASE_IMAGE_NAME="${BASE_IMAGE_NAME:-minimal-os}"
VERSION_MAJOR_MINOR="$(echo "$ARG_VERSION" | cut -d'.' -f1-2)"
OCI_ARTIFACT_REPOSITORY="azurelinux/$VERSION_MAJOR_MINOR/image/$BASE_IMAGE_NAME"

VERSION_SUFFIX="$(echo "$ARG_VERSION" | cut -d'.' -f3-)"
if [[ "$VERSION_SUFFIX" == latest || "$VERSION_SUFFIX" == latest-* ]]; then
    OCI_ARTIFACT_TAG="$VERSION_SUFFIX"
else
    OCI_ARTIFACT_TAG="$ARG_VERSION"
fi

OCI_ARTIFACT_PATH="$OCI_ARTIFACT_REGISTRY/$OCI_ARTIFACT_REPOSITORY:$OCI_ARTIFACT_TAG"
echo "Pulling OCI artifact: '$OCI_ARTIFACT_PATH'"

ARTIFACT_DIR="/container/base"

OCI_MANIFEST_JSON="$(oras manifest fetch "$OCI_ARTIFACT_PATH" 2>/dev/null || echo "")"
if [[ -z "$OCI_MANIFEST_JSON" ]]; then
    echo "Error: failed to fetch manifest for '$OCI_ARTIFACT_PATH'" >&2
    exit 1
fi

OCI_MEDIA_TYPE="$(jq -r '.mediaType // empty' <<< "$OCI_MANIFEST_JSON")"
if [[ -z "$OCI_MEDIA_TYPE" ]]; then
    echo "Error: no media type found in the manifest for '$OCI_ARTIFACT_PATH'" >&2
    exit 1
fi

# New releases that are multi-arch must be fetched with the --platform option, while older (single-arch) releases must
# be fetched without it. Older releases are also always just the minimal-os image, so we do not need to derive the image
# file name from the manifest.
if [[ "$OCI_MEDIA_TYPE" == "application/vnd.oci.image.manifest.v1+json" ]]; then
    oras pull "$OCI_ARTIFACT_PATH" --output "$ARTIFACT_DIR"

    IMAGE_FILE_NAME="image.vhdx"
else
    oras pull --platform "$PLATFORM" "$OCI_ARTIFACT_PATH" --output "$ARTIFACT_DIR"

    IMAGE_FILE_NAME=""

    # The manifest must be re-fetched with the --platform option to obtain the list of files in the artifact. Fetch and
    # inspect the OCI artifact manifest to dynamically detect the image file name by looking for an SBOM file and
    # deriving the image file name from it. In new releases, SBOM files are always named as <image-file-name>.spdx.json.
    OCI_ARTIFACT_FILE_NAMES=($(oras manifest fetch --platform "$PLATFORM" "$OCI_ARTIFACT_PATH" 2>/dev/null | \
        jq -r '.layers[].annotations["org.opencontainers.image.title"]'))
    for name in "${OCI_ARTIFACT_FILE_NAMES[@]}"; do
        if [[ "$name" != *.spdx.json ]]; then
            continue
        fi

        if [[ -n "$IMAGE_FILE_NAME" ]]; then
            echo "Warning: multiple SBOMs found, using the image file name from the first: '$IMAGE_FILE_NAME'" >&2
            continue
        fi

        IMAGE_FILE_NAME="${name%.spdx.json}"
    done

    if [[ -z "$IMAGE_FILE_NAME" ]]; then
        echo "Error: no image file found in the OCI artifact '$OCI_ARTIFACT_PATH'" >&2
        exit 1
    fi
fi

imagecustomizer --image-file "$ARTIFACT_DIR/$IMAGE_FILE_NAME" "$@"
