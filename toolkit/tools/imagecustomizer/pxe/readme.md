# PXE Temporary Workaround

The boot flow is like this now:
- boot loader loads grub.cfg - and then loads kernel and initrd in memory.
- kernel initializes, and calls unto initrd entry point - systemd is launched.
- initrd tells the kernel that the rootfs is an embedded file.
- initrd launches the dracutdownload-artifacts.sh script
  - script reads the url parameter defined in grub.cfg and downloads the trident configuration to /run/initramfs/downloaded-artifacts/trident.yaml
- initrd switches to the embedded rootfs.
- the rootfs initialization entry point is invoked - systemd is launched.
- trident daemon is launched and looks for its configuration under /run/initramfs/downloaded-artifacts/trident.yaml

The implement this:
- Download the base image from Azure Linux artifact feed from [here](https://dev.azure.com/mariner-org/mariner/_artifacts/feed/AzureLinuxArtifacts).
  - If you download `baremetal_vhdx-2.0-stable`, the vhdx will be named `core-2.0.20240425.vhdx`.
  - Let's copy the downloaded vhdx to `~/temp/core-2.0.20240425.vhdx`
- Enlist in AzureLinux
  ```bash
  cd ~/git
  git clone git@github.com:microsoft/azurelinux.git
  cd azurelinux
  ```
- Checkout 3.0 dev
  - Use MIC to create an intermediate ISO.
    - it has trident and all its dependencies installed.
    - trident must be configured to read its configuration from /run/initramfs/downloaded-artifacts/trident.yaml
- Checkout gmileka/mic-iso-pxe
  - Stage the artifacts we need from the base iso:
    ```bash
    enlistmentDir=~/git/CBL-Mariner-PXE
    pxeIsoArtifactsDir=$enlistmentDir/toolkit/tools/imagecustomizer/pxe/config/initrd-additional-artifacts

    # mount the base iso
    sudo mkdir /mnt/trident-mos-testimage.iso
    sudo mount ~/temp/trident-mos-testimage.iso /mnt/trident-mos-testimage.iso
    sudo find /mnt/trident-mos-testimage.iso

    # copy the artifacts we need from the base iso to our local config folder
    sudo cp /mnt/trident-mos-testimage.iso/liveos/rootfs.img $pxeIsoArtifactsDir
    sudo cp /mnt/trident-mos-testimage.iso/images/esp.raw.zst $pxeIsoArtifactsDir
    sudo cp /mnt/trident-mos-testimage.iso/images/root.raw.zst $pxeIsoArtifactsDir
    sudo chown $USER:$USER $pxeIsoArtifactsDir/*
    ```
  - Build the PXE ISO:
    ```bash
    $enlistmentDir/toolkit/tools/imagecustomizer/pxe/gen-pxe-iso.sh \
        ~/temp/core-2.0.20240425.vhdx
    ```
  - Boot the generate iso on hyper-v to make sure it is usable.
  - Extract the artifacts from the generated iso:
    ```bash
    cd $enlistmentDir
    pxeIsoPath=$(ls $enlistmentDir/mic-build/out/initrd-with-downloader*.iso)
    pxeIsoMountPath=/mnt/$(basename $pxeIsoPath)
    sudo mkdir -p $pxeIsoMountPath
    sudo mount $pxeIsoPath $pxeIsoMountPath
    sudo find $pxeIsoMountPath
  
    pxeArtifactsDir=~/temp/pxe-artifacts
    mkdir -p $pxeArtifactsDir
    sudo cp $pxeIsoMountPath/boot/grub2/grub.cfg $pxeArtifactsDir/
    sudo cp $pxeIsoMountPath/boot/vmlinuz $pxeArtifactsDir/
    sudo cp $pxeIsoMountPath/boot/initrd.img $pxeArtifactsDir/
    sudo cp $pxeIsoMountPath/esp.raw.zst $pxeArtifactsDir/
    sudo cp $pxeIsoMountPath/root.raw.zst $pxeArtifactsDir/
    ```
- Update the kernel parameters inside: grub.cfg 
  - Replace the root= with the value you typically use with pxe.
  - Add url=value
    - 'value' can be anything you want azurelinux/toolkit/tools/imagecustomizer/pxe/config/dracut-downloader-module/download-artifacts.sh at gmileka/mic-iso-pxe · microsoft/azurelinux (github.com) to act upon.
- Deploy
