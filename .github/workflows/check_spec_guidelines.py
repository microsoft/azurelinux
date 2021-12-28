#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pyrpm.spec import Spec

import argparse
import re
import sys

license_regex = re.compile(
    r"\b(license verified|verified license)\b", re.IGNORECASE)

valid_release_tag_regex = re.compile(
    r'^([1-9]\d*|%\{release_number\})%\{\?dist\}$')

valid_source_attributions = {
    "Microsoft":                    r'\n-\s+(Original version for CBL-Mariner|Initial CBL-Mariner import from Azure)( \(license: MIT\))?(\.|\n|$)',
    "CentOS":                       r'\n-\s+Initial CBL-Mariner import from CentOS \d+ \(license: MIT\)(\.|\n|$)',
    "Ceph source":                  r'\n-\s+Initial CBL-Mariner import from Ceph source \(license: LGPLv2.1\)(\.|\n|$)',
    "Fedora":                       r'\n-\s+Initial CBL-Mariner import from Fedora \d+ \(license: MIT\)(\.|\n|$)',
    "Magnus Edenhill Open Source":  r'\n-\s+Initial CBL-Mariner import from Magnus Edenhill Open Source \(license: BSD\)(\.|\n|$)',
    "NVIDIA":                       r'\n-\s+Initial CBL-Mariner import from NVIDIA \(license: ASL 2\.0\)(\.|\n|$)',
    "OpenMamba":                    r'\n-\s+Initial CBL-Mariner import from OpenMamba(\.|\n|$)',
    "OpenSUSE":                     r'\n-\s+Initial CBL-Mariner import from openSUSE \w+ \(license: same as "License" tag\)(\.|\n|$)',
    "Photon":                       r'\n-\s+Initial CBL-Mariner import from Photon \(license: Apache2\)(\.|\n|$)'
}

valid_source_attributions_regex = [ re.compile(x) for x in valid_source_attributions.values() ]
valid_source_attributions_one_per_line = "\n".join(f"- {key}: '{value}'" for key, value in valid_source_attributions.items())


def check_release_tag(spec_path: str):
    """Checks if the 'Release' tag is in one of CBL-Mariner's expected formats. """
    spec = Spec.from_file(spec_path)

    if valid_release_tag_regex.match(spec.release) is None:
        print(f"""
ERROR: invalid 'Release' tag.

    Accepted formats are:
    - '[number]%{{?dist}}' (example: 10%{{?dist}}),
    - '%{{release_number}}%{{?dist}}', where the value of 'release_number' must be a single number.
""")
        return False

    if "release_number" in spec.release:
        if not spec.macros["release_number"].isdigit():
            print(f"""
ERROR: invalid 'Release' tag.

    The 'release_number' macro must be a plain number (no nested macros).
    Found '{spec.macros["release_number"]}' instead.
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

    NOTE: for the 'License' tag please use the names from the "Short Name" column inside Fedora's licensing guidelines:
          https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
""")
        return False

    return True


def check_source_attribution(spec_path: str):
    """Checks if we have indicated the source of the spec file in the changelog. """
    spec = Spec.from_file(spec_path)

    for attribution_regex in valid_source_attributions_regex:
        if attribution_regex.findall(spec.changelog):
            return True

    print(f"""
ERROR: no valid source attribution.

    Make sure to indicate the origin of the spec file in the changelog.
    Currently supported source attributions (in form of regular expressions):

{valid_source_attributions_one_per_line}

    If you're importing a spec from a source, which doesn't fit the currently supported list,
    please update the 'valid_source_attributions' variable inside the '{__file__}' script.
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
