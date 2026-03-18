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


def _add_config_to_data(
    data: dict, new_config: dict, override_name: Optional[str]
) -> str:
    """Add a config entry to the data dict."""
    if override_name is None:
        if "default" not in data:
            data["default"] = {
                "name": "default",
                "kernel_configs": [],
            }
        data["default"]["kernel_configs"].append(new_config)
        return "default section"

    for override in data.get("overrides", []):
        if override.get("name") == override_name:
            override["kernel_configs"].append(new_config)
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

    print(
        "\nEnter values for each architecture"
        " (y/n/m or specific value, leave blank to skip):"
    )
    x86_64_value = input("x86_64 value: ").strip()
    arm64_value = input("arm64 value: ").strip()

    justification = input("\nEnter justification: ").strip()

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
