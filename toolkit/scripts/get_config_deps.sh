#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 - CONFIG_FILE
# $2 - CONFIG_BASE_DIR

if [[ $# -ne 2 ]]
then
    echo "ERROR: Must provide CONFIG_FILE and CONFIG_BASE_DIR to get_config_deps.sh" >&2
    exit 1
fi

CONFIG_FILE="$1"
CONFIG_BASE_DIR="$2"

config_other_files=$(grep -E '.json|.sh' $CONFIG_FILE| sed 's/\"Path\"\://' | tr ", \n" " " | tr "\"" " " | xargs)
for filename in $config_other_files
do
    # fix path if it's relative to CONFIG_FILE
	if [ "${filename:0:1}" == "/" ]
	then
		echo "$filename"
	else
		echo "$CONFIG_BASE_DIR$filename"
	fi
done
