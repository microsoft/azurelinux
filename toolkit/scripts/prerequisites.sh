#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

prereq_md_path=""
prereq_json_path=""

function print_help {
    echo "Build prereq utility. Lists or validates pre-requisites for a given distro."
    echo "Usage:"
    echo '[MANDATORY] -s PATH -> path to the src json file'
    echo '[MANDATORY] -d DISTRO -> One of "mariner", "azurelinux" or "ubuntu"'
    echo '[OPTIONAL] -m PATH -> path to the pre-requisite md file, must be provided if not in print mode'
    echo '[OPTIONAL]  -p -> print the canonical pre-requisite list and exit'
    echo '[OPTIONAL]  -h -> print this help dialogue and exit'
}

do_print=false
while getopts "hpm:s:d:" OPTIONS; do
    case ${OPTIONS} in
        m ) prereq_md_path=$OPTARG ;;
        s ) prereq_json_path=$OPTARG ;;
        d ) distro=$OPTARG ;;
        p ) do_print="true" ;;
        h ) print_help; exit 0 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n" >&2; print_help; exit 1 ;;
    esac
done

if [ -z "$prereq_json_path" ]; then
    echo "ERROR: Missing src json file path." >&2
    print_help
    exit 1
fi

if [ ! -f "$prereq_json_path" ]; then
    echo "ERROR: Src json file not found at $prereq_json_path." >&2
    exit 1
fi

if [ -z "$distro" ]; then
    echo "ERROR: Missing distro." >&2
    print_help
    exit 1
fi

if [ "$distro" != "mariner" ] && [ "$distro" != "azurelinux" ] && [ "$distro" != "ubuntu" ]; then
    echo "ERROR: Invalid distro. Must be one of 'azurelinux' or 'ubuntu'." >&2
    print_help
    exit 1
fi
if [ "$distro" == "mariner" ]; then
    distro="azurelinux"
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

if [ -z "$prereq_md_path" ]; then
    echo "ERROR: Missing pre-requisite file path." >&2
    print_help
    exit 1
fi

if [ ! -f "$prereq_md_path" ]; then
    echo "ERROR: Pre-requisite file not found at $prereq_md_path." >&2
    exit 1
fi

# Get the current entry in the .md file:
# 1) Remove all line continuations (backslash followed by newline) and replace with a space
current_prereqs="$(sed -e ':a' -e 'N' -e '$!ba' -e 's/\\\n/ /g' "$prereq_md_path")"

# 2) Remove all leading and trailing whitespace
current_prereqs=$(echo "$current_prereqs" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

# 3) Find the line that starts with "sudo <pkg manager> -y install ..."
if [[ "$distro" == "azurelinux" ]]; then
    current_prereqs=$(echo "$current_prereqs" | grep -oP 'sudo tdnf -y install \K.*')
elif [[ "$distro" == "ubuntu" ]]; then
    current_prereqs=$(echo "$current_prereqs" | grep -oP 'sudo apt -y install \K.*')
fi

# 4) Grab the package list from the line
current_prereqs=$(echo "$current_prereqs" | xargs)

# Compare the current and source pre-requisites. Enforce a 1:1 match including order for consistency.
if [ "$current_prereqs" != "$src_prereqs" ]; then
    echo "ERROR: Pre-requisites do not match. Please update the pre-requisite file."
    echo ""
    echo "Comparing: $prereq_json_path"
    echo "with:      $prereq_md_path"
    echo ""
    echo ".json file:   $src_prereqs"
    echo ".md file:     $current_prereqs"
    exit 1
else
    echo "Pre-requisites match."
    exit 0
fi
