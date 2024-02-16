#!/bin/bash

set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../..

# ---- parameters ----

# mic container
containerRegistery=xyz.azurecr.io
containerName=mic-iso
containerTag=v0.1

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

# works without issues.
docker run --rm \
  --privileged=true \
   -v $inputImageDir:$containerInputImageDir:z \
   -v $inputConfigDdir:$containerInputConfigDir:z \
   -v $outputImageDir:$containerOutputDir:z \
   -v /dev:/dev:z \
   -e MIC_INPUT_IMAGE=$containerInputImage \
   -e MIC_INPUT_CONFIG=$containerInputConfig \
   -e MIC_BUILD_DIR=$containerBuildDir \
   -e MIC_OUTPUT_FORMAT=$outputFormat \
   -e MIC_OUTPUT_IMAGE=$containerOutputImage \
   -e MIC_LOG_LEVEL=$micLogLevel \
   $containerFullPath

# Error:
# Failed to create loopback device using losetup: losetup: cannot find an unused loop device
#
# docker run --rm \
#   --cap-add ALL \
#    -v $inputImageDir:/input:z \
#    -v $outputImageDir:/output:z \
#    $containerFullPath

# Error:
# Failed to create loopback device using losetup: losetup: cannot find an unused loop device
#
# docker run --rm \
#   --cap-add SYS_ADMIN \
#    -v $inputImageDir:/input:z \
#    -v $outputImageDir:/output:z \
#    $containerFullPath

