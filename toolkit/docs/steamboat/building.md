# Building Steamboat

## Dependencies

- [Standard AzL 3.0 dependencies](/toolkit/docs/building/building.md#install-prerequisites)
- parted >=3.6

_Note: If you are on Mariner 2.0, you will need to build Parted 3.6 from source. You should be able to build and install using [this srpm](https://packages.microsoft.com/azurelinux/3.0/prod/base/srpms/Packages/p/parted-3.6-1.azl3.src.rpm) from PMC_

## Building an image
Set up an AzureLinux 3 build environment with coal/experimental. When iterating on packages or images, call `sudo make clean-imagegen` between builds to ensure the imager's local repo stays up-to-date.
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
1. Start your Hyper-V Manager
2. Use `scp` to transfer your **vhdx** from your linux build machine to your windows environment 
3. In Hyper-V Manager, Select `Quick Create...`
4. Select `_Local installation source` and browse to your downloaded vhdx
5. (optionally) Set a name for your vm by opening `more options` in the bottom right of the window
6. Uncheck the `This virtual machine will run Windows (enables Windows Secure Boot)` box.
7. Click `Create Virtual Machine`
8. Connect to your new VM and watch the boot take place
9. To confirm this was booted with the uki, type `bootctl` into the terminal. 
    - This will show the current bootloader (systemd-boot, running from the renamed binary, "grubx64.efi")
    - If you scroll down, you will see the id of the default boot loader entry is `vmlinux-uki-%{kernel-version}.azl3.efi`. This is the entry that was used to boot your VM.