#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pyrpm.spec import Spec
from os.path import dirname, realpath

import argparse
import re
import sys

from spec_source_attributions import get_spec_source, VALID_SOURCE_ATTRIBUTIONS

license_regex = re.compile(
    r"\b(license verified|verified license)\b", re.IGNORECASE)

valid_release_tag_regex = re.compile(
    r'^[1-9]\d*%\{\?dist\}$')

valid_source_attributions_one_per_line = "\n".join(f"- {key}: '{value}'" for key, value in VALID_SOURCE_ATTRIBUTIONS.items())


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


def check_spec(spec_path):
    spec_correct = True

    print(f"Checking {spec_path}")

    if not check_release_tag(spec_path):
        spec_correct = False

    if not check_source_attribution(spec_path):
        spec_correct = False

    if not check_license_verification(spec_path):
        spec_correct = False

    return spec_correct


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if an RPM spec file follows CBL-Mariner's guidelines.")
    parser.add_argument('specs',
                        metavar='spec_path',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='path to an RPM spec file')
    args = parser.parse_args()

    specs_correct = True
    for spec in args.specs:
        if not check_spec(spec.name):
            specs_correct = False

    if not specs_correct:
        print("""
====================== Spec verification FAILED ======================

Please update the spec files listed above.
""")
        sys.exit(1)
