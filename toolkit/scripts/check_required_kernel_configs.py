# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for required kernel configs in a kernel config file
# Usage: python3 check_required_kernel_configs.py --required_configs <path to json of required configs> --config_file <path to config being checked>

import json
import argparse
import sys

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

def check_strings_in_file(json_file, arch, input_file):
    
    with open(json_file, 'r') as file:
        data = json.load(file)
        configData = data['required-configs']

    with open(input_file, 'r') as file:
        contents = file.read().split("\n")

    #missing configs is map: {config: (newValue, expectedValue, comment, PR)}
    missing_configs = {}

    # go through required configs
    for key, value in configData.items():
        # check for arch
        if arch not in value['arch']:
            continue
        # check if config is present with correct value
        found = False
        for line in contents:
            # check for config in line (without extra _VALUE)
            if "{0}=".format(key) in line or "{0} is not set".format(key) in line:
                for val in value['value']:
                    if val in line and val != "":
                        found = True
                        break
                else:
                    missing_configs[key] = (line.split(key)[1].replace('=',''), value['value'], value['comment'], value['PR'])
                    found = True
                    break
        if not found:
            # check if config can be missing
            if "" not in value['value']:
                missing_configs[key] = (line, value['value'], value['comment'], value['PR'])

    return missing_configs

def print_verbose(json_file, results):

    with open(json_file, 'r') as file:
        data = json.load(file)
        configData = data['required-configs']
    print_data = [["Option", "Required Arch", "Expected Value", "Comment"]]
    for key, value in configData.items():
        if key in results:
            print_data.append([key, value['arch'], value['value'], "FAIL: Unexpected value: {0}. See: {1}".format(results[key][0], value['PR'])])
        else:
            print_data.append([key, value['arch'], value['value'], "OK"])
    # Calculate maximum width for each column
    column_widths = [max(len(str(row[i])) for row in print_data) for i in range(len(print_data[0]))]

    # Print columns
    for j, row in enumerate(print_data):
        for i, column in enumerate(row):
            print(str(column).ljust(column_widths[i] + 2), end='')
        print()
        if j == 0:
            print("-" * sum(column_widths) + "")


## Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if known required kernel configs are present.")


    parser.add_argument('--required_configs', help='path to json of required configs', required=True)
    parser.add_argument('--config_file', help='path to config being checked', required=True)
    parser.add_argument('--verbose', action='store_true', help='get full report', required=False)
    args = parser.parse_args()
    requiredConfigs = args.required_configs
    configFile = args.config_file
    arch = check_config_arch(configFile)

    # result is map: {config: (newValue, expectedValue, comment, PR)}
    result = check_strings_in_file(requiredConfigs, arch, configFile)
    print()
    print("===============================================================================")
    print("== Results for {0} ==".format(configFile))
    print("===============================================================================")
    if args.verbose:
        print_verbose(requiredConfigs, result)
    else:
        if result == {}:
            print("All required configs are present")
        else:
            print()
            print ("----------------- Kernel config verification FAILED -----------------")
            for key, value in result.items():
                print('{0} is "{1}", expected {2}.\nReason: {3}'.format(key, value[0], value[1], value[2]))
                if value[3] != None:
                    print('PR: {0}'.format(value[3]))
                print()
            sys.exit(1)