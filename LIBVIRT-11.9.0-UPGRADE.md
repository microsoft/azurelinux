# libvirt 11.9.0 Package Upgrade

This document records the Azure Linux `libvirt` package changes made while
upgrading from 10.10.0-2 to 11.9.0-1. The Azure Linux 4.0 and CentOS Stream 9
specs were used as packaging references, while the upstream libvirt 11.9.0
spec and source tree were used to determine the version-specific build and
file-list changes.

## Version and source metadata

- Changed `Version` from `10.10.0` to `11.9.0` and reset `Release` from `2` to
  `1`, as required for the first Azure Linux package release of a new upstream
  version.
- Replaced the source entry in `libvirt.signatures.json` with
  `libvirt-11.9.0.tar.xz` and SHA-256
  `104f70ee591e72989d4f8c6caa79ed9dacd5dc84efdb0125b848afe544ad0c2d`.
  The checksum was verified against the official archive from
  `download.libvirt.org`.
- Added an 11.9.0 changelog entry and corrected the pre-existing chronological
  placement of the 10.0.0-5 entry so RPM changelog validation succeeds.

The Azure Linux source storage endpoint did not yet contain the 11.9.0 archive
during local validation. A verified copy was therefore placed next to the spec
for the build. Source archives in that location are ignored by the repository
and are not part of the tracked package change.

## Feature macros

- Added `arches_ch` for the architectures supported by the Cloud Hypervisor
  driver (`x86_64` and `aarch64`).
- Added `with_ch` and kept it disabled for Azure Linux. libvirt 11.x has an
  explicit Cloud Hypervisor driver option, so declaring the feature state is
  preferable to relying on Meson auto-detection.
- Added `with_userfaultfd_sysctl` and enabled it. This controls installation of
  libvirt's sysctl configuration for QEMU post-copy migration.
- Added `firewall_backend_priority` with `iptables,nftables`. libvirt 11.x can
  select between firewall backends; this preserves the iptables-first behavior
  of earlier Azure Linux packages rather than accepting a changed upstream
  default.

## Patch set

The following patches remain in the spec because they apply cleanly to the
11.9.0 source and their behavior is not present in that release:

- `libvirt-conf.patch` preserves the Azure Linux default connection URI.
- `CVE-2025-13193.patch` retains the applicable security fix.

The following patch references and files were removed after checking them
against the exact 11.9.0 source:

- `CVE-2025-12748.patch` is fixed or superseded in 11.9.0.
- `libvirt-qemu-tpm-do-not-update-profile-name-for-transient-domains.patch` is
  obsolete with the 11.9.0 QEMU TPM implementation.
- `libvirt-qemu-Rename-outgoingMigration-parameter-in-various-TPM-functions.patch`
  is already represented by the updated upstream TPM migration code.
- `libvirt-qemu-Properly-propagate-migration-state-to-TPM-cleanup-code.patch`
  is already represented by the updated upstream TPM migration code.

Keeping obsolete patches would either fail `%prep` or reapply behavior already
implemented upstream.

## Build dependencies

- Raised the minimum `glib2-devel` version from 2.56 to 2.66 to match the
  minimum required by libvirt 11.9.0.
- Removed `kmod` from `BuildRequires` and added it to the daemon runtime
  requirements. libvirt invokes `modprobe` and `rmmod` at runtime; it does not
  need the executable to compile.
- Removed build-only entries for `polkit`, `util-linux`, `lvm2`,
  `iscsi-initiator-utils`, and `numad`. These commands and services are runtime
  concerns and are already associated with the subpackages that use them; the
  11.9.0 build does not require their executables.
- Removed the duplicate `util-linux` build requirement while retaining
  `nfs-utils`, which is still used for network filesystem discovery.
- Added an exact-version requirement from the lockd plugin to
  `libvirt-daemon-common`, reflecting its dependency on common daemon content.
