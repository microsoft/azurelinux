# Set your Azure subscription ID
export SUBSCRIPTION_ID="b8f169b2-5b23-444a-ae4b-19a31b5e3652"

# Set resource configuration
export RESOURCE_GROUP_NAME="liunanmarinerakstest"
export LOCATION="westus3"
export STORAGE_ACCOUNT_NAME="basevmimage"
export STORAGE_CONTAINER_NAME="vhds"
export PUBLISHER="liunan"
export OFFER="basevmimageoffer"
export VERSION="0.0.1"
export SSH_USER="liunan-test"
export SSH_PUBLIC_KEY_PATH="/home/liunan/.ssh/id_rsa.pub"
export TEST_VM_SIZE="Standard_D2_v4"

# Set local image path
export IMAGE_PATH="./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.vhd"

# Set gallery configuration
export GALLERY_NAME="basevmimagegallery"
export GALLERY_IMAGE_DEFINITION="basevmimage"
export VM_NAME="azl4-vm"