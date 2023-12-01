#!/bin/bash

set -x
set -e

originalISO=$1
isoMountDir=$2
outputDir=$3

function extract_initrd_and_vmlinuz () {
    local inputISO=$1
    local isoMountDir=$2
    local outputDir=$3

    set +e
    mounted=$(mount | grep $isoMountDir)
    set -e

    if [[ ! -z $mounted ]]; then
        sudo umount $isoMountDir
        sudo rm -r $isoMountDir
    fi    

    sourceInitrd=$isoMountDir/isolinux/initrd.img
    sourceVMLinuz=$isoMountDir/isolinux/vmlinuz

    sudo mkdir -p $isoMountDir
    sudo mount -o loop $inputISO $isoMountDir

    sudo rm -rf $outputDir
    mkdir -p $outputDir
    sudo cp $sourceInitrd $outputDir/initrd.img
    sudo cp $sourceVMLinuz $outputDir/vmlinuz

    sudo umount $isoMountDir
    sudo rm -r $isoMountDir
}

extract_initrd_and_vmlinuz \
    $originalISO \
    $isoMountDir \
    $outputDir
