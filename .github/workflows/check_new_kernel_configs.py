# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for new configs which should be in required kernel configs json
# Usage: python3 check_new_kernel_configs.py --required_configs <path to json of required configs> --config_str <string of diff for config file>

import json
import argparse
import sys
import re

# find the lines in the diff that contain +/- CONFIG
# ignore the lines that contain @
def find_matching_lines(input_string):
    pattern = r'(?!.*@)[+-]\s*.*CONFIG.*'
    matching_lines = re.findall(pattern, input_string)

    return matching_lines

# parse diff for new kernel configs
# check if they are in required configs
def find_missing_words(json_file, string):
    # Load the JSON object
    with open(json_file, 'r') as file:
        data = json.load(file)
    configData = data['required-configs']

    # Extract the words from the string
    config_words = find_matching_lines(string)
    holder = [ s.replace('+', '').replace('-', '').replace('=y','').replace('=m','').replace(' is not set', '').replace('#', '').strip() for s in config_words]
    wordSet = set(holder)

    # Find the missing words
    missing_words = []
    for word in wordSet:
        if word not in configData:
            missing_words.append(word)

    return missing_words


parser = argparse.ArgumentParser(
description="Tool for checking if known required kernel configs are present.")
parser.add_argument('--required_configs', help='path to json of required configs', required=True)
parser.add_argument('--config_str', help='path to config being checked', required=True)
args = parser.parse_args()
requiredConfigs = args.required_configs
configStr = args.config_str

missing_words = find_missing_words(requiredConfigs, configStr)
print("Missing words:", missing_words)
if len(missing_words) == 0:
    print("All configs are present in required configs")
else:
    print ("====================== Kernel config verification FAILED ======================")
    for word in missing_words:
        print('{0} is new. Please add to toolkit/scripts/mariner-required-configs.json'.format(word))
    sys.exit(1)
