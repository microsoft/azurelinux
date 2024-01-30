#!/usr/bin/env python3


import argparse
import json


def sort_required_config_lists(config: str) -> None:
    # Sort lists, which is not something done by json.dump.
    for _, info in config["kernel"]["required-configs"].items():
        info["PR"] = sorted(info["PR"])
        info["arch"] = sorted(info["arch"])
        info["value"] = sorted(info["value"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sort and indent the JSON of required configs"
    )
    parser.add_argument("path", help="path to JSON of required configs")
    args = parser.parse_args()
    path = args.path

    with open(path, "r") as f:
        config = json.load(f)

    sort_required_config_lists(config)

    with open(path, "w") as f:
        json.dump(config, f, indent=4, sort_keys=True)
        f.write("\n")
