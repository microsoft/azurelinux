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

# ---- main ----

containerStagingFolder=$(mktemp -d)

function cleanUp() {
    local exit_code=$?
    sudo rm -rf $containerStagingFolder
    exit $exit_code
}
trap 'cleanUp' ERR

containerFullPath=$containerRegistery/$containerName/$containerTag
dockerFile=$enlistmentRoot/toolkit/tools/imagecustomizer/container/Dockerfile.image-builder

mkdir -p $containerStagingFolder/mic

# stage those files that need to be in the container
cp $enlistmentRoot/toolkit/tools/imagecustomizer/imagecustomizer $containerStagingFolder/mic
touch $containerStagingFolder/.mariner-toolkit-ignore-dockerenv

# build the container
pushd $containerStagingFolder
docker build -f $dockerFile . -t $containerFullPath
popd

# clean-up
cleanUp
