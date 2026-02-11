---
applyTo: "**/*.kiwi"
---

# Kiwi Image Definitions (`*.kiwi`)

Kiwi files define Azure Linux image builds. They use the [KIWI NG](https://osinside.github.io/kiwi/) XML format to specify image type, packages, repositories, and configuration.

## How images are registered

Images are defined in `base/images/images.toml`:

```toml
[images.container-base]
description = "Container Base Image"
definition = { type = "kiwi", path = "container-base/container-base.kiwi" }
```

Each image has its own directory under `base/images/` containing the `.kiwi` file.

## Image types

- **Container** (`image="docker"`): OCI container images with `<containerconfig>` for name, tag, entrypoint
- **VM** (`image="oem"`): Virtual machine images with disk format (`vhdx`, `qcow2`), filesystem, bootloader, and partition config

## Key elements

| Element | Purpose |
|---------|---------|
| `<preferences>` | Package manager (`dnf5`), image type, version, locale, timezone |
| `<repository>` | Package sources (RPM repos) |
| `<packages type="image">` | Packages installed in the final image |
| `<packages type="bootstrap">` | Minimal packages for initial chroot setup |
| `<containerconfig>` | Container-specific: name, tag, user, workdir, entrypoint |
| `<type>` | Image format, filesystem, bootloader, kernel cmdline |

## azldev commands

See the CLI reference in [`copilot-instructions.md`](../copilot-instructions.md) for `azldev image` commands (`list`, `build`, `boot`).

## Schema validation

Kiwi files reference the upstream KIWI schema via `<?xml-model?>` processing instruction:

```xml
<?xml-model href="https://raw.githubusercontent.com/OSInside/kiwi/refs/tags/v10.2.33/kiwi/schema/kiwi.rng" type="application/xml"?>
```

Refer to the [KIWI documentation](https://osinside.github.io/kiwi/) for the full schema and element reference.
