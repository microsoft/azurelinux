#!/bin/bash

set -x
set -e

inputImageDir=/input
inputImageName=core-3.0.20240129.1326.vhdx
inputConfigName=mic-config-iso.yaml
isoBuildDir=/build
outputImageDir=/output

mkdir -p $inputImageDir
mkdir -p $isoBuildDir
mkdir -p $outputImageDir

inputImage=$inputImageDir/$inputImageName
inputConfig=$inputImageDir/$inputConfigName
outputImage=$outputImageDir/mic-$(date +'%Y%m%d-%H%M').iso

sudo /mic/imagecustomizer \
    --build-dir $isoBuildDir \
    --image-file $inputImage \
    --output-image-file $outputImage \
    --output-image-format iso \
    --config-file $inputConfig \
    --log-level debug