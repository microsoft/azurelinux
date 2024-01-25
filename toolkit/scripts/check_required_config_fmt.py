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

    # Sort the JSON file and write it to a temporary file.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        json.dump(content, f, indent=4, sort_keys=True)
        tmp_file = f.name

    # Compare the sorted JSON file to the original. If they are different,
    # print the diff that can be applied to the JSON file to fix it and
    # exit with a non-zero exit code. Otherwise, print nothing and exit
    # successfully.
    try:
        subprocess.check_call(['git', 'diff',
            '--no-index',
            required_configs,
            tmp_file])
    except subprocess.CalledProcessError:
        sys.exit(1)
    finally:
        os.remove(tmp_file)
