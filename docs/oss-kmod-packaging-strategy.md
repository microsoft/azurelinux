# Open Source Out-of-Tree Kernel Module Packaging Strategy — Azure Linux 4.0

## Overview

Azure Linux 4.0 builds out-of-tree kernel modules (kmods) as **subpackages of the kernel RPM** rather than as standalone packages. This ensures tight coupling between the kernel binary and its companion modules — eliminating version skew, simplifying dependency resolution, and guaranteeing that modules are always compiled against the exact kernel headers they will run on.

## Two Packaging Patterns

Both patterns build the kernel modules **within the kernel component's build scope**, so the modules are always compiled against the exact kernel they ship with. They differ in how the packaging is authored:

1. **Pure OSS kmods → kernel subpackage** (the default; the rest of this document). A self-contained `kmod-<name>.inc` file defines a `kmod-<name>` subpackage via phase-gated `%include`s. Used for standalone module sets such as `kmod-nvidia-open`.

2. **Combined kmod + userspace packages → `.inc` based on the upstream packaging.** Some vendor stacks ship kernel modules *and* userspace components together — for example the DOCA / NVIDIA MLNX OFED packages such as `mlnx-ofa_kernel`. For these we still use a `.inc` file wired into the kernel component (so the modules are built alongside — and against — the kernel), but instead of separating the kernel-module and userspace halves or renaming the kernel-modules subpackage, we base the `.inc` **on the upstream packaging**, keeping it as close to the upstream spec as possible. Concretely, `mlnx-ofa_kernel` derives its `.inc` from the upstream spec and is added to the Azure Linux 4.0 kernel build so its modules track the kernel they are built with, while its userspace pieces stay faithful to upstream.

   Prefer this pattern when a package is more than a bare set of `.ko` files (it has userspace libraries, tools, or its own subpackage layout), or when tracking a complex upstream spec is more maintainable than porting it to the phase-gated `.inc` framework.

   > **Known limitation — userspace cannot be multi-version.** Because the kmod is built in the kernel scope, its `.ko` files live under `/lib/modules/%{KVERREL}/` and are marked install-only, so the *module* half coexists cleanly across kernels. The **userspace** half (shared libraries, tools, headers) is a normal package: it installs to fixed, non-kernel-qualified paths and is *not* install-only. That means only one version of the userspace can be installed at a time. We hit this with `mlnx-ofa_kernel`: when two kernels each pulled in their own build, the kernel-module portions coexisted fine, but the accompanying userspace packages collided on identical paths / could not be installed side-by-side, so supporting multiple userspace versions simultaneously was not possible. If you need genuinely parallel-installable userspace, that userspace must be split into a separate, kernel-independent component with versioned paths — it cannot ride along inside the kernel scope.

## Architecture
consider kmod-nvidia-open as an example:
```
kernel.comp.toml
├── build.defines.nvidia_open_version = "595.58.03"
├── source-files[] → kernel tarball, NVIDIA tarball
├── overlays
│   ├── [nvidia-open sources] .inc, modprobe.conf (Source6000-6002)
│   └── [nvidia-open phases] spec-append-lines × 5 phases
│
└── Resulting kernel.spec (after overlays)
    ├── %description → %include kmod-nvidia-open.inc (phase=package)
    ├── %prep        → %include kmod-nvidia-open.inc (phase=prep)
    ├── %build       → %include kmod-nvidia-open.inc (phase=build)
    ├── %install     → %include kmod-nvidia-open.inc (phase=install)
    └── %files       → %include kmod-nvidia-open.inc (phase=files)
```

### Key Files

| File | Purpose |
|------|---------|
| `kmod-<name>.inc` | Self-contained subpackage definition with phase-gated `%if` blocks |
| `kmod-<name>-modprobe.conf` | Module loading configuration (blacklists, options) |
| `kernel.comp.toml` | Overlay definitions that wire everything together |

## Phase-Gated Include Pattern

RPM's `%include` directive is a preprocessor operation — it injects file contents literally into the spec at parse time. Since `%include` cannot appear inside macro bodies, we use a **phase-gating** pattern:

```spec
# At each build phase, set the phase variable then include the kmod file:
%global _kmod_phase build
%global _kmod_name nvidia-open
%include %{_sourcedir}/kmod-nvidia-open.inc
```

Inside the `.inc` file, each section is guarded:

```spec
%if "%{_kmod_phase}" == "build"
# ... build commands ...
%endif
```

This allows a single `.inc` file to contain all phases of a kmod's lifecycle while only activating the relevant section at each point in the spec.

### Phase Execution Order

| Phase | Injection Point | Purpose |
|-------|----------------|---------|
| `package` | After `%description` | Declare `%package -n kmod-<name>` (Version = driver, Release = kernel NVR), Provides, Requires |
| `prep` | End of `%prep` | Extract kmod source tarball |
| `build` | End of `%build` | Compile modules against kernel build tree |
| `install` | End of `%install` | Install `.ko` files, configs, licenses |
| `files` | After `%files modules-extra-matched` | `%post`/`%postun` scriptlets and file list |

