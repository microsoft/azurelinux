# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Script to check for required kernel configs in a kernel config file
# Usage: python3 check_required_kernel_configs.py --required_configs <path to json of required configs> --config_file <path to config being checked>

import json
import argparse
import sys
from kernel_sources_analysis import get_data_from_config, get_jsondata_from_jsonfile, extract_kernel_dir_name, extract_config_arch, create_map_of_config_values

def check_required_configs_in_configfile(req_config_json_file, kernel, arch, input_config_map):
    config_json_data = get_jsondata_from_jsonfile(req_config_json_file)
    if kernel not in config_json_data:
        print(f"Kernel {kernel} not found in {req_config_json_file}")
        print(f"Please provide required configs for {kernel} in {req_config_json_file}")
        return None
    required_configs_data = config_json_data[kernel]['required-configs']

    #incorrect configs is map: {config: (newValue, expectedValue, comment, PR)}
    incorrect_configs = {}

    # go through required configs
    for config_option, req_value in required_configs_data.items():
        # check for arch
        if arch not in req_value['arch']:
            continue
        # check required configs present in the kernel's config file
        if config_option in input_config_map:
            # check if value is correct
            if input_config_map[config_option] not in req_value['value']:
                incorrect_configs[config_option] = {
                    "newValue": input_config_map[config_option],
                    "expectedValue": req_value['value'],
                    "comment": f"Unexpected value: {input_config_map[config_option]}",
                    "PR": req_value['PR']
                }
        # check if required configs removed from the kernel's config file
        # Note that some required configs are required to be missing
        elif "<missing>" not in req_value['value']: 
                incorrect_configs[config_option] = {
                    "newValue": "MISSING",
                    "expectedValue": req_value['value'],
                    "comment": f"Config not found.",
                    "PR": req_value['PR']
                }
    return incorrect_configs

def print_verbose(req_config_json_file, kernel, arch, results):
    config_json_data = get_jsondata_from_jsonfile(req_config_json_file)
    required_configs_data = config_json_data[kernel]['required-configs']
    print_data = [["Option", "Required Arch", "Expected Value", "Comment"]]
    for config_option, value in required_configs_data.items():
        if arch in value['arch']:
            if config_option in results:
                print_data.append([config_option, value['arch'], value['value'], f'FAIL - Unexpected value: {results[config_option]["newValue"]} (See: {value["PR"]})'])
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
    parser.add_argument('--kernel', help='kernel for the config being checked', required=False)
    args = parser.parse_args()
    required_configs = args.required_configs
    config_file = args.config_file
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

    config_map = create_map_of_config_values(input_config_data)

    print()
    print("===============================================================================")
    print(f"== Results for {config_file} ==")
    print("===============================================================================")

    # result is map: {config: (newValue, expectedValue, comment, PR)}
    result = check_required_configs_in_configfile(required_configs, kernel, arch, config_map)
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
                print(f'{config_option} is "{result[config_option]["newValue"]}", expected {result[config_option]["expectedValue"]}.\nReason: {result[config_option]["comment"]}')
                print(f'PR: {result[config_option]["PR"]}')
                print()
            sys.exit(1)