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

### Shared profiles

`AzureLinux.kiwi` includes flat fragments from `repositories/`, `components/`,
and `teams/`. Their `<requires>` edges form a **profile DAG/composition**, not
strict class inheritance; a leaf can combine several independent profiles.

- `SystemCore`: shared system packages and services.
- `CloudCore`: Azure cloud guest userspace; requires `SystemCore`, but selects
  neither a kernel nor a bootloader.
- `StandardBootCore`: conventional kernel and GRUB packages; requires `SystemCore`.
- `StandardCloudCore`: requires `CloudCore` and `StandardBootCore`, adding
  conventional cloud boot packages (including kernel modules and grubby).
- `VmBaseCore`: boot-neutral VM-base packages.
- `OnePBase`: boot-neutral first-party packages; requires `VmBaseCore`.
- `MarketplacePackages`: boot-neutral Marketplace payload.
- `UkiBootCore`: requires `SystemCore` and `UefiFstab`; supplies shim,
  systemd-boot, and the packaged virt UKI without selecting cloud policy.
- `UefiFstab`: supplies the UEFI fstab configuration script.
- `PackageManagement`: supplies the Azure Linux repository configuration for
  bootstrap and image package management; selected by image leaves.

### Image composition

Arrows mean "requires"; `+` combines requirements of a leaf:

```text
StandardCloudCore -> CloudCore -> SystemCore
                  \-> StandardBootCore -> SystemCore
OnePBase -> VmBaseCore
UkiBootCore -> SystemCore + UefiFstab

conventional 1P leaves -> PackageManagement + OnePBase + StandardCloudCore
                        + LegacyBoot (Gen1) or UefiBoot (Gen2) [+ Fips]
1p-vm-base-gen2-cvm -> PackageManagement + OnePBase + CloudCore + UkiBootCore
Marketplace leaves -> MarketplaceBase + UefiBoot [+ Fips]
MarketplaceBase -> PackageManagement + MarketplacePackages + StandardCloudCore
```

- Conventional 1P leaves use GRUB/the standard kernel via `StandardCloudCore`
  and add BIOS or UEFI boot packages.
- `1p-vm-base-gen2-cvm` selects boot-neutral cloud/1P layers and `UkiBootCore`,
  **not** `StandardCloudCore` or conventional GRUB/UEFI boot profiles.
- Marketplace leaves share `MarketplaceBase`, not `OnePBase`, and select
  conventional UEFI boot (with optional FIPS).

The ISO installer remains a standalone description under
`base/images/vm-iso-installer/` because its distinct composition and workflow
do not fit naturally into the shared image hierarchy.

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

### KIWI hook payloads

- Keep the root `base/images/config.sh` as the shared dispatcher based on
  `kiwi_profiles`; existing root-level hooks stay in place. Put
  profile-specific rootfs payloads under `base/images/<ProfileName>/`,
  mirroring their destination paths. KIWI overlays that directory onto the
  image root only when the named profile is selected; do not add `<file>`
  entries for these payloads.
- The `UkiBootCore` overlay supplies `image/stage-uki-boot.sh` and
  `etc/kernel/entry-token`. The hook stages shim, systemd-boot, and the packaged
  UKI because KIWI's `systemd_boot` cannot do so.

## azldev commands

See the CLI reference in [`copilot-instructions.md`](../copilot-instructions.md) for `azldev image` commands (`list`, `build`, `boot`).

## Schema validation

Kiwi files reference the upstream KIWI schema via `<?xml-model?>` processing instruction:

```xml
<?xml-model href="https://raw.githubusercontent.com/OSInside/kiwi/refs/tags/v10.2.33/kiwi/schema/kiwi.rng" type="application/xml"?>
```

Refer to the [KIWI documentation](https://osinside.github.io/kiwi/) for the full schema and element reference.
