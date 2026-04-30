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
│   ├── [framework] kmod-macros.inc (Source5999)
│   ├── [nvidia-open sources] .inc, modprobe.conf (Source6000-6002)
│   └── [nvidia-open phases] spec-append-lines × 5 phases
│
└── Resulting kernel.spec (after overlays)
    ├── %include kmod-macros.inc          ← framework preamble
    ├── %description → %include nvidia-open.inc (phase=package)
    ├── %prep        → %include nvidia-open.inc (phase=prep)
    ├── %build       → %include nvidia-open.inc (phase=build)
    ├── %install     → %include nvidia-open.inc (phase=install)
    └── %files       → %include nvidia-open.inc (phase=files)
```

### Key Files

| File | Purpose |
|------|---------|
| `kmod-macros.inc` | Framework documentation and `%global kmod_subpackages` registry |
| `kmod-<name>.inc` | Self-contained subpackage definition with phase-gated `%if` blocks |
| `kmod-<name>.conf` | Module loading configuration (blacklists, options) |
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
| `package` | After `%description` | Declare `%package -n kmod-<name>`, Provides, Requires |
| `prep` | End of `%prep` | Extract kmod source tarball |
| `build` | End of `%build` | Compile modules against kernel build tree |
| `install` | End of `%install` | Install `.ko` files, configs, licenses |
| `files` | After `%files modules-extra-matched` | `%post`/`%postun` scriptlets and file list |

## Versioning Strategy

A kmod subpackage inherits the **kernel version** as its RPM Version/Release (e.g., `kmod-nvidia-open-6.18.5-1.8.azl4.x86_64.rpm`). The actual driver version is tracked via a virtual Provides:

```spec
Provides: nvidia-open-kmod-version = %{nvidia_open_version}
```

This means:
- `Requires: kmod-nvidia-open` → gets whatever version matches the installed kernel
- `Requires: nvidia-open-kmod-version = 595.58.03` → pins to a specific driver version

Consumer packages (e.g., `nvidia-cuda-driver`) should use the virtual Provides, not the RPM version directly.

## Adding a New kmod

### 1. Create the `.inc` file

```
base/comps/kernel/kmod-<name>.inc
```

Use `kmod-nvidia-open.inc` as a template. Implement all 5 phases with `%if "%{_kmod_phase}" == "<phase>"` guards.

### 2. Create supporting files

- `kmod-<name>.conf` — module loading config (blacklists, options)
- Any patches specific to the kmod

### 3. Add source-files entry (if external tarball needed)

```toml
[[components.kernel.source-files]]
filename = "my-module-1.0.tar.gz"
hash = "..."
hash-type = "SHA256"
origin = { type = "download", uri = "https://..." }
```

### 4. Add overlays to `kernel.comp.toml`

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

### 5. Register in kmod-macros.inc

Add the name to the `kmod_subpackages` list:

```spec
%global kmod_subpackages nvidia-open <name>
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
| 5999 | kmod-macros.inc (framework) |
| 6000–6099 | kmod-nvidia-open |
| 6100–6199 | (next kmod) |
| 6200–6299 | (next kmod) |

## RPM Output

A successful kernel build produces (among others) the following RPMs, consider kmod-nvidia-open as an example:

```
kernel-6.18.5-1.8.azl4.x86_64.rpm
kernel-core-6.18.5-1.8.azl4.x86_64.rpm
kernel-modules-6.18.5-1.8.azl4.x86_64.rpm
kmod-nvidia-open-6.18.5-1.8.azl4.x86_64.rpm   ← kmod subpackage
```

The kmod RPM contains:
- `/lib/modules/%{KVERREL}/extra/nvidia/*.ko.xz` — compressed kernel modules
- `/etc/modprobe.d/kmod-nvidia-open.conf` — blacklist conflicting modules
- `/etc/depmod.d/kmod-nvidia-open.conf` — depmod override configuration
- `/usr/share/licenses/kmod-nvidia-open/COPYING` — license file

## Constraints and Limitations

1. **RPM `%include` is a preprocessor directive** — it cannot be used inside `%define`/`%global` macro bodies, generated from Lua, or made conditional at the `%include` line itself (the `%if` must be inside the included file).

2. **No parametric dispatch** — each kmod requires explicit `%global` + `%include` lines per phase. You cannot loop over kmod names with a single macro call due to the `%include` limitation above.

3. **Build time** — each additional kmod adds compilation time to the kernel build. The NVIDIA open modules add ~5-10 minutes to a ~25 minute kernel build.

4. **Module compression** — the kernel spec's `%post` processing compresses `.ko` files to `.ko.xz`. The `%files` section must reference the compressed names.

5. **Architecture restrictions** — use `%ifnarch noarch %nobuildarches` guards in prep/build/install phases to skip kmod work on doc-only or excluded architecture builds.
