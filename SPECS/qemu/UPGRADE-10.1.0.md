# QEMU 10.1.0 Upgrade Rationale

This document explains the changes made while upgrading the Azure Linux 3.0
QEMU package from 9.1.0 to 10.1.0. It records why each structural, macro,
configure, package, and patch-stack change was made so that a future upgrade
does not need to rediscover the same decisions.

## Reference hierarchy

The upgrade used three references, with different authority:

1. The existing Azure Linux 3.0 `qemu.spec` remained authoritative for Azure
   Linux product policy, dependency availability, package identity, and local
   features.
2. The Azure Linux 4.0 QEMU 10.1.4 spec was the primary reference for upstream
   QEMU 10 package topology, removed targets, new modules, configure options,
   and 32-bit host handling.
3. The CentOS Stream 9 `qemu-kvm` 10.1.0-22 spec was used to understand
   downstream fixes and patch history. Its RHEL-specific package identity,
   Epoch, machine types, compiler policy, and single-target package model were
   not copied.

This ordering matters. Azure Linux 4.0 is close enough to show how QEMU 10 is
packaged in Azure Linux, but Azure Linux 3.0 does not have every dependency or
the same release policy. The result therefore ports QEMU 10 structure without
turning the Azure Linux 3.0 package into either the Azure Linux 4.0 package or
the CentOS package.

## Version and source metadata

### Version and release

`Version` changed from `9.1.0` to `10.1.0`, and `Release` restarted at
`1%{?dist}`. Restarting the release is standard when the upstream version
changes. The package remains named `qemu`, and no `Epoch` was imported from
CentOS or Azure Linux 4.0 because Azure Linux 3.0 did not previously need one.
Adding an Epoch without a version-ordering requirement would permanently
change RPM comparison semantics.

### Source signature and component governance manifest

`qemu.signatures.json` now names `qemu-10.1.0.tar.xz` and records SHA-256:

```text
e0517349b50ca73ebec2fa85b06050d5c463ca65c738833bd8fc1f15f180be51
```

`cgmanifest.json` now identifies QEMU 10.1.0 and its matching download URL.
These changes keep source verification and component governance metadata in
sync with `Source0`; updating only the spec would leave the build or compliance
metadata referring to QEMU 9.1.0.

## Azure Linux policy retained

The following controls were intentionally kept because they express Azure
Linux 3.0 policy rather than an upstream-version detail:

- `Name: qemu`, `Vendor: Microsoft Corporation`, and
  `Distribution: Azure Linux`.
- `%bcond_without check`, including the existing test-package behavior.
- `%global azl_no_ui 1`, which keeps the Azure Linux build headless.
- `%global __strip /bin/true`, preserving the existing debug-information and
  packaging workflow.
- Existing Azure firmware locations and `%global ipxe_version 1.21.1`.
- `have_opengl`, `have_ui`, `have_spice`, `have_dbus_display`, and `have_jack`
  remain disabled for Azure Linux.
- `have_liburing` and NFS block support remain enabled, while RBD and Gluster
  block support remain disabled according to repository dependency policy.
- Static user-mode emulators remain enabled.
- `vhostuser-backend(fs)` remains the virtiofs provider relationship.

These settings were not replaced by their CentOS or Azure Linux 4.0
counterparts because doing so would change product behavior beyond the QEMU
version upgrade.

## Macro changes

### Added `have_64bit`

```spec
%global have_64bit 1
%ifarch %{ix86}
%global have_64bit 0
%endif
```

QEMU 10 no longer builds 64-bit emulators on a 32-bit x86 host. The macro was
added from the Azure Linux 4.0 QEMU spec so one condition controls every part
of the RPM model affected by that upstream change:

- metapackage `Requires`;
- dynamic user-mode emulator binaries and SystemTap files;
- static user-mode subpackages, binaries, SystemTap files, and binfmt rules;
- system emulator packages, binaries, firmware, man pages, and SystemTap
  files; and
- cleanup of generated 64-bit binfmt and firmware files during `%install`.

The guarded targets include AArch64, Alpha, HPPA, LoongArch64, S390x, and the
64-bit members of the MIPS, PPC, RISC-V, SPARC, and x86 target families.
Matching `Obsoletes` were added on hosts without 64-bit target support so an
upgrade can remove packages that QEMU 10 can no longer produce. Guarding only
the binaries would be insufficient: RPM would still create dangling
dependencies or `%files` entries for missing outputs.

