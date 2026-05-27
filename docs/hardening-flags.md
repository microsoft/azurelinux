# Hardening Flags for Azure Linux 4.0 Builds

## Why this matters

Azure Linux 4.0 builds use Fedora's `redhat-rpm-config` as-is, which does not
enable `%_hardened_build` by default. As a result, BinSkim compliance scans
fail on most native packages with three rules:

| Rule   | Issue                  | Flag needed                  |
| ------ | ---------------------- | ---------------------------- |
| BA3001 | Not PIE                | `-fPIE -pie`                 |
| BA3003 | No stack protector     | `-fstack-protector-strong`   |
| BA3011 | RELRO not enabled      | `-Wl,-z,relro,-z,now`        |

The fix is to inject these flags through RPM macros so every spec that uses
`%configure`, `%cmake`, `%meson`, or `%make_build` picks them up automatically.
The same approach works for both stage1 and stage2.

## The flags we want set

```
%_hardened_build 1
%__global_compiler_flags -O2 -g -fstack-protector-strong -fstack-clash-protection -fPIE -D_FORTIFY_SOURCE=3
%__global_ldflags -Wl,-z,relro,-z,now -Wl,-z,noexecstack -pie
```

## Option A — set macros per component

Add the macros to a component's `[components.<name>.build.defines]` block in
its `comp.toml`. `azldev` will write a sidecar `<name>.azl.macros` file and
add `%{load:…}` to the rendered spec.

Example: [base/comps/dracut/dracut.comp.toml](../base/comps/dracut/dracut.comp.toml).

**Good for**: trying flag changes on one package without affecting anything else.

**Bad for**: distro-wide rollout — you'd repeat the same block in every
component's TOML.

## Option B — ship the macros in an RPM

Build a tiny noarch package (`azl-bootstrap-hardening`) that drops a
`macros.azl-bootstrap-hardening` file into `/usr/lib/rpm/macros.d/`. When
that package is installed in the buildroot, `rpm` reads the file at startup
and the macros apply to every build.

Install it everywhere by adding it once to `chroot_setup_cmd` in each mock
template:

| Stage  | File |
| ------ | ---- |
| stage1 | [distro/mock/azl4/stage1/azurelinux-4.0.tpl](../distro/mock/azl4/stage1/azurelinux-4.0.tpl) |
| stage2 | [distro/mock/azl4/stage2/azurelinux-4.0.tpl](../distro/mock/azl4/stage2/azurelinux-4.0.tpl) |

No spec edits required.

Package definition: [base/comps/azl-bootstrap-hardening/](../base/comps/azl-bootstrap-hardening/).

## Which to use

|                              | Option A          | Option B           |
| ---------------------------- | ----------------- | ------------------ |
| Spec edits                   | per component     | none               |
| Source of truth              | many TOML files   | one RPM            |
| Arch-conditional macros      | no                | yes (`%ifarch`)    |
| Revert                       | per component     | one mock line      |
| Works in stage1              | yes               | yes                |
| Works in stage2              | yes               | yes                |

**Recommendation: Option B.** Single source of truth, no per-spec churn, and
the same package can be dropped into both stage1 and stage2 buildroots.

Keep Option A available as a way to test flag changes on one package before
updating the distro-wide macros file.

## What this won't fix

Some packages will still fail compliance after the flags are set globally.
These need per-spec work and aren't solved by either option:

- Build systems that clobber `CFLAGS`/`LDFLAGS` (raw `cmake`, raw `go build`).
- Rust uses `RUSTFLAGS`, not `CFLAGS` — needs a separate macro.
- Asm-only or prebuilt-blob packages — candidates for a "known exceptions" list.
