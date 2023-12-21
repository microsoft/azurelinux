#!/bin/bash

set -x
set -e

scriptDir=$(dirname "$BASH_SOURCE")

while getopts ":c:o:" OPTIONS; do
  case "${OPTIONS}" in
    c ) imageConfigFile=$OPTARG ;;
    o ) outputImageFile=$OPTARG ;;

    \? )
        echo "-- Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "-- Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

if [[ -z $imageConfigFile ]]; then
    echo "Specify the image config file (-c image-config.json)."
    exit 1
fi

if [[ -z $outputImageFile ]]; then
    echo "Specify the output image file (-o output-image-file)."
    exit 1
fi

echo "imageConfigFile = $imageConfigFile"
echo "outputImageFile = $outputImageFile"

#------------------------------------------------------------------------------
function create_full_image() {

    local configFile=$1
    local outputImageFile=$2

    sudo rm -rf ./build/imagegen/baremetal
    sudo rm -rf ./out/images/baremetal
    sudo rm -r $outputImageFile

    pushd toolkit
    sudo make image \
        -j$(nproc) \
        REBUILD_TOOLS=y \
        REBUILD_TOOLCHAIN=n \
        REBUILD_PACKAGES=n \
        CONFIG_FILE=$configFile

    mkdir -p $(dirname "$outputImageFile")
    tmpOutputImageFile=$(find ../out/images/baremetal -name "baremetal-*")
    cp $tmpOutputImageFile $outputImageFile

    popd
}

#------------------------------------------------------------------------------
#-- main ----------------------------------------------------------------------
pushd $scriptDir/../../

create_full_image  \
    $imageConfigFile \
    $outputImageFile

popd

ls -la $outputImageFile