# Userland implementations in Azure Linux 4.0

Which implementation of each core system component does Azure Linux 4.0 use? This page answers that for the VM base images, and lists the alternative implementations that are packaged in this repository but not used by default.

This page records **which implementation is chosen for each role**, not which packages an image contains. The image definitions under [`base/images/`](../base/images/images.toml) are the source of truth for exact package lists:

- [`images.toml`](../base/images/images.toml) maps each image to the profile it is built from.
- [`components/common.xml`](../base/images/components/common.xml) holds the packages shared by every bootable image and by Azure guest images.
- [`teams/cloud/vm-base.xml`](../base/images/teams/cloud/vm-base.xml) adds the VM base packages, and [`teams/cloud/onep.xml`](../base/images/teams/cloud/onep.xml) and [`teams/cloud/marketplace.xml`](../base/images/teams/cloud/marketplace.xml) define the first-party and Marketplace VM images.
- [`teams/container.xml`](../base/images/teams/container.xml), [`teams/containers-workloads.xml`](../base/images/teams/containers-workloads.xml), [`teams/minimal-os.xml`](../base/images/teams/minimal-os.xml), [`teams/wsl.xml`](../base/images/teams/wsl.xml) and the [installer image](../base/images/vm-iso-installer/vm-iso-installer.kiwi) define the other image families.

Container, minimal OS, WSL, Marketplace and installer images select different package sets, so check the definition of the image you care about.

## VM base images

These are the implementations selected by the first-party VM base images (`1p-vm-base-gen1`, `1p-vm-base-gen2`, and their FIPS variants).

| Role | Implementation | Package |
|---|---|---|
| C library | GNU C Library | `glibc` |
| Core utilities | GNU coreutils | `coreutils` |
| Shell | GNU Bash | `bash` |
| Init system and service manager | systemd | `systemd` |
| Network configuration | systemd-networkd | `systemd-networkd` |
| DNS resolution | systemd-resolved | `systemd-resolved` |
| Time synchronization | chrony | `chrony` |
| Privilege escalation | sudo | `sudo` |
| Package manager | DNF 5, using the RPM package format | `dnf5` |
| DNS lookup tools | BIND utilities | `bind-utils` |

To check a row against the image definition, from the root of this repository:

```bash
grep -E 'name="(glibc|coreutils|bash|systemd|systemd-networkd|systemd-resolved|chrony|sudo|dnf5|bind-utils)"' \
  base/images/components/common.xml base/images/teams/cloud/vm-base.xml
```

To check it on a running system, ask RPM which package owns the files:

```bash
rpm -qf --qf '%{NAME}\n' /usr/bin/ls /usr/bin/bash /usr/bin/sudo
rpm -q chrony systemd-networkd systemd-resolved dnf5
```

## Packaged, but not selected by any image

These come up often as possible replacements for the components above. They are not what the images use.

| Alternative | Status |
|---|---|
| uutils coreutils | Built as the `uutils-coreutils` subpackage of the [`rust-coreutils`](../specs/r/rust-coreutils/rust-coreutils.spec) component. No image definition selects it. The VM base images use GNU coreutils; the busybox and distroless-debug container images ship busybox instead, and the other distroless images ship neither. |
| mimalloc | Packaged as a regular library (`mimalloc` and `mimalloc-devel`) and used as a build dependency of `mold`. glibc is not patched to use it, and the [rendered `glibc.spec`](../specs/g/glibc/glibc.spec) does not reference it. |
| sudo-rs, ntpd-rs | Not packaged. There is no source package for them in this repository. |
| Hickory DNS | Only some Rust library crates are packaged (the `rust-hickory-*` components, which provide `-devel` subpackages and no binaries). No Hickory DNS server or resolver daemon is built. |

## Keeping this page accurate

Changing one of the choices above in an image definition changes what this page should say, so update it in the same pull request. The commands above are meant to make any drift easy to spot.
