#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pathlib import Path
from typing import List, Optional

import argparse
import hashlib
import json
import os
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

def find_file_and_check(path, filename, expected_signature) -> Optional[bool]:
    path_to_check = os.path.join(path, filename)
    if Path(path_to_check).is_file():
        actual_signature = getSignature(path_to_check)
        if actual_signature == expected_signature:
            return True
        print(f"ERROR: detected a mismatched signature for {filename}, expected [{expected_signature}] does not equal actual [{actual_signature}]")
        return False

    for content in os.listdir(path):
        path_to_check = os.path.join(path, content)
        if os.path.isdir(path_to_check):
            result = find_file_and_check(path_to_check, filename, expected_signature)
            if result is not None:
                return result

    return None

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

def find_spec_folder_with_signatures_json(path: str) -> Optional[str]:
    # Use this path if there are any spec files (XXX.spec) that have
    # a matching signature file (XXX.signatures.json)
    names = find_name_of_all_spec_and_signatures_json_pairs(path)
    if len(names) > 0:
        return path

    # No spec/signatures.json combo found in this folder,
    # check the parent folder (unless the parent folder IS
    # THE SAME as this folder)
    current = Path(path)
    parent = current.parent
    if parent != current:
        return find_spec_folder_with_signatures_json(f"{parent}")

    # If nothing is found, return None
    return None

def check_folder(folder):
    signatures_correct = True

    # find YY (maybe ancestor of path) that has xx/YY/YY.spec
    path = find_spec_folder_with_signatures_json(folder)
    if path is None:
        # no spec/signature files found in path or its ancestors
        return signatures_correct

    names = find_name_of_all_spec_and_signatures_json_pairs(path)
    for name in names:
        signature_path = os.path.join(path, f"{name}.signatures.json")
        with open(signature_path, "r") as f:
            signatures_json = json.load(f)
            for file_to_check, expected_signature in signatures_json["Signatures"].items():
                result = find_file_and_check(path, file_to_check, expected_signature)
                if result is None:
                    print(f"{file_to_check} is not found in CBL-Mariner, build to verify signature")
                elif result is False:
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