- Added an `Obsoletes` entry for `libvirt-daemon-driver-storage-zfs < 11.4.0`
  when ZFS support is disabled. This permits clean upgrades from installations
  that still contain the former ZFS storage-driver subpackage.

## Meson configuration

- Split the ESX driver and curl settings into `arg_esx` and `arg_curl`. Curl is
  needed by either ESX or Cloud Hypervisor, so tying it only to ESX would be
  incorrect once `driver_ch` is modeled explicitly.
- Added `arg_ch` and pass `-Ddriver_ch=enabled` or `disabled` according to
  `with_ch`. Azure Linux currently passes the disabled form.
- Added `arg_userfaultfd_sysctl` and pass the corresponding 11.9.0 Meson
  option. This keeps the installed sysctl file synchronized with the feature
  selection.
- Pass `-Dunitdir=%{_unitdir}` and `-Dsysusersdir=%{_sysusersdir}` so Meson
  installs systemd units and sysusers definitions into the RPM macro-defined
  locations.
- Pass `-Dsysctl_config=enabled` to install the supported sysctl configuration.
- Pass `-Dssh_proxy=enabled` to retain the SSH proxy transport expected by the
  client package.
- Pass `-Dfirewall_backend_priority=%{firewall_backend_priority}` to preserve
  Azure Linux firewall backend ordering.

These options are explicit because several defaults and option relationships
changed in libvirt 11.x. Explicit values make the resulting package independent
of build-host auto-detection.

## Install cleanup

- Remove the Cloud Hypervisor Augeas lens and its test when `with_ch` is
  disabled. Upstream installs these data files independently of whether Azure
  Linux ships the driver, so cleanup keeps the package contents aligned with
  the selected feature set.

## File lists and ownership

- Added ownership of the Augeas lens and lens-test directories to the daemon
  common package. The package now owns the parent directories containing its
  installed lenses.
- Moved ownership of `%{_libdir}/libvirt/lock-driver/` from the lockd plugin to
  the daemon common package. The directory is shared infrastructure; the
  plugin subpackage continues to own `lockd.so` itself.
- Added `%{_sysusersdir}/libvirt.conf` to the daemon common package for the
  common libvirt system users installed by 11.9.0.
- Removed `libvirt_storage_file_fs.so` from the storage-core file list because
  libvirt 11.9.0 no longer builds or installs that module. The remaining
  `libvirt_storage_backend_fs.so` backend is still packaged.
- Made the QEMU post-copy migration sysctl file conditional on
  `with_userfaultfd_sysctl`, matching the Meson option and avoiding a missing
  file when the feature is disabled.
- Changed the QEMU sysusers file path from the hard-coded
  `%{_prefix}/lib/sysusers.d/libvirt-qemu.conf` to
  `%{_sysusersdir}/libvirt-qemu.conf`, matching the build option and RPM macro.
- Added explicit owner, group, and mode attributes to the QEMU runtime ghost
  directories. The top-level, `passt`, and `slirp` directories use mode 0755;
  the `dbus` and `swtpm` directories use mode 0770. All are owned by the
  configured QEMU user and group. This matches the directories created at
  runtime and prevents RPM from recording them as root-owned defaults.

## Validation

The completed package change was validated as follows:

- `rpmspec -P` parsed the updated spec successfully.
- `rpmspec -q` resolved the expected 11.9.0-1 subpackage set.
- `libvirt.signatures.json` passed JSON validation.
- The official 11.9.0 archive matched the recorded SHA-256 checksum.
- Both retained patches applied cleanly to the exact 11.9.0 source.
- `git diff --check` reported no whitespace errors.
- A targeted Azure Linux toolkit build completed successfully with
  `SRPM_PACK_LIST="libvirt"` and `PACKAGE_REBUILD_LIST="libvirt"`.
- The build produced 33 binary RPMs at version `11.9.0-1.azl3`, including all
  daemon drivers, client libraries, development files, documentation, NSS, and
  debuginfo packages.
- Representative built RPMs passed digest verification.
