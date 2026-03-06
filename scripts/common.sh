#!/bin/bash
set -euxo pipefail

REPO_ROOT="$( cd "$SCRIPTS_DIR/.." &> /dev/null && pwd )"

# Set your Azure subscription ID (name for az commands, GUID for resource IDs)
export SUBSCRIPTION_NAME="EdgeOS_AzureLinux_ControlTower_Test"
export SUBSCRIPTION_ID="e4ab81f8-030f-4593-a8f2-3ea2c7630a19"

# Set resource configuration
export RESOURCE_GROUP_NAME="azl-preview-publishing"
export LOCATION="westus3"
export STORAGE_ACCOUNT_NAME="azlpubstagingoxz2o4gw"
export STORAGE_CONTAINER_NAME="images"
export PUBLISHER="MicrosoftAzureLinux"
export OFFER="azure-linux-4"
export TIME_TAG="$(date +%Y%m%d-%H%M%S)"
export STORAGE_BLOB_NAME="azl4-vm-base.x86_64-${TIME_TAG}.vhdfixed"
export VM_NAME="${USER:-${USERNAME:-unknown}}-azl-vm-${TIME_TAG}"
export SSH_USER="azureuser"
export SSH_PUBLIC_KEY_PATH="/c/Users/anphel/.ssh/id_rsa_azure.pub"

# Set VM size based on architecture
ARCH="<test-vm-architecture>" # e.g., "x86_64" or "aarch64"
if [ "$ARCH" = "aarch64" ]; then
    export TEST_VM_SIZE="Standard_D4ps_v6"
else
    export TEST_VM_SIZE="Standard_D4s_v5"
fi

# Set local image path
export IMAGE_PATH="$REPO_ROOT/out/azl4-vm-base.x86_64-0.1-1.vhdfixed"

# Set gallery configuration
export GALLERY_NAME="azlpubStagingGalleryoxz2o4gw"
export GALLERY_IMAGE_DEFINITION="AzureLinuxAlpha1-x64"
export REMOTE_KOJI_REPO_URL="http://20.88.251.114/kojifiles/"

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
