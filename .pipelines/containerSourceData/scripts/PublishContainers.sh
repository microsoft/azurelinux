#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# This script is used to publish the multi-arch tags for the container images.
# Note that this script assumes that 'az login' has already been done.

# parse script parameters:
# -c -> Container source directory (e.g. ~/workspace/CBL-Mariner/.pipelines/containerSourceData)
# -d -> Directory containing the containers list
# -e -> Containers file name prefix
# -f -> Containers file name suffix
# -g -> GitHub branch
# -p -> Publishing level
# -o -> Output folder
while getopts ":c:d:e:f:g:p:o:" OPTIONS; do
    case ${OPTIONS} in
    c ) CONTAINER_SRC_DIR=$OPTARG;;
    d ) PUBLISHED_CONTAINERS_DIR=$OPTARG;;
    e ) PUBLISHED_CONTAINER_FILE_PREFIX=$OPTARG;;
    f ) PUBLISHED_CONTAINER_FILE_SUFFIX=$OPTARG;;
    g ) GITHUB_BRANCH=$OPTARG;;
    p ) PUBLISHING_LEVEL=$OPTARG;;
    o ) OUTPUT_FOLDER=$OPTARG;;

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

FILE_SEARCH_PATTERN="$PUBLISHED_CONTAINER_FILE_PREFIX*$PUBLISHED_CONTAINER_FILE_SUFFIX"
echo "CONTAINER_SRC_DIR     -> $CONTAINER_SRC_DIR"
echo "FILE_SEARCH_PATTERN   -> $FILE_SEARCH_PATTERN"
echo "GITHUB_BRANCH         -> $GITHUB_BRANCH"
echo "PUBLISHING_LEVEL      -> $PUBLISHING_LEVEL"
echo "OUTPUT_FOLDER         -> $OUTPUT_FOLDER"

PUBLISHED_CONTAINER_FILES=$(find "$PUBLISHED_CONTAINERS_DIR" -name "$FILE_SEARCH_PATTERN")
if [[ -z $PUBLISHED_CONTAINER_FILES ]]; then
    echo "Error - No published container lists in $PUBLISHED_CONTAINERS_DIR"
    exit 1
fi

function cleanup {
    echo "+++ logout from Azure Container Registry"
    docker logout
    docker system prune -f
}
trap cleanup EXIT

CONTAINER_TAGS_DIR="$OUTPUT_FOLDER/CONTAINER_TAGS_FOLDER"
mkdir -p "$CONTAINER_TAGS_DIR"
FILE_NAME_PREFIX='PublishedTags'
FILE_EXT='.txt'

# For Azure Linux 2.0, we have shipped the container images with
# the below value in the os-version field in the image manifest.
# TODO: We may need to update this value for Azure Linux 3.0.
OS_VERSION_PREFIX="cbl-mariner-"
DISTRO_IDENTIFIER="cm"

