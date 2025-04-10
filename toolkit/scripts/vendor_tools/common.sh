#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

LOG_LEVELS=(
    [debug]=0
    [warn]=1
    [error]=2
)

function log () {
    local -r type=$1 msg=$2
    shift 2

    if [[ "${LOG_LEVELS[${level}]}" -gt "${LOG_LEVELS[${LOG_LEVEL}]}" ]]; then
        return
    fi

    local -r logtime="$(date --utc +'%FT%T.%NZ')"
    1>&2 echo -e "##[$type] ${logtime}\t${msg}\t"
}

function cleanup {
    local status_code=$?
    if [[ $status_code -ne 0 ]]; then
        log "${LOG_LEVEL:-error}" "Script failed with status code $status_code"
    else
        log "${LOG_LEVEL:-debug}" "Script completed successfully"
    fi

    log "${LOG_LEVEL:-debug}" "cleanup -> remove $TEMP_DIR"
    rm -rf $TEMP_DIR
}

function pushd_with_logging() {
    local dir=$1

    if [[ $dir == $(pwd) ]]
    then
        return
    fi

    log "${LOG_LEVEL:-debug}" "Going inside the folder $dir"
    pushd "$dir" &> /dev/null || {
        log "${LOG_LEVEL:-error}" "Failed to go inside the folder $dir"
        exit 1
    }

    CURRENT_PATH=$(pwd)
}

function common_setup(){
    local src_tarball=$1
    local pkg_version=$2
    local vendor_version=$3
    local suffix=$4
    local vendor_root_finder_file_name=$5

    TEMP_DIR=$(mktemp -d)

    pushd_with_logging "$TEMP_DIR"

    VENDOR_TARBALL=$(get_vendor_tarball_name "$src_tarball" "$pkg_version" "$vendor_version" "$suffix")

    src_tarball=$(download_tarball "$src_tarball" "$TEMP_DIR")

    unpack_tarball "$src_tarball" "$TEMP_DIR"

    # find the first folder in the current path as that is the source folder
    local tarball_folder
    tarball_folder=$(find "$CURRENT_PATH" -mindepth 1 -maxdepth 1 -type d | head -n 1)

    pushd_with_logging "$tarball_folder"

    VENDOR_ROOT_FOLDER=$(get_vendor_folder_location "$vendor_root_finder_file_name")

    pushd_with_logging "$VENDOR_ROOT_FOLDER"
}

function get_name_version() {
    local source_base_name=$1

    local name_ver_arr
    name_ver_arr=($(basename "$source_base_name" | sed -E 's/(.*)-(.*)\.tar\.[^.]+$/ \1 \2/'))

    echo "${name_ver_arr[0]}" "${name_ver_arr[1]}"
}

function get_vendor_tarball_name() {
    local source_base_name=$1
    local vendor_version=$2
    local pkg_version=$3
    local suffix=$4

    # get only name and version in format
    local name
    local version
    read -r name version < <(get_name_version "$source_base_name")

    local vendor_tarball_name
    vendor_tarball_name="$name-$pkg_version-$suffix-v$vendor_version.tar.gz"
    log "${LOG_LEVEL:-debug}" "Vendor tarball name is '$vendor_tarball_name'"

    echo "$vendor_tarball_name"
}

function get_vendor_folder_location(){
    local root_finder_file=$1
    local artifact_location

    if [[ -z "$root_finder_file" ]]; then
        pwd
        return 0
    fi

    log "${LOG_LEVEL:-debug}" "Finding root folder name in current path by looking for the file '$root_finder_file'"

    local artifact_location
    artifact_location=$(find "$(pwd)" -maxdepth 2 -name "$root_finder_file" -exec dirname {} \;)

    log "${LOG_LEVEL:-debug}" "Root folder name is '$artifact_location'"
    echo "$artifact_location"
}

