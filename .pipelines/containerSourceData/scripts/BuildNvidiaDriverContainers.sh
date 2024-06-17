#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# This script is used to build a golden container image for a given component.
# The script takes the following inputs:
# - a) Base container image name (e.g. mcr.microsoft.com/cbl-mariner/base/core:2.0)
# - b) ACR name (e.g. azurelinepreview, acrafoimages, etc.)
# - c) Container repository name (e.g. base/nodejs, base/postgres, base/kubevirt/cdi-apiserver, etc.)
# - d) Image name (e.g. nodejs, postgres, cdi, etc.)
# - e) Source Repo URL
# - f) Output directory for container artifacts.
# - g) RPMS tarball file path (e.g. ./rpms.tar.gz)
# - h) Container source directory (e.g. ~/workspace/CBL-Mariner/.pipelines/containerSourceData)
# - i) Repo prefix (e.g. public/cbl-mariner, unlisted/cbl-mariner, etc.)
# - j) Publishing level (e.g. preview, development)
# - k) Publish to ACR (e.g. true, false. If true, the script will push the container to ACR)
# - l) Create SBOM (e.g. true, false. If true, the script will create SBOM for the container)
# - m) SBOM tool path.
# - n) Script to create SBOM for the container image.

# Assuming you are in your current working directory. Below should be the directory structure:
#   │   rpms.tar.gz
#   │   OUTPUT
#   │   ├── 

# Assuming CBL-Mariner repo is cloned in your home directory. Below should be the directory structure:
#   ~/CBL-Mariner/.pipelines/containerSourceData
#   ├── scripts
#   │   ├── BuildNvidiaContainer.sh
#   |   |── BuildContainerCommonSteps.sh
#   ├── Dockerfile-Nvidia-Setup
#   ├── Dockerfile-Nvidia-Cleanup
#   ├── marinerLocalRepo.repo

# Example usage:
# /bin/bash ~/CBL-Mariner/.pipelines/containerSourceData/scripts/BuildNvidiaContainer.sh \
#     -a "mcr.microsoft.com/cbl-mariner/base/core:2.0" -b azurelinuxlocal \
#     -c "nvidia/driver" -d "cuda" -e "https://github.com/NVIDIA/gpu-driver-container" \
#     -f OUTPUT -g ./rpms.tar.gz -h ~/CBL-Mariner/.pipelines/containerSourceData \
#     -j development -k "false"

while getopts ":a:b:c:d:e:f:g:h:i:j:k:l:m:n:" OPTIONS; do
    case ${OPTIONS} in
    a ) BASE_IMAGE_NAME_FULL=$OPTARG;;
    b ) ACR=$OPTARG;;
    c ) REPOSITORY=$OPTARG;;
    d ) IMAGE=$OPTARG;;
    e ) SOURCE_REPO_URL=$OPTARG;;
    f ) OUTPUT_DIR=$OPTARG;;
    g ) RPMS_TARBALL=$OPTARG;;
    h ) CONTAINER_SRC_DIR=$OPTARG;;
    i ) REPO_PREFIX=$OPTARG;;
    j ) PUBLISHING_LEVEL=$OPTARG;;
    k ) PUBLISH_TO_ACR=$OPTARG;;
    l ) CREATE_SBOM=$OPTARG;;
    m ) SBOM_TOOL_PATH=$OPTARG;;
    n ) SBOM_SCRIPT=$OPTARG;;

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

echo "+++ Create temp folder"
WORK_DIR=$(mktemp -d)
function cleanup {
    echo "+++ Remove temp folder: $WORK_DIR"
    sudo rm -rf "$WORK_DIR"
}
trap cleanup EXIT

function print_inputs {
    echo "BASE_IMAGE_NAME_FULL          -> $BASE_IMAGE_NAME_FULL"
    echo "ACR                           -> $ACR"
    echo "REPOSITORY                    -> $REPOSITORY"
    echo "IMAGE                         -> $IMAGE"
    echo "SOURCE_REPO_URL               -> $SOURCE_REPO_URL"
    echo "OUTPUT_DIR                    -> $OUTPUT_DIR"
    echo "RPMS_TARBALL                  -> $RPMS_TARBALL"
    echo "CONTAINER_SRC_DIR             -> $CONTAINER_SRC_DIR"
    echo "REPO_PREFIX                   -> $REPO_PREFIX"
    echo "PUBLISHING_LEVEL              -> $PUBLISHING_LEVEL"
    echo "PUBLISH_TO_ACR                -> $PUBLISH_TO_ACR"
    echo "CREATE_SBOM                   -> $CREATE_SBOM"
    echo "SBOM_TOOL_PATH                -> $SBOM_TOOL_PATH"
    echo "SBOM_SCRIPT                   -> $SBOM_SCRIPT"
}

function validate_inputs {
    if [[ -z "$BASE_IMAGE_NAME_FULL" ]]; then
        echo "Error - Base container image name cannot be empty."
        exit 1
    fi

    if [[ -z "$ACR" ]]; then
        echo "Error - ACR name cannot be empty."
        exit 1
    fi

    if [[ -z "$REPOSITORY" ]]; then
        echo "Error - Container repository name cannot be empty."
        exit 1
    fi

    if [[ -z "$IMAGE" ]]; then
        echo "Error - Image name cannot be empty."
        exit 1
    fi

    if [[ -z "$SOURCE_REPO_URL" ]]; then
        echo "Error - Source Repo URL cannot be empty."
        exit 1
    fi

    if [ ! -d "$OUTPUT_DIR" ]; then
        echo "Create output directory: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
    fi

    if [[ ! -f $RPMS_TARBALL ]]; then
        echo "Error - No RPMs tarball found."
        exit 1
    fi

    if [ ! -d "$CONTAINER_SRC_DIR" ]; then
        echo "Error - Container source directory does not exist."
        exit 1
    fi

    if [[ -z "$PUBLISHING_LEVEL" ]]; then
        echo "Error - Publishing level cannot be empty."
        exit 1
    fi

    if [[ "$CREATE_SBOM" =~ [Tt]rue ]]; then
        if [[ -z "$SBOM_TOOL_PATH" ]] ; then
            echo "Error - SBOM tool path cannot be empty."
            exit 1
        fi
        if [[ ! -f "$SBOM_SCRIPT" ]]; then
            echo "Error - SBOM script does not exist."
            exit 1
        fi
    fi
}

