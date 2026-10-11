# Confidential Kata UVM kernel

`kernel-uvm-cc` provides an x86_64 guest kernel for standard-injection AMD
SEV-SNP. It is separate from the host kernel and ordinary `kernel-uvm`.

## Source

The source archive is the same public `6.18.52.mshv1` archive used by
`kernel-uvm`. The three patches are exported with `git format-patch` from
[chris-oo/CBL-Mariner-Linux-Kernel](https://github.com/chris-oo/CBL-Mariner-Linux-Kernel),
branch `snp-6.18-guest-unregister`:

| Commit | Change |
|---|---|
| `8e6fbce77670c1b4c8fee378ce500798a18ef79e` | Unregister the decompressor GHCB when the hypervisor advertises support |
| `a8b36965a44c36c6c1a5367e80f23ba987bf64a4` | Enable x2APIC early |
| `6e82e92b07ad74d2b1ec86df90193b1db0d07d48` | Allocate output pages for enlightened SNP AP startup |

The older shared-GHCB reservation workaround and experimental build helper
are not included.

## Configuration

The checked-in `config` is copied unchanged from
`SPECS/kernel-uvm/config` at Azure Linux commit
`93ed6be3c36495aed184b5f22d712dda17f2f3ca`.
It is a full resolved Kconfig, not a feature fragment. Required SNP,
Hyper-V, virtio, EROFS, ext4, device-mapper, and dm-verity support is built in.

To update it, start from the distro UVM config, apply these source patches,
and run `make ARCH=x86_64 oldconfig` with the package build toolchain.
Review all changes before copying the result back. The source tree's
`Microsoft/configs/x86/uvm_defconfig` is an upstream seed, not an exact
replacement for the distro's resolved config.

Package preparation rejects config drift except for the generated release
header and `CONFIG_LOCALVERSION`. The running kernel identifies itself as
`6.18.52-mshv1-<RPM release>.uvm-cc`; moving the upstream flavor after the
first hyphen keeps `X.Y.Z-suffix` parsing compatible with guest userspace.
The RPM version remains `6.18.52.mshv1`. Automatic Git suffixes stay disabled.

Use the same kernel for production/debug IGVM profiles. Console, shell,
and SNP hardware-debug policy still need to be set by the image/runtime
profile; this package does not enforce those policies by itself.

## Installed artifacts

| Path | Purpose |
|---|---|
| `/usr/share/kernel-uvm-cc/bzImage` | Kernel input for `igvmfilegen` |
| `/usr/share/kernel-uvm-cc/vmlinux.bin` | Uncompressed companion; not a substitute for the IGVM bzImage input |
| `/usr/share/kernel-uvm-cc/config` | Actual resolved build configuration |
| `/usr/share/kernel-uvm-cc/kernel.release` | Actual kernel release string |

Build dependencies, compiler flags, default kernel build targets, and the
devel packaging follow `kernel-uvm.spec`. The main package also provides
`/lib/modules/kernel-uvm-cc/vmlinux`, pointing to its own uncompressed image.
The `kernel-uvm-cc-devel` subpackage contains headers, build scripts,
`Module.symvers`, and objtool under `/usr/src/linux-headers-<kernel release>`,
with `/lib/modules/<kernel release>/build` pointing there. Its exact-version
dependency keeps it paired with the main package.

Neither package installs host `/boot` files, GRUB settings, initramfs
triggers, or ordinary UVM files. Like ordinary UVM packaging, the default
kernel build includes configured modules, but no loadable modules are
installed into the RPMs. Required guest functionality is built in.

Installing the RPM does not change an existing guest image. Node image
setup must explicitly use its bzImage when generating the IGVM, retain
the matching rootfs/verity configuration, and record the new measurements.
Signed or endorsed images require the corresponding signing/endorsement
process; do not silently replace their kernel.

Package checks cover artifact presence, required built-ins, and release
identity. They do not establish SNP boot, multi-vCPU, attestation, or
teardown acceptance. Those require the packaged kernel in the intended
host/VMM/Hyper-V stack. ARM64 is not supported by this package.
