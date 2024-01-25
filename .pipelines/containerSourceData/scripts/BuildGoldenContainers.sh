#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# parse script parameters:
# -i -> published base container file
# -m -> folder containing artifacts of CBL-Mariner
# -n -> name of the container registry
# -g -> golden container image
# -o -> folder where to put artifacts to be published
# -s -> manifest tool directory path
# -b -> branch name
# -p -> publishing level
#
while getopts ":i:m:n:g:o:s:b:p:x:" OPTIONS; do
    case ${OPTIONS} in
    i ) BASE_IMAGE_FOLDER=$OPTARG;;
    m ) MARINER_ARTIFACTS_FOLDER=$OPTARG;;
    n ) CONTAINER_REGISTRY_NAME=$OPTARG
        CONTAINER_REGISTRY_NAME_FULL="$CONTAINER_REGISTRY_NAME.azurecr.io";;
    g ) GOLDEN_CONTAINER_IMAGE=$OPTARG;;
    o ) OUTPUT_FOLDER=$OPTARG;;
    s ) MANIFEST_TOOL_DIR=$OPTARG;;
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

MANIFEST_TOOL_DIR="$(cd "$MANIFEST_TOOL_DIR"; pwd)"
OUTPUT_FOLDER="$(cd "$OUTPUT_FOLDER"; pwd)"

echo "- BASE IMAGE_FOLDER               -> $BASE_IMAGE_FOLDER"
echo "- MARINER_ARTIFACTS_FOLDER        -> $MARINER_ARTIFACTS_FOLDER"
echo "- CONTAINER_REGISTRY_NAME         -> $CONTAINER_REGISTRY_NAME"
echo "- CONTAINER_REGISTRY_NAME_FULL    -> $CONTAINER_REGISTRY_NAME_FULL"
echo "- GOLDEN_CONTAINER_IMAGE          -> $GOLDEN_CONTAINER_IMAGE"
echo "- BRANCH_NAME                     -> $BRANCH_NAME"
echo "- PUBLISHING_LEVEL                -> $PUBLISHING_LEVEL"
echo "- MANIFEST_TOOL_DIR               -> $MANIFEST_TOOL_DIR"
echo "- OUTPUT_FOLDER                   -> $OUTPUT_FOLDER"

readonly SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
readonly ROOT_FOLDER="$(git rev-parse --show-toplevel)"

# define golden images dependency components
readonly CDI_BASE_COMPONENT="cdi"
readonly CERT_MANAGER='cert-manager'
readonly CERT_MANAGER_NO_DASH='certmanager'
readonly INFLUX_DB="influxdb"
readonly KUBEVIRT_BASE_COMPONENT="kubevirt"
readonly MEMCACHED="memcached"
readonly MULTUS="multus"
readonly NGINX="nginx"
readonly NODEJS="nodejs"
readonly OPENMPI="openmpi"
readonly PHP="php"
readonly POSTGRES="postgres"
readonly PROMETHEUS="prometheus"
readonly PROMETHEUS_ADAPTER="prometheus-adapter"
readonly PROMETHEUS_ADAPTER_NO_DASH="prometheusadapter"
readonly PYTHON="python"
readonly PYTORCH="pytorch"
readonly RABBITMQSERVER="rabbitmq-server"
readonly RABBITMQSERVER_NO_DASH="rabbitmqserver"
readonly REDIS="redis"
readonly RUBY="ruby"
readonly RUST="rust"
readonly SRIOV_NETWORK_DEVICE_PLUGIN='sriov-network-device-plugin'
readonly SRIOV_NETWORK_DEVICE_PLUGIN_NO_DASH='sriovnetworkdeviceplugin'
readonly TELEGRAF="telegraf"
readonly TENSORFLOW="tensorflow"

# The RPMS of CDI have containerized-data-importer as its prefix whereas the
# containers must have cdi as its prefix. Hence, the BASE component
# is set to cdi. The folder prefix is same as kubevirt.
readonly CDI_FOLDER_PREFIX=$KUBEVIRT_BASE_COMPONENT
readonly KUBEVIRT_FOLDER_PREFIX=$KUBEVIRT_BASE_COMPONENT

