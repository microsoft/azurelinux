#!/bin/bash -e
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

prereq_md_path=""
prereq_json_path=""

function help {
    echo "Pre-requisite installer. Installs azurelinux pre-requisites for the toolkit."
    echo "Usage:"
    echo '[MANDATORY] -m PATH -> path to the pre-requisite md file'
    echo '[MANDATORY] -s PATH -> path to the src json file'
    echo '[MANDATORY] -d DISTRO -> One of "azurelinux" or "ubuntu"'
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
        h ) help; exit 0 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n" >&2; help; exit 1 ;;
    esac
done

if [ -z "$prereq_json_path" ]; then
    echo "ERROR: Missing src json file path." >&2
    help
    exit 1
fi

if [ ! -f "$prereq_json_path" ]; then
    echo "ERROR: Src json file not found at $prereq_json_path." >&2
    exit 1
fi

if [ -z "$distro" ]; then
    echo "ERROR: Missing distro." >&2
    help
    exit 1
fi

if [ "$distro" != "azurelinux" ] && [ "$distro" != "ubuntu" ]; then
    echo "ERROR: Invalid distro. Must be one of 'azurelinux' or 'ubuntu'." >&2
    help
    exit 1
fi

# For print mode, just print the pre-requisites and exit early.
# A distro specific entry may not exist for every package, so get the entries that do exist, and
# select the distro specific value. Convert the result to a space separated string.
src_prereqs=$(jq -r --arg distro "$distro" '[.[] | select(has($distro)) | .[$distro]] | sort | join(" ")' "$prereq_json_path")
if "$do_print"; then
    echo "$src_prereqs"
    exit 0
fi

if [ -z "$prereq_md_path" ]; then
    echo "ERROR: Missing pre-requisite file path." >&2
    help
    exit 1
fi

if [ ! -f "$prereq_md_path" ]; then
    echo "ERROR: Pre-requisite file not found at $prereq_md_path." >&2
    exit 1
fi

# Load the pre-requisite source json for the distro of interest
# Json is of the form:
# [
#     {
#         "name": "pkg",
#         "azurelinux": "pkg-b",
#         "ubuntu": "pkg-a"
#     },
#     ...
#]


current_prereqs="$(sed -e ':a' -e 'N' -e '$!ba' -e 's/\\\n/ /g' "$prereq_md_path")"
if [[ "$distro" == "azurelinux" ]]; then
    # Get the current entry in the .md file:
    # 1) Remove all line continuations (backslash followed by newline) and replace with a space
    # 2) Remove all leading and trailing whitespace
    # 3) Find the line that starts with "sudo tdnf -y install ..."
    # 4) Grab the package list from the line

    current_prereqs=$(echo "$current_prereqs" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    current_prereqs=$(echo "$current_prereqs" | grep -oP 'sudo tdnf -y install \K.*')
    current_prereqs=$(echo "$current_prereqs" | xargs)
elif [[ "$distro" == "ubuntu" ]]; then
    # Get the current entry in the .md file:
    # 1) Remove all line continuations (backslash followed by newline) and replace with a space
    # 2) Remove all leading and trailing whitespace
    # 3) Find the line that starts with "sudo apt -y install ..."
    # 4) Grab the package list from the line

    current_prereqs=$(echo "$current_prereqs" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    current_prereqs=$(echo "$current_prereqs" | grep -oP 'sudo apt -y install \K.*')
    current_prereqs=$(echo "$current_prereqs" | xargs)
fi

# Compare the current and source pre-requisites. Enforce a 1:1 match including order.
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
