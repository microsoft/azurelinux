#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# Add for debuggin purposes
echo "ACR                           -> $ACR"
echo "CONTAINER_IMAGE_NAME_FINAL    -> $CONTAINER_IMAGE_NAME_FINAL"
echo "REPOSITORY                    -> $REPOSITORY"
echo "REPO_PREFIX                   -> $REPO_PREFIX"
echo "IMAGE                         -> $IMAGE"
echo "OUTPUT_DIR                    -> $OUTPUT_DIR"
echo "END_OF_LIFE_1_YEAR            -> $END_OF_LIFE_1_YEAR"
echo "PUBLISH_TO_ACR                -> $PUBLISH_TO_ACR"
echo "CREATE_SBOM                   -> $CREATE_SBOM"
echo "SBOM_TOOL_PATH                -> $SBOM_TOOL_PATH"
echo "SBOM_SCRIPT                   -> $SBOM_SCRIPT"

function initialization {
    echo "+++ Initialization"
    if [ "$PUBLISHING_LEVEL" = "preview" ]; then
        CONTAINER_IMAGE_NAME=${ACR}.azurecr.io/${REPO_PREFIX}/${REPOSITORY}
    elif [ "$PUBLISHING_LEVEL" = "development" ]; then
        CONTAINER_IMAGE_NAME=${ACR}.azurecr.io/${REPOSITORY}
    fi

    BASE_IMAGE_NAME=${BASE_IMAGE_NAME_FULL%:*}  # mcr.microsoft.com/cbl-mariner/base/core
    BASE_IMAGE_TAG=${BASE_IMAGE_NAME_FULL#*:}   # 2.0
    AZURE_LINUX_VERSION=${BASE_IMAGE_TAG%.*}    # 2.0

    # For Azure Linux 2.0, the distro identifier is "cm" 
    # For future versions of Azure Linux, the distro identifer is "azl"
    if [[ "$AZURE_LINUX_VERSION" == "2.0" ]]; then
        DISTRO_IDENTIFIER="cm"
    else
        DISTRO_IDENTIFIER="azl"
    fi
    
    END_OF_LIFE_1_YEAR=$(date -d "+1 year" "+%Y-%m-%dT%H:%M:%SZ")

    echo "Container Image Name          -> $CONTAINER_IMAGE_NAME"
    echo "Base ACR Container Name       -> $BASE_IMAGE_NAME"
    echo "Base ACR Container Tag        -> $BASE_IMAGE_TAG"
    echo "Azure Linux Version           -> $AZURE_LINUX_VERSION"
    echo "Distro Identifier             -> $DISTRO_IDENTIFIER"
    echo "End of Life                   -> $END_OF_LIFE_1_YEAR"
}

function finalize {
    echo "+++ Finalize"
    docker image tag "$CONTAINER_IMAGE_NAME" "$CONTAINER_IMAGE_NAME_FINAL"
    docker rmi -f "$CONTAINER_IMAGE_NAME"
    echo "+++ Save container image name to file PublishedContainers-$IMAGE.txt"
    echo "$CONTAINER_IMAGE_NAME_FINAL" >> "$OUTPUT_DIR/PublishedContainers-$IMAGE.txt"

    # Publish the image to ACR
    publish_to_acr

    # Generate SBOM
    generate_image_sbom
}

function oras_attach {
    local image_name=$1
    oras attach \
        --artifact-type "application/vnd.microsoft.artifact.lifecycle" \
        --annotation "vnd.microsoft.artifact.lifecycle.end-of-life.date=$END_OF_LIFE_1_YEAR" \
        "$image_name"
}

function publish_to_acr {
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

    echo "+++ Publish container $CONTAINER_IMAGE_NAME_FINAL"
    docker image push "$CONTAINER_IMAGE_NAME_FINAL"
    oras_attach "$CONTAINER_IMAGE_NAME_FINAL"
}

function generate_image_sbom {
    if [[ ! "$CREATE_SBOM" =~ [Tt]rue ]]; then
        echo "+++ Skip creating SBOM"
        return
    fi

    echo "+++ Generate SBOM for the container image"
    echo "Sanitized image name has '/' replaced with '-' and ':' replaced with '_'."
    CONTAINER_IMAGE_NAME_SANITIZED=$(echo "$CONTAINER_IMAGE_NAME_FINAL" | tr '/' '-' | tr ':' '_')
    echo "CONTAINER_IMAGE_NAME_SANITIZED   -> $CONTAINER_IMAGE_NAME_SANITIZED"

    DOCKER_BUILD_DIR=$(mktemp -d)
    # SBOM script will create the SBOM at the following path.
    IMAGE_SBOM_MANIFEST_PATH="$DOCKER_BUILD_DIR/_manifest/spdx_2.2/manifest.spdx.json"
    /bin/bash "$SBOM_SCRIPT" \
        "$DOCKER_BUILD_DIR" \
        "$CONTAINER_IMAGE_NAME_FINAL" \
        "$SBOM_TOOL_PATH" \
        "$BASE_IMAGE_NAME-$COMPONENT" \
        "$COMPONENT_VERSION-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"

    SBOM_IMAGES_DIR="$OUTPUT_DIR/SBOM_IMAGES"
    mkdir -p "$SBOM_IMAGES_DIR"
    cp -v "$IMAGE_SBOM_MANIFEST_PATH" "$SBOM_IMAGES_DIR/$CONTAINER_IMAGE_NAME_SANITIZED.spdx.json"
    echo "Generated SBOM:'$SBOM_IMAGES_DIR/$CONTAINER_IMAGE_NAME_SANITIZED.spdx.json'"
    sudo rm -rf "$DOCKER_BUILD_DIR"
}
