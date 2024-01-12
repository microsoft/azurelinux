#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

if [[ $(uname -p) == "x86_64" ]]; then
    ARCHITECTURE="amd64"
else
    ARCHITECTURE="arm64"
fi

PUBLISHING_LEVEL="development"
BRANCH_NAME="main"

# parse script parameters:
# -m -> folder containing artifacts of CBL-Mariner
# -n -> name of the container registry
# -o -> folder where to put artifacts to be published
# -b -> branch name
# -p -> publishing level
# -x -> container source dir from cbl-mariner
while getopts ":m:n:o:b:p:x:" OPTIONS; do
    case ${OPTIONS} in
    m ) MARINER_ARTIFACTS_FOLDER=$OPTARG;;
    n ) CONTAINER_REGISTRY_NAME=$OPTARG
        CONTAINER_REGISTRY_NAME_FULL="$CONTAINER_REGISTRY_NAME.azurecr.io";;
    o ) OUTPUT_FOLDER=$OPTARG;;
    b ) BRANCH_NAME=$OPTARG;;
    p ) PUBLISHING_LEVEL=$OPTARG;;
    x ) CONTAINER_SRC_DIR=$OPTARG;;

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

echo "- MARINER_ARTIFACTS_FOLDER        -> $MARINER_ARTIFACTS_FOLDER"
echo "- CONTAINER_REGISTRY_NAME         -> $CONTAINER_REGISTRY_NAME"
echo "- CONTAINER_REGISTRY_NAME_FULL    -> $CONTAINER_REGISTRY_NAME_FULL"
echo "- ARCHITECTURE                    -> $ARCHITECTURE"
echo "- BRANCH_NAME                     -> $BRANCH_NAME"
echo "- PUBLISHING_LEVEL                -> $PUBLISHING_LEVEL"
echo "- OUTPUT_FOLDER                   -> $OUTPUT_FOLDER"

ROOT_FOLDER="$(git rev-parse --show-toplevel)"

BASE_IMAGE_TARBALL=$(find "$MARINER_ARTIFACTS_FOLDER" -name "core-[0-9.]*.tar.gz")
if [[ ! -f $BASE_IMAGE_TARBALL ]]; then
    echo "Error - No base image tarball in $MARINER_ARTIFACTS_FOLDER"
    exit 1
fi

DISTROLESS_IMAGE_TARBALL=$(find "$MARINER_ARTIFACTS_FOLDER" -name "distroless-base-[0-9.]*.tar.gz")
DISTROLESS_DEBUG_IMAGE_TARBALL=$(find "$MARINER_ARTIFACTS_FOLDER" -name "distroless-debug-[0-9.]*.tar.gz")
DISTROLESS_MINIMAL_IMAGE_TARBALL=$(find "$MARINER_ARTIFACTS_FOLDER" -name "distroless-minimal-[0-9.]*.tar.gz")
if [[ (! -f $DISTROLESS_IMAGE_TARBALL) || \
      (! -f $DISTROLESS_DEBUG_IMAGE_TARBALL) || \
      (! -f $DISTROLESS_MINIMAL_IMAGE_TARBALL) ]]; then
    echo "Error - Missing some distroless image tarball(s) in $MARINER_ARTIFACTS_FOLDER"
    exit 1
fi


echo "+++ create temp folder"
TEMPDIR=$(mktemp -d)

function cleanup {
    echo "+++ remove $TEMPDIR"
    rm -rf "$TEMPDIR"
}
trap cleanup EXIT

readonly BASE="base"
readonly DISTROLESS="distroless"
readonly BUSYBOX="busybox"

# Use this global variable to store the most recently built base image.
LAST_BASE_IMAGE=""

# Use this global variable to store the most recently built distroless image.
LAST_DISTROLESS_IMAGE=""

# Use this global variable to store full container tag from base container image.
# This variable is set in the create_base_image function.
FULL_CONTAINER_TAG=""

# these variables are used to create text files listing golden image names.
readonly file_name_prefix='PublishedContainers'
readonly file_ext='.txt'