function create_multi_arch_tags {
    # $1: original container (without '-amd64' or '-arm64' extension in tag)
    # $2: multi-arch name
    # $3: multi-arch tag
    # $4: azure linux version
    # $5: architecture to build
    local original_container=$1
    local multiarch_name=$2
    local multiarch_tag=$3
    local azure_linux_version=$4
    local architecture_build=$5

    echo "-------------------------------------------------------"
    echo "original_container    -> $original_container"
    echo "multiarch_name        -> $multiarch_name"
    echo "multiarch_tag         -> $multiarch_tag"
    echo "azure_linux_version   -> $azure_linux_version"
    echo "-------------------------------------------------------"

    full_multiarch_tag="$multiarch_name:$multiarch_tag"

    # First check if the already published tag is on the next Azure Linux version.
    # If it is on the next version, then do not overwrite it.
    set +e
    manifest_json=$(docker manifest inspect "$full_multiarch_tag")
    set -e

    if [[ -n $manifest_json ]]; then
        echo "docker manifest found for container $full_multiarch_tag"

        # Parse the manifest json and look for the azure linux version in the key "os.version".
        # Loop through the .manifests array and look for the os.version key.
        # If the os.version key is found, then look for the version in its value starting with $OS_VERSION_PREFIX.
        published_tag_os_version_key="null"
        manifests=$(echo "$manifest_json" | jq .manifests)
        manifest_array=$(echo "$manifests" | jq -c '.[]' | jq -r '.platform | with_entries(select(.key | contains("os.version")))' | jq -c '.[]')
        for key in ${manifest_array[*]}; do
            if [[ $key == *"$OS_VERSION_PREFIX"* ]]; then
                # Remove the quotes from the value.
                key=$(echo "$key" | tr -d \")
                published_tag_os_version_key=$key
                break
            fi
        done

        echo "published_tag_os_version_key  -> $published_tag_os_version_key"

        if [[ $published_tag_os_version_key == "null" ]]; then
            echo "OS Version key not found in the manifest file."
        else
            # OS version found. Look for the version in its value starting with $OS_VERSION_PREFIX.
            published_tag_os_version=$(echo "$published_tag_os_version_key" | tr -d \" | tr -d $OS_VERSION_PREFIX)

            echo "published_tag_os_version      -> $published_tag_os_version"

            # Check if the published tag has a greater Azure Linux version than the current tag's Azure Linux version.
            # 1.0 > 2.0 => 0 (false)
            # 2.0 > 1.0 => 1 (true)
            # 2.0 > 2.0 => 0 (false)
            is_published_tag_os_version_strictly_greater=$(echo "$published_tag_os_version>$azure_linux_version" | bc)

            # If the published tag is on the next Azure Linux version, then do not proceed.
            if [ "$is_published_tag_os_version_strictly_greater" -eq 1 ]; then
                echo "Published tag is already on the next Azure Linux version i.e., $published_tag_os_version."
                echo "Do not overwrite it with $azure_linux_version."
                return
            fi

            echo "Published tag is on Azure Linux version $published_tag_os_version."
            echo "Proceed with overwriting it with Azure Linux version $azure_linux_version."
            echo "+++ update $full_multiarch_tag tag"
        fi
    else
        echo "Manifest does not exist. Proceed with creating new tag."
        echo "+++ create $full_multiarch_tag tag"
    fi

    # create, annotate, and push manifest
    docker manifest create "$full_multiarch_tag" --amend "$original_container-amd64"
    docker manifest annotate "$full_multiarch_tag" "$original_container-amd64" \
        --os-version "$OS_VERSION_PREFIX$azure_linux_version"

    if [[ $architecture_build == *"ARM64"*  ]]; then
        docker manifest create "$full_multiarch_tag" --amend "$original_container-arm64"
        docker manifest annotate "$full_multiarch_tag" "$original_container-arm64" \
             --os-version "$OS_VERSION_PREFIX$azure_linux_version" \
             --variant "v8"
    fi

    echo "+++ push $full_multiarch_tag tag"
    docker manifest push "$full_multiarch_tag"
    echo "+++ $full_multiarch_tag tag pushed successfully"

    # Save the multi-arch tag to a file.
    image_basename=${multiarch_name#*/}
    dash_removed_name=${image_basename//-/}
    final_name=${dash_removed_name////_}
    echo "$full_multiarch_tag" >> "$CONTAINER_TAGS_DIR/$FILE_NAME_PREFIX-$final_name$FILE_EXT"
}

for PUBLISHED_CONTAINER_FILE in $PUBLISHED_CONTAINER_FILES
do
    file_basename=$(basename "$PUBLISHED_CONTAINER_FILE")
    container_type=$(echo "$file_basename" | sed -e "s/$PUBLISHED_CONTAINER_FILE_PREFIX-//" -e "s/$PUBLISHED_CONTAINER_FILE_SUFFIX//")

    # Rename core images to base to get the ACR Repo details.
    if [[ "$container_type" =~ ^(distroless|busybox|marinara)$ ]]; then
      container_type="base"
    fi
    echo "Container Type        -> $container_type"

    TEMP_FILE=$(mktemp)

    python3 "$CONTAINER_SRC_DIR"/scripts/acrRepoParser.py \
        --config-file-path "$CONTAINER_SRC_DIR"/configuration/acrRepoV2.json \
        --image-name "$container_type" \
        --git-branch "$GITHUB_BRANCH" \
        --publishing-level "$PUBLISHING_LEVEL" \
        --output-file-path "$TEMP_FILE"

    IS_CORE_IMAGE=$(jq -r '.data_is_core_image' "$TEMP_FILE")
    IS_GOLDEN_IMAGE=$(jq -r '.data_is_golden_image' "$TEMP_FILE")
    IS_HCI_GOLDEN_IMAGE=$(jq -r '.data_is_hci_golden_image' "$TEMP_FILE")
    ARCHITECTURE_TO_BUILD=$(jq -r '.data_architecture_to_build' "$TEMP_FILE")
    TARGET_ACR=$(jq -r '.data_target_acr' "$TEMP_FILE")

    if [[ -z $TARGET_ACR ]]; then
        echo "##vso[task.logissue type=warning]Target ACR not found for image $container_type"
        continue
    fi

    # Remove the temp file.
    [ -f "$TEMP_FILE" ] && rm "$TEMP_FILE"

    echo "Container Type        -> $container_type"
    echo "IS_CORE_IMAGE         -> $IS_CORE_IMAGE"
    echo "IS_GOLDEN_IMAGE       -> $IS_GOLDEN_IMAGE"
    echo "IS_HCI_GOLDEN_IMAGE   -> $IS_HCI_GOLDEN_IMAGE"
    echo "ARCHITECTURE_TO_BUILD -> $ARCHITECTURE_TO_BUILD"
    echo "TARGET_ACR            -> $TARGET_ACR"

    while IFS= read -r image_name
    do
        echo
        echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        echo "Image name: $image_name"
        echo
        container_registry="${image_name%%.*}"
        echo "+++ login into Azure ACR $container_registry"
        az acr login --name "$container_registry"

        amd64_image=${image_name%-*}-amd64
        docker pull "$amd64_image"

        # Some container images are only built for AMD64 architecture.
        if [[ $ARCHITECTURE_TO_BUILD == *"ARM64"*  ]]; then
            arm64_image=${image_name%-*}-arm64
            docker pull "$arm64_image"
        fi

        if [[ $container_registry != "$TARGET_ACR" ]]; then
            echo "+++ login into Azure ACR $TARGET_ACR"
            az acr login --name "$TARGET_ACR"

            echo "Retagging the images to $TARGET_ACR"
            # E.g., If container_registry is azurelinuxdevpreview and TARGET_ACR is azurelinuxpreview, then
            # azurelinuxdevpreview.azurecr.io/base/core:2.0 -> azurelinuxpreview.azurecr.io/base/core:2.0

            amd64_retagged_image_name=${amd64_image/"$container_registry"/"$TARGET_ACR"}
            echo "Retagged amd64 image: $amd64_retagged_image_name"
            docker image tag "$amd64_image" "$amd64_retagged_image_name"
            docker rmi "$amd64_image"
            docker image push "$amd64_retagged_image_name"

            if [[ $ARCHITECTURE_TO_BUILD == *"ARM64"*  ]]; then
                arm64_retagged_image_name=${arm64_image/"$container_registry"/"$TARGET_ACR"}
                echo "Retagged arm64 image: $arm64_retagged_image_name"
                docker image tag "$arm64_image" "$arm64_retagged_image_name"
                docker rmi "$arm64_image"
                docker image push "$arm64_retagged_image_name"
            fi

            image_name=$amd64_retagged_image_name
        fi

        # image_name has the following format [registry name].azurecr.io/[name]:tag-[amd64 or arm64]
        # e.g.: azurelinuxpreview.azurecr.io/base/core:1.0.20210628-amd64
        # container name is [registry name].azurecr.io/[name]
        # container tag is tag (without -[amd64 or arm64])
        image_name_with_noarch=${image_name%-*}
        container_name=${image_name_with_noarch%:*}
        container_tag=${image_name_with_noarch#*:}

        echo "Image Name:               ------------------>" "$image_name"
        echo "Image Name w/o Arch:      ------------------>" "$image_name_with_noarch"
        echo "Container Name:           ------------------>" "$container_name"
        echo "Container Tag:            ------------------>" "$container_tag"

        if "$IS_CORE_IMAGE"; then
            # For core images, we need to create multi-arch tags for
            # the major version and the full version.
            echo "Create multi-arch tags for core image: $container_type"
            OLDIFS=$IFS
            IFS='.'
            read -ra tag_parts <<< "$container_tag"
            IFS=$OLDIFS

            major_version="${tag_parts[0]}.${tag_parts[1]}"
            azure_linux_version="${tag_parts[0]}.0"

            # create multi-arch tag full version (e.g.: 2.0.20210127)
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$container_tag" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            # create major version tag (e.g.: 2.0)
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$major_version" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"
        elif "$IS_GOLDEN_IMAGE"; then
            # For golden images, we need to create multi-arch tags for
            # the major version, the major and minor version, and the full version.
            echo "Create multi-arch tags for golden image: $container_type"
            package_version=${container_tag%-*}                      # 16.14.0
            package_version_major=${package_version%%.*}             # 16
            package_version_major_minor=${package_version%.*}        # 16.14

            if [[ $package_version == *"-debug-nonroot" ]]; then
                package_version_major=$package_version_major"-debug-nonroot"
                package_version_major_minor=$package_version_major_minor"-debug-nonroot"
            elif [[ $package_version == *"-nonroot" ]]; then
                package_version_major=$package_version_major"-nonroot"
                package_version_major_minor=$package_version_major_minor"-nonroot"
            elif [[ $package_version == *"-debug" ]]; then
                package_version_major=$package_version_major"-debug"
                package_version_major_minor=$package_version_major_minor"-debug"
            fi

            echo "Package Version:          ------------------>" "$package_version"
            echo "Package Version Major:    ------------------>" "$package_version_major"
            echo "Package Version Minor:    ------------------>" "$package_version_major_minor"

            if $IS_HCI_GOLDEN_IMAGE; then
                azure_linux_version=$(awk -F '-' '{print $2}' <<< "$container_tag")                 # 0.59.0-2.2.0.20230607     -> 2.2.0.20230607
                azure_linux_version=$(awk -F '.' '{print $2"."$3}' <<< "$azure_linux_version")      # [2].[2].[0].[20230607]    -> 2.0
                #                                                                                          ^   ^
            else
                azure_linux_version=$(awk -F $DISTRO_IDENTIFIER '{print $2}' <<< "$container_tag")  # 16.19.1-2-cm2.0.20230607  -> 2.0.20230607
                azure_linux_version=$(awk -F '.' '{print $1"."$2}' <<< "$azure_linux_version")      # [2].[0].[20230607]        -> 2.0
                #                                                                                      ^   ^
            fi

            # create multi-arch tag full version
            # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16.14.0-1-cm2.0.20220412
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$container_tag" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            # create multi-arch tag with major version
            # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$package_version_major" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            # create multi-arch tag with major version and azure linux version
            # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16-cm2.0
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$package_version_major-$DISTRO_IDENTIFIER$azure_linux_version" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            # create multi-arch tag with major and minor version
            # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16.14
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$package_version_major_minor" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            # create multi-arch tag with major and minor version and azure linux version
            # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16.14-cm2.0
            create_multi_arch_tags \
                "$image_name_with_noarch" \
                "$container_name" \
                "$package_version_major_minor-$DISTRO_IDENTIFIER$azure_linux_version" \
                "$azure_linux_version" \
                "$ARCHITECTURE_TO_BUILD"

            if $IS_HCI_GOLDEN_IMAGE; then
                # create multi-arch tag with major, minor, and patch version
                # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16.14
                create_multi_arch_tags \
                    "$image_name_with_noarch" \
                    "$container_name" \
                    "$package_version" \
                    "$azure_linux_version" \
                    "$ARCHITECTURE_TO_BUILD"

                # create multi-arch tag with major, minor, and patch version and azure linux version
                # e.g. azurelinuxpreview.azurecr.io/base/nodejs:16.14-cm2.0
                create_multi_arch_tags \
                    "$image_name_with_noarch" \
                    "$container_name" \
                    "$package_version-$DISTRO_IDENTIFIER$azure_linux_version" \
                    "$azure_linux_version" \
                    "$ARCHITECTURE_TO_BUILD"
            fi
        fi
    done < "$PUBLISHED_CONTAINER_FILE"
done
