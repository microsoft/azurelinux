#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

function DockerBuild {
    local containerName=$1
    local azureLinuxVersion=$2
    local imageType=$3
    local packagesToInstall=$4
    local packagesToHoldback=$5
    local installNonrootUser=$6
    local rpmsDir=$7
    local user=root
    local userUid=0

    if $installNonrootUser; then
        user="nonroot"
        userUid=65532
    fi

    # Create container
    echo "+++ Create container $containerName"
    docker build . \
        -t "$containerName" \
        -f "$marinaraSrcDir/dockerfiles/dockerfile-new-image" \
        --build-arg MARINER_VERSION="$azureLinuxVersion" \
        --build-arg IMAGE_TYPE="$imageType" \
        --build-arg PACKAGES_TO_INSTALL="$packagesToInstall" \
        --build-arg PACKAGES_TO_HOLDBACK="$packagesToHoldback" \
        --build-arg USER="$user" \
        --build-arg USER_UID=$userUid \
        --build-arg RPMS="$rpmsDir" \
        --build-arg LOCAL_REPO_FILE="$marinaraSrcDir/local.repo" \
        --no-cache \
        --progress=plain
}

function create_distroless_container {
    echo "+++ Create distroless container"

    distrolessPkgsFile="$CONTAINER_SRC_DIR/$IMAGE/distroless/$PACKAGE_FILE"
    DISTROLESS_PACKAGES_TO_INSTALL=$(paste -s -d' ' < "$distrolessPkgsFile")
    distrolessPkgsHoldbackFile="$CONTAINER_SRC_DIR/$IMAGE/distroless/holdback-$PACKAGE_FILE"
    DISTROLESS_PACKAGES_TO_HOLD_BACK=$(paste -s -d' ' < "$distrolessPkgsHoldbackFile")
    echo "Distroless Packages to install    -> $DISTROLESS_PACKAGES_TO_INSTALL"
    echo "Distroless Packages to hold back  -> $DISTROLESS_PACKAGES_TO_HOLD_BACK"

    DISTROLESS_GOLDEN_IMAGE_NAME=${GOLDEN_IMAGE_NAME//base/distroless}
    standardContainerName="$DISTROLESS_GOLDEN_IMAGE_NAME:$COMPONENT_VERSION-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"
    debugContainerName="$DISTROLESS_GOLDEN_IMAGE_NAME:$COMPONENT_VERSION-debug-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"
    nonrootContainerName="$DISTROLESS_GOLDEN_IMAGE_NAME:$COMPONENT_VERSION-nonroot-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"
    debugNonrootContainerName="$DISTROLESS_GOLDEN_IMAGE_NAME:$COMPONENT_VERSION-debug-nonroot-$DISTRO_IDENTIFIER$BASE_IMAGE_TAG"

    marinara="marinara"
    marinaraSrcDir="$marinara-src"

    echo "+++ Clone marinara repo"
    git clone "https://github.com/microsoft/$marinara.git" "$WORK_DIR/$marinaraSrcDir"
    
    # It is important to operate from the $WORK_DIR to ensure that docker can access the files.
    pushd "$WORK_DIR" > /dev/null

    MARINARA_IMAGE=${BASE_IMAGE_NAME_FULL/base\/core/$marinara}
    echo "MARINARA_IMAGE -> $MARINARA_IMAGE"

    sed -E "s|^FROM .*builder$|FROM $MARINARA_IMAGE as builder|g" -i "$marinaraSrcDir/dockerfiles/dockerfile-new-image"

    # WORK_DIR has a directory named 'Stage' which created inside prepare_docker_directory function
    # This directory has a directory named RPMS which contains the RPMs to be installed in the container.
    # The path to rpms is /Stage/RPMS
    rpmsPath="/Stage/RPMS"

    # Create standard container
    DockerBuild \
        "$standardContainerName" \
        "$AZURE_LINUX_VERSION" \
        "custom" \
        "$DISTROLESS_PACKAGES_TO_INSTALL" \
        "$DISTROLESS_PACKAGES_TO_HOLD_BACK" \
        false \
        "$rpmsPath"

    # Create debug container
    DockerBuild \
        "$debugContainerName" \
        "$AZURE_LINUX_VERSION" \
        "custom-debug" \
        "$DISTROLESS_PACKAGES_TO_INSTALL" \
        "$DISTROLESS_PACKAGES_TO_HOLD_BACK" \
        false \
        "$rpmsPath"

    # Create nonroot container
    DockerBuild \
        "$nonrootContainerName" \
        "$AZURE_LINUX_VERSION" \
        "custom-nonroot" \
        "$DISTROLESS_PACKAGES_TO_INSTALL" \
        "$DISTROLESS_PACKAGES_TO_HOLD_BACK" \
        true \
        "$rpmsPath"

    # Create debug nonroot container
    DockerBuild \
        "$debugNonrootContainerName" \
        "$AZURE_LINUX_VERSION" \
        "custom-debug-nonroot" \
        "$DISTROLESS_PACKAGES_TO_INSTALL" \
        "$DISTROLESS_PACKAGES_TO_HOLD_BACK" \
        true \
        "$rpmsPath"

    popd > /dev/null
    
    echo "+++ Save distroless container images to file PublishedContainers-$IMAGE.txt"
    {
        echo "$standardContainerName";
        echo "$debugContainerName";
        echo "$nonrootContainerName";
        echo "$debugNonrootContainerName";
    } >> "$OUTPUT_DIR/PublishedContainers-$IMAGE.txt"

    publish_to_acr "$standardContainerName"
    publish_to_acr "$debugContainerName"
    publish_to_acr "$nonrootContainerName"
    publish_to_acr "$debugNonrootContainerName"
}
