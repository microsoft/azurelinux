#!/bin/bash
# https://basevmimage.blob.core.windows.net/vhds/azl4-vm-base.x86_64-0.1.vhd
# Find the absolute path of the directory containing this script
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPTS_DIR/common.sh"

storage_account_url="https://$STORAGE_ACCOUNT_NAME.blob.core.windows.net"
storage_account_resource_id="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.Storage/storageAccounts/$STORAGE_ACCOUNT_NAME"

replicationMode="Shallow"
image_version=$VERSION
storage_blob_endpoint="$storage_account_url/$STORAGE_CONTAINER_NAME/$storage_blob_name"

az account set --subscription "$SUBSCRIPTION_ID"

if [ "$(az group exists -n "$RESOURCE_GROUP_NAME")" == "false" ]; then
    az group create \
        --name "$RESOURCE_GROUP_NAME" \
        --location "$LOCATION"
fi

# Ensure STORAGE_ACCOUNT_NAME exists and the managed identity has access
storage_account_resource_id="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.Storage/storageAccounts/$STORAGE_ACCOUNT_NAME"
if ! az storage account show --ids "$storage_account_resource_id"; then
    echo "Could not find storage account \"$STORAGE_ACCOUNT_NAME\" in the expected location. Creating the storage account."

    if [ "$(az storage account check-name --name "$STORAGE_ACCOUNT_NAME" --query nameAvailable)" == "false" ]; then
        echo "Storage account name $STORAGE_ACCOUNT_NAME is not available"
        exit 1
    fi
    az storage account create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$STORAGE_ACCOUNT_NAME" \
        --location "$LOCATION" \
        --allow-shared-key-access false
fi

# Ensure "build_target" storage container exists
containerExists=$(az storage container exists --account-name "$STORAGE_ACCOUNT_NAME" --name "$STORAGE_CONTAINER_NAME" --auth-mode login | jq .exists)
if [[ $containerExists != "true" ]]; then
    echo "Could not find container \"$STORAGE_CONTAINER_NAME\". Creating container \"$STORAGE_CONTAINER_NAME\" in storage account \"$STORAGE_ACCOUNT_NAME\"..."
    az storage container create \
        --account-name "$STORAGE_ACCOUNT_NAME" \
        --name "$STORAGE_CONTAINER_NAME" \
        --auth-mode login
fi

# Upload the image artifact to Steamboat Storage Account
azcopy copy "$IMAGE_PATH" "$storage_blob_endpoint"

# Ensure STEAMBOAT_GALLERY_NAME exists
if ! az sig show -r "$GALLERY_NAME" -g "$RESOURCE_GROUP_NAME"; then
    echo "Could not find image gallery \"$GALLERY_NAME\" in resource group \"$RESOURCE_GROUP_NAME\". Creating the gallery."
    az sig create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --gallery-name "$GALLERY_NAME" \
        --location "$LOCATION"
fi

# Ensure the "build_target" image-definition exists
# Note: We publish only the VHD from the secure-prod the SIG
imageDefinitionExists=$(az sig image-definition list -r "$GALLERY_NAME" -g "$RESOURCE_GROUP_NAME" | grep "name" | grep -c "$GALLERY_IMAGE_DEFINITION" || :;) # the "|| :;" prevents grep from halting the script when it finds no matches and exits with exit code 1
if [[ $imageDefinitionExists -eq 0 ]]; then
    echo "Could not find image-definition \"$GALLERY_IMAGE_DEFINITION\". Creating definition \"$GALLERY_IMAGE_DEFINITION\" in gallery \"$GALLERY_NAME\"..."
    az sig image-definition create \
        --gallery-image-definition "$GALLERY_IMAGE_DEFINITION" \
        --publisher "$PUBLISHER" \
        --offer "$OFFER" \
        --sku "$GALLERY_IMAGE_DEFINITION" \
        --gallery-name "$GALLERY_NAME" \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --location "$LOCATION" \
        --os-type Linux
fi

# Convert comma-separated regions to JSON array for bicep template
# Note: Using a single region for now
REGIONS_JSON=$(echo "$LOCATION" | awk -F, '{
  printf "[";
  for(i=1;i<=NF;i++) {
    printf "\"%s\"", $i;
    if(i<NF) printf ",";
  }
  printf "]";
}')
# Create Image Version from storage account blob
az deployment group create \
  --name "$GALLERY_IMAGE_DEFINITION-$image_version" \
  --resource-group "$RESOURCE_GROUP_NAME" \
  --template-file "$SCRIPTS_DIR/azure-gallery-image-base.bicep" \
  --parameters galleryName="$GALLERY_NAME" \
               imageDefinitionName="$GALLERY_IMAGE_DEFINITION" \
               versionName="$image_version" \
               location="westus3" \
               regions='["westus3"]' \
               sourceDiskId="$storage_account_resource_id" \
               sourceDiskUrl="$storage_blob_endpoint" \
               replicationMode="$replicationMode"


# az group create -n $RESOURCE_GROUP_NAME -l $LOCATION
# az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --location $LOCATION
# az storage container create --account-name $STORAGE_ACCOUNT_NAME --auth-mode login --name $STORAGE_CONTAINER_NAME

# az storage blob upload --account-name $STORAGE_ACCOUNT_NAME --container-name $STORAGE_CONTAINER_NAME \
#     --name image.vhdx \
#     --file image.vhdx \
#     --auth-mode login