#!/bin/bash

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

# This file is needed to provide the kernel and the base for the new initrd.
# The rootfs is irrelevant.
inputVhdxImage=${1:-/home/george/temp/baremetal-core-2.0.20240430.vhdx}
enlistmentDir=$scriptDir/../../../..

micConfigDir=$enlistmentDir/toolkit/tools/imagecustomizer/pxe/config
micConfig=$micConfigDir/mic-config-initrd-downloader.yaml

isoBuildDir=$enlistmentDir/mic-build
isoOutDir=$isoBuildDir/out
imageCustomizerPath=$enlistmentDir/toolkit/out/tools/imagecustomizer


function echo_usage_and_exit() {
    echo "Usage: $0 inputImageFile inputConfigFile outputImageFile"
    echo
    echo "Creates a liveos iso from a full disk image."
    echo
    echo "example:"
    echo
    echo "cd CBL-Mariner"
    echo "$0 /home/george/temp/baremetal-core-2.0.20240430.vhdx ./mic-config.yaml ./mic-out-image.iso"
    echo

    exit 2
}

function buildMic() {
   pushd $enlistmentDir/toolkit
   sudo make go-tidy-all
   sudo rm -f $imageCustomizerPath
   # official, but slower.
   # sudo make go-tools REBUILD_TOOLS=y
   popd

   pushd $enlistmentDir/toolkit/tools/imagecustomizer
   sudo rm -f imagecustomizer
   go build
   sudo rm -f $imageCustomizerPath
   sudo cp imagecustomizer $imageCustomizerPath
   ls -la $imageCustomizerPath
   popd
}

function buildPxeIso() {
  local inputImage=$1
  local inputConfigFile=$2
  local outputFormat=$3
  local outputImagePrefix=$4
  
  outputImage=$isoOutDir/$outputImagePrefix-$(date +'%Y%m%d-%H%M').$outputFormat

  # invoke mic
  sudo $imageCustomizerPath \
      --build-dir $isoBuildDir \
      --image-file $inputImage \
      --output-image-format $outputFormat \
      --output-image-file $outputImage \
      --config-file $inputConfigFile \
      --log-level debug
}

# ---- main ----

if [[ $# > 3 ]]; then
  echo_usage_and_exit
fi

set -x
set -e

sudo apt-get install --assume-yes squashfs-tools

sudo rm -rf $isoBuildDir

buildMic

buildPxeIso \
   $inputVhdxImage \
   $micConfig \
   "iso" \
   "initrd-with-downloader"

echo "Success"