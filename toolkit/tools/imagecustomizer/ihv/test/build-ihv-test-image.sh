#!/bin/bash

set -x
set -e

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

# -- parameters ---------------------------------------------------------------

# need to publish image customier under `latest`
# imageCustomizerContainerTag=${1:-latest}
imageCustomizerContainerTag=${1:-0.4.0}

# need to publish baremetal image under `latest`
# inputImageTag=${2:-3.0.latest}
inputImageTag=${2:-3.0.20240624-rc}

# configurations
ihvArtifactsDir=$scriptDir/ihv-test-artifacts
fixYumConfigFile=fix-yum-repo-paths.yaml
setKernelLockdown=set-kernel-lockdown.yaml
ihvConfigFile=ihv-test-customizations.yaml

# -----------------------------------------------------------------------------
workDir=$(mktemp -d)

imageCustomizerContainerPath=mcr.microsoft.com/azurelinux/imagecustomizer

buildDir=$workDir/build
outDir=$workDir/output

outputImagePrefix=ihv-test
debugLevel=debug

# -----------------------------------------------------------------------------
sudo rm -rf $workDir
mkdir -p $buildDir
mkdir -p $outDir
 
intermediateOutputFormat0=vhdx
intermediateOutputImage0=/output/$outputImagePrefix-0-$(date +'%Y%m%d-%H%M').$intermediateOutputFormat0

sudo docker run --rm \
    --privileged=true \
    -v $ihvArtifactsDir:/ihv-artifacts:z \
    -v $buildDir:/build:z \
    -v $outDir:/output:z \
    -v /dev:/dev \
    $imageCustomizerContainerPath:$imageCustomizerContainerTag \
    run.sh $inputImageTag \
        --config-file /ihv-artifacts/$fixYumConfigFile \
        --build-dir /build \
        --output-image-format $intermediateOutputFormat0 \
        --output-image-file $intermediateOutputImage0 \
            --log-level $debugLevel

sudo chown $USER:$USER $outDir/*
ls -la $outDir

finalOutputFormat=iso
finalOutputImage=/output/$outputImagePrefix-$(date +'%Y%m%d-%H%M').$finalOutputFormat

sudo docker run --rm \
    --privileged=true \
    -v $ihvArtifactsDir:/ihv-artifacts:z \
    -v $buildDir:/build:z \
    -v $outDir:/output:z \
    -v /dev:/dev \
    $imageCustomizerContainerPath:$imageCustomizerContainerTag \
    imagecustomizer \
        --image-file $intermediateOutputImage0 \
        --config-file /ihv-artifacts/$ihvConfigFile \
        --build-dir /build \
        --output-image-format $finalOutputFormat \
        --output-image-file $finalOutputImage \
        --rpm-source /ihv-artifacts/rpm-repo \
        --log-level $debugLevel

sudo chown $USER:$USER $outDir/*
ls -la $outDir
