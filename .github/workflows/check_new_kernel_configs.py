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
def find_matching_lines(input_string):
    pattern = r'(?!.*@)[+-]\s*.*CONFIG.*'
    matching_lines = re.findall(pattern, input_string)

    return matching_lines

# parse diff for new kernel configs
# check if they are in required configs
def find_missing_words(json_file, arch, config_diff):
    # Load the JSON object
    with open(json_file, 'r') as file:
        data = json.load(file)
    configData = data['required-configs']

    # Extract the words from the string
    config_words = find_matching_lines(config_diff)
    holder = [ s.replace('+', '').replace('-', '').replace('=y','').replace('=m','').replace(' is not set', '').replace('#', '').strip() for s in config_words]
    wordSet = set(holder)

    # Find the missing words
    missing_words = []
    for word in wordSet:
        if word not in configData or arch not in configData[word]["arch"] :
            missing_words.append(word)
    return missing_words


parser = argparse.ArgumentParser(
description="Tool for checking if known required kernel configs are present.")
parser.add_argument('--required_configs', help='path to json of required configs', required=True)
parser.add_argument('--config_file', help='path to config', required=True)
parser.add_argument('--config_str', help='config diff', required=True)
args = parser.parse_args()
requiredConfigs = args.required_configs
configFile = args.config_file
configDiff = args.config_str
arch = check_config_arch(configFile)

missing_words = find_missing_words(requiredConfigs, arch, configDiff)
print("Missing words:", missing_words)
if len(missing_words) == 0:
    print("All configs are present in required configs")
else:
    print ("====================== Kernel new config verification FAILED for {0} ======================".format(arch))
    print("New configs detected for {0}. Please add the following to toolkit/scripts/mariner-required-configs.json".format(arch))
    for word in missing_words:
        print('{0}'.format(word))
    sys.exit(1)
