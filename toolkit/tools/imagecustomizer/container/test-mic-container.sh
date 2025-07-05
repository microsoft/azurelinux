# Test container by running run.sh script inside it.
set -eux
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"

containerTag="$1"

outputImage="$SCRIPT_DIR/../../out/containertestoutput.vhdx"
outputImageDir="$(dirname "$outputImage")"
inputConfig="$SCRIPT_DIR/../../pkg/imagecustomizerlib/testdata/partitions-config.yaml"
inputConfigDir="$(dirname "$inputConfig")"

mkdir -p "$outputImageDir"

# Setup input config within the container.
containerInputConfigDir="/mic/config"
containerInputConfig="$containerInputConfigDir/$(basename "$inputConfig")"

# Setup build folder within the container.
containerBuildDir="/mic/build"

# Setup output image within the container.
containerOutputDir="/mic/output"
containerOutputImage="$containerOutputDir/$(basename "$outputImage")"

# Run run.sh script in docker container.
docker run --rm \
    --privileged=true \
    -v "$inputConfigDir":"$containerInputConfigDir":z \
    -v "$outputImageDir":"$containerOutputDir":z \
    -v /dev:/dev \
    "$containerTag" \
    /usr/local/bin/run.sh \
        "3.0.latest" \
        --config-file "$containerInputConfig" \
        --build-dir "$containerBuildDir" \
        --output-image-format "vhdx" \
        --output-image-file "$containerOutputImage"