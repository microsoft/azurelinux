#!/bin/bash

set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../../../..

containerRegistery=xyz.azurecr.io
containerName=mic-iso
containerTag=v0.1

# ---- main ----

containerStagingFolder=$(mktemp -d)

function cleanUp() {
    sudo rm -rf $containerStagingFolder
    exit 1
}
trap 'cleanUp' ERR

containerFullPath=$containerRegistery/$containerName/$containerTag
dockerFile=$enlistmentRoot/toolkit/tools/imagecustomizer/container/Dockerfile.image-builder

mkdir -p $containerStagingFolder/mic

# stage those files that need to be in the container
cp $enlistmentRoot/toolkit/tools/imagecustomizer/imagecustomizer $containerStagingFolder/mic
# cp $enlistmentRoot/gmileka-scripts/container/run-mic.sh $containerStagingFolder/mic
touch $containerStagingFolder/.mariner-toolkit-ignore-dockerenv

# build the container

pushd $containerStagingFolder

docker build -f $dockerFile . -t $containerFullPath

popd

rm -r $containerStagingFolder
