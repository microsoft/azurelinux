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
# - e) Component name (e.g. nodejs18, postgresql, containerized-data-importer-api, etc.)
# - f) Package file name (e.g. nodejs18.pkg, postgres.pkg, api.pkg, etc.)
# - g) Dockerfile name (e.g. Dockerfile-nodejs, Dockerfile-Postgres, Dockerfile-cdi-apiserver, etc.)
# - h) Docker build arguments (e.g. '--build-arg BINARY_NAME="cdi-apiserver" --build-arg USER=1001')
# - i) Dockerfile text replacement (e.g. '@BINARY_PATH@ \"/usr/bin/acmesolver\"')
# - j) Output directory for container artifacts.
# - k) RPMS tarball file path (e.g. ./rpms.tar.gz)
# - l) Container source directory (e.g. ~/workspace/CBL-Mariner/.pipelines/containerSourceData)
# - m) Is HCI image (e.g. true, false. HCI images have different naming convention)
# - n) Use rpm -qa command (e.g. true, false. Some images use rpm -qa command to get installed package)
# - o) Repo prefix (e.g. public/cbl-mariner, unlisted/cbl-mariner, etc.)
# - p) Publishing level (e.g. preview, development)
# - q) Publish to ACR (e.g. true, false. If true, the script will push the container to ACR)
# - r) Create SBOM (e.g. true, false. If true, the script will create SBOM for the container)
# - s) SBOM tool path.
# - t) Script to create SBOM for the container image.
# - u) Create Distroless container (e.g. true, false. If true, the script will also create a distroless container)

# Assuming you are in your current working directory. Below should be the directory structure:
#   │   rpms.tar.gz
#   │   OUTPUT
#   │   ├── 

# Assuming CBL-Mariner repo is cloned in your home directory. Below should be the directory structure:
#   ~/CBL-Mariner/.pipelines/containerSourceData
#   ├── nodejs
#   │   ├── distroless
#   │   │   ├── holdback-nodejs18.pkg
#   │   │   ├── nodejs18.pkg
#   │   ├── Dockerfile-Nodejs
#   │   ├── nodejs18.pkg
#   ├── configuration
#   │   ├── acrRepoV2.json
#   ├── scripts
#   │   ├── BuildGoldenContainer.sh
#   │   ├── acrRepoParser.py
#   ├── Dockerfile-Initial
#   ├── marinerLocalRepo.repo

# Example usage:
# /bin/bash ~/CBL-Mariner/.pipelines/containerSourceData/scripts/BuildGoldenContainer.sh \
#     -a "mcr.microsoft.com/cbl-mariner/base/core:2.0" -b azurelinuxlocal \
#     -c "base/nodejs" -d "nodejs" -e "nodejs18" -f nodejs18.pkg -g Dockerfile-Nodejs \
#     -j OUTPUT -k ./rpms.tar.gz -l ~/CBL-Mariner/.pipelines/containerSourceData \
#     -m "false" -n "false" -p development -q "false" -u "true"

while getopts ":a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:" OPTIONS; do
    case ${OPTIONS} in
    a ) BASE_IMAGE_NAME_FULL=$OPTARG;;
    b ) ACR=$OPTARG;;
    c ) REPOSITORY=$OPTARG;;
    d ) IMAGE=$OPTARG;;
    e ) COMPONENT=$OPTARG;;
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
    echo "COMPONENT                     -> $COMPONENT"
    echo "PACKAGE_FILE                  -> $PACKAGE_FILE"
    echo "DOCKERFILE                    -> $DOCKERFILE"
    echo "DOCKER_BUILD_ARGS             -> $DOCKER_BUILD_ARGS"
    echo "DOCKERFILE_TEXT_REPLACEMENT   -> $DOCKERFILE_TEXT_REPLACEMENT"
    echo "OUTPUT_DIR                    -> $OUTPUT_DIR"
    echo "RPMS_TARBALL                  -> $RPMS_TARBALL"
    echo "CONTAINER_SRC_DIR             -> $CONTAINER_SRC_DIR"
    echo "IS_HCI_IMAGE                  -> $IS_HCI_IMAGE"
    echo "USE_RPM_QA_CMD                -> $USE_RPM_QA_CMD"
    echo "REPO_PREFIX                   -> $REPO_PREFIX"
    echo "PUBLISHING_LEVEL              -> $PUBLISHING_LEVEL"
    echo "PUBLISH_TO_ACR                -> $PUBLISH_TO_ACR"
    echo "CREATE_SBOM                   -> $CREATE_SBOM"
    echo "SBOM_TOOL_PATH                -> $SBOM_TOOL_PATH"
    echo "SBOM_SCRIPT                   -> $SBOM_SCRIPT"
    echo "DISTROLESS                    -> $DISTROLESS"
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

