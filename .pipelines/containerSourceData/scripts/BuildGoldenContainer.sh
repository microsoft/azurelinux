#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# This script is used to build a golden container image for a given component.
# The script takes the following inputs:
# - a) Base container image name (e.g. mcr.microsoft.com/azurelinux/base/core:3.0)
# - b) ACR name (e.g. azurelinepreview, acrafoimages, etc.)
# - c) Container repository name (e.g. base/nodejs, base/postgres, base/kubevirt/cdi-apiserver, etc.)
# - d) Image name (e.g. nodejs, postgres, cdi, etc.)
# - e) Component file name (e.g. nodejs.name, postgres.name, api.name, etc.)
# - f) Package file name (e.g. nodejs18.pkg, postgres.pkg, api.pkg, etc.)
# - g) Dockerfile name (e.g. Dockerfile-nodejs, Dockerfile-Postgres, Dockerfile-cdi-apiserver, etc.)
# - h) Docker build arguments (e.g. '--build-arg BINARY_NAME="cdi-apiserver" --build-arg USER=1001')
# - i) Dockerfile text replacement (e.g. '@BINARY_PATH@ \"/usr/bin/acmesolver\"')
# - j) Output directory for container artifacts.
# - k) RPMS tarball file path (e.g. ./rpms.tar.gz)
# - l) Container source directory (e.g. ~/workspace/azurelinux/.pipelines/containerSourceData)
# - m) Is HCI image (e.g. true, false. HCI images have different naming convention)
# - n) Use rpm -qa command (e.g. true, false. Some images use rpm -qa command to get installed package)
# - o) Repo prefix (e.g. public/azurelinux, unlisted/azurelinux, etc.)
# - p) Publishing level (e.g. preview, development)
# - q) Publish to ACR (e.g. true, false. If true, the script will push the container to ACR)
# - r) Create SBOM (e.g. true, false. If true, the script will create SBOM for the container)
# - s) SBOM tool path.
# - t) Script to create SBOM for the container image.
# - u) Create Distroless container (e.g. true, false. If true, the script will also create a distroless container)
# - v) Version extract command (e.g. 'busybox | head -1 | cut -c 10-15')

# Assuming you are in your current working directory. Below should be the directory structure:
#   │   rpms.tar.gz
#   │   OUTPUT
#   │   ├── 

# Assuming Azure Linux repo is cloned in your home directory. Below should be the directory structure:
#   ~/azurelinux/.pipelines/containerSourceData
#   ├── nodejs
#   │   ├── distroless
#   │   │   ├── holdback-nodejs.pkg
#   │   │   ├── nodejs.pkg
#   │   ├── Dockerfile-Nodejs
#   │   ├── nodejs.pkg
#   |   |── nodejs.name
#   ├── configuration
#   │   ├── acrRepoV2.json
#   ├── scripts
#   │   ├── BuildGoldenContainer.sh
#   │   ├── BuildContainerCommonSteps.sh
#   ├── Dockerfile-Initial
#   ├── azurelinuxlocal.repo

# Example usage:
# /bin/bash ~/azurelinux/.pipelines/containerSourceData/scripts/BuildGoldenContainer.sh \
#     -a "mcr.microsoft.com/azurelinux/base/core:3.0" -b azurelinuxlocal \
#     -c "base/nodejs" -d "nodejs" -e "nodejs18" -f nodejs18.pkg -g Dockerfile-Nodejs \
#     -j OUTPUT -k ./rpms.tar.gz -l ~/azurelinux/.pipelines/containerSourceData \
#     -m "false" -n "false" -p development -q "false" -u "true"

