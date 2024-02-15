#!/bin/bash

set -x
set -e

mkdir -p $MIC_BUILD_DIR
mkdir -p $(dirname $MIC_OUTPUT_IMAGE)

sudo /mic/imagecustomizer \
    --image-file $MIC_INPUT_IMAGE \
    --config-file $MIC_INPUT_CONFIG \
    --build-dir $MIC_BUILD_DIR \
    --output-image-file $MIC_OUTPUT_IMAGE \
    --output-image-format $MIC_OUTPUT_FORMAT \
    --log-level $MIC_LOG_LEVEL