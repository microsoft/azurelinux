#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
set -o errexit

[ -n "${DEBUG:-}" ] && set -o xtrace

readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly IMAGE_BUILD_ROOT=`mktemp --directory -t mariner-coco-build-uvm-image-XXXXXX`

generate_image()
{
    pushd "${IMAGE_BUILD_ROOT}"

    gcc -O2 ${ROOT_FOLDER}/opt/mariner/share/uvm/tools/osbuilder/image-builder/nsdax.gpl.c \
      -o ${IMAGE_BUILD_ROOT}/nsdax

    # build image
    sudo \
      NSDAX_BIN=${IMAGE_BUILD_ROOT}/nsdax \
      ${ROOT_FOLDER}/opt/mariner/share/uvm/tools/osbuilder/image-builder/image_builder.sh \
      ${ROOT_FOLDER}/rootfs-cbl-mariner

    sudo cp kata-containers.img $OUT_DIR

    popd
    sudo rm -rf "${IMAGE_BUILD_ROOT}"
}


while getopts ":r:o:" OPTIONS; do
  case "${OPTIONS}" in
    r ) ROOT_FOLDER=$OPTARG ;;
    o ) OUT_DIR=$OPTARG ;;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

echo "-- ROOT_FOLDER: $ROOT_FOLDER"
echo "-- OUT_DIR: $OUT_DIR"

generate_image $*
