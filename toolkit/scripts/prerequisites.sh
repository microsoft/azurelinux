#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

prereq_json_path=""

function print_help {
    echo "Build prereq utility. Lists or installs pre-requisites for a given distro."
    echo "Usage:"
    echo '[MANDATORY] -s PATH -> path to the src json file'
    echo '[MANDATORY] -d DISTRO -> One of "mariner", "azurelinux" or "ubuntu"'
    echo '[OPTIONAL]  -p -> print the canonical pre-requisite list and exit'
    echo '[OPTIONAL]  -a -> auto install the pre-requisites'
    echo '[OPTIONAL]  -h -> print this help dialogue and exit'
}

do_print=false
do_auto_install=false
while getopts "hpas:d:" OPTIONS; do
    case ${OPTIONS} in
        s ) prereq_json_path=$OPTARG ;;
        d ) distro=$OPTARG ;;
        p ) do_print="true" ;;
        a ) do_auto_install="true" ;;
        h ) print_help; exit 0 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n" >&2; print_help; exit 1 ;;
    esac
done

# Need to pick at least one of print or auto install
if ! "$do_print" && ! "$do_auto_install"; then
    echo "ERROR: Must pick at least one of print or auto install." >&2
    print_help
    exit 1
fi

if [[ -z "$prereq_json_path" ]]; then
    echo "ERROR: Missing src json file path." >&2
    print_help
    exit 1
fi

if [[ ! -f "$prereq_json_path" ]]; then
    echo "ERROR: Src json file not found at $prereq_json_path." >&2
    exit 1
fi

if [[ -z "$distro" ]]; then
    echo "ERROR: Missing distro." >&2
    print_help
    exit 1
fi

if [[ "$distro" != "mariner" ]] && [[ "$distro" != "azurelinux" ]] && [[ "$distro" != "ubuntu" ]]; then
    echo "ERROR: Invalid distro. Must be one of 'azurelinux' or 'ubuntu'." >&2
    print_help
    exit 1
fi
if [[ "$distro" == "mariner" ]]; then
    distro="azurelinux"
fi

# If we are in auto install mode, jq must be installed before we can proceed. If we are in print mode, jq is required
# but we will not install it.
have_jq=$(command -v jq) || true
if [[ -z "$have_jq" ]]; then
    if "$do_auto_install"; then
        if [[ "$distro" = "azurelinux" ]]; then
            tdnf install -y jq
        elif [[ "$distro" = "ubuntu" ]]; then
            apt-get update
            apt-get install -y jq
        fi
    else
        echo "ERROR: jq is required for this script to run. Please install jq and try again." >&2
        exit 1
    fi
fi

# Load the pre-requisite source json for the distro of interest
# Json is of the form:
# {
#   "packages": [
#       {
#           "name": "pkg",
#           "azurelinux": "pkg-b",
#           "ubuntu": "pkg-a"
#       },
#       ...
#   ]
#}
# A distro specific entry may not exist for every package, so get the entries that do exist, and
# select the distro specific value. Convert the result to a space separated string.
src_prereqs=$(jq -r --arg distro "$distro" '[.packages[] | select(has($distro)) | .[$distro]] | sort | join(" ")' "$prereq_json_path")

# For print mode, just print the pre-requisites and exit early.
if "$do_print"; then
    echo "$src_prereqs"
    exit 0
fi

# For auto install mode, install the pre-requisites.
if "$do_auto_install"; then
    read -ra install_list <<< "$src_prereqs"
    if [ "$distro" == "azurelinux" ]; then
        tdnf install -y "${install_list[@]}"
    elif [ "$distro" == "ubuntu" ]; then
        apt-get update
        apt-get install -y "${install_list[@]}"
    fi
fi
