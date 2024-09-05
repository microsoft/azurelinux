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

EXPECTED_DISTRIBUTION_TAG = "Azure Linux"
EXPECTED_VENDOR_TAG = "Microsoft Corporation"

# Checking if the specs contains a 'Distribution' tag.
DISTRIBUTION_TAG_PRESENT_REGEX = re.compile(r"^\s*Distribution:\s*", re.MULTILINE)

# Checking if the specs include only the valid 'Distribution: Azure Linux' tag.
INVALID_DISTRIBUTION_TAG_REGEX = re.compile(
    rf"^\s*Distribution:\s*(?!{EXPECTED_DISTRIBUTION_TAG}\s*$)\S+", re.MULTILINE
)

# Checking if the specs include only the valid 'Vendor: Microsoft Corporation' tag.
INVALID_VENDOR_TAG_REGEX = re.compile(
    rf"^\s*Vendor:\s*(?!{EXPECTED_VENDOR_TAG}\s*$)\S+", re.MULTILINE
)

# Checking if the specs contains a 'Vendor' tag.
VENDOR_TAG_PRESENT_REGEX = re.compile(r"^\s*Vendor:\s*", re.MULTILINE)

# Checking for the deprecated '%patch[number]' format.
# For more info, see: https://rpm-software-management.github.io/rpm/manual/spec.html.
INVALID_PATCH_MACRO_REGEX = re.compile(r"^\s*%patch\d", re.MULTILINE)

# Check for '%patch' macros not using the '-P' flag.
INVALID_TOOLCHAIN_PATCH_MACRO = re.compile(r"^\s*%patch((?!-P\s+\d+).)*$", re.MULTILINE)

LICENSE_REGEX = re.compile(r"\b(license verified|verified license)\b", re.IGNORECASE)

VALID_RELEASE_TAG_REGEX = re.compile(r"^[1-9]\d*%\{\?dist\}$")

VALID_SOURCE_ATTRIBUTIONS_ONE_PER_LINE = "\n".join(
    f"- {key}: '{value}'" for key, value in VALID_SOURCE_ATTRIBUTIONS.items()
)


def check_distribution_tag_correct(spec_path: str):
    """Checks if the 'Distribution' tags match 'Azure Linux'. """
    with open(spec_path) as file:
        contents = file.read()

    if INVALID_DISTRIBUTION_TAG_REGEX.search(contents) is not None:
        print(f"""
ERROR: detected an invalid 'Distribution' tag.

    Please use 'Distribution: {EXPECTED_DISTRIBUTION_TAG}'.
""")
        return False

    return True


def check_distribution_tag_exists(spec_path: str):
    """Checks if the 'Distribution' tag exists. """
    with open(spec_path) as file:
        contents = file.read()

    if DISTRIBUTION_TAG_PRESENT_REGEX.search(contents) is None:
        print(f"""
ERROR: missing 'Distribution' tag.

    Please add 'Distribution: {EXPECTED_DISTRIBUTION_TAG}'.
""")
        return False

    return True


def check_patch_macro(spec_path: str):
    """Checks if the 'patch' macro is not in the format deprecated in RPM 4.18+. """
    with open(spec_path) as file:
        contents = file.read()

    if INVALID_PATCH_MACRO_REGEX.search(contents) is not None:
        print(f"""
ERROR: use of deprecated '%patch[number]' format (no space between '%patch' and the number of the patch).

    Accepted formats are:

        - %patch [number]
        - %patch -P [number]
""")
        return False

    return True


def check_release_tag(spec_path: str):
    """Checks if the 'Release' tag is in one of Azure Linux's expected formats. """
    spec = Spec.from_file(spec_path)

    if VALID_RELEASE_TAG_REGEX.match(spec.release) is None:
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

    if len(LICENSE_REGEX.findall(spec.changelog)) == 0:
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

{VALID_SOURCE_ATTRIBUTIONS_ONE_PER_LINE}

    If you're importing a spec from a source, which doesn't fit the currently supported list,
    please update the 'VALID_SOURCE_ATTRIBUTIONS' variable inside the '{dirname(realpath(__file__))}/spec_source_attributions.py' script.
""")

    return False


def check_toolchain_patch_lines(spec_path: str, toolchain_specs: set):
    """Checks if a toolchain spec file applies patches using the '%patch -P [number]' format.
       RPM < 4.18 will fail building a spec otherwise and toolchain specs are parsed directly on the host,
       which may have older versions of RPM.
    """

    if Path(spec_path).stem not in toolchain_specs:
        return True

    with open(spec_path) as file:
        contents = file.read()

    if INVALID_TOOLCHAIN_PATCH_MACRO.search(contents) is not None:
        print(f"""
ERROR: detected a toolchain spec with invalid '%patch' macros.

    Toolchain specs may only use the '%patch -P [number]' format.
    Using '%patch[number]' or '%patch' without the '-P' flag will cause RPM < 4.18 to fail building the spec.
""")
        return False

    return True


def check_vendor_tag_correct(spec_path: str):
    """Checks if the 'Vendor' tags match 'Microsoft Corporation'. """
    with open(spec_path) as file:
        contents = file.read()

    if INVALID_VENDOR_TAG_REGEX.search(contents) is not None:
        print(f"""
ERROR: detected an invalid 'Vendor' tag.

    Please use 'Vendor: {EXPECTED_VENDOR_TAG}'.
""")
        return False

    return True


def check_vendor_tag_exists(spec_path: str):
    """Checks if the 'Vendor' tag exists. """
    with open(spec_path) as file:
        contents = file.read()

    if VENDOR_TAG_PRESENT_REGEX.search(contents) is None:
        print(f"""
ERROR: missing 'Vendor' tag.

    Please add 'Vendor: {EXPECTED_VENDOR_TAG}'.
""")
        return False

    return True


SPEC_CHECKS = [
    check_distribution_tag_correct,
    check_distribution_tag_exists,
    check_license_verification,
    check_patch_macro,
    check_release_tag,
    check_source_attribution,
    check_vendor_tag_correct,
    check_vendor_tag_exists,
]


def check_spec(spec_path, toolchain_specs):
    spec_correct = True

    print(f"Checking {spec_path}.")

    for spec_check in SPEC_CHECKS:
        if not spec_check(spec_path):
            spec_correct = False

    if not check_toolchain_patch_lines(spec_path, toolchain_specs):
        spec_correct = False

    return spec_correct


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if an RPM spec file follows Azure Linux's guidelines.")
    parser.add_argument('--toolchain_specs',
                        metavar='toolchain_specs',
                        dest='toolchain_specs',
                        help='a list of toolchain specs')
    parser.add_argument('--specs',
                        metavar='spec_path',
                        dest='specs',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='path to an RPM spec file')
    args = parser.parse_args()

    toolchain_specs = set(args.toolchain_specs.split())

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
