#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Wraps the bldtracker tool for timing rpm downloads
# Separate from toolchain.sh since it needs to handle asynchronous operations

# $1 bldtracker tool
# $2 out path
# $3 rpm
# $4 mode

bldtracker="$1"
script_name="download toolchain rpms"
out_file="$2"
rpm="$3"
mode="$4"

if [[ "$mode" == "record" ]]; then
    ${bldtracker} \
        --script-name="${script_name}" \
        --out-path="${out_file}" \
        --mode="record"
fi

if [[ "$mode" == "stop" ]]; then
    ${bldtracker} \
        --script-name="${script_name}" \
        --out-path="${out_file}" \
        --step-path="${rpm}" \
        --mode="stop"
    # We won't know if we are done ahead of time...
fi

# Call this explicitly using make logic
if [[ "$mode" == "complete" ]]; then
    ${bldtracker} \
        --script-name="${script_name}" \
        --out-path="${out_file}" \
        --mode="finish"
fi


