#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
import tempfile
import os

if __name__ == '__main__':
    # Load the JSON file from the command line argument.
    parser = argparse.ArgumentParser(description='Check that a JSON file is sorted and indented')
    parser.add_argument('--required_configs', help='path to JSON of required configs', required=True)
    args = parser.parse_args()
    required_configs = args.required_configs
    with open(required_configs, 'r') as f:
        content = json.load(f)

    # Sort lists, which is not something done by json.dump.
    for config, info in content["kernel"]["required-configs"].items():
        info["PR"] = sorted(info["PR"])
        info["arch"] = sorted(info["arch"])
        info["value"] = sorted(info["value"])

    # Sort the JSON file and write it to a temporary file.
    with tempfile.NamedTemporaryFile(mode='w') as f:
        json.dump(content, f, indent=4, sort_keys=True)

        # Flush the file to disk before passing it to 'git diff' below so
        # that the entire contents of the file are checked against the
        # original.
        f.flush()

        # Compare the sorted JSON file to the original. If they are different,
        # print the diff that can be applied to the JSON file to fix it and
        # exit with a non-zero exit code. Otherwise, print nothing and exit
        # successfully.
        try:
            subprocess.check_call(['git', 'diff',
                '--no-index',
                required_configs,
                f.name])
        except subprocess.CalledProcessError:
            sys.exit(1)
