#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

TEMP_DIR=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $TEMP_DIR"
    rm -rf $TEMP_DIR
}
trap clean-up EXIT

# Mimic the structured logging used by InfluxDB.
# Usage: log <level> <msg> [<key> <val>]...
function log () {
    local -r type=$1 msg=$2
    shift 2

    if [[ "${LOG_LEVELS[${level}]}" -gt "${LOG_LEVELS[${LOG_LEVEL}]}" ]]; then
        return
    fi

    local -r logtime="$(date --utc +'%FT%T.%NZ')"
    1>&2 echo -e "##[$type] ${logtime}\t${msg}\t"
}
