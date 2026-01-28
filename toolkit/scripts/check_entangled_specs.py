#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from os import path, listdir
from typing import FrozenSet, List
import argparse
import sys

from pyrpm.spec import replace_macros, Spec

# Control output verbosity, keeping this module global since we do not
# have a containing top-level scope
verbose=False

version_release_matching_groups = [
    frozenset([
        "SPECS-SIGNED/kernel-hwe-signed/kernel-hwe-signed.spec",
        "SPECS/kernel-hwe/kernel-hwe.spec",
        "SPECS/kernel-hwe-headers/kernel-hwe-headers.spec"
    ]),
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
        "SPECS-SIGNED/kernel-mshv-signed/kernel-mshv-signed.spec",
        "SPECS/kernel-mshv/kernel-mshv.spec",
    ]),
    frozenset([
        "SPECS-SIGNED/systemd-boot-signed/systemd-boot-signed.spec",
        "SPECS/systemd/systemd.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/edk2-hvloader-signed/edk2-hvloader-signed.spec",
        "SPECS/edk2/edk2.spec"
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
    ]),
    frozenset([
        "SPECS-SIGNED/iser-signed/iser-signed.spec",
        "SPECS/iser/iser.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/iser-hwe-signed/iser-hwe-signed.spec",
        "SPECS/iser-hwe/iser-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/isert-signed/isert-signed.spec",
        "SPECS/isert/isert.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/isert-hwe-signed/isert-hwe-signed.spec",
        "SPECS/isert-hwe/isert-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/knem-modules-signed/knem-modules-signed.spec",
        "SPECS/knem/knem.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/knem-hwe-modules-signed/knem-hwe-modules-signed.spec",
        "SPECS/knem-hwe/knem-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mft_kernel-signed/mft_kernel-signed.spec",
        "SPECS/mft_kernel/mft_kernel.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mft_kernel-hwe-signed/mft_kernel-hwe-signed.spec",
        "SPECS/mft_kernel-hwe/mft_kernel-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mlnx-nfsrdma-signed/mlnx-nfsrdma-signed.spec",
        "SPECS/mlnx-nfsrdma/mlnx-nfsrdma.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mlnx-nfsrdma-hwe-signed/mlnx-nfsrdma-hwe-signed.spec",
        "SPECS/mlnx-nfsrdma-hwe/mlnx-nfsrdma-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mlnx-ofa_kernel-modules-signed/mlnx-ofa_kernel-modules-signed.spec",
        "SPECS/mlnx-ofa_kernel/mlnx-ofa_kernel.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/mlnx-ofa_kernel-hwe-modules-signed/mlnx-ofa_kernel-hwe-modules-signed.spec",
        "SPECS/mlnx-ofa_kernel-hwe/mlnx-ofa_kernel-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/srp-signed/srp-signed.spec",
        "SPECS/srp/srp.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/srp-hwe-signed/srp-hwe-signed.spec",
        "SPECS/srp-hwe/srp-hwe.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/xpmem-modules-signed/xpmem-modules-signed.spec",
        "SPECS/xpmem/xpmem.spec"
    ]),
    frozenset([
        "SPECS-SIGNED/xpmem-hwe-modules-signed/xpmem-hwe-modules-signed.spec",
        "SPECS/xpmem-hwe/xpmem-hwe.spec"
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

def print_verbose(message: str):
    "Print 'message' to stdout if global variable 'verbose' is true."
    if verbose:
        print(message)


def _load_macros_from_file(spec: "Spec", macros_path: str) -> None:
    """Load simple %global macro definitions from a macros file into a Spec.

    This is a minimal loader that understands lines of the form::

        %global name value

    It is primarily used to inject values from files like
    macros.releaseversions so that pyrpm can fully expand spec tags.
    """

    try:
        with open(macros_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if not line.startswith("%global"):
                    continue

                parts = line.split(maxsplit=2)
                if len(parts) < 3:
                    continue

                _, name, value = parts
                # pyrpm stores macros on the Spec instance; update in place.
                # getattr/hasattr used for compatibility with library versions.
                macros = getattr(spec, "macros", None)
                if isinstance(macros, dict):
                    macros[name] = value
    except FileNotFoundError:
        # Best-effort: if the macros file is missing we just skip it.
        return


def _hydrate_spec_with_macros(spec_path: str) -> "Spec":
    """Create a Spec object and preload it with macros from macros.d.

    This wires in macros from known locations (notably macros.releaseversions)
    so that calls to replace_macros() see fully defined values.
    """

    spec = Spec.from_file(spec_path)

    # Primary locations used in CI and builds.
    rpm_macro_dirs = [
        "/usr/lib/rpm/macros.d",
        "/usr/lib/rpm",
        "/etc/rpm/macros.d",
        "/etc/rpm",
    ]
    for macro_dir in rpm_macro_dirs:
        if not path.isdir(macro_dir):
            continue
        for entry in listdir(macro_dir):
            macros_path = path.join(macro_dir, entry)
            if path.isfile(macros_path):
                _load_macros_from_file(spec, macros_path)

    # Fallback: when running locally from a tree where the macros files live
    # under build/pkg_artifacts, try to use that directory if present.
    tree_local_macros_dir = path.join(
        path.dirname(path.dirname(path.abspath(__file__))),
        "build",
        "pkg_artifacts",
    )
    if path.isdir(tree_local_macros_dir):
        for entry in listdir(tree_local_macros_dir):
            macros_path = path.join(tree_local_macros_dir, entry)
            if path.isfile(macros_path):
                _load_macros_from_file(spec, macros_path)

    return spec


def read_spec_tag(spec_path: str, tag: str) -> str:
    """Read a spec header tag via pyrpm with macros.d preloaded.

    The returned value has %macros expanded using pyrpm's replace_macros
    after injecting macros from macros.releaseversions.
    """

    spec = _hydrate_spec_with_macros(spec_path)
    value = getattr(spec, tag)
    if value:
        value = replace_macros(value, spec)
    return value

def check_spec_tags(base_path: str, tags: dict, groups: List[FrozenSet]) -> bool:
    """Check if spec set violates matching rules for any of given tags. Return True/False accordingly."""
    has_error = False
    for group in groups:
        print_verbose(f"Processing group: {group}")
        spec_tag_map = {tag: {} for tag in tags}
        for spec_filename in group:
            spec_path = path.join(base_path, spec_filename)
            print_verbose(f"\t{spec_filename}")

            for tag, tag_current in tags.items():
                tag_value = read_spec_tag(spec_path, tag)
                spec_tag_map[tag][spec_filename] = tag_value
                tag_want = f" (want: {tag_current})" if tag_current else ""
                print_verbose(f"\t\ttag({tag}) value: {tag_value}{tag_want}")
        
        for tag, specs_values in spec_tag_map.items():
            # Skip to next tag if tag value is unique and it matches "tag_expected_value" if set
            value_list = list(specs_values.values())
            tag_expected = tags[tag]
            if len(set(value_list)) > 1 or (tag_expected and value_list[0] != tag_expected):
                has_error = True
                print(f'Mismatch in expected value of "{tag}":{tag_expected or ""}')
                for spec_name, value in specs_values.items():
                    print(f"\t{value:30} => {spec_name}")

    return has_error

def check_matches(base_path: str):
    kernel_headers_spec_path = path.join(base_path, "SPECS/kernel-headers/kernel-headers.spec")
    kernel_headers_version = read_spec_tag(kernel_headers_spec_path, 'version')
    kernel_headers_release = read_spec_tag(kernel_headers_spec_path, 'release')
    kernel_version_release = f"{kernel_headers_version}-{kernel_headers_release}"
    
    groups_to_check = [({'mstflintver':{}}, mstflintver_matching_groups),
                       ({'sdkver':{}}, sdkver_matching_groups),
                       ({'epoch':{}, 'version':{}, 'release':{}}, version_release_matching_groups),
                       ({'epoch':{}, 'version':{}}, version_matching_groups)]
    
    check_result = []
    for check_args in groups_to_check:
        print_verbose(f'Calling check_spec_tags with "{check_args}"')
        check_result.append(check_spec_tags(base_path, *check_args))
    if any(check_result):
        print('The current repository state violates one or more spec entanglement rule!')
        sys.exit(1)
    print('Repository state is consistent with spec entanglement rules.')

def main():
    global verbose

    parser = argparse.ArgumentParser()
    parser.add_argument('repo_root', help='path to the root of the Azure Linux repository')
    parser.add_argument ("--verbose", action="store_true", help='Print details about each action')
    args = parser.parse_args()
    verbose = args.verbose
    check_matches(args.repo_root)

if __name__ == '__main__':
    main()
