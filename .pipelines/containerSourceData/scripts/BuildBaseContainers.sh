#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# This script is used to build base containers and publish them to ACR.
# The script takes the following inputs:
# - ACR: Azure Container Registry name.
# - CONTAINER_TARBALLS_DIR: Directory containing the tarballs for the base and distroless containers.
# - RPMS_TARBALL: Tarball containing the RPMs to be used in the containers.
# - CONTAINER_SRC_DIR: Directory containing the source files for the containers.
# - OUTPUT_DIR: Directory to save the published container names.
# - PUBLISHING_LEVEL: The publishing level for the containers. It can be "preview" or "development".
# - REPO_PREFIX: Prefix for the repository in ACR.
# - PUBLISH_TO_ACR: Flag to publish the containers to ACR. It can be "true" or "false".

# Assuming you are in your current working directory. Below should be the directory structure:
#   │   rpms.tar.gz
#   │   out
#   |   ├──
#   │   containerSourceData
#   │   ├── base
#   │   │   ├── Dockerfile-Base-Template
#   │   │   ├── Dockerfile-Base-Nonroot-Template
#   │   │   ├── Dockerfile-Distroless-Template
#   │   │   ├── Dockerfile-Distroless-Nonroot-Template
#   │   container_tarballs
#   │   ├── container_base
#   │   │   ├── core-2.0.20230607.tar.gz
#   │   ├── core_container_builder
#   │   │   ├── core-container-builder-2.0.20230607.tar.gz
#   │   ├── distroless_base
#   │   │   ├── distroless-base-2.0.20230607.tar.gz
#   │   ├── distroless_debug
#   │   │   ├── distroless-debug-2.0.20230607.tar.gz
#   │   ├── distroless_minimal
#   │   │   ├── distroless-minimal-2.0.20230607.tar.gz
#   │   marinaraLocalRepo.repo

# Example usage:
# ./BuildBaseContainers.sh \
#    -a azuerlinuxpreview \
#    -c ./container_tarballs \
#    -k ./rpms.tar.gz \
#    -l ./containerSourceData \
#    -o ./out \
#    -p development \
#    -r "" \
#    -q "false"

while getopts ":a:c:k:l:o:p:r:q:" OPTIONS; do
    case ${OPTIONS} in
    a ) ACR=$OPTARG;;
    c ) CONTAINER_TARBALLS_DIR=$OPTARG;;
    k ) RPMS_TARBALL=$OPTARG;;
    l ) CONTAINER_SRC_DIR=$OPTARG;;
    o ) OUTPUT_DIR=$OPTARG;;
    p ) PUBLISHING_LEVEL=$OPTARG;;
    r ) REPO_PREFIX=$OPTARG;;
    q ) PUBLISH_TO_ACR=$OPTARG;;

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
    echo "ACR                           -> $ACR"
    echo "CONTAINER_TARBALLS_DIR        -> $CONTAINER_TARBALLS_DIR"
    echo "RPMS_TARBALL                  -> $RPMS_TARBALL"
    echo "CONTAINER_SRC_DIR             -> $CONTAINER_SRC_DIR"
    echo "REPO_PREFIX                   -> $REPO_PREFIX"
    echo "PUBLISHING_LEVEL              -> $PUBLISHING_LEVEL"
    echo "PUBLISH_TO_ACR                -> $PUBLISH_TO_ACR"
    echo "OUTPUT_DIR                    -> $OUTPUT_DIR"
}

