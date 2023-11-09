#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: /path/to/dirs/to/make owner_user_name

# Will recursively create all directories in the path, and chown them to the specified user
# If the directory already exists, it will be skipped and no changes will be made.
# New directories will be created with timestamp 0.

DIR="${1}"
USER="${2}"
LOG_FILE="${3}"

function make_dir_recursive {
    dir="${1}"
    user="${2}"
    parent_dir="$(dirname "${dir}")"

    # If the parent directory also needs to be created, recurse
    if [[ ! -d "${parent_dir}" ]]; then
        echo "Creating parent directory ${parent_dir} owned by ${user}" >> "${LOG_FILE}"
        make_dir_recursive "${parent_dir}"
    fi

    if [[ -d "${dir}" ]]; then
        echo "Directory ${dir} already exists, skipping" >> "${LOG_FILE}"
        return 0
    fi

    mkdir -p "${dir}" && chown "${user}" "${dir}" && touch -d @0 "${dir}" >> "${LOG_FILE}" 2>&1 || return 1

    return 0
}

echo "Creating directory ${DIR} owned by ${USER}" >> "${LOG_FILE}"
make_dir_recursive "${DIR}" "${USER}"