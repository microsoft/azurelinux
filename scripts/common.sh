# Set your Azure subscription ID
export SUBSCRIPTION_ID="<your-subscription-id>"

# Set resource configuration
export RESOURCE_GROUP_NAME="<your-resource-group-name>"
export LOCATION="westus3"
export STORAGE_ACCOUNT_NAME="<your-storage-account-name>"
export STORAGE_CONTAINER_NAME="<your-storage-container-name>"
export PUBLISHER="<your-publisher-name>"
export OFFER="<your-offer-name>"
export VERSION="0.0.1"
export storage_blob_name="azl4-vm-base.x86_64-0.1.vhd"
export SSH_USER="<your-ssh-username>"
export SSH_PUBLIC_KEY_PATH="<path-to-your-ssh-public-key>"
export TEST_VM_SIZE="<your-test-vm-size>"

# Set local image path
export IMAGE_PATH="./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhd"

# Set gallery configuration
export GALLERY_NAME="<your-gallery-name>"
export GALLERY_IMAGE_DEFINITION="<your-gallery-image-definition>"
export VM_NAME="<your-vm-name>"
export REMOTE_KOJI_REPO_URL="<your-remote-koji-repo-url>"