function get_container_info {
    local container_file
    local file_name
    local prefix
    local registryPrefix        # (e.g.: public/cbl-mariner for container that go to MCR)
    local temp_name
    local repo_name
    local __name
    local __tag
 
    # $1: container tarball file name
    # $2: name [out param]
    # $3: tag [out param]
    # $4: acr repo
    # $5: prefix [optional, must be the last param]
    container_file=$1
    __name=$2
    __tag=$3
    repo_name=$4
    if [[ -n $5 ]]; then
        prefix=$5
    fi

    # remove path and extension
    file_name=$(basename "$container_file")
    file_name=${file_name%.tar.gz}
    # Mariner 2.0 preview hack (remove "-Preview-" and following char(s) from name)
    file_name=$(echo $file_name | sed "s/-Preview-.*//")

    # get container name and tag
    oldifs=$IFS
    IFS='#'
    read -ra name_parts <<< "$(echo "$file_name" | sed -r 's/-([^-]*)$/#\1/')"
    IFS=$oldifs
    temp_name=${name_parts[0]}
    temp_name=${temp_name//-/\/}

    # build full container name (all base containers are under 'base' in config file)
    getRegistryPrefix 'base' $PUBLISHING_LEVEL $BRANCH_NAME registryPrefix
    if [[ -n $registryPrefix ]]; then
        repo_name=$repo_name/$registryPrefix
    fi
    if [[ -n $prefix ]]; then
        eval "$__name"="$repo_name/$prefix/$temp_name"
    else
        eval "$__name"="$repo_name/$temp_name"
    fi
    eval "$__tag"="${name_parts[1]}-$ARCHITECTURE"
}

function create_base_image {
    local container_name_prefix=$1
    local container_type=$2
    local container_tarball=$3
    local dockerfile=$4
    local container_name
    local container_tag

    get_container_info "$container_tarball" container_name container_tag "$CONTAINER_REGISTRY_NAME_FULL" "$container_name_prefix"

    local full_container_name
    full_container_name="$container_name:$container_tag"

    # FULL_CONTAINER_TAG is used to tag the marinara builder image.
    FULL_CONTAINER_TAG="$container_tag"

    if [[ $container_type == "$BASE" ]]; then
        LAST_BASE_IMAGE=$full_container_name
    elif [[ $container_type == "$DISTROLESS" ]]; then
        LAST_DISTROLESS_IMAGE=$full_container_name
    fi

    echo
    echo "container_name_prefix:    -> $container_name_prefix"
    echo "container_type:           -> $container_type"
    echo "container_tarball:        -> $container_tarball"
    echo "LAST_BASE_IMAGE:          -> $LAST_BASE_IMAGE"
    echo "LAST_DISTROLESS_IMAGE:    -> $LAST_DISTROLESS_IMAGE"
    echo "full_container_name:      -> $full_container_name"
    echo "dockerfile                -> $dockerfile"
    echo

    echo "----------------------------------------------------------------------"
    echo "+++ create container $full_container_name"
    echo "    from $(basename "$container_tarball")"
    echo

    cat "$container_tarball" | docker import - "$full_container_name"

    echo "$full_container_name" >> "$TEMPDIR/$file_name_prefix-$container_type$file_ext"
    echo "----------------------------------------------------------------------"

    local containerBuildDir="$TEMPDIR/ContainerBuildDir"
    mkdir -p "$containerBuildDir"

    cp "$ROOT_FOLDER/pipelines/publish-containers/common/data/EULA-Container.txt" "$containerBuildDir"/
    cp "$CONTAINER_SRC_DIR/$container_type/$dockerfile" "$containerBuildDir/Dockerfile"

    pushd "$containerBuildDir" > /dev/null

    # Build image
    docker build . \
        --build-arg EULA="EULA-Container.txt" \
        --build-arg BASE_IMAGE="$full_container_name" \
        -t "$full_container_name" \
        --no-cache \
        --progress=plain

    popd > /dev/null

    # Clean up temp folder
    sudo rm -rf "$containerBuildDir"
}

function create_base_nonroot_image {
    local mariner_version
    local mariner_build_arch

    local base_container_full_name="$LAST_BASE_IMAGE"
    local base_container_name=${base_container_full_name%:*}
    local base_container_tag=${base_container_full_name#*:}
    mariner_version=$(awk -F '.' '{print $1"."$2}' <<< "$base_container_tag")   # 2.0.20220426-amd64 -> 2.0

    mariner_build_arch=$(awk -F '.' '{print $3}' <<< "$base_container_tag")     # 2.0.20220426-amd64 -> 20220426-amd64
    local full_new_tag=$mariner_version-nonroot.$mariner_build_arch             # 2.0-nonroot.20220426-amd64
    local full_container_name="$base_container_name:$full_new_tag"
    local dockerfile="Dockerfile-Base-Nonroot-Template"

    echo
    echo "base_container_full_name:     -> $base_container_full_name"
    echo "base_container_name:          -> $base_container_name"
    echo "base_container_tag:           -> $base_container_tag"
    echo "mariner_version:              -> $mariner_version"
    echo "full_container_name:          -> $full_container_name"
    echo "dockerfile                    -> $dockerfile"
    echo

    echo "----------------------------------------------------------------------"
    echo "+++ create container $full_container_name"
    echo "    from $base_container_full_name"
    echo

    echo "$full_container_name" >> "$TEMPDIR/$file_name_prefix-$BASE$file_ext"
    echo "----------------------------------------------------------------------"

    local containerBuildDir="$TEMPDIR/ContainerBuildDir"
    mkdir -p "$containerBuildDir"

    cp "$CONTAINER_SRC_DIR/base/$dockerfile" "$containerBuildDir/Dockerfile"

    pushd "$containerBuildDir" > /dev/null

    # Build image
    docker build . \
        --build-arg BASE_IMAGE="$base_container_full_name" \
        --build-arg MARINER_VERSION="$mariner_version" \
        -t "$full_container_name" \
        --no-cache \
        --progress=plain

    popd > /dev/null

    # Clean up temp folder
    sudo rm -rf "$containerBuildDir"
}

function create_busybox_image {
    local mariner_version
    local registryPrefix        # (e.g.: public/cbl-mariner for container that go to MCR)

    mariner_version=$(awk -F '.' '{print $1"."$2}' <<< "$FULL_CONTAINER_TAG") # 2.0.20220426-amd64 -> 2.0

    # Get registry prefix for busybox container. Use the same registry destination as the base container.
    getRegistryPrefix 'base' $PUBLISHING_LEVEL $BRANCH_NAME registryPrefix

    if [[ -n $registryPrefix ]]; then
        full_busybox_container_name="$CONTAINER_REGISTRY_NAME_FULL/$registryPrefix/$BUSYBOX:$FULL_CONTAINER_TAG"
    else
        full_busybox_container_name="$CONTAINER_REGISTRY_NAME_FULL/$BUSYBOX:$FULL_CONTAINER_TAG"
    fi

    echo "----------------------------------------------------------------------"
    echo "+++ create container $full_busybox_container_name"
    echo
    echo "$full_busybox_container_name" >> "$TEMPDIR/$file_name_prefix-$BUSYBOX$file_ext"
    echo "----------------------------------------------------------------------"

    local containerBuildDir="$TEMPDIR/ContainerBuildDir"
    mkdir -p "$containerBuildDir"

    cp "$CONTAINER_SRC_DIR/busybox/Dockerfile-Busybox-Template" "$containerBuildDir/Dockerfile"

    pushd "$containerBuildDir" > /dev/null

    docker build . \
        --build-arg BASE_IMAGE="$LAST_BASE_IMAGE" \
        --build-arg MARINER_VERSION="$mariner_version" \
        -t "$full_busybox_container_name" \
        --no-cache \
        --progress=plain

    popd > /dev/null

    # Clean up temp folder
    sudo rm -rf "$containerBuildDir"
}

function create_marinara_image {
    local mariner_version
    local registryPrefix        # (e.g.: public/cbl-mariner for container that go to MCR)

    mariner_version=$(awk -F '.' '{print $1"."$2}' <<< "$FULL_CONTAINER_TAG") # 2.0.20220426-amd64 -> 2.0
    marinara="marinara"

    # get registry prefix for marinara container (note that marinara is under 'base' in config file)
    getRegistryPrefix 'base' $PUBLISHING_LEVEL $BRANCH_NAME registryPrefix
    if [[ -n $registryPrefix ]]; then
        full_marinara_container_name="$CONTAINER_REGISTRY_NAME_FULL/$registryPrefix/$marinara:$FULL_CONTAINER_TAG"
    else
        full_marinara_container_name="$CONTAINER_REGISTRY_NAME_FULL/$marinara:$FULL_CONTAINER_TAG"
    fi

    marinaraSrcDir="$TEMPDIR/$marinara-src"
    git clone "https://github.com/microsoft/$marinara.git" "$marinaraSrcDir"
    pushd "$marinaraSrcDir"

    echo "----------------------------------------------------------------------"
    echo "+++ create container $full_marinara_container_name"
    echo
    echo "$full_marinara_container_name" >> "$TEMPDIR/$file_name_prefix-$marinara$file_ext"
    echo "----------------------------------------------------------------------"

    # Update dockerfile-marinara to use the current base container
    sed -E "s|^FROM mcr\..*installer$|FROM $LAST_BASE_IMAGE as installer|g" -i "dockerfile-$marinara"

    docker build . \
        -t "$full_marinara_container_name" \
        -f dockerfile-$marinara \
        --no-cache \
        --progress=plain

    popd > /dev/null
    echo "+++ remove $marinaraSrcDir"
    sudo rm -rf "$marinaraSrcDir"
}

function create_distroless_nonroot_image {
    local mariner_version
    local mariner_build_arch

    local base_container_full_name="$LAST_BASE_IMAGE"
    local distroless_container_full_name="$LAST_DISTROLESS_IMAGE"
    local distroless_container_name=${distroless_container_full_name%:*}
    local distroless_container_tag=${distroless_container_full_name#*:}
    mariner_version=$(awk -F '.' '{print $1"."$2}' <<< "$distroless_container_tag") # 2.0.20220426-amd64 -> 2.0

    mariner_build_arch=$(awk -F '.' '{print $3}' <<< "$distroless_container_tag")   # 2.0.20220426-amd64 -> 20220426-amd64
    local full_new_tag=$mariner_version-nonroot.$mariner_build_arch                 # 2.0-nonroot.20220426-amd64
    local full_container_name="$distroless_container_name:$full_new_tag"
    local dockerfile="Dockerfile-Distroless-Nonroot-Template"

    echo
    echo "base_container_full_name:         -> $base_container_full_name"
    echo "distroless_container_full_name:   -> $distroless_container_full_name"
    echo "distroless_container_name:        -> $distroless_container_name"
    echo "distroless_container_tag:         -> $distroless_container_tag"
    echo "mariner_version:                  -> $mariner_version"
    echo "full_container_name:              -> $full_container_name"
    echo "dockerfile                        -> $dockerfile"
    echo

    echo "----------------------------------------------------------------------"
    echo "+++ create container $full_container_name"
    echo "    from $distroless_container_full_name"
    echo

    echo "$full_container_name" >> "$TEMPDIR/$file_name_prefix-$DISTROLESS$file_ext"
    echo "----------------------------------------------------------------------"

    local containerBuildDir="$TEMPDIR/ContainerBuildDir"
    mkdir -p "$containerBuildDir"

    cp "$CONTAINER_SRC_DIR/distroless/$dockerfile" "$containerBuildDir/Dockerfile"

    pushd "$containerBuildDir" > /dev/null

    # Build image
    docker build . \
        --build-arg BASE_IMAGE="$base_container_full_name" \
        --build-arg FINAL_IMAGE="$distroless_container_full_name" \
        --build-arg MARINER_VERSION="$mariner_version" \
        -t "$full_container_name" \
        --no-cache \
        --progress=plain

    popd > /dev/null

    # Clean up temp folder
    sudo rm -rf "$containerBuildDir"
}

function start_building_containers {
    echo
    echo "====================================================================="
    echo "Create Base and Distroless Mariner Containers"
    echo "====================================================================="
    echo

    create_base_image $BASE $BASE "$BASE_IMAGE_TARBALL" "Dockerfile-Base-Template"
    create_base_nonroot_image

    create_busybox_image
    create_marinara_image

    create_base_image "" $DISTROLESS "$DISTROLESS_IMAGE_TARBALL" "Dockerfile-Distroless-Template"
    create_distroless_nonroot_image

    create_base_image "" $DISTROLESS "$DISTROLESS_DEBUG_IMAGE_TARBALL" "Dockerfile-Distroless-Template"
    create_distroless_nonroot_image

    create_base_image "" $DISTROLESS "$DISTROLESS_MINIMAL_IMAGE_TARBALL" "Dockerfile-Distroless-Template"
    create_distroless_nonroot_image
}

# source the CommonFunctions script to get the following function:
# - save_container_list
# - getRegistryPrefix
source $CONTAINER_SRC_DIR/scripts/CommonFunctions.sh

start_building_containers
save_container_list
