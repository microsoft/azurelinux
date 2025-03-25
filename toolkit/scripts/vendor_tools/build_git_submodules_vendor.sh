#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

SOURCE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SOURCE_PATH/common.sh"
GIT_URL=""

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
# --vendorVersion : vendor version

PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --vendorVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            VENDOR_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --gitUrl)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            GIT_URL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

handle_common_parameters

# custom parameters
log "${LOG_LEVEL:-debug}" "--gitUrl                 -> $GIT_URL"

if [ -z "$GIT_URL" ]; then
    log "${LOG_LEVEL:-error}" "--gitUrl parameter cannot be empty"
    exit 1
fi

trap cleanup EXIT
TARBALL_SUFFIX="submodules"
VENDOR_ROOT_FINDER_FILE_NAME=""
read -r PKG_NAME PKG_VERSION < <(get_name_version "$SRC_TARBALL")

function generate_vendor {
    local pkg_name=$1
    local pkg_version=$2
    local git_url=$3

    log "${LOG_LEVEL:-debug}" "Fetching git submodules for package named: $pkg_name version: $pkg_version"

    # makesure we get the correct git url
    local git_origin_url
    git_origin_url=$(echo "$git_url" | grep -oP '^https://github\.com/[^/]+/[^/]+')

    local branch_name="$pkg_name-$pkg_version"
    local remote_name="origin"

    local current_dir
    current_dir=$(pwd)

    log "${LOG_LEVEL:-debug}" "Reinitilizing repo from source, using remote git url $git_origin_url"

    git init
    git remote add "$remote_name" "$git_origin_url"

    local checkout_name="tags/v$pkg_version"
    log "${LOG_LEVEL:-debug}" "fetching all tags depth 1 and checking out $checkout_name"
    git fetch --tags --depth 1 "$remote_name"
    git checkout "$checkout_name" -b "$branch_name" -f

    log "${LOG_LEVEL:-debug}" "fetching submodules with depth 1, recursive"
    git submodule update --depth 1 --init --recursive

    local submodules_list
    submodules_list=($(git config --file .gitmodules --get-regexp path | awk '{ print $2 }'))

    # remove all submodules from the current directory as it creates different sha256sum every time
    log "${LOG_LEVEL:-debug}" "removing .git folders from $current_dir"
    find "$current_dir" -name ".git" | xargs rm -rf

    local another_temp_dir
    another_temp_dir=$(mktemp -d)

    log "${LOG_LEVEL:-debug}" "copying all submodules to $another_temp_dir"
    for submodule in "${submodules_list[@]}"; do
        cp -r "$submodule" "$another_temp_dir"
    done

    popd > /dev/null

    log "${LOG_LEVEL:-debug}" "deleting all files except submodules"
    rm -rf "${current_dir:?}/"*

    mv "$another_temp_dir"/* "$current_dir"
    rm -rf "$another_temp_dir"
}

common_setup "$SRC_TARBALL" "$VENDOR_VERSION" "$PKG_VERSION" "$TARBALL_SUFFIX" "$VENDOR_ROOT_FINDER_FILE_NAME" "$OUT_FOLDER"

generate_vendor "$PKG_NAME" "$PKG_VERSION" "$GIT_URL"

create_vendor_tarball "$VENDOR_TARBALL" "$VENDOR_ROOT_FOLDER" "$OUT_FOLDER"
