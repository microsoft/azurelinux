#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pyrpm.spec import Spec
from os.path import dirname, realpath

import argparse
import re
import sys

def get_glibc_version():
    glibc_spec = Spec.from_file("SPECS/glibc/glibc.spec")
    epoch_prefix = f"{glibc_spec.epoch}:" if glibc_spec.epoch else ""
    release_without_dist = glibc_spec.release.replace("%{?dist}", "")
    release_suffix = f"-{release_without_dist}"
    glibc_version = epoch_prefix + glibc_spec.version + release_suffix
    return glibc_version

def check_spec(path, glibc_version):
    spec = Spec.from_file(path)
    for br in spec.build_requires:
        if br.name == "glibc-static":
            issues = []
            if not br.version:
                issues.append("  * Does not specify a minimum version for its `glibc-static` BuildRequires")
            if br.version and br.version != glibc_version:
                issues.append("  * Does not specify the latest `glibc-static` version in its BuildRequires")
            if br.operator and br.operator != ">=":
                issues.append(f"  * Uses bad BuildRequire `glibc-static` comparison operator `{br.operator}`")

            if issues:
                print(f"Specfile {spec.name} (at {path}):")
                for issue in issues:
                    print(issue)
                print(f"  Use: `BuildRequires: glibc-static >= {glibc_version}%{{?dist}}`")
                print()
                return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if an RPM spec file correctly handles dependencies for statically linked glibc.")
    parser.add_argument('specs',
                        metavar='spec_path',
                        nargs='+',
                        help='path to an RPM spec file')
    args = parser.parse_args()

    glibc_version = get_glibc_version()

    print(f"glibc-static version detected: {glibc_version}")
    print()

    specs_correct = True
    for spec in args.specs:
        if not check_spec(spec, glibc_version):
            specs_correct = False

    if specs_correct:
        print("====================== Spec verification PASSED ======================")
    else:
        print("""====================== Spec verification FAILED ======================

Please update the spec files listed above.
""")
        sys.exit(1)
