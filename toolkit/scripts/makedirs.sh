#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: /path/to/dirs/to/make owner_user_name

# Will recursively create all directories in the path, and chown them to the specified user
# If the directory already exists, it will be skipped and no changes will be made.
# New directories will be created with timestamp 0.

DIR="${1}"
USER="${2}"

function make_dir_recursive {
    local dir="${1}"
    local user="${2}"
    local parent_dir
    parent_dir="$(dirname "${dir}")"

    # If the parent directory also needs to be created, recurse
    if [[ ! -d "${parent_dir}" ]]; then
        make_dir_recursive "${parent_dir}" "${user}" || { echo "Failed to recursively create '${parent_dir}'" ; return 1 ; }
    fi

    if [[ -d "${dir}" ]]; then
        return 0
    fi

    mkdir -p "${dir}" || { echo "Failed to create '${dir}'" ; return 1 ; }
    chown "${user}" "${dir}" || { echo "Failed to chown '${dir}' to user '${user}'" ; return 1 ; }
    touch -d @0 "${dir}" || { echo "Failed to reset timestamp on '${dir}'" ; return 1 ; }

    return 0
}

if [[ -z "${DIR}" ]] || [[ -z "${USER}" ]]; then
    echo "mkdirs.sh: No directory or user specified (input: DIR: '${DIR}', USER: '${USER}')"
    exit 1
fi

if [[ -d "${DIR}" ]]; then
    # Directory already exists, no need to do anything
    exit 0
else
    make_dir_recursive "${DIR}" "${USER}" || { echo "Failed to create '${DIR}'" ; exit 1 ; }
fi
