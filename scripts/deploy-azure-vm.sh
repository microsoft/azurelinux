#!/bin/bash

set -euxo pipefail
# Prevent MSYS2/Git Bash from mangling paths like /subscriptions/... into C:/Program Files/Git/subscriptions/...
export MSYS_NO_PATHCONV=1
# Find the absolute path of the directory containing this script
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPTS_DIR/common.sh"

image_version="$(get-image-version)"
az vm create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$VM_NAME" \
        --size "$TEST_VM_SIZE" \
        --admin-username "$SSH_USER" \
        --ssh-key-values "$(cygpath -w "$SSH_PUBLIC_KEY_PATH")" \
        --image "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.Compute/galleries/$GALLERY_NAME/images/$GALLERY_IMAGE_DEFINITION/versions/$image_version" \
        --location "$LOCATION" \
        --debug
