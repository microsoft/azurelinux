#!/bin/bash

set -x
set -e

originalRawDisk=$1
rawDiskMountDir=$2
workingDir=$3

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

function extract_vmlinuz_from_full_disk() {

  local rawDiskMountDir=$1
  local workingDir=$2

  extractedDir=$workingDir/original-vmlinuz-extracted
  mkdir -p $extractedDir

  pushd $extractedDir

  linuzvm=$(sudo find $rawDiskMountDir/boot/ -name "vmlinuz*")
  sudo cp $linuzvm .

  # change ownership
  localLinuzvmName=$(basename "$linuzvm")
  sudo chown george:george $localLinuzvmName

  echo "---- extracted vmlinuz ----"
  ls -la $extractedDir
  echo "---- ---- ----"

  popd
}

sudo rm -rf $workingDir
mkdir -p $workingDir
pushd $workingDir

mount_raw_disk $originalRawDisk $rawDiskMountDir $workingDir
extract_vmlinuz_from_full_disk $rawDiskMountDir $workingDir
unmount_raw_disk $rawDiskMountDir