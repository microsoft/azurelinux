#!/bin/bash

set -x
set -e

finalOutputImage=$1

debugWorkDir=/home/george/temp/ihv
debugOutputFormat=qcow2
debugOutputImage=$debugWorkDir/output/ihv-debug-$(date +'%Y%m%d-%H%M').$debugOutputFormat
debugLevel=debug

rm -rf $debugWorkDir
mkdir -p $debugWorkDir/build
mkdir -p $debugWorkDir/output

sudo /home/george/git/azurelinux-poc/toolkit/out/tools/imagecustomizer \
        --image-file $finalOutputImage \
        --config-file /home/george/git/azurelinux-poc/toolkit/tools/imagecustomizer/ihv/dev/ihv-dev-artifacts/ihv-dev-debug.yaml \
        --build-dir /home/george/temp/ihv/build \
        --output-image-format $debugOutputFormat \
        --output-image-file $debugOutputImage \
        --log-level $debugLevel

sudo chown $USER:$USER $debugWorkDir/output/*
ls -la $debugWorkDir/output


