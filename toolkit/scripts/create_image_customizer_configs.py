#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import shutil
import yaml

def get_legacy_config_file(name: str) -> str:
    return f"toolkit/imageconfigs/{name}.json"

def get_image_customizer_config_file(name: str) -> str:
    return f"toolkit/imageconfigs/{name}.yaml"

def load_legacy_config(file: str) -> object:
    with open(file, 'r') as f:
        return json.load(f)

def load_image_customizer_config(file: str) -> object:
    with open(file, 'r') as f:
        return yaml.safe_load(f)

def convert_legacy_to_image_customizer_config(legacy_name: str, ic_name: str) -> None:
    legacy_config = load_legacy_config(get_legacy_config_file(legacy_name))
    ic_config = load_image_customizer_config(get_image_customizer_config_file(ic_name))

def generate_arm64_config_from_amd64_config(amd64_name: str, arm64_name: str, arm64_size: str | None = None) -> None:
    amd64_file = get_image_customizer_config_file(amd64_name)
    arm64_file = get_image_customizer_config_file(arm64_name)
    if arm64_size is None:
        print(f"Generating ARM64 config from {amd64_file!r} to {arm64_file!r}")
        shutil.copyfile(amd64_file, arm64_file)
        return

    print(f"Generating ARM64 config from {amd64_file!r} to {arm64_file!r} with new size {arm64_size!r}")
    amd64_config = load_image_customizer_config(amd64_file)
    if not isinstance(amd64_config, dict):
        sys.exit(f"Expected a dictionary in {amd64_file!r}, got {type(amd64_config)}")


    amd64_config = amd64_config["storage"]["disks"][0]["maxSize"] = arm64_size
    with open(arm64_file, 'w') as f:
        f.write(amd64_config)

def main():
    convert_legacy_to_image_customizer_config("baremetal", "baremetal-amd64")
    generate_arm64_config_from_amd64_config("baremetal-amd64", "baremetal-arm64", "1024M")
    convert_legacy_to_image_customizer_config("core-efi", "hyperv-guest-amd64")
    convert_legacy_to_image_customizer_config("core-efi-aarch64", "hyperv-guest-arm64")
    convert_legacy_to_image_customizer_config("marketplace-gen1", "marketplace-gen1-amd64")
    convert_legacy_to_image_customizer_config("marketplace-gen2-aarch64", "marketplace-gen2-arm64")
    convert_legacy_to_image_customizer_config("qemu-guest", "qemu-guest-amd64")
    generate_arm64_config_from_amd64_config("qemu-guest-amd64", "qemu-guest-arm64")

if __name__ == '__main__':
    main()
