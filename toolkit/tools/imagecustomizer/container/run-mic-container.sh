#!/bin/bash

set -e

function showUsage() {
    echo
    echo "usage:"
    echo
    echo "build-mic-container.sh \\"
    echo "    -r <container-registry> \\"
    echo "    -n <container-name> \\"
    echo "    -t <container-tag> \\"
    echo "    -i <input-image-path> \\"
    echo "    -c <input-config-path> \\"
    echo "    -f <output-format> \\"
    echo "    -o <output-image-path> \\"
    echo "   [-l <log-level>"]
    echo
}

while getopts ":r:n:t:i:c:f:o:l:" OPTIONS; do
  case "${OPTIONS}" in
    r ) containerRegistery=$OPTARG ;;
    n ) containerName=$OPTARG ;;
    t ) containerTag=$OPTARG ;;
    i ) inputImage=$OPTARG ;;
    c ) inputConfig=$OPTARG ;;
    f ) outputFormat=$OPTARG ;;
    o ) outputImage=$OPTARG ;;
    l ) logLevel=$OPTARG ;;
  esac
done

if [[ -z $containerRegistery ]]; then
    echo "missing required argument '-r containerRegistry'"
    showUsage
    exit 1
fi

if [[ -z $containerName ]]; then
    echo "missing required argument '-n containerName'"
    showUsage
    exit 1
fi

if [[ -z $containerTag ]]; then
    echo "missing required argument '-t containerTag'"
    showUsage
    exit 1
fi

if [[ -z $inputImage ]]; then
    echo "missing required argument '-i inputImage'"
    showUsage
    exit 1
fi

if [[ -z $inputConfig ]]; then
    echo "missing required argument '-c inputConfig'"
    showUsage
    exit 1
fi

if [[ -z $outputFormat ]]; then
    echo "missing required argument '-f outputFormat'"
    showUsage
    exit 1
fi

if [[ -z $outputImage ]]; then
    echo "missing required argument '-o outputImage'"
    showUsage
    exit 1
fi

if [[ -z $logLevel ]]; then
    logLevel=info
fi

# ---- main ----

containerFullPath=$containerRegistery/$containerName:$containerTag

inputImageDir=$(dirname $inputImage)
inputConfigDdir=$(dirname $inputConfig)
outputImageDir=$(dirname $outputImage)

sudo rm -rf $outputImageDir
sudo mkdir -p $outputImageDir

# setup input image within the container
containerInputImageDir=/mic/input
containerInputImage=$containerInputImageDir/$(basename $inputImage)

# setup input config within the container
containerInputConfigDir=/mic/config
containerInputConfig=$containerInputConfigDir/$(basename $inputConfig)

# setup build folder within the container
containerBuildDir=/mic/build

# setup output image within the container
containerOutputDir=/mic/output
containerOutputImage=$containerOutputDir/$(basename $outputImage)

# invoke
docker run --rm \
  --privileged=true \
   -v $inputImageDir:$containerInputImageDir:z \
   -v $inputConfigDdir:$containerInputConfigDir:z \
   -v $outputImageDir:$containerOutputDir:z \
   -v /dev:/dev:z \
   $containerFullPath \
   imagecustomizer \
      --image-file $containerInputImage \
      --config-file $containerInputConfig \
      --build-dir $containerBuildDir \
      --output-image-format $outputFormat \
      --output-image-file $containerOutputImage \
      --log-level $logLevel
