#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pathlib import Path
from typing import List, Optional

import argparse
import hashlib
import json
import os
import re
import sys

def getSignature(fileName) -> str:
    with open(fileName, "rb") as tarballFile:
        sha256sum = hashlib.sha256()
        while True:
            read_data = tarballFile.read()
            if not read_data:
                break
            sha256sum.update(read_data)
    return sha256sum.hexdigest()

def find_matching_files(path, filename) -> List[str]:
    return_value : List[str] = []
    for matching_file in Path(path).glob(f"**/{filename}"):
        if os.path.exists(matching_file):
            return_value.append(str(matching_file))

    return return_value

def find_name_of_all_spec_and_signatures_json_pairs(path: str) -> List[str]:
    names: List[str] = []
    # Search for all spec files (XXX.spec)
    for spec_path in Path(path).glob("*.spec"):
        if os.path.exists(spec_path):
            name = Path(spec_path).stem
            signature_path = os.path.join(path, f"{name}.signatures.json")
            if os.path.exists(signature_path):
                # If there is a matching signature file (XXX.signatures.json),
                # add it to list
                names.append(name)

    return names

def find_spec_folder_ancestor(path: str) -> Optional[str]:
    # Assume that spec/signatures.json files are only found in
    # SPECS/XX, SPECS-EXTENDED/XX, or SPECS-SIGNED/XX.  Find an
    # ancestor of path that adheres to this assuption.  Return
    # None if not found.
    regex = f".*(SPECS|SPECS-EXTENDED|SPECS-SIGNED){os.sep}[^{os.sep}]+"
    matching_path = re.search(regex, path)
    if matching_path:
        return matching_path.group(0)
    return None

def check_folder(folder):
    signatures_correct = True

    # get SPECS/XX or SPECS-EXTENED/XX ancestor of input
    path = find_spec_folder_ancestor(folder)
    if path is None:
        # no spec/signature files found in path or its ancestors
        return signatures_correct

    for name in find_name_of_all_spec_and_signatures_json_pairs(path):
        signature_path = os.path.join(path, f"{name}.signatures.json")
        with open(signature_path, "r") as f:
            signatures_json = json.load(f)
            for file_to_check, expected_signature in signatures_json["Signatures"].items():
                file_to_check_list = find_matching_files(path, file_to_check)
                if not file_to_check_list:
                    print(f"{file_to_check} is not found in CBL-Mariner, build to verify signature")
                elif len(file_to_check_list) > 1:
                    print(f"ERROR: Unsure which file to validate, detected multiple {file_to_check}: {file_to_check_list}")
                else:
                    actual_signature = getSignature(file_to_check_list[0])
                    if actual_signature != expected_signature:
                        print(f"ERROR: detected a mismatched signature for {file_to_check}, expected [{expected_signature}] does not equal actual [{actual_signature}]")
                        signatures_correct = False

    return signatures_correct

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Tool for checking if a folder containing a signatures.json file contains files with matching signatures.")
    parser.add_argument('folders',
                        metavar='folder_path',
                        nargs='+',
                        help='path to check for signature correctness')
    args = parser.parse_args()

    signatures_correct = True
    for folder_arg in args.folders:
        split_folders = folder_arg.split()
        for folder in split_folders:
            if not check_folder(folder):
                signatures_correct = False

    if signatures_correct:
        print("====================== Signatures verification PASSED ======================")
    else:
        print("""====================== Signatures verification FAILED ======================

Please update the mismatched files listed above.
""")
        sys.exit(1)
