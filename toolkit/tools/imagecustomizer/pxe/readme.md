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
- Enlist in AzureLinux
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
  - Download the latest 2.0 Mariner vhdx to `~/temp/baremetal-core-2.0.20240430.vhdx`.
    - This will be used to provide the kernel/base initrd. We will not use its rootfs.
  - Build the PXE ISO:
    ```bash
    $enlistmentDir/toolkit/tools/imagecustomizer/pxe/gen-pxe-iso.sh \
        ~/temp/baremetal-core-2.0.20240430.vhdx
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
