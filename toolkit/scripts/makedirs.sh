#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: /path/to/dirs/to/make owner_user_name

# Will recursively create all directories in the path, and chown them to the specified user
# If the directory already exists, it will be skipped and no changes will be made.
# New directories will be created with timestamp 0.

DIR="${1}"
MARINER_USER="${2}"

if [[ -z "${DIR}" ]] || [[ -z "${MARINER_USER}" ]]; then
    echo "mkdirs.sh: No directory or user specified (input: DIR: '${DIR}', USER: '${MARINER_USER}')"
    exit 1
fi

if [[ -d "${DIR}" ]]; then
    # Directory already exists, no need to do anything
    exit 0
else
    if [[ "${USER}" == "root" ]]; then
        # If the current user is root, use runuser to create the directory as the specified user
        runuser -u "${MARINER_USER}" -- mkdir -p "${DIR}" || { echo "Failed to create '${DIR}'" ; exit 1 ; }
    elif [[ "${MARINER_USER}" == "${USER}" ]]; then
        # Otherwise check if the user is the same as the current user, and create the directory as the current user
        mkdir -p "${DIR}" || { echo "Failed to create '${DIR}'" ; exit 1 ; }
    else
        # Otherwise, the user is not the current user, and not root, so we cannot create the directory
        echo "mkdirs.sh: Mariner build user '${MARINER_USER}' is not the current user '${USER}', and not running with sudo, cannot create '${DIR}'"
        exit 1
    fi
fi
