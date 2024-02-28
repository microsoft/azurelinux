#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

# General example of how to use this script:
# ./generate_source_tarball.sh --podmanSrcTarball /path/to/podman-3.0.0.tar.gz --commonSrcTarball /path/to/common-3.0.0.tar.gz --podmanPkgVersion 3.0.0 --commonPkgVersion 3.0.0 --releaseNumber 1 --outFolder /path/to/output
# Concrete example:
# sudo ./generate_source_tarball.sh --podmanSrcTarball ./v3.3.1.tar.gz --commonSrcTarball ./v0.44.0.tar.gz --outFolder ./ --podmanPkgVersion 3.3.1 --commonPkgVersion 0.44.0 --releaseNumber 4

RELEASE_NUMBER="" # This is the release number that will be used in the output tarball name
PODMAN_PKG_VERSION_AND_RELEASE="" # This is the version-release string that will be used in the output tarball name
COMMON_PKG_VERSION_AND_RELEASE="" # This is the version-release string that will be used in the output tarball name
PODMAN_PKG_VERSION="" # This is the version string that will be used in the output tarball name
COMMON_PKG_VERSION="" # This is the version string that will be used in the output tarball name
PODMAN_SRC_TARBALL="" # This is the path to the podman src tarball
COMMON_SRC_TARBALL="" # This is the path to the common src tarball

#
# The following arrays are used to iterate over the parameters and variables in the script
# [IMPORTANT] all arrays below must share the same ordering for the package names
#
SRC_PKG_NAMES_LOWERCASE=("podman" "common") # Used for logging, creating the output tarball name, and for the folder name when unpacking the tarball
SRC_TARBALL_PARAMETERS=("podmanSrcTarball" "commonSrcTarball") # Used for error logging, must match the parameter name in the 'case' statement
PKG_VERSION_PARAMETERS=("podmanPkgVersion" "commonPkgVersion") # Used for error logging, must match the parameter name in the 'case' statement
SRC_TARBALLS_TO_VENDOR=("PODMAN_SRC_TARBALL" "COMMON_SRC_TARBALL") # Used to access the actual parameter value, must match the parameter name in the 'case' statement and the variable name above
PKG_VERSIONS=("PODMAN_PKG_VERSION" "COMMON_PKG_VERSION") # Used to access the actual parameter value, must match the parameter name in the 'case' statement and the variable name above
PKG_VERSIONS_TO_VENDOR=("PODMAN_PKG_VERSION_AND_RELEASE" "COMMON_PKG_VERSION_AND_RELEASE") # Used to access the actual variable value, and must match the variable name above
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --podmanSrcTarball  : Podman package's src tarball file
# --commonSrcTarball  : Common package's src tarball file
#                 these file contain the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --podmanPkgVersion  : package version and release number to allow for uploading of multiple releases for the same package version
# --commonPkgVersion  : package version and release number to allow for uploading of multiple releases for the same package version
# --outFolder         : folder where to copy the new tarball(s)

PARAMS=""
while (( "$#" )); do
    case "$1" in
        --podmanSrcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PODMAN_SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --commonSrcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            COMMON_SRC_TARBALL=$2
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
        --releaseNumber)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            RELEASE_NUMBER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --podmanPkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PODMAN_PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --commonPkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            COMMON_PKG_VERSION=$2
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

# Prep inputs


# Get normalized path to output folder
OUT_FOLDER=$(realpath $OUT_FOLDER)

# Verify release number is set
if [ -z "$RELEASE_NUMBER" ]; then
    echo "Error: --releaseNumber parameter cannot be empty"
    exit 1
fi

# Verify src tarballs and pkg versions are set
for i in "${!SRC_TARBALLS_TO_VENDOR[@]}"; do
    if [ -z "${!SRC_TARBALLS_TO_VENDOR[$i]}" ]; then
        echo "--${SRC_TARBALL_PARAMETERS[$i]} parameter cannot be empty"
        exit 1
    fi

    if [ -z "${!PKG_VERSIONS[$i]}" ]; then
        echo "--${PKG_VERSION_PARAMETERS[$i]} parameter cannot be empty"
        exit 1
    fi