while getopts ":a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:" OPTIONS; do
    case ${OPTIONS} in
    a ) BASE_IMAGE_NAME_FULL=$OPTARG;;
    b ) ACR=$OPTARG;;
    c ) REPOSITORY=$OPTARG;;
    d ) IMAGE=$OPTARG;;
    e ) COMPONENT_FILE=$OPTARG;;
    f ) PACKAGE_FILE=$OPTARG;;
    g ) DOCKERFILE=$OPTARG;;
    h ) DOCKER_BUILD_ARGS=$OPTARG;;
    i ) DOCKERFILE_TEXT_REPLACEMENT=$OPTARG;;
    j ) OUTPUT_DIR=$OPTARG;;
    k ) RPMS_TARBALL=$OPTARG;;
    l ) CONTAINER_SRC_DIR=$OPTARG;;
    m ) IS_HCI_IMAGE=$OPTARG;;
    n ) USE_RPM_QA_CMD=$OPTARG;;
    o ) REPO_PREFIX=$OPTARG;;
    p ) PUBLISHING_LEVEL=$OPTARG;;
    q ) PUBLISH_TO_ACR=$OPTARG;;
    r ) CREATE_SBOM=$OPTARG;;
    s ) SBOM_TOOL_PATH=$OPTARG;;
    t ) SBOM_SCRIPT=$OPTARG;;
    u ) DISTROLESS=$OPTARG;;
    v ) VERSION_EXTRACT_CMD=$OPTARG;;
    w ) TOOLCHAIN_RPMS_TARBALL=$OPTARG;;

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
    echo "COMPONENT_FILE                -> $COMPONENT_FILE"
    echo "PACKAGE_FILE                  -> $PACKAGE_FILE"
    echo "DOCKERFILE                    -> $DOCKERFILE"
    echo "DOCKER_BUILD_ARGS             -> $DOCKER_BUILD_ARGS"
    echo "DOCKERFILE_TEXT_REPLACEMENT   -> $DOCKERFILE_TEXT_REPLACEMENT"
    echo "OUTPUT_DIR                    -> $OUTPUT_DIR"
    echo "RPMS_TARBALL                  -> $RPMS_TARBALL"
    echo "CONTAINER_SRC_DIR             -> $CONTAINER_SRC_DIR"
    echo "IS_HCI_IMAGE                  -> $IS_HCI_IMAGE"
    echo "USE_RPM_QA_CMD                -> $USE_RPM_QA_CMD"
    echo "VERSION_EXTRACT_CMD           -> $VERSION_EXTRACT_CMD"
    echo "REPO_PREFIX                   -> $REPO_PREFIX"
    echo "PUBLISHING_LEVEL              -> $PUBLISHING_LEVEL"
    echo "PUBLISH_TO_ACR                -> $PUBLISH_TO_ACR"
    echo "CREATE_SBOM                   -> $CREATE_SBOM"
    echo "SBOM_TOOL_PATH                -> $SBOM_TOOL_PATH"
    echo "SBOM_SCRIPT                   -> $SBOM_SCRIPT"
    echo "DISTROLESS                    -> $DISTROLESS"
    echo "TOOLCHAIN_RPMS_TARBALL -> $TOOLCHAIN_RPMS_TARBALL"
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

    if [[ -z "$PACKAGE_FILE" ]]; then
        echo "Error - Package file name cannot be empty."
        exit 1
    fi

    if [[ -z "$DOCKERFILE" ]]; then
        echo "Error - Dockerfile name cannot be empty."
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

    if [[ ! -f $TOOLCHAIN_RPMS_TARBALL ]]; then
        echo "Error - No TOOLCHAIN_RPMS tarball found under '$TOOLCHAIN_RPMS_TARBALL'."
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

function get_packages_to_install {
    echo "+++ Get packages to install"
    packagesFilePath="$CONTAINER_SRC_DIR/$IMAGE/$PACKAGE_FILE"
    PACKAGES_TO_INSTALL=$(paste -s -d' ' < "$packagesFilePath")
    echo "Packages to install           -> $PACKAGES_TO_INSTALL"
}

function get_component_name {
    echo "+++ Get Component name"
    componentFilePath="$CONTAINER_SRC_DIR/$IMAGE/$COMPONENT_FILE"
    COMPONENT=$(cat "$componentFilePath")
    echo "Component name                -> $COMPONENT"
}

function prepare_dockerfile {
    echo "+++ Prepare dockerfile"
    # Copy original dockerfile from Azure Linux repo.
    cp "$CONTAINER_SRC_DIR/$IMAGE/$DOCKERFILE" "$WORK_DIR/dockerfile"

    # Update the copied dockerfile for later use in container build.
    mainRunInstruction=$(cat "$CONTAINER_SRC_DIR/Dockerfile-Initial")
    sed -E "s|@INCLUDE_MAIN_RUN_INSTRUCTION@|$mainRunInstruction|g" -i "$WORK_DIR/dockerfile"

    if [ -n "$DOCKERFILE_TEXT_REPLACEMENT" ]; then
        TEXT_REPLACEMENT_ARRAY=($DOCKERFILE_TEXT_REPLACEMENT)
        sed -E "s|${TEXT_REPLACEMENT_ARRAY[0]}|${TEXT_REPLACEMENT_ARRAY[1]}|g" -i "$WORK_DIR/dockerfile"
    fi

    echo " Output content of final dockerfile"
    echo "------------------------------------"
    cat "$WORK_DIR/dockerfile"
    echo ""
}