function get_component_name_and_version {
    echo "+++ Get Component name and version"
    COMPONENT="$IMAGE"
    echo "Component name                -> $COMPONENT"

    COMPONENT_VERSION=$(rpm -q --qf '%{VERSION}-%{release}\n' -p $HOST_MOUNTED_DIR/RPMS/x86_64/$IMAGE* |  rev | cut -d '.' -f 2- | rev)
    echo "Component Version             -> $COMPONENT_VERSION"
}

function prepare_dockerfile {
    echo "+++ Prepare dockerfile"
    SOURCE_DIR=$(mktemp -d)
    # Download the source code from the specified source URL
    git clone "$SOURCE_REPO_URL" "$SOURCE_DIR"

    # Copy Dockerfile and other files into WORK_DIR
    cp $SOURCE_DIR/azurelinux/* "$WORK_DIR/"
    sudo rm -rf "$SOURCE_DIR"

    # Update the copied dockerfile for later use in container build.
    setupInstruction=$(cat "$CONTAINER_SRC_DIR/Dockerfile-Nvidia-Setup")
    cleanupInstruction=$(cat "$CONTAINER_SRC_DIR/Dockerfile-Nvidia-Cleanup")
    sed -E "s#^FROM.*#$setupInstruction#g" -i "$WORK_DIR/Dockerfile"
    echo "$cleanupInstruction" | tee -a "$WORK_DIR/Dockerfile"

    echo " Output content of final dockerfile"
    echo "------------------------------------"
    cat "$WORK_DIR/Dockerfile"
    echo ""
}

function prepare_docker_directory {
    echo "+++ Prepare docker directory"
    HOST_MOUNTED_DIR="$WORK_DIR/Stage"
    mkdir -pv "$HOST_MOUNTED_DIR"

    # Copy files into docker context directory
    tar -xf "$RPMS_TARBALL" -C "$HOST_MOUNTED_DIR"/
    cp -v "$CONTAINER_SRC_DIR/marinerLocalRepo.repo" "$HOST_MOUNTED_DIR"/
}

function prepare_docker_build_args {
    echo "+++ Prepare NVIDIA docker build arguments"
    KERNEL_VERSION=$(rpm -q --qf '%{VERSION}-%{release}\n' -p $HOST_MOUNTED_DIR/RPMS/x86_64/kernel-devel*)
    DRIVER_VERSION=$(rpm -q --qf '%{VERSION}' -p $HOST_MOUNTED_DIR/RPMS/x86_64/$IMAGE*)
    DRIVER_BRANCH="${DRIVER_VERSION%%.*}"

    DOCKER_BUILD_ARGS="--build-arg KERNEL_VERSION=$KERNEL_VERSION --build-arg DRIVER_VERSION=$DRIVER_VERSION --build-arg AZURE_LINUX_VERSION=$AZURE_LINUX_VERSION"
}

function docker_build {
    echo "+++ Build container"
    pushd "$WORK_DIR" > /dev/null
    ls
    echo " docker build command"
    echo "----------------------"
    # 
    prepare_docker_build_args
    
    echo "docker buildx build $DOCKER_BUILD_ARGS" \
    "--build-arg BASE_IMAGE=$BASE_IMAGE_NAME_FULL" \
    "-t $CONTAINER_IMAGE_NAME --no-cache --progress=plain" \
    "-f $WORK_DIR/Dockerfile ."

    echo ""
    docker buildx build $DOCKER_BUILD_ARGS \
        --build-arg BASE_IMAGE="$BASE_IMAGE_NAME_FULL" \
        -t "$CONTAINER_IMAGE_NAME" --no-cache --progress=plain \
        -f "$WORK_DIR/Dockerfile" .
    popd > /dev/null
}

function set_image_tag {
    echo "+++ Get version of the installed package in the container."
    local containerId

    containerId=$(docker run --entrypoint /bin/sh -dt "$CONTAINER_IMAGE_NAME")
    echo "Container ID                  -> $containerId"

    # Fetch the ID and VERSION_ID from /etc/os-release file
    NAMESPACE=$(docker exec -u 0 "$containerId" cat /etc/os-release | grep "^ID=" | cut -d'=' -f2)
    VERSION=$(docker exec -u 0 "$containerId" cat /etc/os-release | grep "^VERSION_ID=" | cut -d'=' -f2 | sed -e 's/^"//' -e 's/"$//')
    OS_TAG=$NAMESPACE$VERSION

    # Rename the image to include package version, kernel version and OS tag
    # Example: azurelinuxpreview.azurecr.io/base/driver:550-5.15.153.1-1.cm2-mariner2.0
    CONTAINER_IMAGE_NAME_FINAL="$CONTAINER_IMAGE_NAME:$DRIVER_BRANCH-$KERNEL_VERSION-$OS_TAG"
    docker rm -f "$containerId"
}

source "$CONTAINER_SRC_DIR/scripts/BuildContainerCommonSteps.sh"
print_inputs
validate_inputs
initialization
prepare_dockerfile
prepare_docker_directory
get_component_name_and_version
docker_build
set_image_tag
finalize