done

# Set "version-release" strings
PODMAN_PKG_VERSION_AND_RELEASE="${PODMAN_PKG_VERSION}-${RELEASE_NUMBER}"
COMMON_PKG_VERSION_AND_RELEASE="${COMMON_PKG_VERSION}-${RELEASE_NUMBER}"

# Debug dump
echo " -- generate_source_tarball debug info -- "
echo "Arrays:"
echo "SRC_PKG_NAMES_LOWERCASE: ${SRC_PKG_NAMES_LOWERCASE[*]}"
echo "SRC_TARBALL_PARAMETERS: ${SRC_TARBALL_PARAMETERS[*]}"
echo "PKG_VERSION_PARAMETERS: ${PKG_VERSION_PARAMETERS[*]}"
echo "SRC_TARBALLS_TO_VENDOR: ${SRC_TARBALLS_TO_VENDOR[*]}"
echo "PKG_VERSIONS_TO_VENDOR: ${PKG_VERSIONS_TO_VENDOR[*]}"
echo "" # Echo new line when a section has multi-line output

echo " -- Captured parameters -- "
echo "--podmanSrcTarball   -> $PODMAN_SRC_TARBALL"
echo "--commonSrcTarball   -> $COMMON_SRC_TARBALL"
echo "--outFolder    -> $OUT_FOLDER"
echo "--releaseNumber   -> $RELEASE_NUMBER"
echo "--podmanPkgVersion   -> $PODMAN_PKG_VERSION"
echo "--commonPkgVersion   -> $COMMON_PKG_VERSION"
echo "" # Echo new line when a section has multi-line output

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT


# shellcheck disable=SC2091
for i in "${!SRC_TARBALLS_TO_VENDOR[@]}"; do
    # Get normalized path to each tarball
    declare "${SRC_TARBALLS_TO_VENDOR[$i]}=$(realpath ${!SRC_TARBALLS_TO_VENDOR[$i]})"
    echo "${SRC_TARBALLS_TO_VENDOR[$i]} -> ${!SRC_TARBALLS_TO_VENDOR[$i]}"

    VENDORED_TARBALL_DESTINATION="${OUT_FOLDER}/libcontainers-common-${SRC_PKG_NAMES_LOWERCASE[$i]}-${!PKG_VERSIONS_TO_VENDOR[$i]}.tar.gz"
    
    # Jump into tmpdir to begin unpacking and vendoring
    pushd $tmpdir > /dev/null

    echo "-- Unpacking ${SRC_TARBALLS_TO_VENDOR[$i]}"
    mkdir -p "${SRC_PKG_NAMES_LOWERCASE[$i]}"
    tar -C "${SRC_PKG_NAMES_LOWERCASE[$i]}" -xzf ${!SRC_TARBALLS_TO_VENDOR[$i]}
    cd "${SRC_PKG_NAMES_LOWERCASE[$i]}"
    cd * # assumes the tarball contains a single folder that contains the src code. Not perfect, but close enough and it's what we've done in other generate_source_tarball.sh scripts
    echo "-- Getting vendored modules"
    # Upgrading runc from v1.0.1 to v1.1.12 to avoid CVE-2024-21626
    go get github.com/opencontainers/runc@v1.1.12
    if [ $? -ne 0 ]; then
        echo "Error: go get failed"
        exit 1
    fi
    go mod tidy -go=1.15 # This should match the go version in the go.mod file of the tarball
    if [ $? -ne 0 ]; then
        echo "Error: go mod tidy failed"
        exit 1
    fi
    go mod vendor
    if [ $? -ne 0 ]; then
        echo "Error: go mod vendor failed"
        exit 1
    fi
    echo "-- Tar vendored modules"
    cd ..
    tar  --sort=name \
        --mtime="2021-04-26 00:00Z" \
        --owner=0 --group=0 --numeric-owner \
        --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
        -czf "$VENDORED_TARBALL_DESTINATION" *
    echo "${SRC_PKG_NAMES_LOWERCASE[$i]} tarball is available at $VENDORED_TARBALL_DESTINATION"
    popd > /dev/null
done