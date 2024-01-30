#!/bin/bash

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

echo_usage_and_exit() {
    echo "Usage: $0 inputImageFile inputConfigFile outputImageFile"
    echo
    echo "Creates a liveos iso from a full disk image."
    echo
    echo "example:"
    echo
    echo "cd CBL-Mariner"
    echo "$0 ./out/images/baremetal/core-2.0.20240119.1908.vhdx ./mic-config.yaml ./mic-out-image.iso"
    echo

    exit 2
}

if [[ $# > 3 ]]; then
  echo_usage_and_exit
fi

set -x
set -e

enlistmentRoot=$scriptDir
isoBuildDir=$enlistmentRoot/mic-build
isoOutDir=$isoBuildDir/out

inputImage=${1:-$scriptDir/out/images/baremetal/core-3.0.20240129.1326.vhdx}
inputConfigFile=${2:-$scriptDir/mic-config.yaml}
outputImage=${3:-$isoOutDir/mic-$(date +'%Y%m%d-%H%M').iso}

sudo apt-get install --assume-yes squashfs-tools

pushd $scriptDir/toolkit
sudo make go-tidy-all
popd

# build mic
pushd $scriptDir/toolkit/tools/imagecustomizer
go build

# invoke mic
sudo rm -rf $isoBuildDir
sudo ./imagecustomizer \
    --build-dir $isoBuildDir \
    --image-file $inputImage \
    --output-image-file $outputImage \
    --output-image-format iso \
    --config-file $inputConfigFile
    # \
    # --log-level debug


popd