function download_tarball() {
    local src_tarball=$1
    local download_to_folder=$2

    local tarball_name
    tarball_name=$(basename "$src_tarball")

    local download_location="$download_to_folder/$tarball_name"

    if [[ -f "$src_tarball" ]]
    then
        cp "$src_tarball" "$download_to_folder"
    else
        log "${LOG_LEVEL:-debug}" "Tarball '$tarball_name' doesn't exist. Will attempt to download from blobstorage."
        if ! wget -q "https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/$tarball_name" -O "$download_location"
        then
            log "${LOG_LEVEL:-error}" "ERROR: failed to download the source tarball."
            exit 1
        fi
        cp "$download_location" "$(dirname "$src_tarball")"
        log "${LOG_LEVEL:-debug}" "Download successful."
    fi

    echo "$download_location"
}

function unpack_tarball() {
    local src_tarball=$1
    local path_to_unpack=$2

    path_to_unpack=$(realpath "$path_to_unpack")

    log "${LOG_LEVEL:-debug}" "Unpacking source tarball $src_tarball"
    tar -xf "$src_tarball" -C "$path_to_unpack"
}

function create_vendor_tarball() {
    local vendor_tarball=$1
    local folder_to_tar=$2
    local out_folder=$3
    local exclude_parent_folder=$4

    if [[ ! -d "$out_folder" ]]; then
        log "${LOG_LEVEL:-error}" "Output folder $out_folder does not exist."
        exit 1
    fi

    local vendor_tarball_path
    vendor_tarball_path=$(realpath "$out_folder/$vendor_tarball")

    local folder_to_tar_name
    folder_to_tar_name=$(basename "$folder_to_tar")
    if [[ "$exclude_parent_folder" =~ [Tt]rue ]]; then
        log "${LOG_LEVEL:-debug}" "Excluding parent folder $folder_to_tar_name from tarball"
        folder_to_tar_name="."
    else
        folder_to_tar=$(dirname "$folder_to_tar")
    fi

    log "${LOG_LEVEL:-debug}" "Creating new tarball $vendor_tarball in $out_folder from folder $folder_to_tar"
    PIGZ=-n tar -Ipigz --sort=name \
        --mtime="2021-04-26 00:00Z" \
        --owner=0 --group=0 --numeric-owner \
        --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
        -cf "$vendor_tarball_path" -C "$folder_to_tar" "$folder_to_tar_name"

    if [[ -f "$vendor_tarball_path" ]]; then
        log "${LOG_LEVEL:-debug}" "Tarball created successfully (sha256sum) (tarball_name): \n $(sha256sum "$vendor_tarball_path")"
    else
        log "${LOG_LEVEL:-error}" "Failed to create tarball $vendor_tarball."
        exit 1
    fi
}

# COMMON PARAMETERS
PKG_VERSION=""
SRC_TARBALL=""
VENDOR_VERSION="1"
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameter handling
function handle_common_parameters() {
    log "${LOG_LEVEL:-debug}" "--srcTarball             -> $SRC_TARBALL"
    log "${LOG_LEVEL:-debug}" "--outFolder              -> $OUT_FOLDER"
    log "${LOG_LEVEL:-debug}" "--pkgVersion             -> $PKG_VERSION"
    log "${LOG_LEVEL:-debug}" "--vendorVersion          -> $VENDOR_VERSION"

    if [[ -z "$SRC_TARBALL" ]]; then
        log "${LOG_LEVEL:-error}" "--srcTarball parameter cannot be empty"
        exit 1
    fi

    if [[ -z "$PKG_VERSION" ]]; then
        log "${LOG_LEVEL:-error}" "--pkgVersion parameter cannot be empty"
        exit 1
    fi

    if [[ -z "$VENDOR_VERSION" ]]; then
        log "${LOG_LEVEL:-error}" "--vendorVersion parameter cannot be empty"
        exit 1
    fi

    if [[ ! -d "$OUT_FOLDER" ]]; then
        log "${LOG_LEVEL:-error}" "--outFolder does not exist"
        exit 1
    fi
}