function validate_inputs {
    if [[ -z "$ACR" ]]; then
        echo "Error - ACR name cannot be empty."
        exit 1
    fi

    if [[ -z "$CONTAINER_TARBALLS_DIR" ]]; then
        echo "Error - Container tarballs directory cannot be empty."
        exit 1
    fi

    BASE_TARBALL=$(find "$CONTAINER_TARBALLS_DIR" -name "core-[0-9.]*.tar.gz")
    BASE_BUILDER_TARBALL=$(find "$CONTAINER_TARBALLS_DIR" -name "core-container-builder-[0-9.]*.tar.gz")
    DISTROLESS_BASE_TARBALL=$(find "$CONTAINER_TARBALLS_DIR" -name "distroless-base-[0-9.]*.tar.gz")
    DISTROLESS_DEBUG_TARBALL=$(find "$CONTAINER_TARBALLS_DIR" -name "distroless-debug-[0-9.]*.tar.gz")
    DISTROLESS_MINIMAL_TARBALL=$(find "$CONTAINER_TARBALLS_DIR" -name "distroless-minimal-[0-9.]*.tar.gz")
    if [[ (! -f $BASE_TARBALL)  || \
        (! -f $DISTROLESS_BASE_TARBALL) || \
        (! -f $DISTROLESS_DEBUG_TARBALL) || \
        (! -f $DISTROLESS_MINIMAL_TARBALL) ]]; then
        echo "Error - Missing some tarball(s) in $CONTAINER_TARBALLS_DIR"
        exit 1
    fi

    if [[ ! -f $RPMS_TARBALL ]]; then
        echo "Error - No RPMs tarball found."
        # exit 1
    fi

    if [ ! -d "$CONTAINER_SRC_DIR" ]; then
        echo "Error - Container source directory does not exist."
        exit 1
    fi

    if [[ -z "$PUBLISHING_LEVEL" ]]; then
        echo "Error - Publishing level cannot be empty."
        exit 1
    fi

    if [ ! -d "$OUTPUT_DIR" ]; then
        echo "Create output directory: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
    fi
}

