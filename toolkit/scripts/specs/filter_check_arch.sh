#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# This tool checks if the spec file is valid for the current arch (or the arch specified).
# It uses mariner_rpmspec to read the spec file and check if the current arch is in the list of
# exclusive arch and not in the list of excluded arch. If the spec file is valid, it returns 0,
# otherwise it returns 1. Target arch can be specified as an argument, otherwise it defaults to
# the current system arch.

set -e

help() {
    echo "Usage: $0 [--path='path to spec file'] [--arch='(optional) rpm target arch'] [--check-compat]"
    echo "  --path:           path to spec file to check"
    echo "  --arch:           (optional) rpm target arch to check against, defaults to system arch"
    echo "  --check-compat:   checks if the rpmspec tool is available and supports the --load argument"
    exit 0
}

# Find the path to rpmops.sh relative to this script
SCRIPT_PATH="$(realpath "$0")"
REPO_ROOT="$(realpath "$(dirname "$SCRIPT_PATH")/../../../")"
source "$REPO_ROOT/toolkit/scripts/rpmops.sh"

get_current_system_arch() {
    # Get the current system arch as understood by rpm (x86_64 and aarch64)
    rpm --eval "%{_arch}"
}

check_rpmspec_load_arg() {
    # check if rpmspec supports --load argument
    rpmspec --help | grep -qe "--load" || { echo "FILTER ERROR: rpmspec does not support --load argument"; return 1; }
    return 0
}

parsed_spec_read_tag() {
    local spec_path

    spec_path="$1"
    current_arch="$2"

    # Check if exclusive arch is ok
    exlusive_arch=$(mariner_rpmspec --query --queryformat="[%{EXCLUSIVEARCH} ]" --srpm "$spec_path" 2>/dev/null)
    # Check if the current arch is in the list of exclusive arch or if the list is empty
    if [[ ! "$exlusive_arch" == *"$current_arch"* ]] && [[ ! -z "$exlusive_arch" ]]; then
        echo "WRONG ARCH: The current arch $current_arch is not in the list of exclusive arch $exlusive_arch"
        return 1
    fi

    # Check if excluded arch is ok
    excluded_arch=$(mariner_rpmspec --query --queryformat="[%{EXCLUDEARCH} ]" --srpm "$spec_path" 2>/dev/null)
    # Check if the current arch is in the list of excluded arch
    if [[ "$excluded_arch" == *"$current_arch"* ]]; then
        echo "WRONG ARCH: The current arch $current_arch is in the list of excluded arch $excluded_arch"
        return 1
    fi
}

# Check if we have the right number of arguments
if [[ $# -lt 1 ]]; then
    echo "FILTER ERROR: Invalid number of arguments"
    help
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --path=*)
            spec_file_path="${1#*=}"
            shift
            ;;
        --arch=*)
            target_arch="${1#*=}"
            shift
            ;;
        --check-compat)
            check_rpmspec_load_arg && exit 0
            echo "FILTER ERROR: rpmspec does not support --load argument!"
            rpmspec --help
            exit 1
            ;;
        *)
            echo "FILTER ERROR: Invalid argument $1"
            help
            ;;
    esac
done

# Check if the spec file path is specified
if [[ -z "$spec_file_path" ]]; then
    echo "FILTER ERROR: Spec file path not specified"
    exit 1
fi
if [[ ! -f "$spec_file_path" ]]; then
    echo "FILTER ERROR: Spec file $spec_file_path does not exist"
    exit 1
fi

# Default arch to get_current_system_arch() if not specified
if [[ -z "$target_arch" ]]; then
    target_arch=$(get_current_system_arch)
fi
# Check if the arch override is valid (x86_64 or aarch64)
valid_arches="x86_64 aarch64 fobar"
if [[ ! " $valid_arches" == *"$target_arch"* ]]; then
    echo "FILTER ERROR: Invalid arch $target_arch"
    exit 1
fi

# Check if we have a good version of rpmspec
check_rpmspec_load_arg || exit 1

# Check if the spec file is a valid spec file
if parsed_spec_read_tag "$spec_file_path" "$target_arch"; then
    echo "SUCCESS: Spec file $spec_file_path is valid"
    exit 0
else
    echo "FAILURE: Spec file '$spec_file_path' is invalid for the specified arch '$target_arch'"
    exit 1
fi
