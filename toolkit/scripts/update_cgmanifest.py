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
import rpm
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


def update_component(component, name, url, version):
    component["component"]["other"]["name"] = name
    component["component"]["other"]["downloadUrl"] = url
    component["component"]["other"]["version"] = version


def process_spec(spec_path, components, update_mode):
    print(f"Processing {spec_path}.")

    spec = Spec.from_file(spec_path)

    name = spec.name
    version = spec.version    
    source_url = ""
    if len(spec.sources) > 0:
        source_url = replace_macros(spec.sources[0], spec)
    
    if not validators.url(source_url):
        print(f"WARNING: first 'Source' tag ({source_url}) is not a valid URL, skipping.")
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
