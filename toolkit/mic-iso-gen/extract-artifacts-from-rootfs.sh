#!/bin/bash

set -x
set -e

originalRawDisk=$1
rawDiskMountDir=$2
workingDir=$3
outputDir=$4

extractedVmLinuzFileRootDir=$outputDir/extracted-vmlinuz-file
extractedInitrdFileRootDir=$outputDir/extracted-initrd-file
extractedInitrdRootDir=$outputDir/extracted-initrd
extractedRootfsRootDir=$outputDir/extracted-rootfs

function mount_raw_disk() {
    local originalRawDisk=$1
    local rawDiskMountDir=$2
    local workingDir=$3

    set +e
    mounted=$(mount | grep $rawDiskMountDir)
    set -e

    if [[ ! -z $mounted ]]; then
        sudo umount $rawDiskMountDir
        sudo rm -r $rawDiskMountDir
    fi

    cp $originalRawDisk $workingDir/
    rawDisk=$workingDir/$(basename "$originalRawDisk")

    loDevice=$(sudo losetup --show -f -P $rawDisk)
    echo "Found lo device: $loDevice"
    
    sudo rm -rf $rawDiskMountDir
    sudo mkdir -p $rawDiskMountDir
    sudo mount ${loDevice}p2 $rawDiskMountDir
}

function unmount_raw_disk() {
    local rawDiskMountDir=$1
    sudo umount $rawDiskMountDir
}

function copy_vmlinuz_from_full_disk() {

    local rawDiskMountDir=$1
    local extractedVmLinuzFileRootDir=$2

    sudo rm -rf $extractedVmLinuzFileRootDir
    mkdir -p $extractedVmLinuzFileRootDir

    pushd $extractedVmLinuzFileRootDir

    linuzvm=$(sudo find $rawDiskMountDir/boot/ -name "vmlinuz*")
    sudo cp $linuzvm .

    # change ownership
    localLinuzvmName=$(basename "$linuzvm")
    sudo chown george:george $localLinuzvmName

    echo "---- extracted vmlinuz ----"
    ls -la $extractedVmLinuzFileRootDir
    echo "---- ---- ----"

    popd
}

function copy_rootfs_contents() {
    local sourceRoot=$1
    local extractedRootfsRootDir=$2

    sudo rm -rf $extractedRootfsRootDir
    mkdir -p $extractedRootfsRootDir
    sudo cp -r -a $sourceRoot/* $extractedRootfsRootDir/

    ls -la $extractedRootfsRootDir
    sudo du -sh $extractedRootfsRootDir
}

function extract_and_expand_initrd_from_full_disk() {
  local rawDiskMountDir=$1
  local extractedInitrdFileRootDir=$2
  local extractedInitrdRootDir=$3
  local workingDir=$4

  pushd $workingDir

  #
  # 22 MB compressed, 42MB decompressed
  # Copy original to working directory
  originalInitrdImg=$(sudo find $rawDiskMountDir/boot -name "initrd.img*")
  mkdir -p $extractedInitrdFileRootDir
  sudo cp $originalInitrdImg $extractedInitrdFileRootDir/

  sudo cp $originalInitrdImg $workingDir/

  # Rename
  tempInitrdImg=$(find $workingDir -name "initrd.img*")
  mv $tempInitrdImg ${tempInitrdImg}.gz
  tempInitrdImgGz=${tempInitrdImg}.gz
  
  # change ownership
  sudo chown george:george $tempInitrdImgGz

  # decompress
  pigz -k -d $tempInitrdImgGz

  # extract from archive
  mkdir -p $extractedInitrdRootDir
  pushd $extractedInitrdRootDir
  set +e
  cpio -i --make-directories < $tempInitrdImg
  # cpio: dev/console: Cannot mknod: Operation not permitted
  # cpio: dev/kmsg: Cannot mknod: Operation not permitted
  # cpio: dev/null: Cannot mknod: Operation not permitted
  # cpio: dev/random: Cannot mknod: Operation not permitted
  # cpio: dev/urandom: Cannot mknod: Operation not permitted
  # 85524 blocks
  set -e
  echo "---- extracted initrd contents ----"
  ls -la $extractedInitrdRootDir
  echo "---- ---- ----"
  popd

  popd
}

sudo rm -rf $workingDir
mkdir -p $workingDir
pushd $workingDir

mount_raw_disk $originalRawDisk $rawDiskMountDir $workingDir
copy_vmlinuz_from_full_disk $rawDiskMountDir $extractedVmLinuzFileRootDir
extract_and_expand_initrd_from_full_disk $rawDiskMountDir $extractedInitrdFileRootDir $extractedInitrdRootDir $workingDir
copy_rootfs_contents $rawDiskMountDir $extractedRootfsRootDir
unmount_raw_disk $rawDiskMountDir

popd

ls -la $outputDir