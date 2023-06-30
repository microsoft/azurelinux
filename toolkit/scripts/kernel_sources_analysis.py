# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import os
import re
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
    match = os.path.basename(os.path.dirname(input_file))
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

# Regex matching pairs of kernel config name and its value.
#
# Sample input:
#   CONFIG_ABC=y
#   CONFIG_XYZ=""
#   # CONFIG_111 is not set
#
# Result:
#   {
#     'CONFIG_ABC': 'y',
#     'CONFIG_XYZ': '""',
#     'CONFIG_111': 'is not set'
#   }
CONFIG_TO_VALUE_REGEX=re.compile(r'(CONFIG_\w+)[ =](.*)')
def create_map_of_config_values(input_config_data):
    return dict(CONFIG_TO_VALUE_REGEX.findall(input_config_data))