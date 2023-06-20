# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import json
import argparse
import sys
import re
from kernel_sources_analysis import get_data_from_config, extract_kernel_dir_name, extract_config_arch

# Regex for finding config options
# Matches words that start with +/-CONFIG_ or +/-# CONFIG_
# Examples:
# "+CONFIG_ABC=y" -> "CONFIG_ABC"
# "-# CONFIG_XYZ is not set" -> "CONFIG_XYZ"
CONFIG_REGEX=re.compile(r'(?:(?<=[-+])|(?<=[-+]# ))CONFIG_\w+')

def extract_modified_configs(input_string):
    matching_configs = CONFIG_REGEX.findall(input_string)
    return set(matching_configs)

# Parse diff for new kernel configs
# Check if they are in required configs
def find_missing_configs(config_json_path, kernel, arch, config_diff):
    # Load the JSON object
    with open(config_json_path, 'r') as config_json_file:
        config_json_data = json.load(config_json_file)
        if kernel not in config_json_data:
            print(f"Kernel {kernel} not found in {config_json_path}")
            print(f"Please provide required configs for {kernel} in {config_json_path}")
            return None
        required_configs_data = config_json_data[kernel]['required-configs']

    # Extract the configs from the string
    config_set = extract_modified_configs(config_diff)

    # Find the missing configs
    missing_configs = []
    for config_option in config_set:
        if config_option not in required_configs_data or arch not in required_configs_data[config_option]["arch"] :
            missing_configs.append(config_option)
    return missing_configs

## Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description="Tool for checking new configs are present in required configs JSON.")
    parser.add_argument('--required_configs', help='path to JSON of required configs', required=True)
    parser.add_argument('--config_file', help='path to config', required=True)
    parser.add_argument('--config_diff', help='diff showing changes for just the config_file', required=True)
    parser.add_argument('--kernel', help='kernel for the config being checked', required=False)
    args = parser.parse_args()
    required_configs = args.required_configs
    config_file = args.config_file
    config_diff = args.config_diff
    if args.kernel:
        kernel = args.kernel
    else:
        kernel = extract_kernel_dir_name(config_file)
    if kernel == None:
        print("ERROR: Kernel name not found. Please provide kernel name using --kernel flag or ensure config file path is correct")
        sys.exit(1)
    print(f"Analyzing for Kernel: {kernel}")

    input_config_data = get_data_from_config(config_file)

    arch = extract_config_arch(input_config_data)
    if arch == None:
        print("ERROR: Architecture not found in config file")
        sys.exit(1)

    missing_configs = find_missing_configs(required_configs, kernel, arch, config_diff)
    if missing_configs == None:
        print(f"ERROR: Could not find required configs for {kernel}")
        sys.exit(0)

    if len(missing_configs) == 0:
        print("All configs are present in required configs")
    else:
        print (f"====================== Kernel new config verification FAILED for {arch} ======================")
        print(f"New configs detected for {arch}. Please add the following to {required_configs}")
        for word in missing_configs:
            print(word)
        sys.exit(1)
