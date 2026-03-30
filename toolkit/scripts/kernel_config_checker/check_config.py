#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Simple kernel config checker script.
Checks a Linux kernel .config file against intentional configuration settings.
"""

import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from kernel_config_checker.add_config import add_config_interactive
from kernel_config_checker.schema.schema import (
    IntentionalKernelConfigSchema,
    KernelConfig,
    load_schema,
)


def _resolve_value(value) -> str:
    """Resolve an enum or string config value to its string representation."""
    return value.value if isinstance(value, Enum) else value


def _get_arch_value(
    kernel_config: KernelConfig, architecture: str
) -> Optional[str]:
    """Get the resolved value for a specific architecture, or None if not found."""
    for arch_pair in kernel_config.values:
        if arch_pair.architecture.value == architecture:
            return _resolve_value(arch_pair.value)
    return None


def _collect_configs(
    kernel_configs: List[KernelConfig], architecture: str, source: str
) -> Dict[str, dict]:
    """Collect config expectations for a given architecture."""
    configs = {}
    for kc in kernel_configs:
        value = _get_arch_value(kc, architecture)
        if value is not None:
            configs[kc.name] = {
                "expected": value,
                "justification": kc.justification,
                "source": source,
            }
    return configs


def parse_kernel_config(config_path: Path) -> Dict[str, str]:
    """Parse a Linux kernel .config file."""
    config = {}
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") and "is not set" in line:
                config_name = line.split()[1]
                config[config_name] = "n"
            elif line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key] = value
    return config


def check_kernel_config(
    actual_config: Dict[str, str],
    schema: IntentionalKernelConfigSchema,
    kernel_name: str,
    architecture: str,
) -> bool:
    """Check if actual kernel config matches intentional config."""
    print(f"Checking kernel config for: {kernel_name} ({architecture})")

    all_configs = _collect_configs(
        schema.default.kernel_configs, architecture, "default"
    )

    for override in schema.overrides:
        if override.name == kernel_name:
            print(f"✓ Found kernel-specific overrides for '{kernel_name}'")
            all_configs.update(
                _collect_configs(
                    override.kernel_configs,
                    architecture,
                    f"override ({kernel_name})",
                )
            )
            break

    print(
        f"✓ Checking {len(all_configs)} configurations (default + overrides)"
    )

    errors = []
    for config_name, config_info in all_configs.items():
        expected_value = config_info["expected"]
        actual_value = actual_config.get(config_name, "n")

        if actual_value != expected_value:
            error_msg = f"  ✗ {config_name}: expected '{expected_value}', got '{actual_value}' (from {config_info['source']})"
            errors.append(error_msg)
            print(error_msg)

    if errors:
        correct_count = len(all_configs) - len(errors)
        print(
            f"\n✗ Found {len(errors)} configuration errors ({correct_count} correct)"
        )
        return False

    print(f"\n✓ All {len(all_configs)} configurations are correct")
    return True


def check_config_across_all(
    schema: IntentionalKernelConfigSchema, config_name: str
) -> None:
    """Check the value of a specific config across all architectures and kernels."""
    print(f"Config: {config_name}")

    found_configs = []
    for section in [schema.default] + schema.overrides:
        for kernel_config in section.kernel_configs:
            if kernel_config.name == config_name:
                found_configs.append((section.name, kernel_config))
                break

    if not found_configs:
        print("❌ Not found")
        return

    all_values: Dict = {}
    for section_name, kernel_config in found_configs:
        for arch_pair in kernel_config.values:
            all_values.setdefault(arch_pair.architecture, []).append(
                (section_name, _resolve_value(arch_pair.value))
            )

    for arch in sorted(all_values, key=lambda a: a.value):
        values = [f"{section}={value}" for section, value in all_values[arch]]
        print(f"  {arch.value}: {', '.join(values)}")

    conflicts = [
        arch.value
        for arch in all_values
        if len({v for _, v in all_values[arch]}) > 1
    ]
    if conflicts:
        print(f"  ⚠️  Conflicts in: {', '.join(conflicts)}")

    if found_configs:
        print(f"  Reason: {found_configs[0][1].justification}")


def main():
    parser = argparse.ArgumentParser(
        description="Check kernel .config file against intentional configuration"
    )
    parser.add_argument(
        "--add-config",
        metavar="JSON_FILE",
        help="Interactively add a new config to the JSON file",
    )
    parser.add_argument(
        "--check-all",
        nargs=2,
        metavar=("JSON_FILE", "CONFIG_NAME"),
        help="Check a config value across all architectures and kernels",
    )
    parser.add_argument(
        "kernel_config", nargs="?", help="Path to kernel .config file"
    )
    parser.add_argument(
        "intentional_config",
        nargs="?",
        help="Path to intentional config JSON file",
    )
    parser.add_argument(
        "kernel_name", nargs="?", help="Name of the kernel to check"
    )
    parser.add_argument(
        "architecture",
        nargs="?",
        help="Architecture (x86_64 or arm64; 'aarch64' is accepted as arm64)",
    )

    args = parser.parse_args()

    # Normalize and validate architecture early to avoid silent success on typos.
    if args.architecture:
        # Normalize common alias to the canonical name used in configs.
        if args.architecture == "aarch64":
            args.architecture = "arm64"
        valid_architectures = {"x86_64", "arm64"}
        if args.architecture not in valid_architectures:
            parser.error(
                f"Invalid architecture '{args.architecture}'. "
                f"Expected one of: {', '.join(sorted(valid_architectures))}"
            )

    if args.add_config:
        try:
            add_config_interactive(Path(args.add_config))
            return 0
        except Exception as e:
            print(f"\u2717 Error adding config: {e}")
            return 1

    if args.check_all:
        try:
            json_file, config_name = args.check_all
            schema = load_schema(Path(json_file))
            print(f"✓ Loaded intentional config: {json_file}")
            check_config_across_all(schema, config_name)
            return 0
        except Exception as e:
            print(f"✗ Error checking config: {e}")
            return 1

    if not all(
        [
            args.kernel_config,
            args.intentional_config,
            args.kernel_name,
            args.architecture,
        ]
    ):
        parser.error(
            "kernel_config, intentional_config, kernel_name,"
            " and architecture are required"
            " when not using --add-config or --check-all"
        )

    try:
        kernel_config_path = Path(args.kernel_config)
        actual_config = parse_kernel_config(kernel_config_path)
        print(
            f"✓ Parsed kernel config: {kernel_config_path} ({len(actual_config)} settings)"
        )

        intentional_config_path = Path(args.intentional_config)
        schema = load_schema(intentional_config_path)
        print(f"✓ Loaded intentional config: {intentional_config_path}")

        is_valid = check_kernel_config(
            actual_config, schema, args.kernel_name, args.architecture
        )

        if is_valid:
            print("✓ Kernel configuration check passed")
            return 0
        else:
            print("✗ Kernel configuration check failed")
            return 1

    except Exception as e:
        print(f"✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
