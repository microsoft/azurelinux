#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import json
import os
import sys
from collections import defaultdict

_REPO_KEY = "Repo"
_SPEC_PATH_KEY = "SpecPath"
_SRPM_PATH_KEY = "SrpmPath"


def find_srpm_duplicates(specs_file_paths: list[str]) -> list[tuple[str, set[str]]]:
    """
    Analyze multiple specs JSON files to find specs producing the same SRPM.
    """
    srpm_to_specs = defaultdict(set)

    for specs_file_path in specs_file_paths:
        with open(specs_file_path, "r") as f:
            data = json.load(f)

        if _REPO_KEY not in data:
            raise ValueError(
                f"Invalid JSON format in {specs_file_path}. Expected '{_REPO_KEY}' key."
            )

        # Process each item in the repo
        for item in data["Repo"]:
            if _SRPM_PATH_KEY not in item or _SPEC_PATH_KEY not in item:
                raise ValueError(
                    f"Invalid JSON format in {specs_file_path}. Expected '{_SPEC_PATH_KEY}' and '{_SRPM_PATH_KEY}' keys in each element of '{_REPO_KEY}'."
                )

            srpm = os.path.basename(item[_SRPM_PATH_KEY])
            srpm_to_specs[srpm].add(item[_SPEC_PATH_KEY])

    return [
        (srpm, specs_paths)
        for srpm, specs_paths in srpm_to_specs.items()
        if len(specs_paths) > 1
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "specs_file_paths",
        nargs="+",
        help="Paths to the specs JSON files to analyze.",
    )
    args = parser.parse_args()

    srpm_duplicates = find_srpm_duplicates(args.specs_file_paths)
    if srpm_duplicates:
        print("Error: detected specs building the same SRPM.", file=sys.stderr)
        for srpm, specs_paths in srpm_duplicates:
            print(f"{srpm}:", file=sys.stderr)
            for spec_path in specs_paths:
                print(f"  - {spec_path}", file=sys.stderr)
            print(file=sys.stderr)
        sys.exit(1)

    print("No SRPM duplicates found.")