function initialization {
    echo "+++ Initialization"

    echo "+++ Extracting RPMs into $WORK_DIR"
    tar -xf "$RPMS_TARBALL" -C "$WORK_DIR"
    RPMS_DIR="RPMS"

    echo "+++ Copy local repo files to $WORK_DIR"
    LOCAL_REPO_FILE="local.repo"
    cp "$CONTAINER_SRC_DIR/marinerLocalRepo.repo" "$WORK_DIR/$LOCAL_REPO_FILE"

    if [ "$PUBLISHING_LEVEL" = "preview" ]; then
        ACR_NAME_FULL=${ACR}.azurecr.io/${REPO_PREFIX}
    elif [ "$PUBLISHING_LEVEL" = "development" ]; then
        ACR_NAME_FULL=${ACR}.azurecr.io
    fi

    echo "ACR Name Full                 -> $ACR_NAME_FULL"

    if [[ $(uname -p) == "x86_64" ]]; then
        ARCHITECTURE="amd64"
    else
        ARCHITECTURE="arm64"
    fi

    echo "ARCHITECTURE                  -> $ARCHITECTURE"

    EULA_FILE_NAME="EULA-Container.txt"

    # Image types
    BASE_BUILDER="base-builder"
    BASE="base"
    DISTROLESS="distroless"
    MARINARA="marinara"

    base_tarball_file_name=$(basename "$BASE_TARBALL")      # core-2.0.20230607.tar.gz
    base_tag_tar_gz=${base_tarball_file_name##*-}           # 2.0.20230607.tar.gz
    BASE_IMAGE_TAG=${base_tag_tar_gz%.tar.gz}               # 2.0.20230607
    echo "BASE_IMAGE_TAG                -> $BASE_IMAGE_TAG"
    AZL_VERSION=${BASE_IMAGE_TAG%.*}                        # 2.0
    echo "AZL_VERSION                   -> $AZL_VERSION"
    BUILD_ID=${BASE_IMAGE_TAG##*.}                          # 20230607
    echo "BUILD_ID                      -> $BUILD_ID"

    IMAGE_TAG=$BASE_IMAGE_TAG-$ARCHITECTURE
    NONROOT_IMAGE_TAG=$AZL_VERSION-nonroot.$BUILD_ID-$ARCHITECTURE

    # Set various image names.
    BASE_IMAGE_NAME="$ACR_NAME_FULL/base/core:$IMAGE_TAG"
    BASE_NONROOT_IMAGE_NAME="$ACR_NAME_FULL/base/core:$NONROOT_IMAGE_TAG"
    DISTROLESS_BASE_IMAGE_NAME="$ACR_NAME_FULL/distroless/base:$IMAGE_TAG"
    DISTROLESS_BASE_NONROOT_IMAGE_NAME="$ACR_NAME_FULL/distroless/base:$NONROOT_IMAGE_TAG"
    DISTROLESS_MINIMAL_IMAGE_NAME="$ACR_NAME_FULL/distroless/minimal:$IMAGE_TAG"
    DISTROLESS_MINIMAL_NONROOT_IMAGE_NAME="$ACR_NAME_FULL/distroless/minimal:$NONROOT_IMAGE_TAG"
    DISTROLESS_DEBUG_NONROOT_IMAGE_NAME="$ACR_NAME_FULL/distroless/debug:$NONROOT_IMAGE_TAG"
    DISTROLESS_DEBUG_IMAGE_NAME="$ACR_NAME_FULL/distroless/debug:$IMAGE_TAG"

    MARINARA_IMAGE_NAME="$ACR_NAME_FULL/marinara:$IMAGE_TAG"

    echo "BASE_IMAGE_NAME                       -> $BASE_IMAGE_NAME"
    echo "BASE_NONROOT_IMAGE_NAME               -> $BASE_NONROOT_IMAGE_NAME"
    echo "DISTROLESS_BASE_IMAGE_NAME            -> $DISTROLESS_BASE_IMAGE_NAME"
    echo "DISTROLESS_BASE_NONROOT_IMAGE_NAME    -> $DISTROLESS_BASE_NONROOT_IMAGE_NAME"
    echo "DISTROLESS_MINIMAL_IMAGE_NAME         -> $DISTROLESS_MINIMAL_IMAGE_NAME"
    echo "DISTROLESS_MINIMAL_NONROOT_IMAGE_NAME -> $DISTROLESS_MINIMAL_NONROOT_IMAGE_NAME"
    echo "DISTROLESS_DEBUG_IMAGE_NAME           -> $DISTROLESS_DEBUG_IMAGE_NAME"
    echo "DISTROLESS_DEBUG_NONROOT_IMAGE_NAME   -> $DISTROLESS_DEBUG_NONROOT_IMAGE_NAME"
    echo "MARINARA_IMAGE_NAME                   -> $MARINARA_IMAGE_NAME"
}

function build_builder_image {
    echo "+++ Build builder image"
    docker import - "$BASE_BUILDER" < "$BASE_BUILDER_TARBALL"
}
function docker_build {
    local image_type=$1
    local image_full_name=$2
    local image_tarball=$3
    local dockerfile=$4

    echo "+++ Importing container image: $image_full_name"
    local temp_image=${image_full_name}_temp
    docker import - "$temp_image" < "$image_tarball"

    local build_dir="$WORK_DIR/container_build_dir"
    mkdir -p "$build_dir"

    ROOT_FOLDER="$(git rev-parse --show-toplevel)"
    EULA_FILE_PATH="$ROOT_FOLDER/.pipelines/container_artifacts/data"
    if [ -d "$EULA_FILE_PATH" ]; then
        cp "$EULA_FILE_PATH/$EULA_FILE_NAME" "$build_dir"/
    fi

    cp "$CONTAINER_SRC_DIR/base/$dockerfile" "$build_dir/dockerfile"

    pushd "$build_dir" > /dev/null

    echo "+++ Build image: $image_full_name"
    docker build . \
        --build-arg EULA="$EULA_FILE_NAME" \
        --build-arg BASE_IMAGE="$temp_image" \
        -t "$image_full_name" \
        --no-cache \
        --progress=plain

    docker rmi "$temp_image"
    popd > /dev/null
    sudo rm -rf "$build_dir"

    publish_to_acr "$image_full_name"
    save_container_image "$image_type" "$image_full_name"
}

function docker_build_custom {
    local image_type=$1
    local image_full_name=$2
    local final_image_to_use=$3
    local dockerfile=$4

    # $WORK_DIR has $RPMS_DIR directory and $LOCAL_REPO_FILE file.
    pushd "$WORK_DIR" > /dev/null

    echo "+++ Build image: $image_full_name"
    docker build . \
        --build-arg BASE_IMAGE="$BASE_IMAGE_NAME" \
        --build-arg FINAL_IMAGE="$final_image_to_use" \
        --build-arg AZL_VERSION="$AZL_VERSION" \
        --build-arg RPMS="$RPMS_DIR" \
        --build-arg LOCAL_REPO_FILE="$LOCAL_REPO_FILE" \
        -t "$image_full_name" \
        -f "$CONTAINER_SRC_DIR/base/$dockerfile" \
        --no-cache \
        --progress=plain

    popd > /dev/null

    publish_to_acr "$image_full_name"
    save_container_image "$image_type" "$image_full_name"
}

function docker_build_marinara {
    echo "+++ Build Marinara image: $MARINARA_IMAGE_NAME"
    local build_dir="$WORK_DIR/marinara_build_dir"
    mkdir -p "$build_dir"
    git clone "https://github.com/microsoft/$MARINARA.git" "$build_dir"
    pushd "$build_dir"
    sed -E "s|^FROM mcr\..*installer$|FROM $BASE_BUILDER as installer|g" -i "dockerfile-$MARINARA"

    docker build . \
        -t "$MARINARA_IMAGE_NAME" \
        -f dockerfile-$MARINARA \
        --build-arg AZL_VERSION="$AZL_VERSION" \
        --build-arg INSTALL_DEPENDENCIES=false \
        --no-cache \
        --progress=plain

    popd > /dev/null
    sudo rm -rf "$build_dir"

    publish_to_acr "$MARINARA_IMAGE_NAME"
    save_container_image "$MARINARA" "$MARINARA_IMAGE_NAME"
}

function publish_to_acr {
    local image=$1
    if [[ ! "$PUBLISH_TO_ACR" =~ [Tt]rue ]]; then
        echo "+++ Skip publishing to ACR"
        return
    fi
    echo "+++ Publish container $image"
    echo "login into ACR: $ACR"
    az acr login --name "$ACR"
    docker image push "$image"
}

function save_container_image {
    local image_type=$1
    local image_name=$2
    echo "+++ Save image name to file PublishedContainers-$image_type.txt"
    echo "$image_name" >> "$OUTPUT_DIR/PublishedContainers-$image_type.txt"
}

function build_images {
    echo "+++ Build images"

    docker_build $BASE "$BASE_IMAGE_NAME" "$BASE_TARBALL" "Dockerfile-Base-Template"
    docker_build $DISTROLESS "$DISTROLESS_BASE_IMAGE_NAME" "$DISTROLESS_BASE_TARBALL" "Dockerfile-Distroless-Template"
    docker_build $DISTROLESS "$DISTROLESS_MINIMAL_IMAGE_NAME" "$DISTROLESS_MINIMAL_TARBALL" "Dockerfile-Distroless-Template"
    docker_build $DISTROLESS "$DISTROLESS_DEBUG_IMAGE_NAME" "$DISTROLESS_DEBUG_TARBALL" "Dockerfile-Distroless-Template"

    docker_build_custom $BASE "$BASE_NONROOT_IMAGE_NAME" "" "Dockerfile-Base-Nonroot-Template"
    docker_build_custom $DISTROLESS "$DISTROLESS_BASE_NONROOT_IMAGE_NAME" "$DISTROLESS_BASE_IMAGE_NAME" "Dockerfile-Distroless-Nonroot-Template"
    docker_build_custom $DISTROLESS "$DISTROLESS_MINIMAL_NONROOT_IMAGE_NAME" "$DISTROLESS_MINIMAL_IMAGE_NAME" "Dockerfile-Distroless-Nonroot-Template"
    docker_build_custom $DISTROLESS "$DISTROLESS_DEBUG_NONROOT_IMAGE_NAME" "$DISTROLESS_DEBUG_IMAGE_NAME" "Dockerfile-Distroless-Nonroot-Template"

    docker_build_marinara
}

print_inputs
validate_inputs
initialization
build_builder_image
build_images
