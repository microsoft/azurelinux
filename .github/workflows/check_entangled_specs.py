from collections import defaultdict
from pyrpm.spec import Spec
from pathlib import Path

import argparse
import sys

version_release_matching_groups = [
    {
        "SPECS-SIGNED/kernel-signed-x64/kernel-signed-x64.spec",
        "SPECS-SIGNED/kernel-signed-aarch64/kernel-signed-aarch64.spec",
        "SPECS/kernel/kernel.spec"
    },
    {
        "SPECS-SIGNED/grub2-efi-binary-signed-x64/grub2-efi-binary-signed-x64.spec",
        "SPECS-SIGNED/grub2-efi-binary-signed-aarch64/grub2-efi-binary-signed-aarch64.spec",
        "SPECS/grub2/grub2.spec"
    }
]

version_matching_groups = [
    {
        "SPECS/hyperv-daemons/hyperv-daemons.spec",
        "SPECS/kernel/kernel.spec",
        "SPECS/kernel-headers/kernel-headers.spec",
        "SPECS/kernel-hyperv/kernel-hyperv.spec"
    }
]


def check_spec_attributes(base_path, attributes, groups):
    errs = set()
    for group in groups:
        variants = defaultdict(set)
        for spec_filename in group:
            parsed_spec = Spec.from_file(Path(base_path, spec_filename))
            for attribute in attributes:
                variants[attribute].add(getattr(
                    parsed_spec, attribute))
        for attribute in variants:
            if len(variants[attribute]) > 1:
                errs.add(group)
    return errs


def check_version_release_match_groups(base_path):
    return check_spec_attributes(base_path, ['version', 'release'], version_release_matching_groups)


def check_version_match_groups(base_path):
    return check_spec_attributes(base_path, ['version'], version_matching_groups)


def check_matches(base_path):
    version_match_results = check_version_match_groups(base_path)
    version_release_match_results = check_version_release_match_groups(
        base_path)

    if len(version_match_results) or len(version_release_match_results):
        print('#####')
        print('This repository violates a spec entanglement rule!')

        if len(version_match_results):
            print(
                'Please update the following sets of specs to have the same version attributes:')
            for e in version_match_results:
                print(e)

        if len(version_release_match_results):
            print(
                'Please update the following sets of specs to have the same version and release attributes:')
            for e in version_release_match_results:
                print(e)
        print('#####')
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_root', help='path to the root of the CBL-Mariner repository')
    args = parser.parse_args()
    check_matches(args.repo_root)
