#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Logs into Azure
function azure_login {
    # Note this script assumes that az login has already been done
    echo "    -> login into ACR $1"
    az acr login --name "$1"
}

# Builds SBOM
function generate_container_sbom {
    local component_name=$1
    local base_container_name=$2
    local base_container_tag=$3
    local container_name=$4
    local component_version_revision=$5
    local container_name_sanitized=$6

    echo
    echo "====================================================================="
    echo "Generate SBOM for containers $container_image_name"
    echo "====================================================================="
    echo

    DOCKER_BUILD_DIR="$(pwd)"

    # generate-container-sbom.sh will create the SBOM at the following path
    IMAGE_SBOM_MANIFEST_PATH="$DOCKER_BUILD_DIR/_manifest/spdx_2.2/manifest.spdx.json"
    "$ROOT_FOLDER"/.pipelines/generate-container-sbom.sh \
        "$DOCKER_BUILD_DIR" \
        "$container_name" \
        "$MANIFEST_TOOL_DIR" \
        "$base_container_name-$component_name" \
        "$component_version_revision-cm$base_container_tag"

    cp -v "$IMAGE_SBOM_MANIFEST_PATH" "$OUTPUT_FOLDER/SBOM_IMAGES/$container_name_sanitized.spdx.json"
    echo "Generated SBOM:'$OUTPUT_FOLDER/SBOM_IMAGES/$container_name_sanitized.spdx.json'"
}

readonly DOCKER_DAEMON_JSON_FILE="/etc/docker/daemon.json"
readonly DOCKER_DAEMON_JSON_BACKUP_FILE="/etc/docker/daemon.json.cfbackup"

# Sets the docker storage location to a user provided path which larger disk space
function SetDockerDefaultStorageLocation {
    local newLocation=$1
    echo "Change docker default storage location"
    echo "Default docker storage location"
    sudo systemctl start docker
    docker info | grep "Docker Root Dir"

    echo "Stop docker"
    sudo systemctl stop docker.service
    sudo systemctl stop docker.socket

    ls -lR /etc/docker

    # Do not clobber existing backup to not accidentally overwrite the valid backup
    if [ ! -f $DOCKER_DAEMON_JSON_BACKUP_FILE ] && [ -f $DOCKER_DAEMON_JSON_FILE ]; then
        echo "Backup daemon.json"
        sudo cp $DOCKER_DAEMON_JSON_FILE $DOCKER_DAEMON_JSON_BACKUP_FILE
    fi

    echo "Copy data-root property to daemon.json"
    echo "{ \"data-root\": \"${newLocation}\" }" > daemon.json

    echo "Display daemon.json"
    sudo cat daemon.json

    echo "Copy daemon.json to docker"
    sudo cp daemon.json $DOCKER_DAEMON_JSON_FILE

    mkdir -p "${newLocation}"

    echo "Restart docker"
    sudo systemctl daemon-reload
    sudo systemctl start docker

    echo "New docker storage location"
    docker info | grep "Docker Root Dir"

    echo "--------------------------------------------"
}

# Resets the docker storage location from backup
function ResetDockerDefaultStorageLocation {
    local currentLocation=$1
    echo "Reset docker default storage location"
    echo "Stop docker"
    sudo systemctl stop docker.service
    sudo systemctl stop docker.socket

    echo "Recovering daemon.json from backup"
    if [ -f $DOCKER_DAEMON_JSON_BACKUP_FILE ]; then
        sudo mv $DOCKER_DAEMON_JSON_BACKUP_FILE $DOCKER_DAEMON_JSON_FILE
    else 
        sudo rm $DOCKER_DAEMON_JSON_FILE
    fi

    echo "Restart docker"
    sudo systemctl daemon-reload
    sudo systemctl start docker

    echo "New docker storage location"
    docker info | grep "Docker Root Dir"
}

# Saves the container list in folder named CONTAINER_LISTS_FOLDER
function save_container_list {
    # Save text files generated in TEMPDIR
    echo
    echo "====================================================================="
    echo "Publish container list into pipeline artifacts"
    echo "====================================================================="
    echo

    mkdir -pv "$OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER"
    cp "$TEMPDIR"/$file_name_prefix-*$file_ext "$OUTPUT_FOLDER"/CONTAINER_LISTS_FOLDER
}