## Naming and Versioning Strategy

The kmod subpackage name is **stable** — it does *not* embed the driver version
(e.g., `kmod-nvidia-open`). The driver version and the kernel it was built for
are encoded in the RPM Version/Release instead:

```spec
%package -n kmod-%{_kmod_name}
Version: %{nvidia_open_version}
Release: %{_azl_kver}.%{_azl_krel}   # kernel Version.Release
```

This yields NVRAs like `kmod-nvidia-open-595.58.03-6.18.5.1.8.azl4.x86_64.rpm`,
where `595.58.03` is the NVIDIA driver version and `6.18.5-1.8.azl4` is the
kernel NVR. The package is marked install-only (`installonlypkg(kernel-module)`)
so that one build per kernel can be installed side-by-side.

### The `%{version}`/`%{release}` macro dance

Setting `Version:`/`Release:` inside a subpackage clobbers the global
`%{version}`/`%{release}` macros at parse time. Because this `.inc` is included
into the middle of `kernel.spec`, the kernel NVR is snapshotted before the
`%package` and restored **immediately after the `Version:`/`Release:` tags** —
before anything downstream (the `Requires:` and `%description`) uses them. This
matters because `%{KVERREL}` is defined as `%{specversion}-%{release}.%{_target_cpu}`;
if `%{release}` is still clobbered when the `Requires: %{name}-core-uname-r =
%{KVERREL}` line is parsed, the kmod requires a bogus, unsatisfiable kernel and
`dnf install` fails to resolve:

```spec
%global _azl_kver %{version}    # snapshot kernel NVR
%global _azl_krel %{release}
%package -n kmod-%{_kmod_name}
Version: %{nvidia_open_version}
Release: %{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}     # restore immediately, before %{KVERREL} is used
%global release %{_azl_krel}
...
Requires: %{name}-core-uname-r = %{KVERREL}
```

The driver version is also exposed via virtual Provides so that consumers can
depend on it without pinning the kernel version:

```spec
Provides: nvidia-open-kmod-version = %{nvidia_open_version}
Provides: nvidia-kmod = %{nvidia_open_version}
```

This means:
- `Requires: kmod-nvidia-open` → gets the kmod matching the installed kernel
- `Requires: nvidia-open-kmod-version = 595.58.03` → pins a specific driver version
- `Requires: nvidia-kmod` → any NVIDIA kmod flavor (open or closed)

Consumer packages (e.g., `nvidia-cuda-driver`) can use the virtual Provides,
instead of the RPM version directly.

### Per-kernel file paths

Files that do not already live under `/lib/modules/%{KVERREL}/` — the modprobe
config and the license — are keyed by `%{KVERREL}` (not the driver version) so
that multiple per-kernel kmod packages sharing the same driver version do not
collide on identical paths:

- `%{_modprobedir}/kmod-nvidia-open-%{KVERREL}.conf`
- `%{_datadir}/licenses/kmod-nvidia-open-%{KVERREL}/COPYING`

## Auto-upgrade: kernel-tracked kmod via a `-matched` sentinel

### The problem

The per-kernel kmod is install-only and hard-requires its exact kernel
(`Requires: %{name}-core-uname-r = %{KVERREL}`). That guarantees a kmod is only
ever installed next to the kernel it was built against, but it gives dnf no
reason to install the kmod for a *newly upgraded* kernel. A plain `dnf upgrade`
therefore pulls in the new kernel, keeps the old kernel + old kmod (both
install-only), and leaves the new kernel with **no NVIDIA modules** — after
rebooting into it the driver is silently missing until someone manually runs
`dnf install kmod-nvidia-open`.

### The fix — a `-matched` sentinel package

Mirroring the kernel's own `kernel-modules-extra-matched` mechanism, we add a
tiny, file-less **sentinel** subpackage plus a boolean dependency so that kmod
installation tracks the kernel automatically — but only when the admin has
opted in. Three pieces:

1. The per-kernel kmod advertises a version-matched capability:

   ```spec
   Provides: kmod-nvidia-open-uname-r = %{KVERREL}
   ```

2. An empty meta/sentinel subpackage acts as the opt-in switch:

   ```spec
   %package -n kmod-nvidia-open-matched
   Summary: Meta package to ensure kmod-nvidia-open is installed for all kernels
   %description -n kmod-nvidia-open-matched
   ...
   %files -n kmod-nvidia-open-matched
   # empty sentinel package — no files
   ```

3. The **base kernel package** gains a rich/boolean dependency (guarded to the
   supported arches), right next to
   the existing `kernel-modules-extra-matched` requirement:

   ```spec
   Requires: ((kmod-nvidia-open-uname-r = %{KVERREL}) if kmod-nvidia-open-matched)
   ```

   Read it as: *"if `kmod-nvidia-open-matched` is installed, then this kernel
   requires the kmod built for exactly this kernel."*

### Why this works

- **Opt-in / opt-out:** if the sentinel is not installed, the `if` clause is
  false, so no kernel forces an NVIDIA kmod — users who don't want the driver
  are unaffected.