echo "+++ create temp folder"
TEMPDIR=$ROOT_FOLDER/TEMPDIR_CONTAINER
mkdir -pv "$OUTPUT_FOLDER/SBOM_IMAGES"

function cleanup {
    echo "+++ remove $TEMPDIR"
    sudo rm -rf "$TEMPDIR"
}
trap cleanup EXIT

declare -A COMPONENT_VERSIONS
declare -A BUILDER_IMAGES

# these variables are used to create text files listing golden image names.
readonly file_name_prefix='PublishedContainers'
readonly file_ext='.txt'

# Validates the input such as base images exist and the Mariner RPMs tarball exists.
function input_validation {
    BASE_IMAGE_FILE=$(find "$BASE_IMAGE_FOLDER" -name "PublishedContainers-base.txt")
    if [[ ! -f $BASE_IMAGE_FILE ]]; then
        echo "Error - No base image file in $BASE_IMAGE_FOLDER"
        exit 1
    fi

    MARINER_RPMS_TARBALL=$(find "$MARINER_ARTIFACTS_FOLDER" -name "rpms.tar.gz" -maxdepth 1)
    if [[ ! -f $MARINER_RPMS_TARBALL ]]; then
        echo "Error - No Mariner RPMs tarball in $MARINER_ARTIFACTS_FOLDER"
        exit 1
    fi
}

