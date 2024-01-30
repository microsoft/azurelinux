#!/usr/bin/env python3


import argparse
import json
import subprocess
import sys
import tempfile


from sort_required_configs import sort_required_config_lists


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check that a JSON of required configs is sorted and indented"
    )
    parser.add_argument(
        "--path", help="path to JSON of required configs", required=True
    )
    args = parser.parse_args()
    path = args.path

    with open(path, "r") as f:
        config = json.load(f)

    sort_required_config_lists(config)

    # Sort the JSON file and write it to a temporary file.
    with tempfile.NamedTemporaryFile(mode="w") as f:
        json.dump(config, f, indent=4, sort_keys=True)
        f.write("\n")

        # Flush the file to disk before passing it to 'git diff' below so
        # that the entire contents of the file are checked against the
        # original.
        f.flush()

        # Compare the sorted JSON file to the original. If they are different,
        # print the diff that can be applied to the JSON file to fix it and
        # exit with a non-zero exit code. Otherwise, print nothing and exit
        # successfully.
        try:
            subprocess.check_call(["git", "diff", "--no-index", path, f.name])
        except subprocess.CalledProcessError:
            print(
                "\n"
                f"The JSON file at {path} is not sorted and indented correctly.\n"
                f"Apply the patch above or run 'toolkit/scripts/sort_required_configs.py {path}' to fix it.",
                file=sys.stderr,
            )
            sys.exit(1)
