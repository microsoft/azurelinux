#!/bin/bash

set -x
set -e

originalRawDisk=$1
rawDiskMountDir=$2
workingDir=$3
outputDir=$4

newInitrdRoot=$outputDir/new-initrd-root

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

  # make a copy of the raw disk
  cp $originalRawDisk $workingDir/
  rawDisk=$workingDir/$(basename "$originalRawDisk")

  # mount the raw disk copy
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

function duplicate() {
    local sourceRoot=$1
    local targetRoot=$2

    sudo rm -rf $targetRoot
    mkdir -p $targetRoot
    sudo cp -r -a $sourceRoot/* $targetRoot/
}

sudo rm -rf $workingDir
mkdir -p $workingDir
mkdir -p $outputDir
pushd $workingDir

mount_raw_disk $originalRawDisk $rawDiskMountDir $workingDir
duplicate $rawDiskMountDir $newInitrdRoot

ls -la $newInitrdRoot
sudo du -sh $newInitrdRoot

# sudo chroot $newInitrdRoot

unmount_raw_disk $rawDiskMountDir