The existing `system-x86` subpackage remains scoped to `x86_64`. This differs
slightly from the Azure Linux 4.0 layout but preserves the Azure Linux 3.0
subpackage declaration policy.

### Added `requires_device_uefi_vars`

QEMU 10 builds `hw-uefi-vars.so` as a separate loadable module. The new macro:

```spec
%define requires_device_uefi_vars Requires: %{name}-device-uefi-vars = %{evr}
```

was added to `requires_all_modules`, and the matching
`qemu-device-uefi-vars` subpackage owns the module. This follows the Azure
Linux 4.0 QEMU 10 layout and preserves the existing convention that system
emulator metapackages depend on all loadable device modules they may need.

### Neutralized generic audio dependency macros

The generic audio dependency macros for ALSA, OSS, PulseAudio, PipeWire, SDL,
JACK, and D-Bus now expand to `%{nil}`. The old `pa_drv`, `sdl_drv`, and
`jack_drv` list-fragment macros were removed because the final audio driver
list is deliberately empty.

The macro names were retained rather than deleting every reference from
`requires_all_modules`. This keeps the module dependency composition uniform
and makes the disabled policy explicit. It also avoids introducing a second
Azure-specific version of the module aggregation macro.

This matches the headless audio policy seen in the Azure Linux 4.0 QEMU spec.
The conditional SPICE audio module remains governed by `have_spice`; it is not
part of the removed generic host-audio backend set.

### Added CRIS obsoletes

QEMU 10 removed CRIS system and user emulation. The package no longer declares
CRIS dependencies, subpackages, scriptlets, file lists, binaries, tapsets, or
binfmt rules. Obsoletes were added for:

- `qemu-system-cris`;
- `qemu-system-cris-core`; and
- `qemu-user-static-cris`.

The obsoletes are necessary because simply deleting the package declarations
would leave old CRIS RPMs installed after an upgrade. This removal and upgrade
handling are also present in the Azure Linux 4.0 QEMU spec.

## Configure changes

### Updated `disable_everything`

`disable_everything` is the baseline used before selected features are enabled
for each build. Keeping it complete prevents Meson `auto` detection from
silently changing the package when the buildroot gains a new dependency.

The following QEMU 10 options were added to the disabled baseline:

- `--disable-asan`
- `--disable-debug-remap`
- `--disable-igvm`
- `--disable-libcbor`
- `--disable-passt`
- `--disable-pvg`
- `--disable-qpl`
- `--disable-rust`
- `--disable-strict-rust-lints`
- `--disable-uadk`
- `--disable-ubsan`
- `--disable-valgrind`

These switches exist in the QEMU 10 configuration surface but are not selected
for Azure Linux 3.0. In particular, the repository does not provide all of the
dependencies needed for IGVM, libcbor, passt, QPL, UADK, and the newer Rust
path. Explicit disables make the build reproducible and match the conservative
feature baseline used by the Azure Linux 4.0 spec where applicable.

The following obsolete aggregate or CPU-feature switches were removed:

- `--disable-avx2`
- `--disable-avx512bw`
- `--disable-sanitizers`

QEMU 10 no longer exposes these old configure switches in this form. Sanitizer
selection is represented by individual ASAN, UBSAN, and related options, while
the old AVX configure toggles are no longer accepted. Leaving obsolete options
would make configure fail instead of disabling a feature.

### Disabled host audio and SDL explicitly

The main build now passes:

```text
--disable-alsa
--disable-jack
--disable-oss
--disable-pa
--disable-pipewire
--audio-drv-list=
--disable-sdl
--disable-sdl-image
```

The prior spec enabled some of these backends and then packaged a module for
each one. Azure Linux builds QEMU as a headless virtualization component, and
the Azure Linux 4.0 QEMU spec no longer carries these generic audio packages.
Explicitly disabling both the feature and the driver list prevents module files
from being generated accidentally and keeps the configure result aligned with
the RPM package graph.

### Removed obsolete enables

`--enable-avx2` and `--enable-avx512bw` were removed for the same reason as
their disabled counterparts: QEMU 10 no longer accepts those configure
switches.

`--enable-virtfs-proxy-helper` was removed because QEMU 10 no longer exposes a
separate configure option for that helper. `--enable-virtfs` remains, so the
supported virtfs functionality is still enabled without passing an invalid
legacy switch.

## Package and file-layout changes

### Removed generic audio subpackages

The following package declarations and `%files` sections were removed:

