#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from bisect import bisect_left
from enum import Enum
from functools import cmp_to_key
from sys import version
from pyrpm.spec import Spec, replace_macros

import argparse
import json
import re
import rpm
import shlex
import subprocess
import validators

class ElementSelection(Enum):
    first = 'first'
    last = 'last'
    new = 'new'

    def __str__(self):
        return self.value

# Custom implementation with our own comparator because "bisect_left" doesn't support
# a custom "key" argument before Python 3.10.
#
# Returns the index of any matching element or -1, if the elements is not there.
def binary_search(arr, searched, comparator, lower_bound = 0, upper_bound = -1):
    if upper_bound == -1:
        upper_bound = len(arr) - 1

    while lower_bound <= upper_bound:
        current = (upper_bound + lower_bound) // 2
        comparison_result = comparator(arr[current], searched)

        if comparison_result < 0:
            lower_bound = current + 1
        elif comparison_result > 0:
            upper_bound = current - 1
        else:
            return current

    return -1

# Custom implementation with our own comparator because "bisect_left" doesn't support
# a custom "key" argument before Python 3.10.
#
# Returns the index of the first or last matching element or -1, if the elements is not there.
def binary_search_specific(arr, searched, comparator, element_selection, lower_bound = 0, upper_bound = -1):
    if upper_bound == -1:
        upper_bound = len(arr) - 1

    first_index = -1
    new_first = binary_search(arr, searched, comparator, lower_bound = lower_bound, upper_bound = upper_bound)
    while new_first != -1:
        first_index = new_first
        if element_selection == ElementSelection.first:
            new_first = binary_search(arr, searched, comparator, lower_bound = lower_bound, upper_bound = new_first - 1)
        else:
            new_first = binary_search(arr, searched, comparator, lower_bound = new_first + 1, upper_bound = upper_bound)

    return first_index


def component(name, version, url):
    return {
        "component": {
            "type": "other",
            "other": {
                "name": f"{name}",
                "version": f"{version}",
                "downloadUrl": f"{url}"
            }
        }
    }


def component_name(component):
    return component["component"]["other"]["name"]


def component_url(component):
    return component["component"]["other"]["downloadUrl"]


def component_version(component):
    return component["component"]["other"]["version"]


def components_compare_name(item1, item2):
    name1 = component_name(item1).lower()
    name2 = component_name(item2).lower()

    if name1 < name2:
        return -1
    elif name1 > name2:
        return 1

    return 0


def components_compare_name_and_version(item1, item2):
    name_comparison = components_compare_name(item1, item2)
    if name_comparison != 0:
        return name_comparison

    DUMMY_EPOCH = '1'
    DUMMY_RELEASE = '1'

    evr1 = (DUMMY_EPOCH, component_version(item1), DUMMY_RELEASE)
    evr2 = (DUMMY_EPOCH, component_version(item2), DUMMY_RELEASE)

    return rpm.labelCompare(evr1, evr2)


COMPONENT_KEY_NAME_AND_VERSION = cmp_to_key(components_compare_name_and_version)

# Can't rely on the 'pyrpm.spec' module - it's not as good with parsing the spec as 'rpmspec' and tends to leave unexpanded macros.
RPMSPEC_COMMAND_COMMON="rpmspec --parse -D 'forgemeta %{nil}' -D 'py3_dist X' -D 'with_check 0' -D 'dist .cm2' -D '__python3 python3' -D '_sourcedir SPECS-EXTENDED/python-oslo-config' -D 'fillup_prereq fillup'"
SOURCE0_LINE_REGEX = re.compile(r"^\s*Source0*:")
SOURCE_VALUE_REGEX = re.compile(r"(?<=[\s:])[^\s#]+", )
def read_spec_tag(spec_path, tag):
    return str(subprocess.check_output(shlex.split(f"{RPMSPEC_COMMAND_COMMON} --srpm --qf '%{{{tag}}}' -q {spec_path}"), stderr=subprocess.DEVNULL),
                       encoding="utf-8",
                       errors="strict")


def read_spec_name(spec_path):
    return read_spec_tag(spec_path, "NAME")


def read_spec_source0(spec_path):
    process = subprocess.Popen(shlex.split(f"{RPMSPEC_COMMAND_COMMON}  --parse {spec_path}"), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    lines = [ str(x, encoding="utf-8", errors="strict").strip() for x in process.stdout ]

    source0_line = list(filter(SOURCE0_LINE_REGEX.match, lines))
    if len(source0_line) == 0:
        return None
    return SOURCE_VALUE_REGEX.search(source0_line[0]).group()


def read_spec_version(spec_path):
    return read_spec_tag(spec_path, "VERSION")


def update_component(component, name, url, version):
    component["component"]["other"]["name"] = name
    component["component"]["other"]["downloadUrl"] = url
    component["component"]["other"]["version"] = version


def process_spec(spec_path, components, update_mode):
    print(f"Processing: {spec_path}")

    name = read_spec_name(spec_path)
    version = read_spec_version(spec_path)
    source_url = read_spec_source0(spec_path)

    if source_url is None:
        print(f"""
WARNING: failed to retrieve the URL of the source tarball - spec contains no 'Source' tags.
         If that's correct, you must ignore the spec inside the '.github/workflows/validate-cg-manifest.sh' script.
         If this is incorrect and the spec should build with a source tarball, please update the spec accordingly.

No 'Source' tag: {spec_path}
""")
        return

    if not validators.url(source_url):
        print(f"""
WARNING: failed to retrieve the URL of the source tarball - first 'Source' tag ({source_url}) is not a valid URL.
         Please make sure at least the first 'Source' tag contains a valid URL to the source tarball required to build that package.
         If tag is correct and the package build doesn't rely on any source tarballs, you must ignore the spec inside the '.github/workflows/validate-cg-manifest.sh' script.

'Source' not a valid URL: {spec_path}
""")
        return

    processed_component = component(name, version, source_url)

    insertion_index = -1
    if update_mode != ElementSelection.new:
        insertion_index = binary_search_specific(components, processed_component, components_compare_name, update_mode)

    if insertion_index == -1:
        components.insert(0, processed_component)
    else:
        update_component(components[insertion_index], name, source_url, version)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for updating the 'cgmanifest.json' with values from the input spec files.")
    parser.add_argument('update_mode',
                        type=ElementSelection,
                        choices=list(ElementSelection),
                        default=ElementSelection.last,
                        help='entry to be updated, if it already exists')
    parser.add_argument('cgmanifest_file',
                        metavar='cgmanifest_path',
                        type=argparse.FileType('r'),
                        help='path to the "cgmanifest.json" file')
    parser.add_argument('specs',
                        metavar='spec_path',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='path to an RPM spec file')
    args = parser.parse_args()

    cgmanifest = json.load(args.cgmanifest_file)
    args.cgmanifest_file.close()

    cgmanifest["Registrations"].sort(key=COMPONENT_KEY_NAME_AND_VERSION)
    for spec in args.specs:
        process_spec(spec.name, cgmanifest["Registrations"], args.update_mode)
    cgmanifest["Registrations"].sort(key=COMPONENT_KEY_NAME_AND_VERSION)

    with (open(args.cgmanifest_file.name, "w")) as cgmanifest_file:
        json.dump(cgmanifest, cgmanifest_file, indent=2)
        cgmanifest_file.write("\n")
