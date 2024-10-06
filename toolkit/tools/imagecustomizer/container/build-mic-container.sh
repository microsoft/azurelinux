#!/bin/bash

# set -x
set -e

scriptDir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
enlistmentRoot="$scriptDir/../../../.."

ARCH="amd64"
ORAS_VERSION="1.1.0"

function showUsage() {
    echo
    echo "usage:"
    echo
    echo "build-mic-container.sh \\"
    echo "    -t <container-tag> \\"
    echo "    [-a <architecture>]"
    echo
    echo "    Architecture can be 'amd64' or 'arm64'. Default is 'amd64'."
    echo
}

while getopts ":a:t:" OPTIONS; do
  case "${OPTIONS}" in
    t ) containerTag=$OPTARG ;;
    a ) ARCH=$OPTARG ;;
    \? ) echo "Invalid option: -$OPTARG" >&2; showUsage; exit 1 ;;
    : ) echo "Option -$OPTARG requires an argument." >&2; showUsage; exit 1 ;;
  esac
done

if [[ -z $containerTag ]]; then
    echo "missing required argument '-t <container-tag>'"
    showUsage
    exit 1
fi

if [[ "$ARCH" != "amd64" && "$ARCH" != "arm64" ]]; then
    echo "Invalid architecture: $ARCH"
    showUsage
    exit 1
fi

# ---- main ----

buildDir="$(mktemp -d)"
containerStagingFolder="$buildDir/container"

function cleanUp() {
    local exit_code=$?
    rm -rf "$buildDir"
    exit $exit_code
}
trap 'cleanUp' ERR

micLocalFile="$enlistmentRoot/toolkit/out/tools/imagecustomizer"
stagingBinDir="${containerStagingFolder}/usr/local/bin"

dockerFile="$scriptDir/Dockerfile.mic-container"
runScriptPath="$scriptDir/run.sh"

# stage those files that need to be in the container
mkdir -p "${stagingBinDir}"
cp "$micLocalFile" "${stagingBinDir}"
cp "$runScriptPath" "${stagingBinDir}"

touch ${containerStagingFolder}/.mariner-toolkit-ignore-dockerenv

# download oras
ORAS_TAR="${buildDir}/oras_${ORAS_VERSION}_linux_${ARCH}.tar.gz"

curl -L "https://github.com/oras-project/oras/releases/download/v${ORAS_VERSION}/oras_${ORAS_VERSION}_linux_${ARCH}.tar.gz" \
  -o "$ORAS_TAR"

mkdir "${buildDir}/oras-install/"
tar -zxf "$ORAS_TAR" -C "${buildDir}/oras-install/"
mv "${buildDir}/oras-install/oras" "${stagingBinDir}"

# build the container
docker build -f "$dockerFile" "$containerStagingFolder" -t "$containerTag"

# clean-up
cleanUp