# Tests golden container
function test_golden_container {
    local container_type=$1
    local container_image_name=$2

    echo
    echo "====================================================================="
    echo "Test container $container_image_name"
    echo "====================================================================="
    echo

    "$ROOT_FOLDER/pipelines/test-golden-image-pipeline/test-source-artifacts/$container_type/TestRunner.sh" \
        -n "$container_image_name" \
        -o "$PWD"
}

function test_distroless_container {
    local test_dir_name=$1
    local builder_image=$2
    local container_image_name=$3

    echo
    echo "====================================================================="
    echo "Test container $container_image_name"
    echo "====================================================================="
    echo

    "$ROOT_FOLDER/pipelines/test-golden-image-pipeline/test-source-artifacts/$test_dir_name/TestRunner.sh" \
        -b "$builder_image" \
        -n "$container_image_name" \
        -o "$PWD"
}

# Publishes the given golden container to azure container registry
function publish_container {
    local container_name=$1
    echo
    echo "====================================================================="
    echo "Publish container $container_name"
    echo "====================================================================="
    echo

    previous_login="none"
    OLDIFS=$IFS
    IFS='.'
    read -ra name_parts <<< "$container_name"
    IFS=$OLDIFS
    container_registry="${name_parts[0]}"

    if [[ "$previous_login" != "$container_registry" ]]; then
        echo "    -> login into ACR $container_registry"
        az acr login --name "$container_registry"
        previous_login=$container_registry
    fi

    docker image push "$container_name"
    echo
}

# Checks if $GOLDEN_CONTAINER_IMAGE is an HCI image by looking at the config file.
# Assigns a boolean to the out variables.
# The caller must define ROOT_FOLDER and GOLDEN_CONTAINER_IMAGE.
function checkIfHciImage {
    local __containerImageName=$1 # [out parameter]
    local isHciImage=false
    ACR_MAPPING_CONFIG_FILE="$ROOT_FOLDER/pipelines/publish-containers/common/configuration/acrRepoMapping.json"
    marinerHciGoldenImagesArray=$(jq ".MarinerHciGoldenImages[]" "$ACR_MAPPING_CONFIG_FILE" | tr -d \")
    for marinerHciGoldenImage in $marinerHciGoldenImagesArray; do
        if [[ $marinerHciGoldenImage == "$GOLDEN_CONTAINER_IMAGE" ]]; then
            isHciImage=true
            break
        fi
    done
	eval $__containerImageName=$isHciImage
}

# get registry prefix (if any)
# Assigns a string to the out variables.
# The caller must define ROOT_FOLDER
function getRegistryPrefix {
    local container_name=$1
    local publishingLevel=$2
    local gitBranch=$3
    local __registryPrefix=$4 # [out parameter]
    local prefix=""

    local git_branch_json=""
    local acr_repo_mapping_json=""
    local image_json=""

    ACR_MAPPING_CONFIG_FILE="$ROOT_FOLDER/pipelines/publish-containers/common/configuration/acrRepoMapping.json"
	eval $__registryPrefix=$prefix

    git_branch_json=$(jq ".gitBranches[]|select(.gitBranch == \"$gitBranch\")" "$ACR_MAPPING_CONFIG_FILE")
    if [[ -z $git_branch_json ]]; then
        echo "No branch tag '$gitBranch' in json ($ACR_MAPPING_CONFIG_FILE)"
        return
    fi

    acr_repo_mapping_json=$(echo $git_branch_json | jq ".acrRepoMapping[]|select(.publishingLevel == \"$publishingLevel\")")
    if [[ -z $acr_repo_mapping_json ]]; then
        echo "No publishing level '$publishingLevel' for branch '$gitBranch' in json ($ACR_MAPPING_CONFIG_FILE)"
        return
    fi

    image_json=$(echo $acr_repo_mapping_json | jq ".images[]|select(.name == \"$container_name\")")
    if [[ -z $image_json ]]; then
        echo "No container named '$container_name' for publishing level '$publishingLevel' for branch '$gitBranch' in json ($ACR_MAPPING_CONFIG_FILE)"
        return
    fi

    prefix=$(echo $image_json | jq .repoPrefix | tr -d \")
    # reset registry prefix to "" if it is not defined in json (jq return 'null') 
    if [[ $prefix == "null" ]]; then
        prefix=""
        echo "No registry prefix for '$container_name' branch '$gitBranch' publishing level '$publishingLevel'"
    else
        echo "Registry prefix '$prefix' for '$container_name' branch '$gitBranch' publishing level '$publishingLevel'"
    fi

	eval $__registryPrefix=$prefix
}