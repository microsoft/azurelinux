# Userland implementations in VM base images

The first-party VM base images (`1p-vm-base-*`) select the following implementations for common system roles. The names in parentheses are binary RPMs, not necessarily source component names.

| Role | Implementation (selected RPMs) |
|---|---|
| C library | GNU C Library (`glibc`) |
| Core command-line utilities | GNU coreutils (`coreutils`) |
| Shell | Bash (`bash`) |
| Init, services, and networking | systemd (`systemd`, `systemd-networkd`, `systemd-resolved`) |
| Package management | DNF 5 (`dnf5`) over the RPM package format |
| Privilege delegation | sudo (`sudo`) |
| Time synchronization | chrony (`chrony`) |
| DNS command-line tools | BIND utilities (`bind-utils`) |

These selections come from the `VmBaseCore` profile in [vm-base.xml](teams/cloud/vm-base.xml), which inherits `CloudCore` and `BootableCore` from [common.xml](components/common.xml). To check the listed RPMs against those definitions, run this from the repository root:

```bash
grep -E 'name="(glibc|coreutils|bash|systemd|systemd-networkd|systemd-resolved|dnf5|sudo|chrony|bind-utils)"' \
  base/images/components/common.xml base/images/teams/cloud/vm-base.xml
```

This is a summary of implementation choices, not a complete package manifest. Container, distroless, minimal OS, WSL, Marketplace, and installer images can select different packages. [images.toml](images.toml) maps each image to its definition and profile; follow those definitions for the current selections. Update this summary when changing one of the choices above.
