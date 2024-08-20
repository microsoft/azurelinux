# Building Steamboat

## Dependencies

- [Standard AzL 3.0 dependencies](/toolkit/docs/building/building.md#install-prerequisites)
- parted >=3.6

_Note: If you are on Mariner 2.0, you will need to build Parted 3.6 from source. You should be able to build and install using [this srpm](https://packages.microsoft.com/azurelinux/3.0/prod/base/srpms/Packages/p/parted-3.6-1.azl3.src.rpm) from PMC_

## Building an image
Set up an AzureLinux 3 build environment with coal/experimental. When iterating on packages or images, call `sudo make clean-imagegen` b/w builds to ensure the imager's local repo stays up-to-date.
```
# Setup the repo and clone the coal/experimental branch
git clone git@github.com:microsoft/azurelinux.git
cd azurelinux/toolkit
git checkout origin/coal/experimental

# Grab the azure-init sources to use as a local tarball
pushd ../SPECS/azure-init/
./generate-vendor-tarball.sh
popd

# Set credentials for your test image
TEST_PASSWORD="somePassw0rd"
sed -i "s/{{# SET THIS BEFORE BUILDING #}}/\"${TEST_PASSWORD}\"/g" ./imageconfigs/marketplace-gen2-coal.json

# Setup the build environment and build the marketplace-gen2-coal image definition
sudo make toolchain -j100 \
  REBUILD_TOOLCHAIN=n \
  REBUILD_TOOLS=y \
  USE_PREVIEW_REPO=y

sudo make image -j100 \
  CONFIG_FILE="./imageconfigs/marketplace-gen2-coal.json" \
  REBUILD_TOOLS=y \
  SRPM_PACK_LIST="dracut kernel-uki azure-init" \
  SRPM_FILE_SIGNATURE_HANDLING=update \
  PRECACHE=n \
  USE_PREVIEW_REPO=y
```

## Booting on Hyper-V
1. Start your Hyper-V server
2. use `scp` to transfer your **vhdx** from your linux build machine to your windows environment 