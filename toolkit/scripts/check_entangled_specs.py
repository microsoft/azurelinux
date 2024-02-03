#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import FrozenSet, List, Set
from pyrpm.spec import Spec

import argparse
from collections import defaultdict
from pathlib import Path
import pprint
import sys

version_release_matching_groups = [
    frozenset([
        "SPECS-SIGNED/kernel-signed/kernel-signed.spec",
        "SPECS/kernel/kernel.spec",
        "SPECS/kernel-headers/kernel-headers.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/kernel-hci-signed/kernel-hci-signed.spec",
        "SPECS/kernel-hci/kernel-hci.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/grub2-efi-binary-signed/grub2-efi-binary-signed.spec",
        "SPECS/grub2/grub2.spec"
    ]),
    frozenset([
        "SPECS/ca-certificates/ca-certificates.spec",
        "SPECS/prebuilt-ca-certificates/prebuilt-ca-certificates.spec",
        "SPECS/prebuilt-ca-certificates-base/prebuilt-ca-certificates-base.spec"
    ]),
    frozenset([
        "SPECS/jflex/jflex.spec",
        "SPECS/jflex/jflex-bootstrap.spec"
    ]),
    frozenset([
        "SPECS/cyrus-sasl/cyrus-sasl.spec",
        "SPECS/cyrus-sasl-bootstrap/cyrus-sasl-bootstrap.spec"
    ])
]

version_matching_groups = [
    frozenset([
        "SPECS/hyperv-daemons/hyperv-daemons.spec",
        "SPECS/kernel/kernel.spec"
    ]),
    frozenset([
        "SPECS/python-flit/python-flit.spec",
        "SPECS/python-flit-core/python-flit-core.spec"
    ]),
    frozenset([
        "SPECS/influxdb/influxdb.spec",
        "SPECS/influx-cli/influx-cli.spec"
    ]),
    frozenset([
        "SPECS/clang/clang.spec",
        "SPECS/compiler-rt/compiler-rt.spec",
        "SPECS/lld/lld.spec",
        "SPECS/lldb/lldb.spec",
        "SPECS/llvm/llvm.spec"
    ])
]


def check_spec_tags(base_path: str, tags: List[str], groups: List[FrozenSet]) -> Set[FrozenSet]:
    """Returns spec sets which violate matching rules for given tags. """
    err_groups = set()
    for group in groups:
        variants = defaultdict(set)

        for spec_filename in group:
            parsed_spec = Spec.from_file(Path(base_path, spec_filename))
            for tag in tags:
                variants[tag].add(getattr(
                    parsed_spec, tag))

        for tag in tags:
            if len(variants[tag]) > 1:
                err_groups.add(group)
    return err_groups


def check_version_release_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['epoch', 'version', 'release'], version_release_matching_groups)


def check_version_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['epoch', 'version'], version_matching_groups)


def check_matches(base_path: str):
    version_match_errors = check_version_match_groups(base_path)
    version_release_match_errors = check_version_release_match_groups(
        base_path)

    printer = pprint.PrettyPrinter()

    if len(version_match_errors) or len(version_release_match_errors):
        print('The current repository state violates a spec entanglement rule!')

        if len(version_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same "Epoch" and "Version" tags:')
            for e in version_match_errors:
                printer.pprint(e)

        if len(version_release_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same "Epoch", "Version", and "Release" tags:')
            for e in version_release_match_errors:
                printer.pprint(e)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_root', help='path to the root of the CBL-Mariner repository')
    args = parser.parse_args()
    check_matches(args.repo_root)
