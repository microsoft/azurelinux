# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import re

def get_data_from_config(input_file):
    with open(input_file, 'r') as file:
        input_config_data = file.read()
    return input_config_data

def extract_kernel_dir_name(input_file):
    match = re.search(r'SPECS/(.*?)/', input_file)
    if match:
        return match.group(1)
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


