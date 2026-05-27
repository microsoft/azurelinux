# Open Source Out-of-Tree Kernel Module Packaging Strategy — Azure Linux 4.0

## Overview

Azure Linux 4.0 builds out-of-tree kernel modules (kmods) as **subpackages of the kernel RPM** rather than as standalone packages. This ensures tight coupling between the kernel binary and its companion modules — eliminating version skew, simplifying dependency resolution, and guaranteeing that modules are always compiled against the exact kernel headers they will run on.

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
| `package` | After `%description` | Declare `%package -n kmod-<name>-<version>`, Provides, Requires |
| `prep` | End of `%prep` | Extract kmod source tarball |
| `build` | End of `%build` | Compile modules against kernel build tree |
| `install` | End of `%install` | Install `.ko` files, configs, licenses |
| `files` | After `%files modules-extra-matched` | `%post`/`%postun` scriptlets and file list |

## Naming and Versioning Strategy

The driver version is embedded directly in the kmod subpackage name (e.g., `kmod-nvidia-open-595.58.03`).

The subpackage is declared as:

```spec
%package -n kmod-%{_kmod_name}-%{nvidia_open_version}
```

The RPM Version/Release is inherited from the **kernel** (e.g., `kmod-nvidia-open-595.58.03-6.18.5-1.8.azl4.x86_64.rpm`). The driver version is also exposed via virtual Provides so that consumers can depend on it without pinning the kernel version:

```spec
Provides: nvidia-open-kmod-version = %{nvidia_open_version}
Provides: nvidia-kmod = %{nvidia_open_version}
Provides: kmod-nvidia-open = %{version}-%{release}
```

This means:
- `Requires: kmod-nvidia-open` → gets any driver version that matches the installed kernel
- `Requires: kmod-nvidia-open-595.58.03` → pins to that specific driver version's RPM name
- `Requires: nvidia-open-kmod-version = 595.58.03` → pins to a specific driver version via virtual Provides

Consumer packages (e.g., `nvidia-cuda-driver`) should use the virtual Provides, not the RPM version directly.

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
<name>_version = "1.0.0"     # driver version — becomes part of the RPM name
```

The driver version is embedded directly in the subpackage name (e.g., `kmod-foo-1.0.0`), enabling multiple driver versions to coexist (e.g., `kmod-foo-1.0.0` and `kmod-foo-2.0.0`).

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
kmod-nvidia-open-595.58.03-6.18.5-1.8.azl4.x86_64.rpm   ← kmod subpackage (driver 595.58.03)
```

The kmod RPM contains:
- `/lib/modules/%{KVERREL}/extra/nvidia/*.ko.xz` — compressed kernel modules
- `/etc/modprobe.d/kmod-nvidia-open-595.58.03.conf` — blacklist conflicting modules
- `/etc/depmod.d/kmod-nvidia-open-595.58.03.conf` — depmod override configuration
- `/usr/share/licenses/kmod-nvidia-open-595.58.03/COPYING` — license file

## Constraints and Limitations

1. **RPM `%include` is a preprocessor directive** — it cannot be used inside `%define`/`%global` macro bodies, generated from Lua, or made conditional at the `%include` line itself (the `%if` must be inside the included file).

2. **No parametric dispatch** — each kmod requires explicit `%global` + `%include` lines per phase. You cannot loop over kmod names with a single macro call due to the `%include` limitation above.

3. **Build time** — each additional kmod adds compilation time to the kernel build. The NVIDIA open modules add ~5-10 minutes to a ~25 minute kernel build.

4. **Module compression** — the kernel spec's `%post` processing compresses `.ko` files to `.ko.xz`. The `%files` section must reference the compressed names.

5. **Architecture restrictions** — use `%ifarch x86_64 aarch64` guards in prep/build/install phases to skip kmod work on architectures where the module is not supported.
