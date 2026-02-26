#!/bin/bash
set -euxo pipefail

REPO_ROOT="$( cd "$SCRIPTS_DIR/.." &> /dev/null && pwd )"

# Set your Azure subscription ID
export SUBSCRIPTION_ID="<your-subscription-id>"

# Set resource configuration
export RESOURCE_GROUP_NAME="<your-resource-group-name>"
export LOCATION="westus3"
export STORAGE_ACCOUNT_NAME="<your-storage-account-name>"
export STORAGE_CONTAINER_NAME="<your-storage-container-name>"
export PUBLISHER="<your-publisher-name>"
export OFFER="<your-offer-name>"
export TIME_TAG="$(date +%Y%m%d-%H%M%S)"
export STORAGE_BLOB_NAME="azl4-vm-base.x86_64-${TIME_TAG}.vhdfixed"
export VM_NAME="${USER}-azl-vm-${TIME_TAG}"
export SSH_USER="<your-ssh-username>"
export SSH_PUBLIC_KEY_PATH="<path-to-your-ssh-public-key>"
export TEST_VM_SIZE="<your-test-vm-size>"

# Set local image path
export IMAGE_PATH="./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhdfixed"

# Set gallery configuration
export GALLERY_NAME="<your-gallery-name>"
export GALLERY_IMAGE_DEFINITION="<your-image-definition-name>"
export REMOTE_KOJI_REPO_URL="<your-remote-koji-repo-url>"

function get-image-version() {
    # If the image definition doesn't exist yet, return the initial version
    if ! az sig image-definition show --resource-group "$RESOURCE_GROUP_NAME" --gallery-name "$GALLERY_NAME" --gallery-image-name "$GALLERY_IMAGE_DEFINITION" >/dev/null 2>&1; then
        echo "0.0.1"
        return 0
    fi

    # Get the latest version from the gallery
    local image_version
    image_version=$(az sig image-version list \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --gallery-name "$GALLERY_NAME" \
        --gallery-image-name "$GALLERY_IMAGE_DEFINITION" --query '[].name' -o tsv |
        sort -t "." -k1,1n -k2,2n -k3,3n |
        tail -1)

    if [ -z "$image_version" ]; then
        echo "0.0.1"
    else
        echo "$image_version"
    fi
}

function increment-version() {
    local version="${1:?Usage: increment-version <major.minor.patch>}"
    echo "$version" | awk -F. '{print $1"."$2"."$3+1}'
}
