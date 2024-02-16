#!/bin/bash

set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../../../..

# ---- parameters ----

# mic container
containerRegistery=mcr.azurecr.io
containerName=imagecustomizer
containerTag=v0.0.1

# mic arguments
inputImage=$enlistmentRoot/out/images/baremetal/core-3.0.20240129.1326.vhdx
inputConfig=$enlistmentRoot/gmileka-scripts/mic-config-iso.yaml
outputFormat=iso
outputImage=$enlistmentRoot/mic-build/out/mic-$(date +'%Y%m%d-%H%M').iso
micLogLevel=debug

# ---- main ----

containerFullPath=$containerRegistery/$containerName/$containerTag

inputImageDir=$(dirname $inputImage)
inputConfigDdir=$(dirname $inputConfig)
outputImageDir=$(dirname $outputImage)

sudo rm -rf $outputImageDir
sudo mkdir -p $outputImageDir

containerInputImageDir=/mic/input
containerInputImage=$containerInputImageDir/$(basename $inputImage)
containerInputConfigDir=/mic/config
containerInputConfig=$containerInputConfigDir/$(basename $inputConfig)
containerBuildDir=/mic/build
containerOutputDir=/mic/output
containerOutputImage=$containerOutputDir/$(basename $outputImage)

docker run --rm \
  --privileged=true \
   -v $inputImageDir:$containerInputImageDir:z \
   -v $inputConfigDdir:$containerInputConfigDir:z \
   -v $outputImageDir:$containerOutputDir:z \
   -v /dev:/dev:z \
   $containerFullPath \
   /mic/imagecustomizer \
      --image-file $containerInputImage \
      --config-file $containerInputConfig \
      --build-dir $containerBuildDir \
      --output-image-format $outputFormat \
      --output-image-file $containerOutputImage \
      --log-level $micLogLevel
