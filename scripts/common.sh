#!/bin/bash
set -euxo pipefail
# Set your Azure subscription ID
export SUBSCRIPTION_ID="<your-subscription-id>"

# Set resource configuration
export RESOURCE_GROUP_NAME="<your-resource-group-name>"
export LOCATION="westus3"
export STORAGE_ACCOUNT_NAME="<your-storage-account-name>"
export STORAGE_CONTAINER_NAME="<your-storage-container-name>"
export PUBLISHER="<your-publisher-name>"
export OFFER="<your-offer-name>"
export storage_blob_name="azl4-vm-base.x86_64-$(date +%Y%m%d-%H%M%S).vhdfixed"
export SSH_USER="<your-ssh-username>"
export SSH_PUBLIC_KEY_PATH="<path-to-your-ssh-public-key>"
export TEST_VM_SIZE="<your-test-vm-size>"

# Set local image path
export IMAGE_PATH="./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhdfixed"

# Set gallery configuration
export GALLERY_NAME="<your-gallery-name>"
export GALLERY_IMAGE_DEFINITION="<your-gallery-image-definition>"
export VM_NAME="${USER}-azl-vm-$(date +%Y%m%d-%H%M%S)"
export REMOTE_KOJI_REPO_URL="<your-remote-koji-repo-url>"

function get-latest-version() {
    # Check if the image definition exists - return empty string if it doesn't (this is expected for new images)
    if ! az sig image-definition show --resource-group "$RESOURCE_GROUP_NAME" --gallery-name "$GALLERY_NAME" --gallery-image-name "$GALLERY_IMAGE_DEFINITION" >/dev/null 2>&1; then
        # Image definition doesn't exist, return empty string (this is normal for new images)
        return 0
    fi

    # If the image definition does exist, get the latest version
    az sig image-version list \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --gallery-name "$GALLERY_NAME" \
        --gallery-image-name "$GALLERY_IMAGE_DEFINITION" --query '[].name' -o tsv |
        sort -t "." -k1,1n -k2,2n -k3,3n |
        tail -1
}

function get-image-version() {
    local OP="${1:-}"

    if ! image_version=$(get-latest-version); then
        # get-latest-version failed, propagate the error
        echo "Error: Failed to retrieve latest image version from gallery '$GALLERY_NAME' in resource group '$RESOURCE_GROUP_NAME' for offer '$OFFER'" >&2
        return 1
    fi
    if [ -z "$image_version" ]; then
        image_version=0.0.1
    else
        if [ "$OP" == "increment" ]; then
            # Increment the semver version
            image_version=$(echo "$image_version" | awk -F. '{print $1"."$2"."$3+1}')
        fi
    fi

    echo "$image_version"
}

# Set VERSION to the latest image version in the gallery (used by publish and deploy scripts)
export VERSION
VERSION=$(get-latest-version 2>/dev/null || echo "")
if [ -z "$VERSION" ]; then
    VERSION="0.0.1"
fi