function prepare_docker_directory {
    echo "+++ Prepare docker directory"
    # Get additional required files for the container build from Azure Linux repo.
    configurationDirectoryPath="$CONTAINER_SRC_DIR/$IMAGE/configuration-files"
    if [ -d "$configurationDirectoryPath" ]; then
        cp -v "$configurationDirectoryPath"/* "$WORK_DIR"
    fi

    HOST_MOUNTED_DIR="$WORK_DIR/Stage"
    mkdir -pv "$HOST_MOUNTED_DIR"

    # Copy files into docker context directory
    tar -xvf "$RPMS_TARBALL" -C "$HOST_MOUNTED_DIR"/
    # we look for the toolchain rpms in the same directory as the rpms tarball
    tar -xvf "$TOOLCHAIN_RPMS_TARBALL" -C "$HOST_MOUNTED_DIR/RPMS"/
    cp -v "$CONTAINER_SRC_DIR/azurelinuxlocal.repo" "$HOST_MOUNTED_DIR"/
}

function docker_build {
    echo "+++ Build container"
    pushd "$WORK_DIR" > /dev/null
    echo " docker build command"
    echo "----------------------"
    echo "docker buildx build $DOCKER_BUILD_ARGS" \
    "--build-arg BASE_IMAGE=$BASE_IMAGE_NAME_FULL" \
    "--build-arg RPMS_TO_INSTALL=$PACKAGES_TO_INSTALL" \
    "-t $CONTAINER_IMAGE_NAME --no-cache --progress=plain" \
    "-f $WORK_DIR/Dockerfile ."

    echo ""
    docker buildx build $DOCKER_BUILD_ARGS \
        --build-arg BASE_IMAGE="$BASE_IMAGE_NAME_FULL" \
        --build-arg RPMS_TO_INSTALL="$PACKAGES_TO_INSTALL" \
        -t "$CONTAINER_IMAGE_NAME" --no-cache --progress=plain \
        -f "$WORK_DIR/Dockerfile" .
    popd > /dev/null
}

function set_image_tag {
    echo "+++ Get version of the installed package in the container."
    local containerId
    local installedPackage

    containerId=$(docker run --entrypoint /bin/sh -dt "$CONTAINER_IMAGE_NAME")

    echo "Container ID                  -> $containerId"

    if [[ -n "$VERSION_EXTRACT_CMD" ]]; then
        echo "Using custom version extract command."
        COMPONENT_VERSION=$(docker exec "$containerId" sh -c "$VERSION_EXTRACT_CMD")
    else
        if [[ $USE_RPM_QA_CMD =~ [Tt]rue ]] ; then
            echo "Using rpm -qa command to get installed package."
            installedPackage=$(docker exec "$containerId" rpm -qa | grep ^"$COMPONENT")
        else
            echo "Using tdnf repoquery command to get installed package."
            # exec as root as the default user for some containers is non-root
            installedPackage=$(docker exec -u 0 "$containerId" tdnf repoquery --installed "$COMPONENT" | grep ^"$COMPONENT")
        fi
        echo "Full Installed Package:       -> $installedPackage"
        COMPONENT_VERSION=$(echo "$installedPackage" | awk '{n=split($0,a,"-")};{split(a[n],b,".")}; {print a[n-1]"-"b[1]}') # 16.16.0-1
    fi

    echo "Component Version             -> $COMPONENT_VERSION"
    docker rm -f "$containerId"

    # Rename the image to include package version
    # For HCI Images, do not include "-$DISTRO_IDENTIFIER" in the image tag; Instead use a "."
    if [ "$IS_HCI_IMAGE" = true ]; then
        # Example: acrafoimages.azurecr.io/base/kubevirt/virt-operator:0.59.0-2.2.0.20230607-amd64
        CONTAINER_IMAGE_NAME_FINAL="$CONTAINER_IMAGE_NAME:$COMPONENT_VERSION.$BASE_IMAGE_TAG"
    else
        # Example: azurelinuxpreview.azurecr.io/base/nodejs:16.19.1-2-$DISTRO_IDENTIFIER2.0.20230607-amd64
        CONTAINER_IMAGE_NAME_FINAL="$CONTAINER_IMAGE_NAME:$COMPONENT_VERSION-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"
    fi
}

function distroless_container {
    if [[ ! "$DISTROLESS" =~ [Tt]rue ]]; then
            echo "+++ Skip creating distroless container"
        return
    fi

    # shellcheck source=/dev/null
    source "$CONTAINER_SRC_DIR/scripts/BuildGoldenDistrolessContainer.sh"
    create_distroless_container
}

source "$CONTAINER_SRC_DIR/scripts/BuildContainerCommonSteps.sh"
print_inputs
validate_inputs
initialization
get_packages_to_install
get_component_name
prepare_dockerfile
prepare_docker_directory
docker_build
set_image_tag
finalize
distroless_container
