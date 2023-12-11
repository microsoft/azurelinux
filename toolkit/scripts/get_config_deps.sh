#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 - config_file

if [[ $# -ne 1 ]]
then
    echo "ERROR: Must provide config file to get_config_deps.sh" >&2
    exit 1
fi

config_file="$1"

if [[ ! -f "$config_file" ]]
then
    echo "ERROR: Config file '$config_file' does not exist" >&2
    exit 1
fi

config_base_dir=$(dirname "$config_file")

config_other_files=$(grep -E '.json|.sh' $config_file| sed 's/\"Path\"\://' | tr ", \n" " " | tr "\"" " " | xargs)
for filename in $config_other_files
do
    # fix path if it's relative to config_file
	if [ "${filename:0:1}" == "/" ]
	then
		echo $(realpath "$filename")
	else
		echo $(realpath "$config_base_dir/$filename")
	fi
done
