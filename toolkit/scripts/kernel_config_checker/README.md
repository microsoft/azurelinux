# Kernel Config Checker

A robust kernel configuration validation system using Pydantic v2 schemas. Supports default configurations and per-kernel overrides with architecture-specific settings.

## Features

- **Schema-based validation** - Uses Pydantic v2 for robust config validation
- **Multi-architecture support** - Handles x86_64 and arm64 architectures
- **Flexible overrides** - Default configs with per-kernel overrides
- **Interactive config management** - Add new configs with guided prompts
- **Config querying** - Check config values across all kernels/architectures
- **Legacy conversion** - Tools to migrate existing configurations

## Installation

From the repo root, install the Python dependencies:

```bash
pip install -r toolkit/scripts/requirements.txt
```

All commands below should be run from `toolkit/scripts/`:

```bash
cd toolkit/scripts
```

## Usage

### Check Kernel Config

Validate a `.config` file against intentional configurations:

```bash
python -m kernel_config_checker.check_config /path/to/.config kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json kernel-name architecture
```

Example:

```bash
python -m kernel_config_checker.check_config kernel.config kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json kernel x86_64
```

### Add New Config

Interactively add a new kernel configuration:

```bash
python -m kernel_config_checker.check_config --add-config kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json
```

Features:

- Add to default or override sections
- Support for single or multiple architectures
- Leave architectures blank to omit them from JSON
- Create new override sections or use existing ones

### Query Config Values

Check a config value across all architectures and kernels:

```bash
python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json CONFIG_NAME
```

Example:

```bash
python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json CONFIG_DRM
```

## Configuration Schema

The system uses a structured JSON schema with default and override sections:

```json
{
  "default": {
    "kernel_configs": [
      {
        "name": "CONFIG_EXAMPLE",
        "values": [
          {
            "architecture": "x86_64",
            "value": "y"
          },
          {
            "architecture": "arm64", 
            "value": "m"
          }
        ],
        "justification": "Explanation for this config"
      }
    ]
  },
  "overrides": [
    {
      "name": "kernel-64k",
      "kernel_configs": [
        {
          "name": "CONFIG_ARM64_64K_PAGES",
          "values": [
            {
              "architecture": "arm64",
              "value": "y"
            }
          ],
          "justification": "needed for 64k page size"
        }
      ]
    }
  ]
}
```

### Architecture Support

- Configs can specify values for `x86_64`, `arm64`, or both
- When adding configs, leaving an architecture blank omits it from the JSON
- At least one architecture must be specified

### Value Types

- `y` - Built into kernel
- `m` - Built as module  
- `n` - Disabled ("is not set" or missing)
- Custom values supported for specific configs

## Project Structure

```text
toolkit/scripts/kernel_config_checker/
├── schema/
│   ├── __init__.py         # Package init
│   ├── schema.py           # Pydantic schema definitions
│   └── print_schema.py     # Schema utility
├── kernel_configs_json/
│   └── azl3-os-required-kernel-configs.json  # Main config file
├── __init__.py             # Package init
├── check_config.py         # Main checker and utilities
└── README.md               # This file
```

## Examples

### Adding a Config for Single Architecture

```bash
$ python -m kernel_config_checker.check_config --add-config test.json
Adding new kernel configuration...
Enter config name (e.g., CONFIG_EXAMPLE): CONFIG_X86_ONLY
Enter values for each architecture (y/n/m or specific value, leave blank to skip):
x86_64 value: y
arm64 value: 
Enter justification: Only needed on x86_64
Add to [d]efault or [o]verride? [d]: d
✓ Added CONFIG_X86_ONLY to default section
```

Results in:

```json
{
  "name": "CONFIG_X86_ONLY",
  "values": [
    {
      "architecture": "x86_64", 
      "value": "y"
    }
  ],
  "justification": "Only needed on x86_64"
}
```

### Querying Config Values

```bash
$ python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl3-os-required-kernel-configs.json CONFIG_DRM
Config: CONFIG_DRM
  arm64: default=m, kernel-hwe=y
  x86_64: default=m
  ⚠️  Conflicts in: arm64
  Reason: amdgpu - https://github.com/microsoft/azurelinux/pull/10612
```

## Contributing

1. Ensure all configs have proper justifications
2. Test schema validation after changes
3. Use the add-config command for consistency
4. Validate configs against actual kernel .config files

## License

This project follows the same licensing as the Azure Linux project.