- `qemu-audio-alsa`
- `qemu-audio-dbus`
- `qemu-audio-oss`
- `qemu-audio-pa`
- `qemu-audio-pipewire`
- `qemu-audio-sdl`
- `qemu-audio-jack`

This is the package-side counterpart to disabling the backends at configure
time. Retaining empty package declarations would create packages with no
payload, while retaining file lists would fail when the disabled modules are
not built.

### Added `qemu-device-uefi-vars`

The new package owns:

```text
%{_libdir}/qemu/hw-uefi-vars.so
```

Splitting the module follows the existing one-module-per-subpackage pattern and
the Azure Linux 4.0 QEMU 10 spec. Placing it in `qemu-common` instead would make
the common package architecture-specific and would bypass the module
dependency macros.

### Removed CRIS package surfaces

All CRIS system and static-user declarations, scriptlets, and file entries were
removed because no corresponding QEMU 10 output exists. This includes the CRIS
emulator binaries, SystemTap probes, man page, and static binfmt integration.

### Guarded 64-bit package surfaces

Every 64-bit file list is guarded by `have_64bit`, including 64-bit members
inside mixed target packages such as `qemu-user-static-mips` and
`qemu-system-riscv`. The `%install` cleanup removes 64-bit binfmt files that
`qemu-binfmt-conf.sh` can generate independently of the selected target list,
plus firmware files owned only by guarded packages. This avoids both unpackaged
files and references to files not built on i686.

## Patch-stack decisions

Patch compatibility was checked against the exact pristine
`qemu-10.1.0.tar.xz` source. A patch was removed only after one of these stronger
conditions was established:

- reverse application showed the exact change was already upstream; or
- QEMU 10.1 contained the complete behavior or a generalized replacement, not
  merely similar-looking code.

Failure to apply by itself was not treated as proof that a patch was obsolete.

### Patches removed because the exact fixes are upstream

| Patch | Reason for removal |
| --- | --- |
| `kvm-migration-Ensure-vmstate_save-sets-errp.patch` | The `vmstate_save()` error propagation fix is already in pristine QEMU 10.1. |
| `kvm-net-Fix-announce_self.patch` | The `announce_self` networking fix is already in pristine QEMU 10.1. |
| `kvm-block-Allow-inactivating-already-inactive-nodes.patch` | QEMU 10.1 already makes repeated node inactivation safe. |
| `kvm-block-Don-t-attach-inactive-child-to-active-node.patch` | The active-parent/inactive-child protection is already upstream. |
| `kvm-block-Fix-crash-on-block_resize-on-inactive-node.patch` | The inactive-node resize crash fix is already upstream. |
| `kvm-nbd-server-Support-inactive-nodes.patch` | NBD export handling for inactive nodes is already upstream. |
| `kvm-migration-Fix-UAF-for-incoming-migration-on-Migratio.patch` | The incoming migration use-after-free fix is already upstream. |

Keeping any of these patches would duplicate upstream code and increase the
chance of conflicts or accidentally reverting a later upstream refinement.

### Late block activation series removed as integrated upstream

The following downstream series introduced late block activation and inactive
block-node management. QEMU 10.1 already contains the complete resulting
surface, including `migration_get_target_runstate()`,
`migration/block-active.c`, `bdrv_activate()`/`bdrv_inactivate()`, the
`blockdev-set-active` QMP command, inactive-node creation, active-state
reporting, and the `allow-inactive` block export option.

| Patch | QEMU 10.1 behavior that supersedes it |
| --- | --- |
| `kvm-migration-Add-helper-to-get-target-runstate.patch` | `migration_get_target_runstate()` is present and used by incoming migration. |
| `kvm-qmp-cont-Only-activate-disks-if-migration-completed.patch` | Disk activation is coordinated through the upstream migration block-active state. |
| `kvm-migration-block-Make-late-block-active-the-default.patch` | Late activation is part of the upstream incoming migration flow. |
| `kvm-migration-block-Apply-late-block-active-behavior-to-.patch` | The behavior covered by the series is integrated into the upstream migration paths. |
| `kvm-migration-block-Fix-possible-race-with-block_inactiv.patch` | Upstream block-active handling contains the serialized activation/inactivation flow. |
| `kvm-migration-block-Rewrite-disk-activation.patch` | QEMU 10.1 has the rewritten activation implementation in `migration/block-active.c`. |
| `kvm-block-Add-active-field-to-BlockDeviceInfo.patch` | QEMU 10.1 exposes block-node active state through its block QAPI. |
| `kvm-block-Inactivate-external-snapshot-overlays-when-nec.patch` | External overlay inactivation is included in the upstream block graph handling. |
| `kvm-migration-block-active-Remove-global-active-flag.patch` | The upstream implementation uses per-node activation rather than the old global flag. |
| `kvm-block-Add-option-to-create-inactive-nodes.patch` | QEMU 10.1 supports creating inactive block nodes. |
| `kvm-block-Add-blockdev-set-active-QMP-command.patch` | `blockdev-set-active` is defined in QEMU 10.1 QAPI. |
| `kvm-block-Support-inactive-nodes-in-blk_insert_bs.patch` | Upstream block insertion supports the inactive-node model. |
| `kvm-block-export-Don-t-ignore-image-activation-error-in-.patch` | The upstream export path calls `bdrv_activate()` and propagates errors. |
| `kvm-block-export-Add-option-to-allow-export-of-inactive-.patch` | The `allow-inactive` export option is present in QEMU 10.1 QAPI and implementation. |

