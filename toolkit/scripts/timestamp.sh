#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Set of functions to generate timing data for shell-script based parts of the build

# Set
#   BLDTRACKER=/path/to/bldtracker
# Set
#   TIMESTAMP_FILE_PATH=/path/to/output.json
# Include via
#   source timestamp.sh

# Invoke by calling:
#   begin_timestamp [# of sub-steps if known]
#
# Record an event starting. It will add intermediate components as needed
#   start_record_timestamp /path/of/timestamp           [# of sub-steps if desired] [optional weight value for this step]
#   start_record_timestamp /path/of/timestamp/substep   [# of sub-steps if desired] [optional weight value for this step]
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
        _timestamp_steps="$1"
        [[ -z "$_timestamp_steps" ]] && _timestamp_steps=0
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --expected-weight="$_timestamp_steps" \
            --log-level=$_loglevel \
            --mode="init"
    fi
}

start_record_timestamp () {
    if [[ -z "$BLDTRACKER" ]] || [[ -z "$TIMESTAMP_FILE_PATH" ]]; then
        echo 'Must set $BLDTRACKER and $TIMESTAMP_FILE_PATH before calling begin_timestamp'
    else
        _timestamp_path="$1"
        _timestamp_steps="$2"
        _timestamp_weight="$3"
        [[ -z "$_timestamp_steps" ]] && _timestamp_steps=0

        if [[ -n "$_timestamp_weight" ]]; then
            _weight_arg="--weight=$_timestamp_weight"
        else
            _weight_arg=""
        fi
        $BLDTRACKER \
            --script-name=$_timestamp_script_name \
            --out-path="$TIMESTAMP_FILE_PATH" \
            --step-path="$_timestamp_path" \
            --expected-weight="$_timestamp_steps" \
            --log-level=$_loglevel \
            --mode="record" \
            $_weight_arg
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
            --mode="stop"
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
            --mode="finish"
    fi
}