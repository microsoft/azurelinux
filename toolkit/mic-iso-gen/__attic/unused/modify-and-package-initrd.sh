#!/bin/bash

set -x
set -e

originalInitrdExpandedDir=$1
workingDir=$2
modifiedInitrd=$3

function modifyInitrd() {
    local originalInitrdExpandedDir=$1
    local modifiedInitrdExpandedDir=$2

    mkdir -p $modifiedInitrdExpandedDir
    cp -r $originalInitrdExpandedDir/* $modifiedInitrdExpandedDir/

    ls -la $modifiedInitrdExpandedDir

  # patch /etc/passwrd @ root
  # < root::0:0::/root:/bin/sh
  # > root::0:0::/root:/root/mariner-iso-start-up.sh
  # cp ~/temp/iso-initrd-inspect/extract/root/mariner-iso-start-up.sh ~/temp/full-image-initrd-inspect/extract/root
}

function buildInitrd() {
    local modifiedInitrdExpandedDir=$1
    local modifiedInitrd=$2

    pushd $modifiedInitrdExpandedDir

    find . -depth | cpio -o > $modifiedInitrd
    pigz -c $modifiedInitrd > ${modifiedInitrd}.gz
    mv $modifiedInitrd ${modifiedInitrd}-uncompressed
    mv ${modifiedInitrd}.gz $modifiedInitrd
    popd
}

sudo rm -rf $workingDir

modifiedInitrdExpandedDir=$workingDir/modified-initrd-extracted

modifyInitrd $originalInitrdExpandedDir $modifiedInitrdExpandedDir
buildInitrd $modifiedInitrdExpandedDir $modifiedInitrd