Removing this series as a unit is important. Its patches depend on each other;
retaining only fragments would mix old downstream interfaces with the final
upstream design.

### Virtio queue-loading patch removed as superseded

`kvm-virtio-net-Add-queues-before-loading-them.patch` added a
`pre_load_queues` callback so virtio-net queues existed before migration state
was loaded. QEMU 10.1 contains a generalized version:

- the callback receives the migrated queue count as `uint32_t n`;
- `virtio_load()` invokes it after validating the count and before loading
  queue state; and
- virtio-net resizes its queues through that callback.

The old patch was therefore removed instead of rebased. Reapplying it would
replace the newer callback contract with an older, less capable version.

### Patches retained because they still apply and remain needed

- `0001-pc-bios-optionrom-Fix-pvh.img-ld-build-failure-on-fe.patch` still
  applies and preserves the existing linker compatibility fix.
- `CVE-2021-20255.patch`, `CVE-2025-11234.patch`, `CVE-2025-12464.patch`,
  `CVE-2024-8354.patch`, `CVE-2025-14876.patch`, `CVE-2026-3195.patch`,
  `CVE-2026-48914.patch`, and `CVE-2026-3196.patch` still apply to QEMU 10.1
  and continue to provide Azure Linux security servicing fixes.
- `kvm-block-Drain-nodes-before-inactivating-them.patch` still applies and is
  not present in pristine QEMU 10.1, so it remains in the stack.

### Azure migration-test patch rebased

`0002-Disable-failing-tests-on-azl.patch` previously modified the monolithic
`tests/qtest/migration-test.c`. QEMU 10 split those tests into the migration
test framework, so the patch now targets:

- `tests/qtest/migration/framework.c`, where it forces `env->has_uffd` false to
  skip userfaultfd/postcopy paths that hang in the Azure Linux RPM build
  environment; and
- `tests/qtest/migration/tls-tests.c`, where it disables only TLS-PSK test
  registrations that fail with `The curve is unsupported`.

TLS X.509 registrations were deliberately left enabled. The purpose of the
patch is to preserve known Azure Linux exclusions, not to disable all TLS
coverage.

### CVE-2026-3842 patch rebased

The Hyper-V synthetic debugger fix still applies logically, but QEMU 10.1
changed the receive buffer from a page-sized array to `MSG_BUFSZ` and added an
assertion. The patch context was updated for that layout while retaining the
security behavior:

- remember the requested mapping length;
- reject a null or short `cpu_physical_memory_map()` result;
- copy only the mapped length; and
- unmap only when a mapping was returned.

This is a context rebase, not a change to the intended CVE fix.

## Validation performed

The upgrade was checked with the following focused validations:

- `rpmspec --define 'azl 1' --target x86_64 --parse`;
- `rpmspec --define 'azl 1' --target i686 --parse`, including checks that
  guarded 64-bit Requires and file lists are absent;
- a clean `rpmbuild --nodeps -bp` against QEMU 10.1.0, which applies the entire
  remaining patch stack successfully;
- direct `git apply --check` of both rebased patches against pristine QEMU
  10.1.0;
- SHA-256 verification of the source archive;
- JSON parsing of `qemu.signatures.json` and `cgmanifest.json`; and
- `git diff --check`.

A full binary RPM build was not part of this rebase validation. The next
highest-value check is a repository-native QEMU build to reconcile generated
file lists and exercise the QEMU test suite with the Azure Linux buildroot
dependencies.
