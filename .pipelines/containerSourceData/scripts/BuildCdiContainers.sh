#!/bin/bash

function create_cdi_container_image_base {
    local componentName
    local baseContainerName
    local baseContainerTag
    local initialDockerfile
    local containerBuildDir
    local binaryPath
    local containerUser
    local packagesToInstall

    # $1: sub-component name
    # $2: container type
    # $3: base container name
    # $4: base container tag
    # $5: packages to install
    # $6: initial Dockerfile
    # $7: binary path
    # $8: container user
    componentName=$1
    containerType=$2
    baseContainerName=$3
    baseContainerTag=$4
    packagesToInstall=$5
    initialDockerfile=$6
    binaryPath=$7
    containerUser=$8

    echo "------ Display Arguments ------"
    echo "Component Name:           -> $componentName"
    echo "Container Type:           -> $containerType"
    echo "Base Container Name:      -> $baseContainerName"
    echo "Base Container Tag:       -> $baseContainerTag"
    echo "Packages to Install:      -> $packagesToInstall"
    echo "Initial Dockerfile:       -> $initialDockerfile"
    echo "Binary Path:              -> $binaryPath"
    echo "Container User:           -> $containerUser"

    # compose the container name. E.g. for branch-main this will look like
    # cblmarinermain.azurecr.io/kubevirt/cdi-apiserver:1.51.0-1-cm2.0.20220811-amd64
    # cblmarinermain.azurecr.io -> repo
    # kubevirt -> CDI_FOLDER_PREFIX
    # cdi-apiserver -> $containerType (sub component)
    # 1.51.0-1-cm2.0.20220811-amd64 -> version for cdi v1.51.0 rpms with base version details

    local originalContainerName="$CONTAINER_REGISTRY_NAME_FULL/base/$CDI_FOLDER_PREFIX/$containerType"

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create container $originalContainerName"

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

    # Workaround till proper binaries are built as part of the cdi rpm & renames are removed
    # https://github.com/microsoft/CBL-Mariner/pull/5708/files#
    cp "$containerSrcDir/$CDI_BASE_COMPONENT/configuration-files"/* "$containerBuildDir"
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
      --build-arg BINARY_NAME="$(basename $binaryPath)" \
      --build-arg USER="$containerUser" \
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

    local containerTypeNoDash=${containerType//-/}    # Removes dash from containerType. Ex: azure-cli -> azurecli
    echo "$containerName" >> $TEMPDIR/$file_name_prefix-$containerTypeNoDash$file_ext

    ResetDockerDefaultStorageLocation "$newDockerStorageLocation"

    # Clean up docker storage folder
    sudo rm -rf "$newDockerStorageLocation"


    # clean up temp folder
    popd > /dev/null
    sudo rm -rf $containerBuildDir

    echo "----------------------------------------------------------------------"
}

# Create containers for cdi-apiserver, cdi-cloner, cdi-controller, cdi-importer,
# cdi-operator, cdi-uploadproxy, cdi-uploadserver for CDI_BASE_COMPONENT
function create_cdi_subcomp_containers {
  declare -A cdi_container_components
  declare -A cdi_binary_path
  declare -A cdi_container_user

  local sub_components
  local CDI_PACKAGE_BASE="containerized-data-importer"

  sub_components=('api' 'cloner' 'controller' 'importer' 'operator' 'uploadproxy' 'uploadserver')

  # populate the cdi container names
  for comp in ${sub_components[@]}
  do
    cdi_container_components[$comp]=$comp

    # replace 'api with 'apiserver'
    [ "$comp" = "api" ] && cdi_container_components[$comp]='apiserver'

    cdi_binary_path[$comp]="/usr/bin/cdi-${cdi_container_components[$comp]}"

    # Setting the active user in the container based on upstream images
    # By default set the user to be a non-root user (who is in the root group)
    cdi_container_user[$comp]=1001
  done

  mkdir -p $OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER

  for comp in ${sub_components[@]}
  do
    # To build for specific versions - include it here with the name
    dependency_component=$CDI_PACKAGE_BASE-$comp
    echo "+++ CDI component name for $comp set at ${cdi_container_components[$comp]}"
    cdi_comp=$CDI_BASE_COMPONENT-${cdi_container_components[$comp]}

    local pkgsFileName="$comp.pkg"
    local packagesToInstall=()
    getPkgsFromFile $CDI_BASE_COMPONENT $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"

    echo "+++ CDI binary path for $comp ==> ${cdi_binary_path[$comp]}"
    echo "+++ create container based on $base_container_name:$base_container_tag for $dependency_component"
    create_cdi_container_image_base \
      "$dependency_component" \
      "$cdi_comp" \
      "$base_container_name"\
      "$base_container_tag" \
      "$packages" \
      "$containerSrcDir/$CDI_BASE_COMPONENT/Dockerfile-$cdi_comp" \
      ${cdi_binary_path[$comp]} \
      ${cdi_container_user[$comp]}

    # Save text files generated in TEMPDIR
    echo "+++ publish container list into pipeline artifacts"
    cp $TEMPDIR/$file_name_prefix-*$file_ext $OUTPUT_FOLDER/CONTAINER_LISTS_FOLDER

  done
}
