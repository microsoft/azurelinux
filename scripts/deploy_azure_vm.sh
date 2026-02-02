#!/bin/bash

set -euxo pipefail
# Find the absolute path of the directory containing this script
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPTS_DIR/common.sh"

az vm create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$VM_NAME" \
        --size "$TEST_VM_SIZE" \
        --os-disk-size-gb 60 \
        --admin-username "$SSH_USER" \
        --ssh-key-values "$SSH_PUBLIC_KEY_PATH" \
        --image "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.Compute/galleries/$GALLERY_NAME/images/$GALLERY_IMAGE_DEFINITION/versions/$VERSION" \
        --location "$LOCATION" \
        --debug