# Reads base container names from the passed in text files
function read_base_container_name {
    baseImageName="none"

    while read image; do
        if [[ $baseImageName == "none" ]]; then
            baseImageName=$image
        fi
    done < "$BASE_IMAGE_FILE"

    echo "- Full base ACR image name: $baseImageName"
    base_container_acr=${baseImageName%%.*}
    base_container_name_with_core=${baseImageName%:*}
    base_container_name=${base_container_name_with_core%/*}
    base_container_tag=${baseImageName#*:}

    echo "Base ACR Name -> $base_container_acr"
    echo "Base ACR Container Name -> $base_container_name"
    echo "Base ACR Container Tag -> $base_container_tag"
}

# Builds, Tests, and Publishes Golden Container Image.
# The first argument is the main package name i.e., component name (e.g., nodejs, postgresql, etc)
# The second argument is the image name i.e., container type (e.g., nodejs, postgres, etc)
# The third argument is the base container name
# The fourth argument is the base container tag
# The fifth argument is the set of packages to be installed in the image.
# The sixth argument is the path to the corresponding dockerfile.
# The seventh argument is the runTest flag (0/1)
# The eighth argument is the passed in full containerName
function CreateGoldenContainer {
    local componentName=$1
    local containerType=$2
    local baseContainerName=$3
    local baseContainerTag=$4
    local packagesToInstall=$5
    local goldenImageDockerfile=$6
    local runTest=$7
    local originalContainerName=$8
    local containerTypeNoDash

    echo "------ Display Arguments ------"
    echo "Component Name:           -> $componentName"
    echo "Container Type:           -> $containerType"
    echo "Base Container Name:      -> $baseContainerName"
    echo "Base Container Tag:       -> $baseContainerTag"
    echo "Packages to Install:      -> $packagesToInstall"
    echo "Dockerfile:               -> $goldenImageDockerfile"
    echo "Test Container:           -> $runTest"
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
    cp "$CONTAINER_SRC_DIR/$containerTypeNoDash/$goldenImageDockerfile" "$containerBuildDir/Dockerfile"

    # Ensure that the path exists before copying files.
    if [ -d "$CONTAINER_SRC_DIR/$containerTypeNoDash/configuration-files" ]; then
        cp "$CONTAINER_SRC_DIR/$containerTypeNoDash/configuration-files"/* "$containerBuildDir"
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
    COMPONENT_VERSIONS[$containerType]=$componentVersion
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
    BUILDER_IMAGES[$componentName]=$containerName
    docker rmi -f "$originalContainerName"
    echo "Container Name:           -> $containerName"

    # Test image
    if [ $runTest -ne 0 ]; then
        test_golden_container "$containerTypeNoDash" "$containerName"
    fi

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

function DockerBuild {
    local containerName=$1
    local marinerVersion=$2
    local imageType=$3
    local packagesToInstall=$4
    local packagesToHoldback=$5
    local installNonrootUser=$6
    local user=root
    local userUid=0

    if $installNonrootUser; then
        user="nonroot"
        userUid=65532
    fi

    # Create container
    docker build . \
        -t "$containerName" \
        -f dockerfiles/dockerfile-new-image \
        --build-arg MARINER_VERSION="$marinerVersion" \
        --build-arg IMAGE_TYPE="$imageType" \
        --build-arg PACKAGES_TO_INSTALL="$packagesToInstall" \
        --build-arg PACKAGES_TO_HOLDBACK="$packagesToHoldback" \
        --build-arg USER="$user" \
        --build-arg USER_UID=$userUid \
        --no-cache \
        --progress=plain
}

# Builds, Tests, and Publishes Distroless Golden Container Image.
# The first argument is the main package name i.e., component name (e.g., nodejs, postgresql, etc).
# The second argument is the image name i.e., container type (e.g., nodejs, postgres, etc).
# The third argument is the base container tag.
# The fourth argument is the set of packages to be installed in the image.
# The fifth argument is the set of packages to holdback from getting installed.
# The sixth argument is component version.
# The seventh argument is the passed in full containerName.
# The eighth argument is builder image to use in distroless test.
# The ninth argument is the flag to indicate whether to run the test or not.
function CreateDistrolessGoldenContainers {
    local componentName=$1
    local containerType=$2
    local baseContainerTag=$3
    local packagesToInstall=$4
    local packagesToHoldback=$5
    local componentVersion=$6
    local containerName=$7
    local builderImage=$8
    local runTest=$9
    local containerTypeNoDash

    echo "------ Display Arguments ------"
    echo "Component Name:           -> $componentName"
    echo "Container Type:           -> $containerType"
    echo "Base Container Tag:       -> $baseContainerTag"
    echo "Packages to Install:      -> $packagesToInstall"
    echo "Packages to Holdback:     -> $packagesToHoldback"
    echo "Component Version:        -> $componentVersion"
    echo "Container Name:           -> $containerName"
    echo "Run Test:                 -> $runTest"

    echo "+++ create distroless container for $componentName"
    containerTypeNoDash=${containerType//-/}

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create container $containerName"

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
      echo "  -> Modified Container Name: $containerName"
    fi

    standardContainerName="$containerName:$componentVersion-cm$base_container_tag"
    debugContainerName="$containerName:$componentVersion-debug-cm$base_container_tag"
    nonrootContainerName="$containerName:$componentVersion-nonroot-cm$base_container_tag"
    debugNonrootContainerName="$containerName:$componentVersion-debug-nonroot-cm$base_container_tag"

    marinara="marinara"
    marinaraSrcDir="$TEMPDIR/$marinara-src"
    git clone "https://github.com/microsoft/$marinara.git" "$marinaraSrcDir"
    pushd "$marinaraSrcDir"

    # replace base container registry prefix by golden container registry prefix (if any)
    if [[ -n $baseRegistryPrefix ]]; then
        # add base container registry prefix to MARINARA
        MARINARA_IMAGE=$CONTAINER_REGISTRY_NAME_FULL/$baseRegistryPrefix/$marinara:$baseContainerTag
    else
        MARINARA_IMAGE=$CONTAINER_REGISTRY_NAME_FULL/$marinara:$baseContainerTag
    fi
    echo "MARINARA_IMAGE -> $MARINARA_IMAGE"

    # Get Mariner version from base container tag
    OLDIFS=$IFS
    IFS='.'
    read -ra tag_parts <<< "$baseContainerTag"
    IFS=$OLDIFS

    mariner_version="${tag_parts[0]}.0"

    # Update dockerfile-marinara to use the current base container
    sed -E "s|^FROM .*builder$|FROM $MARINARA_IMAGE as builder|g" -i "dockerfiles/dockerfile-new-image"

    # Create standard container
    DockerBuild "$standardContainerName" "$mariner_version" "custom" "$packagesToInstall" "$packagesToHoldback" false

    # Create debug container
    DockerBuild "$debugContainerName" "$mariner_version" "custom-debug" "$packagesToInstall" "$packagesToHoldback" false

    # Create nonroot container
    DockerBuild "$nonrootContainerName" "$mariner_version" "custom-nonroot" "$packagesToInstall" "$packagesToHoldback" true

    # Create debug nonroot container
    DockerBuild "$debugNonrootContainerName" "$mariner_version" "custom-debug-nonroot" "$packagesToInstall" "$packagesToHoldback" true

    popd > /dev/null

    echo "+++ remove $marinaraSrcDir"
    sudo rm -rf "$marinaraSrcDir"

    # Test image
    if [ $runTest -ne 0 ]; then
        test_distroless_container "$containerTypeNoDash-distroless" "$builderImage" "$standardContainerName"
        test_distroless_container "$containerTypeNoDash-distroless" "$builderImage" "$debugContainerName"
        test_distroless_container "$containerTypeNoDash-distroless" "$builderImage" "$nonrootContainerName"
        test_distroless_container "$containerTypeNoDash-distroless" "$builderImage" "$debugNonrootContainerName"
    fi

    # Publish containers
    publish_container "$standardContainerName"
    publish_container "$debugContainerName"
    publish_container "$nonrootContainerName"
    publish_container "$debugNonrootContainerName"

    # Save containers names
    {
        echo "$standardContainerName";
        echo "$debugContainerName";
        echo "$nonrootContainerName";
        echo "$debugNonrootContainerName";
    } >> "$TEMPDIR/$file_name_prefix-$containerTypeNoDash$file_ext"
    echo "----------------------------------------------------------------------"

    save_container_list
}

function getPkgsFromFile() {
    local folderName=$1
    local fileName=$2
    local -n array=$3
    while read -r pkg; do
        array+=("$pkg")
    done < "$CONTAINER_SRC_DIR/$folderName/$fileName"
}

# Creates memcached container
function create_memcached_container {
    local pkgsFileName="$MEMCACHED.pkg"
    local packagesToInstall=()
    getPkgsFromFile $MEMCACHED $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$MEMCACHED" \
        "$MEMCACHED" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Memcached" \
        1 \
        "$base_container_name/$MEMCACHED"
}

# Creates nginx container
function create_nginx_container {
    local pkgsFileName="$NGINX.pkg"
    local packagesToInstall=()
    getPkgsFromFile $NGINX $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$NGINX" \
        "$NGINX" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Nginx" \
        1 \
        "$base_container_name/$NGINX"
}

# Creates nodejs container
function create_nodejs_container {
    local nodejsPkgsFileName="$NODEJS.pkg"
    local packagesToInstall=()
    getPkgsFromFile $NODEJS $nodejsPkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$NODEJS" \
        "$NODEJS" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Nodejs" \
        1 \
        "$base_container_name/$NODEJS"

    local packagesToInstallInDistrolessNodejs=('distroless-packages-base' 'nodejs')
    local packagesInDistrolessNodejs="${packagesToInstallInDistrolessNodejs[*]}"

    local packagesToHoldbackInDistrolessNodejs=('bash' 'bzi' 'coreutils' 'gmp' 'grep' 'libselinux' 'pcre' 'pcre-libs')
    local holdbackInDistroless="${packagesToHoldbackInDistrolessNodejs[*]}"

    componentVersion=${COMPONENT_VERSIONS[$NODEJS]}
    builderImage=${BUILDER_IMAGES[$NODEJS]}
    CreateDistrolessGoldenContainers \
        "$NODEJS" \
        "$NODEJS" \
        "$base_container_tag" \
        "$packagesInDistrolessNodejs" \
        "$holdbackInDistroless" \
        "$componentVersion" \
        "$CONTAINER_REGISTRY_NAME_FULL/distroless/$NODEJS" \
        "$builderImage" \
        1

    local nodejs18PkgsFileName="${NODEJS}18.pkg"
    local packagesToInstall18=()
    getPkgsFromFile $NODEJS $nodejs18PkgsFileName packagesToInstall18
    local packages18="${packagesToInstall18[*]}"
    CreateGoldenContainer \
        "${NODEJS}18" \
        "$NODEJS" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages18" \
        "Dockerfile-Nodejs" \
        1 \
        "$base_container_name/$NODEJS"


    local packagesToInstallInDistrolessNodejs18=('distroless-packages-base' 'nodejs18')
    local packagesInDistrolessNodejs18="${packagesToInstallInDistrolessNodejs18[*]}"
    componentVersion=${COMPONENT_VERSIONS[$NODEJS]}
    builderImage=${BUILDER_IMAGES[${NODEJS}18]}
    CreateDistrolessGoldenContainers \
        "${NODEJS}18" \
        "$NODEJS" \
        "$base_container_tag" \
        "$packagesInDistrolessNodejs18" \
        "$holdbackInDistroless" \
        "$componentVersion" \
        "$CONTAINER_REGISTRY_NAME_FULL/distroless/$NODEJS" \
        "$builderImage" \
        1
}

# Creates php container
function create_php_container {
    local pkgsFileName="$PHP.pkg"
    local packagesToInstall=()
    getPkgsFromFile $PHP $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$PHP" \
        "$PHP" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-PHP" \
        1 \
        "$base_container_name/$PHP"
}

# Creates python container
function create_python_container {
    local pkgsFileName="$PYTHON.pkg"
    local packagesToInstall=()
    getPkgsFromFile $PYTHON $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$PYTHON" \
        "$PYTHON" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Python" \
        1 \
        "$base_container_name/$PYTHON"

    local packagesToInstallInDistroless=('distroless-packages-base' 'python3')
    local packagesInDistroless="${packagesToInstallInDistroless[*]}"

    local packagesToHoldbackInDistroless=('bash' 'grep' 'coreutils' 'gmp' 'libselinux' 'pcre' 'pcre-libs')
    local holdbackInDistroless="${packagesToHoldbackInDistroless[*]}"

    componentVersion=${COMPONENT_VERSIONS[$PYTHON]}
    builderImage=${BUILDER_IMAGES[$PYTHON]}
    CreateDistrolessGoldenContainers \
        "$PYTHON" \
        "$PYTHON" \
        "$base_container_tag" \
        "$packagesInDistroless" \
        "$holdbackInDistroless" \
        "$componentVersion" \
        "$CONTAINER_REGISTRY_NAME_FULL/distroless/$PYTHON" \
        "$builderImage" \
        0
}

# Creates pytorch container
function create_pytorch_container {
    local pkgsFileName="$PYTORCH.pkg"
    local packagesToInstall=()
    getPkgsFromFile $PYTORCH $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "${PYTHON}3-$PYTORCH" \
        "$PYTORCH" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Pytorch" \
        1 \
        "$base_container_name/$PYTORCH"
}

# Creates rabbitmq-server container
function create_rabbitmqserver_container {
    local pkgsFileName="$RABBITMQSERVER_NO_DASH.pkg"
    local packagesToInstall=()
    getPkgsFromFile $RABBITMQSERVER_NO_DASH $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$RABBITMQSERVER" \
        "$RABBITMQSERVER" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-rabbitmq-server" \
        0 \
        "$base_container_name/$RABBITMQSERVER"
}

# Creates ruby container
function create_ruby_container {
    # Packages already installed in base mariner -> readline, zlib, bzip2.
    # Replacement ruby runtime dependency:
    # musl -> glibc, kernel-headers, binutils; no musl rpm in PMC.
    local pkgsFileName="$RUBY.pkg"
    local packagesToInstall=()
    getPkgsFromFile $RUBY $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$RUBY" \
        "$RUBY" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Ruby" \
        1 \
        "$base_container_name/$RUBY"
}

# Creates rust container
function create_rust_container {
    local pkgsFileName="$RUST.pkg"
    local packagesToInstall=()
    getPkgsFromFile $RUST $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$RUST" \
        "$RUST" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Rust" \
        0 \
        "$base_container_name/$RUST"
}

# Creates postgres container
function create_postgres_container {
    local pkgsFileName="$POSTGRES.pkg"
    local packagesToInstall=()
    getPkgsFromFile $POSTGRES $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "${POSTGRES}ql" \
        "$POSTGRES" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Postgres" \
        1 \
        "$base_container_name/$POSTGRES"
}

# Creates InfluxDB container
function create_influxdb_container {
    local pkgsFileName="$INFLUX_DB.pkg"
    local packagesToInstall=()
    getPkgsFromFile $INFLUX_DB $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$INFLUX_DB" \
        "$INFLUX_DB" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Influxdb" \
        1 \
        "$base_container_name/$INFLUX_DB"
}

# Creates prometheus container
function create_prometheus_container {
    local pkgsFileName="$PROMETHEUS.pkg"
    local packagesToInstall=()
    getPkgsFromFile $PROMETHEUS $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$PROMETHEUS" \
        "$PROMETHEUS" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Prometheus" \
        1 \
        "$base_container_name/$PROMETHEUS"

    local packagesToInstallInDistroless=('distroless-packages-base' 'prometheus')
    local packagesInDistroless="${packagesToInstallInDistroless[*]}"

    # Potentially extraneous, can be investigated more.
    local packagesToHoldbackInDistroless=('bash' 'grep' 'coreutils' 'gmp' 'libselinux' 'pcre' 'pcre-libs')
    local holdbackInDistroless="${packagesToHoldbackInDistroless[*]}"

    componentVersion=${COMPONENT_VERSIONS["$PROMETHEUS"]}
    builderImage=${BUILDER_IMAGES[$PROMETHEUS]}
    CreateDistrolessGoldenContainers \
        "$PROMETHEUS" \
        "$PROMETHEUS" \
        "$base_container_tag" \
        "$packagesInDistroless" \
        "$holdbackInDistroless" \
        "$componentVersion" \
        "$CONTAINER_REGISTRY_NAME_FULL/distroless/$PROMETHEUS" \
        "$builderImage" \
        0
}

function create_redis_container {
    local pkgsFileName="$REDIS.pkg"
    local packagesToInstall=()
    getPkgsFromFile $REDIS $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$REDIS" \
        "$REDIS" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Redis" \
        1 \
        "$base_container_name/$REDIS"
}

# Creates prometheus-adapter container
function create_prometheus_adapter_container {
    local pkgsFileName="$PROMETHEUS_ADAPTER_NO_DASH.pkg"
    local packagesToInstall=()
    getPkgsFromFile $PROMETHEUS_ADAPTER_NO_DASH $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$PROMETHEUS_ADAPTER" \
        "$PROMETHEUS_ADAPTER" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Prometheus-Adapter" \
        0 \
        "$base_container_name/$PROMETHEUS_ADAPTER"

    local packagesToInstallInDistroless=('distroless-packages-base' 'prometheus-adapter')
    local packagesInDistroless="${packagesToInstallInDistroless[*]}"

    # Potentially extraneous, can be investigated more.
    local packagesToHoldbackInDistroless=('bash' 'grep' 'coreutils' 'gmp' 'libselinux' 'pcre' 'pcre-libs')
    local holdbackInDistroless="${packagesToHoldbackInDistroless[*]}"

    componentVersion=${COMPONENT_VERSIONS["$PROMETHEUS_ADAPTER"]}
    builderImage=${BUILDER_IMAGES[$PROMETHEUS_ADAPTER]}
    CreateDistrolessGoldenContainers \
        "$PROMETHEUS_ADAPTER" \
        "$PROMETHEUS_ADAPTER" \
        "$base_container_tag" \
        "$packagesInDistroless" \
        "$holdbackInDistroless" \
        "$componentVersion" \
        "$CONTAINER_REGISTRY_NAME_FULL/distroless/$PROMETHEUS_ADAPTER" \
        "$builderImage" \
        0
}

# Creates telegraf container
function create_telegraf_container {
    local pkgsFileName="$TELEGRAF.pkg"
    local packagesToInstall=()
    getPkgsFromFile $TELEGRAF $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$TELEGRAF" \
        "$TELEGRAF" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Telegraf" \
        1 \
        "$base_container_name/$TELEGRAF"
}

# Creates tensorflow container
function create_tensorflow_container {
    local pkgsFileName="$TENSORFLOW.pkg"
    local packagesToInstall=()
    getPkgsFromFile $TENSORFLOW $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "python3-${TENSORFLOW}" \
        "$TENSORFLOW" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Tensorflow" \
        1 \
        "$base_container_name/$TENSORFLOW"
}

# Creates openmpi container
function create_openmpi_container {
    local pkgsFileName="$OPENMPI.pkg"
    local packagesToInstall=()
    getPkgsFromFile $OPENMPI $pkgsFileName packagesToInstall
    local packages="${packagesToInstall[*]}"
    CreateGoldenContainer \
        "$OPENMPI" \
        "$OPENMPI" \
        "$base_container_name" \
        "$base_container_tag" \
        "$packages" \
        "Dockerfile-Openmpi" \
        1 \
        "$base_container_name/$OPENMPI"
}

# ---- Mariner HCI IMAGES ----

# Creates Cdi containers
function create_cdi_containers {
    source $CONTAINER_SRC_DIR/scripts/BuildCdiContainers.sh
    create_cdi_subcomp_containers
}

# Creates Cert-Manager containers
function create_cert_manager_containers {
    source $CONTAINER_SRC_DIR/scripts/BuildCertManagerContainers.sh
    create_cert_manager_subcomp_containers
}

# Create containers for each of the kubevirt sub components -
# virt-operator, virt-api, virt-handler, virt-launcher, virt-controller
function create_kubevirt_containers {
    source $CONTAINER_SRC_DIR/scripts/BuildKubevirtContainers.sh
    create_kubevirt_subcomp_containers
}

# Create Multus container
function create_multus_container_helper {
    source $CONTAINER_SRC_DIR/scripts/BuildMultusContainer.sh
    create_multus_container
}

# Create Sriov network device plugin container
function create_sriov_dp_containers {
    source $CONTAINER_SRC_DIR/scripts/BuildSriovDpContainer.sh
    create_sriov_dp_container
}

function start_building_containers {
    case $GOLDEN_CONTAINER_IMAGE in

    "$MEMCACHED")
        create_memcached_container
        ;;

    "$NGINX")
        create_nginx_container
        ;;

    "$NODEJS")
        create_nodejs_container
        ;;

    "$PHP")
        create_php_container
        ;;

    "$PYTHON")
        create_python_container
        ;;

    "$RABBITMQSERVER_NO_DASH")
        create_rabbitmqserver_container
        ;;

    "$REDIS")
        create_redis_container
        ;;

    "$RUBY")
        create_ruby_container
        ;;

    "$RUST")
        create_rust_container
        ;;

    "$POSTGRES")
        create_postgres_container
        ;;

    "$INFLUX_DB")
        create_influxdb_container
        ;;

    "$PROMETHEUS")
        create_prometheus_container
        ;;

    "$PROMETHEUS_ADAPTER_NO_DASH")
        create_prometheus_adapter_container
        ;;

    "$PYTORCH")
        create_pytorch_container
        ;;

    "$TELEGRAF")
        create_telegraf_container
        ;;

    "$TENSORFLOW")
        create_tensorflow_container
        ;;

    "$OPENMPI")
        create_openmpi_container
        ;;

    "$CDI_BASE_COMPONENT")
        create_cdi_containers
        ;;

    "$CERT_MANAGER_NO_DASH")
        create_cert_manager_containers
        ;;

    "$KUBEVIRT_BASE_COMPONENT")
        create_kubevirt_containers
        ;;

    "$MULTUS")
        create_multus_container_helper
        ;;

    "$SRIOV_NETWORK_DEVICE_PLUGIN_NO_DASH")
        create_sriov_dp_containers
        ;;
    esac
}

# source the CommonFunctions script to get the following functions:
# - azure_login
# - generate_container_sbom
# - SetDockerDefaultStorageLocation
# - ResetDockerDefaultStorageLocation
# - save_container_list
# - test_golden_container
# - publish_container
# - getRegistryPrefix
source $CONTAINER_SRC_DIR/scripts/CommonFunctions.sh

input_validation
read_base_container_name
azure_login "$base_container_acr"

# Create a variable to store the value of whether GOLDEN_CONTAINER_IMAGE is an HCI image
export IS_HCI_IMAGE=false
checkIfHciImage IS_HCI_IMAGE
echo "Is this an HCI Image: $IS_HCI_IMAGE"

start_building_containers
