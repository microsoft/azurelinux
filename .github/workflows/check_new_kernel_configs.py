# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import json
import argparse
import sys
import re

def check_config_arch(input_file):
    with open(input_file, 'r') as file:
        contents = file.read()
    file.close()
    if "Linux/x86_64" in contents:
        return "AMD64"
    elif "Linux/arm64" in contents:
        return "ARM64"
    else:
        return None

# find the lines in the diff that contain +/- CONFIG
# ignore the lines that contain @
# return the set of words that follow +/-
def find_matching_lines(input_string):
    pattern = r'(?!.*@)[+-]\s*.*CONFIG.*'
    matching_lines = re.findall(pattern, input_string)
    holder=[re.sub(r"\+|\-|=y|=m|\#|is not set", r"", s).strip() for s in matching_lines]
    config_set = set(holder)
    return config_set

# parse diff for new kernel configs
# check if they are in required configs
def find_missing_configs(json_file, arch, config_diff):
    # Load the JSON object
    with open(json_file, 'r') as file:
        data = json.load(file)
    config_data = data['required-configs']

    # Extract the words from the string
    config_words = find_matching_lines(config_diff)

    # Find the missing words
    missing_configs = []
    for word in config_words:
        if word not in config_data or arch not in config_data[word]["arch"] :
            missing_configs.append(word)
    return missing_configs


parser = argparse.ArgumentParser(
description="Tool for checking new configs are present in required configs JSON.")
parser.add_argument('--required_configs', help='path to JSON of required configs', required=True)
parser.add_argument('--config_file', help='path to config', required=True)
parser.add_argument('--config_diff', help='config diff', required=True)
args = parser.parse_args()
required_configs = args.required_configs
config_file = args.config_file
config_diff = args.config_diff
arch = check_config_arch(config_file)

missing_configs = find_missing_configs(required_configs, arch, config_diff)
print("Missing words:", missing_configs)
if len(missing_configs) == 0:
    print("All configs are present in required configs")
else:
    print (f"====================== Kernel new config verification FAILED for {arch} ======================")
    print(f"New configs detected for {arch}. Please add the following to toolkit/scripts/mariner-required-configs.json")
    for word in missing_configs:
        print(word)
    sys.exit(1)
