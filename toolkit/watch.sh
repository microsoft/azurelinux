#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Set BLDTRACKER=/path/to/bldtracker
# Set TIMESTAMP_FILE_PATH=/path/to/output.json

files=$(find ../build/timestamp/*.json 2> /dev/null | sort -u)

if [[ -z "${files}" ]]; then
    echo "Waiting on build to start..."
fi

for f in ${files}; do
    name=$(basename $f)
    progress=$(./out/tools/bldtracker --out-path $f --mode watch --script-name $name)
    echo $name: $progress%
done