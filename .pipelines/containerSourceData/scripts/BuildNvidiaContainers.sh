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

# Assuming you are in your current working directory. Below should be the directory structure:
#   │   rpms.tar.gz
#   │   OUTPUT
#   │   ├── 

# Assuming CBL-Mariner repo is cloned in your home directory. Below should be the directory structure:
#   ~/CBL-Mariner/.pipelines/containerSourceData
#   ├── scripts
#   │   ├── BuildNvidiaContainer.sh
#   ├── Dockerfile-Nvidia-Setup
#   ├── Dockerfile-Nvidia-Cleanup
#   ├── marinerLocalRepo.repo

# Example usage:
# /bin/bash ~/CBL-Mariner/.pipelines/containerSourceData/scripts/BuildNvidiaContainer.sh \
#     -a "mcr.microsoft.com/cbl-mariner/base/core:2.0" -b azurelinuxlocal \
#     -c "nvidia/driver" -d "cuda" -e "https://github.com/NVIDIA/gpu-driver-container" \
#     -f OUTPUT -g ./rpms.tar.gz -h ~/CBL-Mariner/.pipelines/containerSourceData \
#     -j development -k "false"

while getopts ":a:b:c:d:e:f:g:h:i:j:k:" OPTIONS; do
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
}

function initialization {
    echo "+++ Initialization"
    if [ "$PUBLISHING_LEVEL" = "preview" ]; then
        NVIDIA_IMAGE_NAME=${ACR}.azurecr.io/${REPO_PREFIX}/${REPOSITORY}
    elif [ "$PUBLISHING_LEVEL" = "development" ]; then
        NVIDIA_IMAGE_NAME=${ACR}.azurecr.io/${REPOSITORY}
    fi

    BASE_IMAGE_NAME=${BASE_IMAGE_NAME_FULL%:*}  # mcr.microsoft.com/cbl-mariner/base/core
    BASE_IMAGE_TAG=${BASE_IMAGE_NAME_FULL#*:}   # 2.0
    AZURE_LINUX_VERSION=${BASE_IMAGE_TAG%.*}    # 2.0
    END_OF_LIFE_1_YEAR=$(date -d "+1 year" "+%Y-%m-%dT%H:%M:%SZ")

    echo "Nvidia Image Name             -> $NVIDIA_IMAGE_NAME"
    echo "Base ACR Container Name       -> $BASE_IMAGE_NAME"
    echo "Base ACR Container Tag        -> $BASE_IMAGE_TAG"
    echo "Azure Linux Version           -> $AZURE_LINUX_VERSION"
    echo "End of Life                   -> $END_OF_LIFE_1_YEAR"
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
    "-t $NVIDIA_IMAGE_NAME --no-cache --progress=plain" \
    "-f $WORK_DIR/Dockerfile ."

    echo ""
    docker buildx build $DOCKER_BUILD_ARGS \
        --build-arg BASE_IMAGE="$BASE_IMAGE_NAME_FULL" \
        -t "$NVIDIA_IMAGE_NAME" --no-cache --progress=plain \
        -f "$WORK_DIR/Dockerfile" .
    popd > /dev/null
}

function set_image_tag {
    echo "+++ Get version of the installed package in the container."
    local containerId

    containerId=$(docker run --entrypoint /bin/sh -dt "$NVIDIA_IMAGE_NAME")
    echo "Container ID                  -> $containerId"

    # Fetch the ID and VERSION_ID from /etc/os-release file
    NAMESPACE=$(docker exec -u 0 "$containerId" cat /etc/os-release | grep "^ID=" | cut -d'=' -f2)
    VERSION=$(docker exec -u 0 "$containerId" cat /etc/os-release | grep "^VERSION_ID=" | cut -d'=' -f2 | sed -e 's/^"//' -e 's/"$//')
    OS_TAG=$NAMESPACE$VERSION

    # Rename the image to include package version, kernel version and OS tag
    # Example: azurelinuxpreview.azurecr.io/base/driver:550-5.15.153.1-1.cm2-mariner2.0
    NVIDIA_IMAGE_NAME_FINAL="$NVIDIA_IMAGE_NAME:$DRIVER_BRANCH-$KERNEL_VERSION-$OS_TAG"
    docker rm -f "$containerId"
}

function finalize {
    echo "+++ Finalize"
    docker image tag "$NVIDIA_IMAGE_NAME" "$NVIDIA_IMAGE_NAME_FINAL"
    docker rmi -f "$NVIDIA_IMAGE_NAME"
    echo "+++ Save container image name to file PublishedContainers-$IMAGE.txt"
    echo "$NVIDIA_IMAGE_NAME_FINAL" >> "$OUTPUT_DIR/PublishedContainers-$IMAGE.txt"
}

function oras_attach {
    local image_name=$1
    oras attach \
        --artifact-type "application/vnd.microsoft.artifact.lifecycle" \
        --annotation "vnd.microsoft.artifact.lifecycle.end-of-life.date=$END_OF_LIFE_1_YEAR" \
        "$image_name"
}

function publish_to_acr {
    CONTAINER_IMAGE=$1
    if [[ ! "$PUBLISH_TO_ACR" =~ [Tt]rue ]]; then
        echo "+++ Skip publishing to ACR"
        return
    fi
    local oras_access_token

    echo "+++ az login into Azure ACR $ACR"
    oras_access_token=$(az acr login --name "$ACR" --expose-token --output tsv --query accessToken)
    oras login "$ACR.azurecr.io" \
        --username "00000000-0000-0000-0000-000000000000" \
        --password "$oras_access_token"

    echo "+++ Publish container $CONTAINER_IMAGE"
    docker image push "$CONTAINER_IMAGE"
    oras_attach "$CONTAINER_IMAGE"
}


print_inputs
validate_inputs
initialization
prepare_dockerfile
prepare_docker_directory
docker_build
set_image_tag
finalize
publish_to_acr "$NVIDIA_IMAGE_NAME_FINAL"

