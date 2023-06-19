# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import os
import json

def get_data_from_config(input_file):
    with open(input_file, 'r') as file:
        input_config_data = file.read()
    return input_config_data

def get_jsondata_from_jsonfile(input_json_file):
    with open(input_json_file, 'r') as req_config_json_file:
        config_json_data = json.load(req_config_json_file)
    return config_json_data

def extract_kernel_dir_name(input_file):
    match =  os.path.basename(os.path.dirname(input_file))
    if match:
        return match
    else:
        print("Error: Could not find kernel name in path for config file")
        return None

def extract_config_arch(input_config_data):
    if "Linux/x86_64" in input_config_data:
        return "AMD64"
    elif "Linux/arm64" in input_config_data:
        return "ARM64"
    else:
        print("Error: Could not find architecture in config file")
        return None

def create_map_of_config_values(input_config_data):
    config_map = {}
    for line in input_config_data.split('\n'):
        if "=" in line:
            config_map[line.split('=')[0]] = line.split('=')[1]
        # Find configs that are not set
        # Example: # CONFIG_FOO is not set
        elif "is not set" in line:
            config_map[line.split()[1]] = "is not set"
    return config_map