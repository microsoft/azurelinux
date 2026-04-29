# Azure Linux Image Tests

Static validation framework for built Azure Linux images (VM and container).
Mounts images read-only and runs pytest tests against the filesystem
without booting.

## How it gets invoked

These tests are wired into `azldev` via the `[test-suites.static-image-checks]`
table in `base/images/images.toml`, and referenced by each image's
`tests.test-suites`. The standard entry point is:

```bash
azldev image build vm-base
azldev image test  vm-base

azldev image build container-base
azldev image test  container-base
```

`azldev` creates a per-suite Python venv, installs this directory's
`pyproject.toml`, and invokes pytest with the right `--image-path`,
`--image-name`, and `--capabilities` arguments.

## Direct (manual) invocation

```bash
cd base/images/tests

# VM image — shared + VM-specific tests
uv run pytest cases/ \
    --image-path /path/to/image.raw \
    --image-name vm-base \
    --capabilities machine-bootable,systemd,runtime-package-management

# Container image — shared + container-specific tests
uv run pytest cases/ \
    --image-path /path/to/image.oci.tar.xz \
    --image-name container-base \
    --capabilities container,runtime-package-management
```

Test selection follows standard pytest positional arguments. Tests
under `cases/<image-name>/` auto-skip when `--image-name` doesn't match
(via the `image` marker, applied in each subdirectory's `conftest.py`).
Tests marked `@pytest.mark.require_capability("…")` skip when the named
capability isn't in `--capabilities`.

> Always pass `--image-name` when running manually if you want
> image-specific tests under `cases/<image-name>/` to run. Without
> it, every `@pytest.mark.image(...)`-tagged test is skipped.

## Prerequisites

System packages (not pip-installable):

- **`libguestfs-tools`** + **`guestfs-tools`** — `guestmount`,
  `guestunmount`, `virt-inspector` (VM images)
- **`skopeo`** — OCI archive conversion (container images)
- **`umoci`** — OCI image unpacking (container images)
- **`buildah`** — cleanup of rootless umoci extracts (container images)
- **`rpm`** — for `rpm --root` package queries
- **`uv`** — Python project/package manager

`pytest_configure` does a preflight check and fails fast if any tool
needed for the current `--image-type` is missing.

## Layout

```
base/images/
├── images.toml                          # Image registry + test-suite wiring
└── tests/
    ├── pyproject.toml                   # uv project: pytest, plugin entry point
    ├── conftest.py                      # Session fixtures
    ├── utils/                           # Helper package (not test-collected)
    │   ├── pytest_plugin.py             # CLI options, markers, tool preflight
    │   ├── extract.py                   # Image mounting / extraction
    │   ├── disk.py                      # virt-inspector → DiskInfo
    │   ├── parsers.py                   # File content parsers
    │   ├── types.py                     # Dataclasses
    │   └── tools.py                     # Native-tool registry
    └── cases/                           # Test cases
        ├── test_os_release.py           # Shared: /etc/os-release
        ├── test_packages.py             # Shared: rpm-db checks (capability-gated)
        ├── vm-base/                     # VM-specific tests (auto-restricted to vm-base)
        │   ├── test_kernel.py
        │   └── test_partitions.py
        └── container-base/              # Container-specific tests (auto-restricted to container-base)
            └── test_container.py
```

## Available fixtures

| Fixture | Scope | Type | Description |
|---------|-------|------|-------------|
| `image_path` | session | `Path` | From `--image-path` |
| `image_name` | session | `str \| None` | From `--image-name` |
| `image_type` | session | `str` | `"vm"` or `"container"` (explicit / capabilities / extension) |
| `capabilities` | session | `set[str]` | Parsed `--capabilities` |
| `workdir` | session | `Path` | Working directory for mounts/extractions |
| `rootfs` | session | `Path` | Mounted/extracted root filesystem |
| `os_release` | session | `dict[str, str]` | Parsed `/etc/os-release` |
| `installed_packages` | session | `set[str]` | Installed RPM names (`rpm --root`) |
| `disk_info` | session | `DiskInfo \| None` | VM only |
| `partition_table` | session | `list[PartitionInfo]` | VM only — auto-skips on containers |

## Adding tests

- **Shared (every image):** add a `cases/test_<topic>.py`. Use
  `@pytest.mark.require_capability("…")` if the test only applies to
  images with a given capability.
- **Image-specific:** add `cases/<image-name>/test_<topic>.py`. Tests
  in such subdirectories are **automatically** restricted to that
  `--image-name` (the plugin applies `@pytest.mark.image("<dir>")`
  during collection — no boilerplate per file or per subdir).

## Adding a native-tool dependency

Each `utils/*.py` module declares the CLI tools it shells out to as
module-level `NativeTool` constants and uses them at the call sites:

```python
# utils/extract.py
GUESTMOUNT = NativeTool(
    name="guestmount",
    package_hint="libguestfs-tools",
    reason="FUSE-mount VM images",
    when="vm",            # "always" | "vm" | "container"
)

def mount_vm_image(...):
    subprocess.run([GUESTMOUNT.name, "--ro", ...])
```

Construction registers the tool, and `pytest_configure` does a
preflight check against `$PATH` for every tool whose `when` matches
the current image type. Missing tools fail fast with the
`package_hint`. Run `uv run python -m utils.tools` to see the full
status.
