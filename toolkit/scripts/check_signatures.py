#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pathlib import Path
from typing import Optional

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

def find_spec_folder_with_signatures_json(path: str) -> Optional[str]:
    current = Path(path)
    if Path(os.path.join(path, f"{current.name}.spec")).is_file():
        if Path(os.path.join(path, f"{current.name}.signatures.json")).is_file():
            return path
    parent = current.parent
    if parent != current:
        return find_spec_folder_with_signatures_json(f"{parent}")
    return None

def check_folder(folder):
    signatures_correct = True

    print(f"check {folder}")

    # find YY (maybe ancestor of path) that has xx/YY/YY.spec
    path = find_spec_folder_with_signatures_json(folder)
    if path is None:
        # no spec/signature files found in path or its ancestors
        return signatures_correct

    print(f"actually check {path}")

    for signature_path in Path(path).glob("*.signatures.json"):
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
