#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pathlib import Path
from pyrpm.spec import Spec
from os.path import dirname, realpath

import argparse
import re
import sys

from spec_source_attributions import get_spec_source, VALID_SOURCE_ATTRIBUTIONS

any_patch_tag = re.compile(
    r'^\s*Patch\d*:', re.MULTILINE)

# Checking if the specs include only the valid 'Distribution: Azure Linux' tag.
invalid_distribution_tag_regex = re.compile(
    r'^\s*Distribution:\s*(?!Azure Linux\s*$)\S+', re.MULTILINE)

# Checking for the deprecated '%patch[number]' format.
# For more info, see: https://rpm-software-management.github.io/rpm/manual/spec.html.
invalid_patch_macro_regex = re.compile(
    r'^\s*%patch\d', re.MULTILINE)

license_regex = re.compile(
    r"\b(license verified|verified license)\b", re.IGNORECASE)

valid_release_tag_regex = re.compile(
    r'^[1-9]\d*%\{\?dist\}$')

valid_source_attributions_one_per_line = "\n".join(f"- {key}: '{value}'" for key, value in VALID_SOURCE_ATTRIBUTIONS.items())

zero_patch_tag = re.compile(
    r'^\s*Patch0?:', re.MULTILINE)


def check_distribution_tag(spec_path: str):
    """Checks if the 'Distribution' tags match 'Azure Linux'. """
    with open(spec_path) as file:
        contents = file.read()

    if invalid_distribution_tag_regex.search(contents) is not None:
        print(f"""
ERROR: detected an invalid 'Distribution' tag.

    Please use 'Distribution: Azure Linux'.
""")
        return False

    return True


def check_patch_macro(spec_path: str):
    """Checks if the 'patch' macro is not in the format deprecated in RPM 4.18+. """
    with open(spec_path) as file:
        contents = file.read()

    if invalid_patch_macro_regex.search(contents) is not None:
        print(f"""
ERROR: use of deprecated '%patch[number]' format (no space between '%patch' and the number of the patch).

    Accepted formats are:

        - %patch [number]
        - %patch -P [number]
""")
        return False

    return True


def check_release_tag(spec_path: str):
    """Checks if the 'Release' tag is in one of CBL-Mariner's expected formats. """
    spec = Spec.from_file(spec_path)

    if valid_release_tag_regex.match(spec.release) is None:
        print(f"""
ERROR: invalid 'Release' tag.

    Accepted format is:

        '[number]%{{?dist}}' (example: 10%{{?dist}})
""")
        return False

    return True


def check_license_verification(spec_path: str):
    """Checks if the package's license has been verified. """
    spec = Spec.from_file(spec_path)

    if len(license_regex.findall(spec.changelog)) == 0:
        print(f"""
ERROR: license not verified.

    Make sure the package's license matches the information provided inside the 'License' tag.
    Once that's done, indicate that through a changelog entry "License verified" or "Verified license".

    NOTE: For the 'License' tag, please use SPDX license expressions:
          https://spdx.dev/learn/handling-license-info/
""")
        return False

    return True


def check_source_attribution(spec_path: str):
    """Checks if we have indicated the source of the spec file in the changelog. """

    if get_spec_source(spec_path) is not None:
        return True

    print(f"""
ERROR: no valid source attribution.

    Make sure to indicate the origin of the spec file in the changelog.
    Currently supported source attributions (in form of regular expressions):

{valid_source_attributions_one_per_line}

    If you're importing a spec from a source, which doesn't fit the currently supported list,
    please update the 'VALID_SOURCE_ATTRIBUTIONS' variable inside the '{dirname(realpath(__file__))}/spec_source_attributions.py' script.
""")

    return False


def check_toolchain_patch_lines(spec_path: str, toolchain_specs: list):
    """Checks if a toolchain spec file contains either no patches, or a 'Patch' or 'Patch0' tag.
       RPM < 4.18 will fail parsing a spec otherwise and toolchain specs are parsed on the host, which may have older versions of RPM.
    """

    if Path(spec_path).stem not in toolchain_specs:
        return True

    with open(spec_path) as file:
        contents = file.read()
        
    if any_patch_tag.search(contents) is None:
        return True

    if zero_patch_tag.search(contents) is None:
        print(f"""
ERROR: detected a toolchain spec with invalid 'Patch' tags.

    If a toolchain spec contains a patch, it must have one "zero" patch tag: 'Patch' or 'Patch0'.
    More patches are allowed. Patch tags with higher numbers have no specific requirements.
""")
        return False

    return True


def check_spec(spec_path, toolchain_specs):
    spec_correct = True

    print(f"Checking {spec_path}")

    if not check_distribution_tag(spec_path):
        spec_correct = False

    if not check_patch_macro(spec_path):
        spec_correct = False

    if not check_release_tag(spec_path):
        spec_correct = False

    if not check_source_attribution(spec_path):
        spec_correct = False

    if not check_license_verification(spec_path):
        spec_correct = False
    
    if not check_toolchain_patch_lines(spec_path, toolchain_specs):
        spec_correct = False

    return spec_correct


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if an RPM spec file follows CBL-Mariner's guidelines.")
    parser.add_argument('toolchain_specs',
                        type=argparse.FileType('r'),
                        help='Path to a file containing a list of toolchain specs.')
    parser.add_argument('specs',
                        metavar='spec_path',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='path to an RPM spec file')
    args = parser.parse_args()
    
    toolchain_specs = set(args.toolchain_specs.read().splitlines())

    specs_correct = True
    for spec in args.specs:
        if not check_spec(spec.name, toolchain_specs):
            specs_correct = False

    if not specs_correct:
        print("""
====================== Spec verification FAILED ======================

Please update the spec files listed above.
""")
        sys.exit(1)
