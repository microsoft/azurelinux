#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
CONTAINER_TAG="imagecustomizertestrpms:latest"
DOCKERFILE_DIR="$SCRIPT_DIR/downloader"

AZURELINUX_2_CONTAINER_IMAGE="mcr.microsoft.com/cbl-mariner/base/core:2.0"

IMAGE_VERSION="2.0"

while getopts "t:" flag
do
    case "${flag}" in
        t) IMAGE_VERSION="$OPTARG";;
        h) ;;&
        ?)
            echo "Usage: download-test-rpms.sh [-t IMAGE_VERSION]"
            echo ""
            echo "Args:"
            echo "  -t IMAGE_VERSION   The Azure Image version to download the RPMs for."
            echo "  -h Show help"
            exit 1;;
    esac
done

case "${IMAGE_VERSION}" in
  2.0)
    CONTAINER_IMAGE="$AZURELINUX_2_CONTAINER_IMAGE"
    ;;
  *)
    echo "error: unsupported Azure Linux version: $IMAGE_VERSION"
    exit 1;;
esac

set -x

DOWNLOADER_RPMS_DIRS="$SCRIPT_DIR/downloadedrpms"
OUT_DIR="$DOWNLOADER_RPMS_DIRS/$IMAGE_VERSION"
REPO_FILE="$DOWNLOADER_RPMS_DIRS/rpms-$IMAGE_VERSION.repo"

mkdir -p "$OUT_DIR"

# Build a container image that contains the RPMs.
docker build \
  --build-arg "baseimage=$AZURELINUX_2_CONTAINER_IMAGE" \
  --tag "$CONTAINER_TAG" \
  "$DOCKERFILE_DIR"

# Extract the RPM files.
docker run \
  --rm \
   -v $OUT_DIR:/outdir:z \
   "$CONTAINER_TAG" \
   cp -r /downloadedrpms/. "/outdir"

# Create repo file.
cat << EOF > "$REPO_FILE"
[localrpms]
name=Local RPMs repo
baseurl=file://$OUT_DIR
enabled=1
EOF
