---
applyTo: "**/*.kiwi"
---

# Kiwi Image Definitions (`*.kiwi`)

Kiwi files define Azure Linux image builds. They use the [KIWI NG](https://osinside.github.io/kiwi/) XML format to specify image type, packages, repositories, and configuration.

## How images are registered

Images are defined in `base/images/images.toml`. Each image is
declared as a canonical (unsuffixed) entry plus a `-dev` variant,
each selecting the matching kiwi `profile`:

```toml
[images.container-base]
description = "Container Base Image"
definition = { type = "kiwi", path = "container-base/container-base.kiwi", profile = "core" }

[images.container-base-dev]
description = "Container Base Image (dev)"
definition = { type = "kiwi", path = "container-base/container-base.kiwi", profile = "core-dev" }
```

The two variants share the same kiwi description; they differ only
in which `azurelinux-repos*` package is shipped (controlling where
the resulting OS points at runtime), and — for the `core` container
specifically — the OCI tag (`:4.0` + `:latest` for canonical,
`:4.0-dev` for the dev variant). Both variants build their RPMs
from the same source (the kiwi `<repository>`); koji overrides this
during distro builds.

Distroless container images strip the package manager entirely, so
they ship no `-repos` package and have only a single (canonical)
entry — there's no `-dev` sibling because it would be byte-identical.

Each image has its own directory under `base/images/` containing the
`.kiwi` file.

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
