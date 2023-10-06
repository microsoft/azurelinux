#!/usr/bin/python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
from collections import OrderedDict
import json
from os.path import isdir, isfile
from pathlib import Path
import sys

from spec_source_attributions import get_spec_source, KNOWN_SOURCE_ORIGINS

# Expected Schema:
# class LicenseCollection:
#     header: str
#     table_headers: List[str]
#     licenses: List[License]
#
# class License:
#     origin: str
#     license: str
#     specs: List[str]

def generate_markdown(license_collection):
    res = []
    res.append(license_collection["header"])
    res.append('')
    res.append('| ' + ' | '.join(license_collection["table_headers"]) + ' |')
    res.append('|' + '|'.join([' --- ' for _ in license_collection["table_headers"]]) + '|')

    for origin, details in license_collection["licenses"].items():
        details["specs"].sort(key=str.lower)
        res.append('| {0} | {1} | {2} |'.format(origin, details["license"], ' <br> '.join(details["specs"])))
    
    return '\n'.join(res) + '\n'


def sort_licenses(license_collection):
    license_collection["licenses"] = OrderedDict(sorted(license_collection["licenses"].items(), key=lambda item:str.lower(item[0])))
    for details in license_collection["licenses"].values():
        # Remove duplicates with "set()" and return a sorted list.
        details["specs"] = sorted(set(details["specs"]), key=str.lower)


def process_spec_file(spec_path, license_collection, specs_in_files, specs_unknown_distro):
    spec_name = spec_path.stem

    distribution = get_spec_source(spec_path)
    if distribution is None:
        specs_unknown_distro.add(spec_name)
    else:
        specs_in_files[distribution].add(spec_name)
        license_collection["licenses"][distribution]["specs"].append(spec_name)


def retrieve_license_info(file_paths, license_collection):
    specs_in_json = {}
    for origin, details in license_collection["licenses"].items():
        specs_in_json[origin] = set(details["specs"])

    specs_in_files = {}
    for origin in KNOWN_SOURCE_ORIGINS:
        specs_in_files[origin] = set()

    specs_unknown_distro = set()
    updated_license_collection = license_collection

    for file_path in file_paths:
        if isdir(file_path):
            for spec_path in file_path.glob('**/*.spec'):
                process_spec_file(spec_path, updated_license_collection, specs_in_files, specs_unknown_distro)
        else:
                process_spec_file(file_path, updated_license_collection, specs_in_files, specs_unknown_distro)

    specs_not_in_json = {}
    specs_not_in_files = {}
    for origin, specs_in_files_for_origin in specs_in_files.items():
        specs_not_in_json[origin] = specs_in_files_for_origin - specs_in_json[origin]
        specs_not_in_files[origin] = specs_in_json[origin] - specs_in_files_for_origin

    return specs_not_in_json, specs_not_in_files, specs_unknown_distro, updated_license_collection


def print_specs_error(header_message, specs_list):
    if len(specs_list):
        print(header_message)
        for s in sorted(specs_list, key=str.lower):
            print('\t' + s)
        print()


def remove_missing_specs(license_collection, specs_not_in_files):
    for origin, specs_not_in_files_for_origin in specs_not_in_files.items():
        origin_licenses_set = set(license_collection["licenses"][origin]["specs"])
        license_collection["licenses"][origin]["specs"] = list(origin_licenses_set - specs_not_in_files_for_origin)


def print_specs_error_by_origin(header_message, specs_by_origin_list):
    for origin, specs in specs_by_origin_list.items():
        print_specs_error(f"[Origin '{origin}]' {header_message}", specs)


def process_licenses(json_filename, markdown_filename, file_paths, check, update, remove_missing):
    with open(json_filename, 'r') as licenses_file:
        license_collection = json.load(licenses_file)

    specs_not_in_json, specs_not_in_files, specs_unknown_distro, updated_license_collection = retrieve_license_info(file_paths, license_collection)

    if remove_missing:
        remove_missing_specs(updated_license_collection, specs_not_in_files)

    sort_licenses(updated_license_collection)

    with open(markdown_filename, 'r') as output_file:
        old_content = output_file.read()
    new_content = generate_markdown(updated_license_collection)

    if update:
        with (open(json_filename, "w")) as licenses_file:
            json.dump(updated_license_collection, licenses_file, indent=4)
            licenses_file.write("\n")

        with open(markdown_filename, 'w') as output_file:
            output_file.write(new_content)

    if check:
        missing_specs = False
        for origin in specs_not_in_json.keys():
            if len(specs_not_in_json[origin]) or len(specs_not_in_files[origin]):
                missing_specs = True
                break

        outdated_markdown = old_content != new_content
        if missing_specs or len(specs_unknown_distro) or outdated_markdown:
            print_specs_error_by_origin("Specs present in the spec files that are not present in the JSON file:", specs_not_in_json)
            print_specs_error_by_origin("Specs present in the JSON file that are not present in the spec files:", specs_not_in_files)
            print_specs_error("Specs from unknown distributions:", specs_unknown_distro)

            if outdated_markdown:
                print(f"License map '{markdown_filename}' is out of date.")

            print(f"""
Specs' license information is out of date. Run the following command to regenerate:

    {__file__} --no_check --update --remove_missing \\
        {json_filename} \\
        {markdown_filename} \\
        SPECS SPECS-EXTENDED SPECS-SIGNED

NOTE: the script requires installation of the 'python-rpm-spec' module:

    python3 -m pip install python-rpm-spec
""")

            sys.exit(1)


def is_valid_path(parser, file_path):
    if isdir(file_path) or isfile(file_path):
        return Path(file_path)

    parser.error(f"The path '{file_path}' must exist and be either a directory or a regular file!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes spec license data, find missing entries, and regenerate license map file.')
    parser.add_argument('json_filename', type=Path, help='Path to data file with license data.')
    parser.add_argument('markdown_filename', type=Path, help='Path to license map markdown file.')
    parser.add_argument('file_paths', type=lambda file_path: is_valid_path(parser, file_path), nargs='+', help='Directories containing specs or spec files themselves.')
    parser.add_argument('--no_check', dest="check", help='Don\'t compare the spec information from the JSON file with the information from the spec files.', action='store_false')
    parser.add_argument('--remove_missing', help='Remove entries from the JSON file, which are not present in any of the spec files.', action='store_true')
    parser.add_argument('--update', help='Removes licenses not found in the provided directories and spec files from the JSON and markdown files.', action='store_true')
    p = parser.parse_args()

    if not p.check and not p.update:
        print("WARNING: nothing to do. Must at least check or update the spec licenses.")
        exit(1)

    process_licenses(p.json_filename, p.markdown_filename, p.file_paths, p.check, p.update, p.remove_missing)
