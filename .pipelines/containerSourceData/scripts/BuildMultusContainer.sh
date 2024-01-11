#!/bin/bash

function create_multus_container_image_base {
    local componentName
    local baseContainerName
    local baseContainerTag
    local containerBuildDir
    local initialDockerfile
    local packagesToInstall

    # $1: component name
    # $2: container name
    # $3: container tag
    # $4: packages to install
    # $5: initial Dockerfile
    componentName=$1
    baseContainerName=$2
    baseContainerTag=$3
    packagesToInstall=$4
    initialDockerfile=$5

    local originalContainerName="$CONTAINER_REGISTRY_NAME_FULL/base/$componentName"

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create container $containerName"

    containerBuildDir="$TEMPDIR/ContainerBuildDir"
    hostMountedDir="$TEMPDIR/ContainerBuildDir/Stage"
    newDockerStorageLocation="$TEMPDIR/storage"

    mkdir -p "$containerBuildDir"
    mkdir -p "$hostMountedDir"
    mkdir -p "$newDockerStorageLocation"

    # Copy files into docker context directory
    tar -xf "$MARINER_RPMS_TARBALL" -C "$hostMountedDir"/
    cp "$containerSrcDir/marinerLocalRepo.repo" "$hostMountedDir"/
    cp "$containerSrcDir/Dockerfile-Initial" "$containerBuildDir/Dockerfile-Initial"
    cp $initialDockerfile $containerBuildDir/Dockerfile

    pushd $containerBuildDir > /dev/null

    # set Dockerfile
    echo "+++ Updating Dockerfile"
    mainRunInstruction=$(cat Dockerfile-Initial)
    sed -E "s|@INCLUDE_MAIN_RUN_INSTRUCTION@|$mainRunInstruction|g" -i Dockerfile

    SetDockerDefaultStorageLocation "$newDockerStorageLocation"

    # Build image
    docker buildx build \
        --build-arg BASE_IMAGE="$baseContainerName/core:$baseContainerTag" \
        --build-arg RPMS_TO_INSTALL="$packagesToInstall" \
        -t "$originalContainerName" --no-cache --progress=plain .

    # Get the installed package's version
    echo "+++ Get version of the installed package in the container"

    local containerId=$(docker run --entrypoint /bin/bash -dt "$originalContainerName")
    local installedPackage=$(docker exec "$containerId" rpm -qa | grep ^"$componentName") # nodejs-16.16.0-1.cm2.x86_64
    echo "Full Installed Package:   -> $installedPackage"
    local componentVersion=$(echo "$installedPackage" | awk '{n=split($0,a,"-")};{split(a[n],b,".")}; {print a[n-1]"-"b[1]}') # 16.16.0-1
    echo "Component Version         -> $componentVersion"
    docker rm -f "$containerId"

    # Rename the image to include package version
    local containerName="$originalContainerName:$componentVersion.$baseContainerTag"
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
    
    local containerNameSanitized=$(echo "$containerName" | tr '/' '-' | tr ':' '_')

    publish_container "$containerName"

    # Call generate_container_sbom function to generate SBOM
    generate_container_sbom \
        "$componentName" \
        "$baseContainerName" \
        "$baseContainerTag" \
        "$containerName" \
        "$componentVersion" \
        "$containerNameSanitized"   

    echo "$containerName" >> $TEMPDIR/$file_name_prefix-$componentName$file_ext

    ResetDockerDefaultStorageLocation "$newDockerStorageLocation"

    # Clean up docker storage folder
    sudo rm -rf "$newDockerStorageLocation"

    # clean up temp folder
    popd > /dev/null
    sudo rm -rf $containerBuildDir

    echo "----------------------------------------------------------------------"
}

function create_multus_container {
    mkdir -p $OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER
    local dependency_component=$MULTUS
    local pkgsFileName="$MULTUS.pkg"
    local packagesToInstall=()
    getPkgsFromFile $MULTUS $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"

    echo "+++ create container based on $base_container_name:$base_container_tag for $dependency_component"
    create_multus_container_image_base \
        "$dependency_component" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "$containerSrcDir/$MULTUS/Dockerfile-Multus"

    # Save text files generated in TEMPDIR
    echo "+++ publish container list into pipeline artifacts"
    cp $TEMPDIR/$file_name_prefix-*$file_ext $OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER

}