#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

SOURCE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SOURCE_PATH/common.sh"

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

trap cleanup EXIT

TARBALL_SUFFIX="cargovendor"
VENDOR_ROOT_FINDER_FILE_NAME="Cargo.toml"
VENDOR_FOLDER_NAME="vendor"

common_setup "$SRC_TARBALL" "$VENDOR_VERSION" "$PKG_VERSION" "$TARBALL_SUFFIX" "$VENDOR_ROOT_FINDER_FILE_NAME" "$OUT_FOLDER"

# fetch cargo crates
log "${LOG_LEVEL:-debug}" "Fetching cargo crates at $(pwd)"
cargo vendor > config.toml

VENDOR_FOLDER=$(find . -type d -name "$VENDOR_FOLDER_NAME")

create_vendor_tarball "$VENDOR_TARBALL" "$VENDOR_FOLDER" "$OUT_FOLDER"
