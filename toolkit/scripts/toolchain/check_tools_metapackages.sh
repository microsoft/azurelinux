#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
set -euox pipefail

function display_usage_help() {
    echo "Script to check that distro tools meta-packages match toolchain manifests"
    echo ""
    echo "Usage:"
    echo "    $(basename $0) [-a <arch>] [-m <manifest_dir>] [-s <specs_dir>] [-v]"
    echo ""
    echo "Options:"
    echo "    -a    architecture to run for (x86_64 or aarch64, defaults to x86_64)"
    echo "    -m    MANIFESTS_DIR"
    echo "    -s    SPECS_DIR"
    echo "    -v    enable verbose output"
}

# assign default values
SPECS_DIR=$(make --no-print-directory -s printvar-SPECS_DIR  2> /dev/null)
MANIFESTS_DIR=$(make --no-print-directory -s printvar-TOOLCHAIN_MANIFESTS_DIR  2> /dev/null)
ARCH=x86_64
PKGGEN_TOOL_SPEC=azurelinux-tools-packagebuild
VERBOSE=0

while getopts ":a:m:s:v" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARCH=$OPTARG ;;
    m ) MANIFESTS_DIR=$OPTARG ;;
    s ) SPECS_DIR=$OPTARG ;;
    v ) VERBOSE=1
        set -x ;;
    \? )
        echo "ERROR: Invalid Option: -$OPTARG" 1>&2
        echo "" >&2
        display_usage_help >&2
        exit 1
        ;;
    : )
        echo "ERROR: Invalid Option: -$OPTIONS requires an argument" 1>&2
        echo "" >&2
        display_usage_help >&2
        exit 1
        ;;
  esac
done

function expand_packages_from_spec() {
    spec_reqs=$(rpmspec -q $1 --requires)

    (
        dnf repoquery -y ${spec_reqs[@]} --latest-limit=1 --quiet --qf '%{name}';
        dnf repoquery -y ${spec_reqs[@]} --latest-limit=1 --quiet --recursive --resolve --requires --qf '%{name}'
    ) | sort | uniq | tr '\n' ' '
}

function get_packages_from_manifest() {
    sed -e 's/-[\.0-9]\+-[0-9]\+\(\.azl3\)\?\.\(x86_64\|aarch64\|noarch\)\.rpm\s*$//' $1 | sort | uniq | tr '\n' ' '
}

SPEC_PATH=${SPECS_DIR}/${PKGGEN_TOOL_SPEC}/${PKGGEN_TOOL_SPEC}.spec
MANIFEST_PATH="${MANIFESTS_DIR}/pkggen_core_${ARCH}.txt"

RAW_PKGS_FROM_MANIFEST=$(get_packages_from_manifest ${MANIFEST_PATH})
RAW_PKGS_FROM_SPEC=$(expand_packages_from_spec ${SPEC_PATH})

declare -A PKGS_FROM_MANIFEST
declare -A PKGS_FROM_SPEC

for p in ${RAW_PKGS_FROM_SPEC}; do
    PKGS_FROM_SPEC[$p]=1
done

for p in ${RAW_PKGS_FROM_MANIFEST}; do
    PKGS_FROM_MANIFEST[$p]=1
done

echo "Checking manifest vs. spec:"
echo "  $MANIFEST_PATH"
echo "  $SPEC_PATH"

declare -i errors=0
for p in ${!PKGS_FROM_MANIFEST[@]}; do
    if [ -z ${PKGS_FROM_SPEC[$p]:-} ]; then
        echo "ERROR: package in manifest missing from spec: $p" >&2
        errors+=1
    fi
done

declare -i extra_pkgs=0
for p in ${!PKGS_FROM_SPEC[@]}; do
    if [ -z ${PKGS_FROM_MANIFEST[$p]:-} ]; then
        extra_pkgs+=1
        if [[ $VERBOSE != 0 ]]; then
            echo "WARNING: package in spec (but not manifest): $p" >&2
        fi
    fi
done

if [[ ${errors} > 0 ]]; then
    echo "ERROR: missing packages were found" >&2
    exit $errors
fi

echo
echo "No missing packages found."

if [[ ${extra_pkgs} > 0 ]]; then
    echo "${extra_pkgs} extra package(s) found."
    if [[ $VERBOSE != 0 ]] then
        echo "Run with -v for more details."
    fi
fi