function initialization {
    echo "+++ Initialization"
    if [ "$PUBLISHING_LEVEL" = "preview" ]; then
        GOLDEN_IMAGE_NAME=${ACR}.azurecr.io/${REPO_PREFIX}/${REPOSITORY}
    elif [ "$PUBLISHING_LEVEL" = "development" ]; then
        GOLDEN_IMAGE_NAME=${ACR}.azurecr.io/${REPOSITORY}
    fi

    BASE_IMAGE_NAME=${BASE_IMAGE_NAME_FULL%:*}  # mcr.microsoft.com/cbl-mariner/base/core
    BASE_IMAGE_TAG=${BASE_IMAGE_NAME_FULL#*:}   # 2.0
    AZURE_LINUX_VERSION=${BASE_IMAGE_TAG%.*}    # 2.0

    # For Azure Linux 2.0, we have shipped the container images with
    # the below value of DISTRO_IDENTIFIER in the image tag.
    # TODO: We may need to update this value for Azure Linux 3.0.
    DISTRO_IDENTIFIER="cm"

    echo "Golden Image Name             -> $GOLDEN_IMAGE_NAME"
    echo "Base ACR Container Name       -> $BASE_IMAGE_NAME"
    echo "Base ACR Container Tag        -> $BASE_IMAGE_TAG"
    echo "Azure Linux Version           -> $AZURE_LINUX_VERSION"
    echo "Distro Identifier             -> $DISTRO_IDENTIFIER"
}

function prepare_dockerfile {
    echo "+++ Prepare dockerfile"
    # Copy original dockerfile from CBL-Mariner repo.
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

function get_packages_to_install {
    echo "+++ Get packages to install"
    packagesFilePath="$CONTAINER_SRC_DIR/$IMAGE/$PACKAGE_FILE"
    PACKAGES_TO_INSTALL=$(paste -s -d' ' < "$packagesFilePath")
    echo "Packages to install           -> $PACKAGES_TO_INSTALL"
}

function prepare_docker_directory {
    echo "+++ Prepare docker directory"
    # Get additional required files for the container build from CBL-Mariner repo.
    configurationDirectoryPath="$CONTAINER_SRC_DIR/$IMAGE/configuration-files"
    if [ -d "$configurationDirectoryPath" ]; then
        cp -v "$configurationDirectoryPath"/* "$WORK_DIR"
    fi

    HOST_MOUNTED_DIR="$WORK_DIR/Stage"
    mkdir -pv "$HOST_MOUNTED_DIR"

    # Copy files into docker context directory
    tar -xf "$RPMS_TARBALL" -C "$HOST_MOUNTED_DIR"/
    cp -v "$CONTAINER_SRC_DIR/marinerLocalRepo.repo" "$HOST_MOUNTED_DIR"/
}

function docker_build {
    echo "+++ Build container"
    pushd "$WORK_DIR" > /dev/null
    echo " docker build command"
    echo "----------------------"
    echo "docker buildx build $DOCKER_BUILD_ARGS" \
    "--build-arg BASE_IMAGE=$BASE_IMAGE_NAME_FULL" \
    "--build-arg RPMS_TO_INSTALL=$PACKAGES_TO_INSTALL" \
    "-t $GOLDEN_IMAGE_NAME --no-cache --progress=plain" \
    "-f $WORK_DIR/Dockerfile ."

    echo ""
    docker buildx build $DOCKER_BUILD_ARGS \
        --build-arg BASE_IMAGE="$BASE_IMAGE_NAME_FULL" \
        --build-arg RPMS_TO_INSTALL="$PACKAGES_TO_INSTALL" \
        -t "$GOLDEN_IMAGE_NAME" --no-cache --progress=plain \
        -f "$WORK_DIR/Dockerfile" .
    popd > /dev/null
}

function set_image_tag {
    echo "+++ Get version of the installed package in the container."
    local containerId
    local installedPackage

    containerId=$(docker run --entrypoint /bin/bash -dt "$GOLDEN_IMAGE_NAME")

    echo "Container ID                  -> $containerId"

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
    echo "Component Version             -> $COMPONENT_VERSION"
    docker rm -f "$containerId"

    # Rename the image to include package version
    # For HCI Images, do not include "-$DISTRO_IDENTIFIER" in the image tag; Instead use a "."
    if [ "$IS_HCI_IMAGE" = true ]; then
        # Example: acrafoimages.azurecr.io/base/kubevirt/virt-operator:0.59.0-2.2.0.20230607-amd64
        GOLDEN_IMAGE_NAME_FINAL="$GOLDEN_IMAGE_NAME:$COMPONENT_VERSION.$BASE_IMAGE_TAG"
    else
        # Example: azurelinuxpreview.azurecr.io/base/nodejs:16.19.1-2-$DISTRO_IDENTIFIER2.0.20230607-amd64
        GOLDEN_IMAGE_NAME_FINAL="$GOLDEN_IMAGE_NAME:$COMPONENT_VERSION-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"
    fi
}

function finalize {
    echo "+++ Finalize"
    docker image tag "$GOLDEN_IMAGE_NAME" "$GOLDEN_IMAGE_NAME_FINAL"
    docker rmi -f "$GOLDEN_IMAGE_NAME"
    echo "+++ Save container image name to file PublishedContainers-$IMAGE.txt"
    echo "$GOLDEN_IMAGE_NAME_FINAL" >> "$OUTPUT_DIR/PublishedContainers-$IMAGE.txt"
}

function publish_to_acr {
    CONTAINER_IMAGE=$1
    if [[ ! "$PUBLISH_TO_ACR" =~ [Tt]rue ]]; then
        echo "+++ Skip publishing to ACR"
        return
    fi
    echo "+++ Publish container $CONTAINER_IMAGE"
    echo "login into ACR: $ACR"
    az acr login --name "$ACR"
    docker image push "$CONTAINER_IMAGE"
}

function generate_image_sbom {
    if [[ ! "$CREATE_SBOM" =~ [Tt]rue ]]; then
        echo "+++ Skip creating SBOM"
        return
    fi

    echo "+++ Generate SBOM for the container image"
    echo "Sanitized image name has '/' replaced with '-' and ':' replaced with '_'."
    GOLDEN_IMAGE_NAME_SANITIZED=$(echo "$GOLDEN_IMAGE_NAME_FINAL" | tr '/' '-' | tr ':' '_')
    echo "GOLDEN_IMAGE_NAME_SANITIZED   -> $GOLDEN_IMAGE_NAME_SANITIZED"

    DOCKER_BUILD_DIR=$(mktemp -d)
    # SBOM script will create the SBOM at the following path.
    IMAGE_SBOM_MANIFEST_PATH="$DOCKER_BUILD_DIR/_manifest/spdx_2.2/manifest.spdx.json"
    /bin/bash "$SBOM_SCRIPT" \
        "$DOCKER_BUILD_DIR" \
        "$GOLDEN_IMAGE_NAME_FINAL" \
        "$SBOM_TOOL_PATH" \
        "$BASE_IMAGE_NAME-$COMPONENT" \
        "$COMPONENT_VERSION-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"

    SBOM_IMAGES_DIR="$OUTPUT_DIR/SBOM_IMAGES"
    mkdir -p "$SBOM_IMAGES_DIR"
    cp -v "$IMAGE_SBOM_MANIFEST_PATH" "$SBOM_IMAGES_DIR/$GOLDEN_IMAGE_NAME_SANITIZED.spdx.json"
    echo "Generated SBOM:'$SBOM_IMAGES_DIR/$GOLDEN_IMAGE_NAME_SANITIZED.spdx.json'"
    sudo rm -rf "$DOCKER_BUILD_DIR"
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

print_inputs
validate_inputs
initialization
prepare_dockerfile
get_packages_to_install
prepare_docker_directory
docker_build
set_image_tag
finalize
publish_to_acr "$GOLDEN_IMAGE_NAME_FINAL"
generate_image_sbom
distroless_container
