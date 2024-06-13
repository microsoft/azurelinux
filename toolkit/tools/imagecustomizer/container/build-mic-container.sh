#!/bin/bash

# set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot=$scriptDir/../../../..

function showUsage() {
    echo
    echo "usage:"
    echo
    echo "build-mic-container.sh \\"
    echo "    -t <container-tag>"
    echo
}

while getopts ":r:n:t:" OPTIONS; do
  case "${OPTIONS}" in
    t ) containerTag=$OPTARG ;;
  esac
done

if [[ -z $containerTag ]]; then
    echo "missing required argument '-t containerTag'"
    showUsage
    exit 1
fi

# ---- main ----

containerStagingFolder=$(mktemp -d)

function cleanUp() {
    local exit_code=$?
    rm -rf $containerStagingFolder
    exit $exit_code
}
trap 'cleanUp' ERR

micLocalFile=$enlistmentRoot/toolkit/out/tools/imagecustomizer
micContainerFolder=/usr/bin

dockerFile=$enlistmentRoot/toolkit/tools/imagecustomizer/container/Dockerfile.mic-container

# stage those files that need to be in the container
mkdir -p ${containerStagingFolder}${micContainerFolder}
cp $micLocalFile ${containerStagingFolder}${micContainerFolder}
touch ${containerStagingFolder}/.mariner-toolkit-ignore-dockerenv

# build the container
pushd $containerStagingFolder
docker build -f $dockerFile . -t "$containerTag"
popd

# clean-up
cleanUp
