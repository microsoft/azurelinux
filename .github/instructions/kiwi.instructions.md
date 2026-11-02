---
applyTo: "**/*.kiwi"
---

# Kiwi Image Definitions (`*.kiwi`)

Kiwi files define Azure Linux image builds. They use the [KIWI NG](https://osinside.github.io/kiwi/) XML format to specify image type, packages, repositories, and configuration.

## How images are registered

Images are defined in `base/images/images.toml`. Most images select a leaf
profile from the shared `base/images/AzureLinux.kiwi` description:

```toml
[images.container-base]
description = "Container Base Image"
definition = { type = "kiwi", path = "AzureLinux.kiwi", profile = "core" }
```

`AzureLinux.kiwi` includes reusable fragments from `repositories/`,
`components/`, and `teams/`. Includes remain flat in the root description;
profile requirements express inheritance between fragments.

Shared KIWI hook scripts live directly under `base/images/`, because that
directory is the shared description root. The root `config.sh` dispatches
profile-specific behavior using `kiwi_profiles`, following Fedora's
shared-description model.

The ISO installer remains a standalone description under
`base/images/vm-iso-installer/` because its distinct composition and workflow
do not fit naturally into the shared image hierarchy.

## Package image configuration

KIWI profiles must not inject bare files into the image, including through
`<file>` entries, unless there is absolutely no alternative. Always build a
config RPM as a subpackage of `azurelinux-release` or another suitable component
for configuration overrides, and include that RPM in the owning profile's
package list. This keeps file ownership, upgrades, and removal managed by RPM.

If there is no alternative to bare-file injection, document why a config RPM
cannot be used. Keep the `<file>` entry scoped to the owning profile so its
payload does not leak into other images. For the shared description, place any
such sources directly under `base/images/`.

## Image types

- **Container** (`image="oci"`): OCI container images with `<containerconfig>` for name, tag, entrypoint
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
