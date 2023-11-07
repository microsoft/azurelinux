#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Set of functions to generate timing data for shell-script based parts of the build

# Set
#   BLDTRACKER=/path/to/bldtracker
# Set
#   TIMESTAMP_FILE_PATH=/path/to/output.jsonl
# Include via
#   source timestamp.sh

# Invoke by calling:
#   begin_timestamp
#
# Record an event starting. It will add intermediate components as needed
#   start_record_timestamp /path/of/timestamp
#   start_record_timestamp /path/of/timestamp/substep
#
# Finish recording this step and all substeps inside it
#   stop_record_timestamp  /path/of/timestamp
#
# Finish the measurements
#   finish_timestamp

if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
    echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling any timestamp.sh functions'
fi

_timestamp_script_name="$(basename $0)"
[[ -z "$_loglevel" ]] && _loglevel="info"

begin_timestamp()  {
    if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
        echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling begin_timestamp'
    else
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --log-level=$_loglevel \
            --mode="init" || true
    fi
}

start_record_timestamp () {
    if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
        echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling begin_timestamp'
    else
        _timestamp_path="$1"
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --step-path="$_timestamp_path" \
            --log-level=$_loglevel \
            --mode="record" || true
    fi
}

stop_record_timestamp () {
    if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
        echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling begin_timestamp'
    else
        _timestamp_path="$1"
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --step-path="$_timestamp_path" \
            --log-level=$_loglevel \
            --mode="stop" || true
    fi
}

finish_timestamp() {
    if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
        echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling begin_timestamp'
    else
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --log-level=$_loglevel \
            --mode="finish" || true
    fi
}