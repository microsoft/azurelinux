#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

function create_kubevirt_container_image_base {
    local componentName=$1
    local containerType=$2
    local baseContainerName=$3
    local baseContainerTag=$4
    local packagesToInstall=$5
    local goldenImageDockerfile=$6
    local originalContainerName=$7
    local containerTypeNoDash

    echo "------ Display Arguments ------"
    echo "Component Name:           -> $componentName"
    echo "Container Type:           -> $containerType"
    echo "Base Container Name:      -> $baseContainerName"
    echo "Base Container Tag:       -> $baseContainerTag"
    echo "Packages to Install:      -> $packagesToInstall"
    echo "Dockerfile:               -> $goldenImageDockerfile"
    echo "Container Name:           -> $originalContainerName"
    
    echo "+++ create container based on $baseContainerName/core:$baseContainerTag for $componentName"
    containerTypeNoDash=${containerType//-/}

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create container $originalContainerName"

    local containerBuildDir="$TEMPDIR/ContainerBuildDir"
    hostMountedDir="$TEMPDIR/ContainerBuildDir/Stage"
    newDockerStorageLocation="$TEMPDIR/storage"

    mkdir -p "$containerBuildDir"
    mkdir -p "$hostMountedDir"
    mkdir -p "$newDockerStorageLocation"

    # Copy files into docker context directory
    tar -xf "$MARINER_RPMS_TARBALL" -C "$hostMountedDir"/
    cp "$CONTAINER_SRC_DIR/marinerLocalRepo.repo" "$hostMountedDir"/
    cp "$CONTAINER_SRC_DIR/Dockerfile-Initial" "$containerBuildDir/Dockerfile-Initial"
    cp "$CONTAINER_SRC_DIR/$KUBEVIRT_BASE_COMPONENT/$goldenImageDockerfile" "$containerBuildDir/Dockerfile"

    # Ensure that the path exists before copying files.
    if [ -d "$CONTAINER_SRC_DIR/$KUBEVIRT_BASE_COMPONENT/configuration-files" ]; then
        cp "$CONTAINER_SRC_DIR/$KUBEVIRT_BASE_COMPONENT/configuration-files"/* "$containerBuildDir"
    fi

    pushd "$containerBuildDir"

    # set Dockerfile
    echo "+++ Updating Dockerfile"
    mainRunInstruction=$(cat Dockerfile-Initial)
    sed -E "s|@INCLUDE_MAIN_RUN_INSTRUCTION@|$mainRunInstruction|g" -i Dockerfile

    cat Dockerfile

    if [ "$DISABLE_DOCKER_REDIRECTION" != "true" ]; then
        SetDockerDefaultStorageLocation "$newDockerStorageLocation"
    fi

    # Build image
    docker buildx build \
        --build-arg BASE_IMAGE="$baseContainerName/core:$baseContainerTag" \
        --build-arg RPMS_TO_INSTALL="$packagesToInstall" \
        -t "$originalContainerName" --no-cache --progress=plain \
        -f $containerBuildDir/Dockerfile .

    # Get the installed package's version
    echo "+++ Get version of the installed package in the container"

    local containerId
    local installedPackage
    local componentVersion

    containerId=$(docker run --entrypoint /bin/bash -dt "$originalContainerName")
    # exec as root as the default user for some containers is non-root
    # componentName e.g. nodejs-16.16.0-1.cm2.x86_64
    installedPackage=$(docker exec -u 0 "$containerId" tdnf repoquery --installed "$componentName" | grep ^"$componentName")
    echo "Full Installed Package:   -> $installedPackage"
    componentVersion=$(echo "$installedPackage" | awk '{n=split($0,a,"-")};{split(a[n],b,".")}; {print a[n-1]"-"b[1]}') # 16.16.0-1
    echo "Component Version         -> $componentVersion"
    docker rm -f "$containerId"

    # Rename the image to include package version
    # For HCI Images, do not include "-cm" in the image tag; Instead use a "."
    if $IS_HCI_IMAGE; then
        # Example: acrafoimages.azurecr.io/base/kubevirt/virt-operator:0.59.0-2.2.0.20230607-amd64
        local containerName="$originalContainerName:$componentVersion.$baseContainerTag"
    else
        # Example: cblmarinermain.azurecr.io/base/nodejs:16.19.1-2-cm2.0.20230607-amd64
        local containerName="$originalContainerName:$componentVersion-cm$baseContainerTag"
    fi

    # replace base container registry prefix by golden container registry prefix (if any)
    local baseRegistryPrefix=""
    local goldenRegistryPrefix=""
    getRegistryPrefix 'base' $PUBLISHING_LEVEL $BRANCH_NAME baseRegistryPrefix
    getRegistryPrefix $GOLDEN_CONTAINER_IMAGE $PUBLISHING_LEVEL $BRANCH_NAME goldenRegistryPrefix
    if [[ -n $goldenRegistryPrefix ]]; then
      if [[ -n $baseRegistryPrefix && \
            $containerName == *"$baseRegistryPrefix"* ]]; then
        # replace base container registry prefix by golden container registry prefix
        echo "replace $baseRegistryPrefix with $goldenRegistryPrefix in $containerName"
        containerName=${containerName/"$baseRegistryPrefix"/"$goldenRegistryPrefix"}
      else
        # add golden container registry prefix
        echo "add $goldenRegistryPrefix prefix to $containerName"
        containerName=${containerName/"$CONTAINER_REGISTRY_NAME_FULL"/"$CONTAINER_REGISTRY_NAME_FULL/$goldenRegistryPrefix"}
      fi
    fi

    docker image tag "$originalContainerName" "$containerName"
    docker rmi -f "$originalContainerName"
    echo "Container Name:           -> $containerName"

    # Publish image
    publish_container "$containerName"

    local containerNameSanitized
    containerNameSanitized=$(echo "$containerName" | tr '/' '-' | tr ':' '_')

    if [[ "$DISABLE_SBOM_GENERATION" != "true" ]]; then
        # Call generate_container_sbom function to generate SBOM
        generate_container_sbom \
            "$componentName" \
            "$baseContainerName" \
            "$baseContainerTag" \
            "$containerName" \
            "$componentVersion" \
            "$containerNameSanitized"
    fi
    popd

    if [ "$DISABLE_DOCKER_REDIRECTION" != "true" ]; then
        ResetDockerDefaultStorageLocation "$newDockerStorageLocation"
    fi

    sudo rm -rf "$newDockerStorageLocation"

    # Clean up temp folder
    sudo rm -rf "$containerBuildDir"

    # Save container name
    echo "$containerName" >> "$TEMPDIR/$file_name_prefix-$containerTypeNoDash$file_ext"
    echo "----------------------------------------------------------------------"

    save_container_list
}

function create_kubevirt_subcomp_containers {
    # NOTE: qemu and edk2 are architecture specific packages.
    # Include this if when edk2 is availble for ARM as well
    # if [[ $CONTAINER_ARCHITECTURE == "*AMD64*" ]]; then
    # else add virtlauncher_rpmsToInstall+=('qemu-system-aarch64')

    mkdir -p $OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER
    local sub_components
    sub_components=('virt-operator' 'virt-api' 'virt-controller' 'virt-handler' 'virt-launcher')

    for comp in ${sub_components[@]}
    do
        # To build for specific versions - include it here with the name
        dependency_component=$KUBEVIRT_BASE_COMPONENT-$comp
        local pkgsFileName="$comp.pkg"
        local packagesToInstall=()
        getPkgsFromFile $KUBEVIRT_BASE_COMPONENT $pkgsFileName packagesToInstall
        local packages="${packagesToInstall[*]}"
        echo "packages to install " $packages
        create_kubevirt_container_image_base \
            "$dependency_component" \
            "$comp" \
            "$base_container_name" \
            "$base_container_tag" \
            "$packages" \
            "Dockerfile-$dependency_component" \
            "$CONTAINER_REGISTRY_NAME_FULL/base/$KUBEVIRT_FOLDER_PREFIX/$comp"
    done
}
