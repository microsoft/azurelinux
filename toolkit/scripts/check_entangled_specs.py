#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from collections import defaultdict
from os import path
from typing import FrozenSet, List, Set
import argparse
import pprint
import sys

from pyrpm.spec import replace_macros, Spec

version_release_matching_groups = [
    frozenset([
        "SPECS-SIGNED/kernel-signed/kernel-signed.spec",
        "SPECS-SIGNED/kernel-64k-signed/kernel-64k-signed.spec",
        "SPECS-SIGNED/kernel-uki-signed/kernel-uki-signed.spec",
        "SPECS/kernel/kernel.spec",
        "SPECS/kernel-64k/kernel-64k.spec",
        "SPECS/kernel/kernel-uki.spec",
        "SPECS/kernel-headers/kernel-headers.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/systemd-boot-signed/systemd-boot-signed.spec",
        "SPECS/systemd/systemd.spec"
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
    ]),
    frozenset([
        "SPECS/shim/shim.spec",
        "SPECS/shim-unsigned-x64/shim-unsigned-x64.spec",
        "SPECS/shim-unsigned-aarch64/shim-unsigned-aarch64.spec"
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
        "SPECS/libcxx/libcxx.spec",
        "SPECS/lld/lld.spec",
        "SPECS/lldb/lldb.spec",
        "SPECS/llvm/llvm.spec"
    ])
]

sdkver_matching_groups = [
    frozenset([
        "SPECS/glslang/glslang.spec",
        "SPECS/spirv-tools/spirv-tools.spec",
        "SPECS/spirv-headers/spirv-headers.spec"
    ])
]

mstflintver_matching_groups = [
    frozenset([
        "SPECS/mstflint/mstflint.spec",
        "SPECS/kernel/kernel.spec"
    ])
]

def check_spec_tags(base_path: str, tags: List[str], groups: List[FrozenSet]) -> Set[FrozenSet]:
    """Returns spec sets which violate matching rules for given tags. """
    err_groups = set()
    for group in groups:
        variants = defaultdict(set)

        for spec_filename in group:
            parsed_spec = Spec.from_file(path.join(base_path, spec_filename))
            for tag in tags:
                tag_value = get_tag_value(parsed_spec, tag)
                variants[tag].add(tag_value)

        for tag in tags:
            if len(variants[tag]) > 1: err_groups.add(group)
    return err_groups


def check_mstflintver_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['mstflintver'], mstflintver_matching_groups)

def check_sdkver_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['sdkver'], sdkver_matching_groups)

def check_version_release_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['epoch', 'version', 'release'], version_release_matching_groups)

def check_version_match_groups(base_path: str) -> Set[FrozenSet]:
    return check_spec_tags(base_path, ['epoch', 'version'], version_matching_groups)


def check_matches(base_path: str):
    version_match_errors = check_version_match_groups(base_path)
    version_release_match_errors = check_version_release_match_groups(base_path)
    sdkver_match_errors = check_sdkver_match_groups(base_path)
    mstflintver_match_errors = check_mstflintver_match_groups(base_path)

    printer = pprint.PrettyPrinter()

    if len(version_match_errors) or len(version_release_match_errors) or len(sdkver_match_errors) or len(mstflintver_match_errors):
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

        if len(sdkver_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same "sdkver" global variables:')
            for e in sdkver_match_errors:
                printer.pprint(e)
        
        if len(mstflintver_match_errors):
            print(
                '\nPlease update the following sets of specs to have the same "mstflintver" global variables:')
            for e in mstflintver_match_errors:
                printer.pprint(e)
                
        sys.exit(1)


def get_tag_value(spec: "Spec", tag: str) -> str:
    value = getattr(spec, tag)
    if value:
        value = replace_macros(value, spec)
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_root', help='path to the root of the Azure Linux repository')
    args = parser.parse_args()
    check_matches(args.repo_root)
