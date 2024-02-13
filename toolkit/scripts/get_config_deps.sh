#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

# Parses config_file using jquery to find realpath to all filenames under:
#
#   - PackageLists
#   - PostInstallScripts
#   - PreInstallScripts
#   - FinalizeImageScripts
#   - AdditionalFiles (source file paths)

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

pkg_lists=$(jq -r '.SystemConfigs[]?.PackageLists[]?' $config_file)
postinstall_scripts=$(jq -r '.SystemConfigs[]?.PostInstallScripts[]?.Path' $config_file)
preinstall_scripts=$(jq -r '.SystemConfigs[]?.PreInstallScripts[]?.Path' $config_file)
finalizeimg_scripts=$(jq -r '.SystemConfigs[]?.FinalizeImageScripts[]?.Path' $config_file)
additional_files=$(jq -r '.SystemConfigs[]?.AdditionalFiles?|keys?|join("\n")' $config_file)
config_other_files="$pkg_lists $postinstall_scripts $preinstall_scripts $finalizeimg_scripts $additional_files"
for filename in $config_other_files
do
	# fix path if it's relative to config_file
	if [ "${filename:0:1}" == "/" ]
	then
		echo "$filename"
	else
		echo $(realpath "$config_base_dir/$filename")
	fi
done
