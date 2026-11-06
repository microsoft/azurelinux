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

## Cloud image boot console defaults

The Marketplace and first-party VM base definitions in
[marketplace.xml](teams/cloud/marketplace.xml) and [onep.xml](teams/cloud/onep.xml)
use `loglevel=4 systemd.show_status=error` for all architectures and profiles,
including FIPS. The serial and early console parameters
remain enabled: `console=ttyS0 earlyprintk=ttyS0` on x86_64 and
`console=ttyAMA0 earlyprintk=ttyAMA0` on aarch64.

`loglevel=4` limits kernel console output to errors and higher-severity messages
from early boot, rather than waiting for a sysctl to apply. The systemd setting
retains failure status output while suppressing routine boot status lines.
These settings reduce serial-console overhead without disabling normal kernel
ring-buffer or journal collection. To troubleshoot early boot, temporarily
remove these verbosity restrictions.
