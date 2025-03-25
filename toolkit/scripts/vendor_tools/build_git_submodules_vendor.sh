#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENDOR_VERSION="1"
GIT_URL=""

source "$OUT_FOLDER/common.sh"

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

log "${LOG_LEVEL:-debug}" "--srcTarball             -> $SRC_TARBALL"
log "${LOG_LEVEL:-debug}" "--outFolder              -> $OUT_FOLDER"
log "${LOG_LEVEL:-debug}" "--pkgVersion             -> $PKG_VERSION"
log "${LOG_LEVEL:-debug}" "--vendorVersion          -> $VENDOR_VERSION"
log "${LOG_LEVEL:-debug}" "--submoduleDirectoryName -> $SUBMODULE_DIRECTORY_NAME"
log "${LOG_LEVEL:-debug}" "--gitUrl                 -> $GIT_URL"

if [ -z "$SRC_TARBALL" ]; then
    log "${LOG_LEVEL:-error}" "--srcTarball parameter cannot be empty"
    exit 1
fi

if [ -z "$PKG_VERSION" ]; then
    log "${LOG_LEVEL:-error}" "--pkgVersion parameter cannot be empty"
    exit 1
fi

if [ -z "$VENDOR_VERSION" ]; then
    log "${LOG_LEVEL:-error}" "--vendorVersion parameter cannot be empty"
    exit 1
fi

if [ -z "$GIT_URL" ]; then
    log "${LOG_LEVEL:-error}" "--gitUrl parameter cannot be empty"
    exit 1
fi

trap cleanup EXIT
TARBALL_SUFFIX="submodules"
VENDOR_ROOT_FINDER_FILE_NAME=""
VENDOR_FOLDER_NAME=""
read -r PKG_NAME PKG_VERSION < <(get_name_version "$SRC_TARBALL")

function generate_vendor {
    local pkg_name=$1
    local pkg_version=$2
    local git_url=$3

    log "${LOG_LEVEL:-debug}" "Fetching git submodules for $pkg_name"

    # makesure we get the correct git url
    local git_origin_url
    git_origin_url=$(echo "$git_url" | grep -oP '^https://github\.com/[^/]+/[^/]+')

    local branch_name="$pkg_name-$pkg_version"
    local remote_name="origin"

    local current_dir
    current_dir=$(pwd)

    log "${LOG_LEVEL:-debug}" "using remote git url $git_origin_url"

    git init
    git remote add "$remote_name" "$git_origin_url"
    git fetch --tags --depth 1 "$remote_name"

    local checkout_name="tags/v$pkg_version"
    log "${LOG_LEVEL:-debug}" "checking out $checkout_name"
    git checkout "$checkout_name" -b "$branch_name" -f

    log "${LOG_LEVEL:-debug}" "fetching submodules with depth 1, recursive"
    git submodule update --depth 1 --init --recursive

    local submodules_list
    submodules_list=($(git config --file .gitmodules --get-regexp path | awk '{ print $2 }'))

    log "${LOG_LEVEL:-debug}" "removing .git folder from"
    find "$current_dir" -name ".git" | xargs rm -rf

    local another_temp_dir
    another_temp_dir=$(mktemp -d)

    log "${LOG_LEVEL:-debug}" "copying all submodules to $another_temp_dir"
    for submodule in "${submodules_list[@]}"; do
        log "${LOG_LEVEL:-debug}" "removing $submodule"
        cp -r "$submodule" "$another_temp_dir"
    done

    popd > /dev/null

    log "${LOG_LEVEL:-debug}" "deleting all files except submodules"
    rm -rf "${current_dir:?}/"*

    mv "$another_temp_dir"/* "$current_dir"
    rm -rf "$another_temp_dir"

    popd > /dev/null
}

common_setup "$SRC_TARBALL" "$VENDOR_VERSION" "$TARBALL_SUFFIX" "$VENDOR_ROOT_FINDER_FILE_NAME" "$OUT_FOLDER"

VENDOR_FOLDER_NAME=$(pwd)

generate_vendor "$PKG_NAME" "$PKG_VERSION" "$GIT_URL"

create_vendor_tarball "$VENDOR_TARBALL" "$VENDOR_FOLDER_NAME" "$OUT_FOLDER"




