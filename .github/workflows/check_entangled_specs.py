from typing import FrozenSet, List, Set
from pyrpm.spec import Spec

import argparse
from collections import defaultdict
from pathlib import Path
import pprint
import sys

version_release_matching_groups = [
    frozenset([
        "SPECS-SIGNED/kernel-signed-x64/kernel-signed-x64.spec",
        "SPECS-SIGNED/kernel-signed-aarch64/kernel-signed-aarch64.spec",
        "SPECS/kernel/kernel.spec",
        "SPECS/kernel-headers/kernel-headers.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/grub2-efi-binary-signed-x64/grub2-efi-binary-signed-x64.spec",
        "SPECS-SIGNED/grub2-efi-binary-signed-aarch64/grub2-efi-binary-signed-aarch64.spec",
        "SPECS/grub2/grub2.spec"
    ])
]

version_matching_groups = [
    frozenset([
        "SPECS/hyperv-daemons/hyperv-daemons.spec",
        "SPECS/kernel/kernel.spec",
        "SPECS/kernel-hyperv/kernel-hyperv.spec"
    ])
]


def check_spec_attributes(base_path: str, attributes: List[str], groups: List[FrozenSet]) -> Set[FrozenSet]:
    """Returns spec sets which violate matching rules for given attributes"""
    err_groups = set()
    for group in groups:
        variants = defaultdict(set)

        for spec_filename in group:
            parsed_spec = Spec.from_file(Path(base_path, spec_filename))
            for attribute in attributes:
                variants[attribute].add(getattr(
                    parsed_spec, attribute))

        for attribute in variants:
            if len(variants[attribute]) > 1:
                err_groups.add(group)
    return err_groups


def check_version_release_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_attributes(base_path, ['version', 'release'], version_release_matching_groups)


def check_version_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_attributes(base_path, ['version'], version_matching_groups)


def check_matches(base_path: str):
    version_match_errors = check_version_match_groups(base_path)
    version_release_match_errors = check_version_release_match_groups(
        base_path)

    printer = pprint.PrettyPrinter()

    if len(version_match_errors) or len(version_release_match_errors):
        print('The current repository state violates a spec entanglement rule!')

        if len(version_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same version attributes:')
            for e in version_match_errors:
                printer.pprint(e)

        if len(version_release_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same version and release attributes:')
            for e in version_release_match_errors:
                printer.pprint(e)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_root', help='path to the root of the CBL-Mariner repository')
    args = parser.parse_args()
    check_matches(args.repo_root)
