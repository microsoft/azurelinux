# Kernel Config Checker

A robust kernel configuration validation system using Pydantic v2 schemas. Supports default configurations and per-kernel overrides with architecture-specific settings.

## Features

- **Schema-based validation** - Uses Pydantic v2 for robust config validation
- **Multi-architecture support** - Handles x86_64 and arm64 architectures
- **Flexible overrides** - Default configs with per-kernel overrides
- **Interactive config management** - Add new configs with guided prompts
- **Config querying** - Check config values across all kernels/architectures

## Installation

From the repo root, install the Python dependencies:

```bash
pip install -r scripts/ci/kernel/kernel-config-checker/requirements.txt
```

All commands below should be run from `scripts/ci/kernel/kernel-config-checker/`:

```bash
cd scripts/ci/kernel/kernel-config-checker
```

## Usage

### Check Kernel Config

Validate a `.config` file against intentional configurations:

```bash
python -m kernel_config_checker.check_config /path/to/.config kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json kernel-name architecture
```

Example:

```bash
python -m kernel_config_checker.check_config kernel.config kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json kernel x86_64
```

### Add New Config

Interactively add a new kernel configuration:

```bash
python -m kernel_config_checker.check_config --add-config kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json
```

Features:

- Add to default or override sections
- Support for single or multiple architectures
- Leave architectures blank to omit them from JSON
- Create new override sections or use existing ones

### Query Config Values

Check a config value across all architectures and kernels:

```bash
python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json CONFIG_NAME
```

Example:

```bash
python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json CONFIG_DRM
```

### Run the CI validation locally

The `Kernel Required Configs Check` GitHub Actions workflow validates changed kernel configs by running the pytest harness in `tests/`. To reproduce a run locally, invoke pytest with the same base/head SHAs the workflow would use:

```bash
python -m pytest tests/ \
  --base-sha "$(git merge-base HEAD origin/4.0)" \
  --head-sha HEAD
```

Omit the flags to default to `HEAD^..HEAD`. The harness walks the diff, filters to `base/comps/kernel*/*config*` paths whose kernel appears in the policy JSON's `overrides`, and runs the same `check_kernel_config` logic used by the CLI. Deletions of tracked kernel config files fail a dedicated test.

To add a new check (e.g. a lint over the policy JSON, or a per-arch invariant), drop another `test_*.py` into `tests/` — no workflow changes required.

## Configuration Schema

The system uses a structured JSON schema with default and override sections:

```json
{
  "default": {
    "name": "default",
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
      "name": "kernel-hwe",
      "kernel_configs": [
        {
          "name": "CONFIG_DRM",
          "values": [
            {
              "architecture": "arm64",
              "value": "y"
            }
          ],
          "justification": "amdgpu - https://github.com/microsoft/azurelinux/pull/10612"
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
scripts/ci/kernel/kernel-config-checker/
├── kernel_config_checker/
│   ├── schema/
│   │   ├── __init__.py         # Package init
│   │   ├── schema.py           # Pydantic schema definitions
│   │   └── print_schema.py     # Schema utility
│   ├── kernel_configs_json/
│   │   └── azl4-os-required-kernel-configs.json  # Main config file
│   ├── __init__.py             # Package init
│   ├── add_config.py           # Interactive config adder
│   └── check_config.py         # Main checker and utilities
├── tests/                       # Pytest harness invoked by CI
│   ├── conftest.py              # Shared fixtures + git-diff parametrization
│   └── test_kernel_config_validation.py  # Policy checks over changed configs
├── requirements.txt            # Python dependencies
└── README.md                   # This file
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
$ python -m kernel_config_checker.check_config --check-all kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json CONFIG_DRM
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
