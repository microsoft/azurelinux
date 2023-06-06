# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for required kernel configs in a kernel config file
# Usage: python3 check_required_kernel_configs.py --required_configs <path to json of required configs> --config_file <path to config being checked>

import json
import argparse
import sys
from kernel_sources_analysis import get_data_from_config, extract_kernel_dir_name, extract_config_arch

# Define a class
    #incorrect configs is map: {config: (newValue, expectedValue, comment, PR)}
class IncorrectConfig:
    def __init__(self, name, newValue, expectedValue, comment, PR):
        self.name = name
        self.newValue = newValue
        self.expectedValue = expectedValue
        self.comment = comment
        self.PR = PR

def check_strings_in_file(json_file, kernel, arch, input_config_data):
    with open(json_file, 'r') as req_config_json_file:
        config_json_data = json.load(req_config_json_file)
        if kernel not in config_json_data:
            print(f"Kernel {kernel} not found in {json_file}")
            print(f"Please provide required configs for {kernel} in {json_file}")
            print(f"Exiting...")
            return None
        required_configs_data = config_json_data[kernel]['required-configs']

    #incorrect configs is map: {config: (newValue, expectedValue, comment, PR)}
    incorrect_configs = {}

    # go through required configs
    for config_option, value in required_configs_data.items():
        # check for arch
        if arch not in value['arch']:
            continue
        # check if required config is present with correct value
        found = False
        # check for required config in each input config line (without extra _VALUE)
        for line in input_config_data.split('\n'):
            if f"{config_option}=" in line or f"{config_option} is not set" in line:
                for val in value['value']:
                    if val in line and val != "":
                        found = True
                        break
                # config was found but value is not correct
                # mark as found and add to incorrect_configs
                if not found:
                    incorrect_configs[config_option] = (IncorrectConfig(config_option, line.split(config_option)[1].replace('=',''), value['value'], value['comment'], value['PR']))
                    found = True
        if not found:
            # check if config can be missing
            if "" not in value['value']:
                incorrect_configs[config_option] = (IncorrectConfig(config_option, line, value['value'], value['comment'], value['PR']))

    return incorrect_configs

def print_verbose(json_file, kernel, arch, results):
    with open(json_file, 'r') as req_config_json_file:
        data = json.load(req_config_json_file)
        required_configs_data = data[kernel]['required-configs']
    print_data = [["Option", "Required Arch", "Expected Value", "Comment"]]
    for config_option, value in required_configs_data.items():
        if arch in value['arch']:
            if config_option in results:
                print_data.append([config_option, value['arch'], value['value'], f"FAIL: Unexpected value: {results[config_option].newValue} See: {value['PR']}"])
            else:
                print_data.append([config_option, value['arch'], value['value'], "OK"])
    # Calculate maximum width for each column
    column_widths = [max(len(str(row[i])) for row in print_data) for i in range(len(print_data[0]))]

    # Print columns
    for j, row in enumerate(print_data):
        for i, column in enumerate(row):
            print(str(column).ljust(column_widths[i] + 2), end='')
        print()
        if j == 0:
            print("-------------------------------------------------------------------------------")


## Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if known required kernel configs are present.")


    parser.add_argument('--required_configs', help='path to json of required configs', required=True)
    parser.add_argument('--config_file', help='path to config being checked', required=True)
    parser.add_argument('--verbose', action='store_true', help='get full report', required=False)
    args = parser.parse_args()
    required_configs = args.required_configs
    config_file = args.config_file

    kernel = extract_kernel_dir_name(config_file)
    if kernel == None:
        print("Kernel not found in config filepath")
        sys.exit(1)

    input_config_data = get_data_from_config(config_file)

    arch = extract_config_arch(input_config_data)
    if arch == None:
        print("Architecture not found in config file")
        sys.exit(1)

    print()
    print("===============================================================================")
    print(f"== Results for {config_file} ==")
    print("===============================================================================")

    # result is map: {config: (newValue, expectedValue, comment, PR)}
    result = check_strings_in_file(required_configs, kernel, arch, input_config_data)
    # check if required configs are present
    # not an error is not all kernels are being checked
    if result == None:
        print(f"No required configs for {kernel} in json")
        sys.exit(0)
    
    if args.verbose:
        print_verbose(required_configs, kernel, arch, result)
    else:
        if result == {}:
            print("All required configs are present")
        else:
            print()
            print ("----------------- Kernel config verification FAILED -----------------")
            for config_option, value in result.items():
                print(f'{config_option} is "{value.newValue}", expected {value.expectedValue}.\nReason: {value.comment}')
                print(f"PR: {value.PR}")
                print()
            sys.exit(1)