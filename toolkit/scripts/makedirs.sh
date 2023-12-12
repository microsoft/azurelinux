#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: /path/to/dirs/to/make owner_user_name

# Will recursively create all directories in the path, and chown them to the specified user
# If the directory already exists, it will be skipped and no changes will be made.
# New directories will be created with timestamp 0.

DIR="${1}"
USER="${2}"

if [[ -z "${DIR}" ]] || [[ -z "${USER}" ]]; then
    echo "mkdirs.sh: No directory or user specified (input: DIR: '${DIR}', USER: '${USER}')"
    exit 1
fi

if [[ -d "${DIR}" ]]; then
    # Directory already exists, no need to do anything
    exit 0
else
    runuser -u "${USER}" -- mkdir -p "${DIR}" || { echo "Failed to create '${DIR}'" ; exit 1 ; }
fi
