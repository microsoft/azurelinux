#!/bin/bash

set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../..

containerStagingFolder=~/temp/container-staging

containerRegistery=xyz.azurecr.io
containerName=mic-iso
containerTag=v0.1
containerFullPath=$containerRegistery/$containerName/$containerTag

dockerFile=$enlistmentRoot/gmileka-scripts/container/Dockerfile.image-builder

sudo rm -rf $containerStagingFolder
mkdir -p $containerStagingFolder/mic

# stage those files that need to be in the container
cp $enlistmentRoot/toolkit/tools/imagecustomizer/imagecustomizer $containerStagingFolder/mic
cp $enlistmentRoot/gmileka-scripts/container/run-mic.sh $containerStagingFolder/mic
touch $containerStagingFolder/.mariner-toolkit-ignore-dockerenv

# build the container

pushd $containerStagingFolder

docker build -f $dockerFile . -t $containerFullPath

popd