- **Auto-tracking:** once the sentinel is installed a single time, *every*
  kernel package (present and future) carries the conditional requirement. When
  `dnf upgrade` installs a new kernel, that kernel's boolean `Requires` fires
  and dnf pulls in the `kmod-nvidia-open` whose
  `Provides: kmod-nvidia-open-uname-r = %{KVERREL}` matches the new kernel —
  installed alongside the retained old one. Boot into the new kernel and the
  modules are already present.

The dependency is attached to the *kernel* package (not the kmod) precisely so
that it re-evaluates for each kernel that gets installed; that is what makes
future kernels keep dragging in their own matching kmod without any manual step.

## Adding a New kmod

### 1. Create the `.inc` file

```
base/comps/kernel/kmod-<name>.inc
```

Use `kmod-nvidia-open.inc` as a template. Implement all 5 phases with `%if "%{_kmod_phase}" == "<phase>"` guards.

### 2. Create supporting files

- `kmod-<name>-modprobe.conf` — module loading config (blacklists, options)
- Any patches specific to the kmod

### 3. Add build defines for version

In `kernel.comp.toml`, add the driver version define:

```toml
[components.kernel.build.defines]
<name>_version = "1.0.0"     # driver version — becomes the RPM Version of the kmod
```

The driver version becomes the RPM `Version:` of the kmod subpackage while the
subpackage name stays stable (e.g., `kmod-foo`). Combined with the install-only
marker, this lets the per-kernel builds coexist.

### 4. Add source-files entry (if external tarball needed)

```toml
[[components.kernel.source-files]]
filename = "my-module-1.0.tar.gz"
hash = "..."
hash-type = "SHA256"
origin = { type = "download", uri = "https://..." }
```

### 5. Add overlays to `kernel.comp.toml`

```toml
# Source registration (use Source6100+ range for the new kmod)
[[components.kernel.overlays]]
description = "Add kmod-<name>.inc to sources"
type = "file-add"
file = "kmod-<name>.inc"
source = "kmod-<name>.inc"

[[components.kernel.overlays]]
description = "Register kmod-<name> tarball as Sourcexxxx"
type = "spec-insert-tag"
tag = "Sourcexxxx"
value = "my-module-1.0.tar.gz"

[[components.kernel.overlays]]
description = "Register kmod-<name>.inc as Sourcexxxx++"
type = "spec-insert-tag"
tag = "Sourcexxx++"
value = "kmod-<name>.inc"

# Phase injection (repeat for each phase)
[[components.kernel.overlays]]
description = "Run kmod-<name> 'package' phase"
type = "spec-append-lines"
section = "%description"
lines = [
    "",
    "%global _kmod_phase package",
    "%global _kmod_name <name>",
    "%include %{_sourcedir}/kmod-<name>.inc",
]

# ... repeat for prep, build, install, files ...
```

### 6. Validate

```bash
azldev comp render -p kernel          # Check overlays apply cleanly
azldev comp build -p kernel           # Full build + kmod compilation
```

## Source Number Allocation

| Range | Reserved For |
|-------|-------------|
| 5000–5099 | AZL kernel configs and certificates |
| 6000–6099 | kmod-nvidia-open |
| 6100–6199 | (next kmod) |
| 6200–6299 | (next kmod) |

## RPM Output

A successful kernel build produces (among others) the following RPMs, consider kmod-nvidia-open as an example:

```
kernel-6.18.5-1.8.azl4.x86_64.rpm
kernel-core-6.18.5-1.8.azl4.x86_64.rpm
kernel-modules-6.18.5-1.8.azl4.x86_64.rpm
kmod-nvidia-open-595.58.03-6.18.5.1.8.azl4.x86_64.rpm   ← kmod subpackage (Version = driver 595.58.03, Release = kernel NVR)
```

The kmod RPM contains:
- `/lib/modules/%{KVERREL}/extra/nvidia/*.ko.xz` — compressed kernel modules
- `/usr/lib/modprobe.d/kmod-nvidia-open-%{KVERREL}.conf` — blacklist conflicting modules
- `/usr/share/licenses/kmod-nvidia-open-%{KVERREL}/COPYING` — license file

## Constraints and Limitations

1. **RPM `%include` is a preprocessor directive** — it cannot be used inside `%define`/`%global` macro bodies, generated from Lua, or made conditional at the `%include` line itself (the `%if` must be inside the included file).

2. **No parametric dispatch** — each kmod requires explicit `%global` + `%include` lines per phase. You cannot loop over kmod names with a single macro call due to the `%include` limitation above.

3. **Build time** — each additional kmod adds compilation time to the kernel build. The NVIDIA open modules add ~5-10 minutes to a ~25 minute kernel build.

4. **Module compression** — the kernel spec's `%post` processing compresses `.ko` files to `.ko.xz`. The `%files` section must reference the compressed names.

5. **Architecture restrictions** — use `%ifarch x86_64 aarch64` guards in prep/build/install phases to skip kmod work on architectures where the module is not supported.
