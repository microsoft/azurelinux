#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Interactively add a new kernel configuration to the JSON file.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from kernel_config_checker.schema.schema import (
    IntentionalKernelConfigSchema,
    save_schema,
)


def _select_override(data: dict) -> str:
    """Prompt user to select or create an override section."""
    overrides = data.get("overrides", [])
    if not overrides:
        print("No override sections found. Creating 'kernel' override...")
        return "kernel"

    print("\nAvailable override sections:")
    for i, override in enumerate(overrides):
        name = override.get("name", f"override-{i}")
        count = len(override.get("kernel_configs", []))
        print(f"  {i + 1}. {name} ({count} configs)")

    if len(overrides) == 1:
        name = overrides[0].get("name", "kernel")
        print(f"Using: {name}")
        return name

    while True:
        choice = input(
            f"\nSelect override (1-{len(overrides)})" " or enter new name: "
        ).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(overrides):
                return overrides[idx].get("name", f"override-{idx}")
        else:
            return choice


def _find_existing(configs: list, name: str) -> Optional[int]:
    """Return the index of an existing config with the given name, or None."""
    for i, cfg in enumerate(configs):
        if cfg.get("name") == name:
            return i
    return None


def _insert_or_replace(configs: list, new_config: dict) -> bool:
    """Insert config, prompting to replace if a duplicate exists.

    Returns True if the config was added/replaced, False if the user declined.
    """
    idx = _find_existing(configs, new_config["name"])
    if idx is not None:
        print(f"⚠  {new_config['name']} already exists in this section.")
        choice = input("Replace existing entry? [y/N]: ").strip().lower()
        if choice != "y":
            print("Aborted.")
            return False
        configs[idx] = new_config
    else:
        configs.append(new_config)
    return True


def _add_config_to_data(
    data: dict, new_config: dict, override_name: Optional[str]
) -> Optional[str]:
    """Add a config entry to the data dict. Returns section label or None if aborted."""
    if override_name is None:
        if "default" not in data:
            data["default"] = {
                "name": "default",
                "kernel_configs": [],
            }
        if not _insert_or_replace(data["default"]["kernel_configs"], new_config):
            return None
        return "default section"

    for override in data.get("overrides", []):
        if override.get("name") == override_name:
            if not _insert_or_replace(override["kernel_configs"], new_config):
                return None
            return f"'{override_name}' override section"

    if "overrides" not in data:
        data["overrides"] = []
    data["overrides"].append(
        {"name": override_name, "kernel_configs": [new_config]}
    )
    print(f"Created new override section: {override_name}")
    return f"'{override_name}' override section"


def add_config_interactive(schema_path: Path) -> None:
    """Interactively add a new kernel config to the JSON file."""
    print("Adding new kernel configuration...")

    config_name = input("Enter config name (e.g., CONFIG_EXAMPLE): ").strip()
    if not config_name.startswith("CONFIG_"):
        config_name = "CONFIG_" + config_name

    if config_name == "CONFIG_" or not config_name[len("CONFIG_"):].replace("_", "").isalnum():
        print("❌ Error: Invalid config name. Must be a non-empty"
              " alphanumeric symbol like CONFIG_EXAMPLE")
        return

    print(
        "\nEnter values for each architecture"
        " (y/n/m or specific value, leave blank to skip):"
    )
    x86_64_value = input("x86_64 value: ").strip()
    arm64_value = input("arm64 value: ").strip()

    justification = input("\nEnter justification: ").strip()
    if not justification:
        print("❌ Error: Justification is required for auditability")
        return

    with open(schema_path, "r") as f:
        data = json.load(f)

    target = input("\nAdd to [d]efault or [o]verride? [d]: ").strip().lower()
    override_name = _select_override(data) if target.startswith("o") else None

    values = []
    if x86_64_value:
        values.append({"architecture": "x86_64", "value": x86_64_value})
    if arm64_value:
        values.append({"architecture": "arm64", "value": arm64_value})

    if not values:
        print("❌ Error: At least one architecture value" " must be provided")
        return

    new_config = {
        "name": config_name,
        "values": values,
        "justification": justification,
    }

    section_label = _add_config_to_data(data, new_config, override_name)
    if section_label is None:
        return

    try:
        validated = IntentionalKernelConfigSchema.model_validate(data)
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return

    save_schema(validated, schema_path)
    print(f"✓ Added {config_name} to {section_label}")
    print(f"✓ Updated {schema_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Interactively add a new kernel config"
    )
    parser.add_argument(
        "json_file", help="Path to the intentional config JSON file"
    )
    args = parser.parse_args()

    try:
        add_config_interactive(Path(args.json_file))
        return 0
    except Exception as e:
        print(f"✗ Error adding config: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
