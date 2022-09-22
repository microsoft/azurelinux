#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Set BLDTRACKER=/path/to/bldtracker
# Set TIMESTAMP_FILE_PATH=/path/to/output.json

set -e
set -x

BLDTRACKER=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/toolkit/out/tools/bldtracker
TIMESTAMP_FILE_PATH=./test.json
source ./timestamp.sh

begin_timestamp 20

 start_record_timestamp "foo/A" 4 20
# stop_record_timestamp "A"
 start_record_timestamp "B"
# stop_record_timestamp "B"
# start_record_timestamp "C"
# stop_record_timestamp "C"
# start_record_timestamp "D"
# stop_record_timestamp "D"

finish_timestamp