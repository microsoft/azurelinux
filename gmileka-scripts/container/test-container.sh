#!/bin/bash

set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../..

# cp /home/george/git/CBL-Mariner-POC/out/images/baremetal/core-3.0.20240129.1326.vhdx  /home/george/git/CBL-Mariner-POC/gmileka-scripts/container/input-mount/
# cp /home/george/git/CBL-Mariner-POC/gmileka-scripts/mic-config-iso.yaml /home/george/git/CBL-Mariner-POC/gmileka-scripts/container/input-mount/

inputDir=$enlistmentRoot/gmileka-scripts/container/input-mount
outputDir=$enlistmentRoot/gmileka-scripts/container/output-mount

containerRegistery=xyz.azurecr.io
containerName=mic-iso
containerTag=v0.1
containerFullPath=$containerRegistery/$containerName/$containerTag

sudo rm -rf $outputDir
mkdir -p $outputDir

# works without issues.
docker run --rm \
  --privileged=true \
   -v $inputDir:/input:z \
   -v $outputDir:/output:z \
   $containerFullPath

# Error:
# Failed to create loopback device using losetup: losetup: cannot find an unused loop device
#
# docker run --rm \
#   --cap-add ALL \
#    -v $inputDir:/input:z \
#    -v $outputDir:/output:z \
#    $containerFullPath

# Error:
# Failed to create loopback device using losetup: losetup: cannot find an unused loop device
#
# docker run --rm \
#   --cap-add SYS_ADMIN \
#    -v $inputDir:/input:z \
#    -v $outputDir:/output:z \
#    $containerFullPath

