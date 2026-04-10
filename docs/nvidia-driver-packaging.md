# NVIDIA Driver Packaging Guidelines for Azure Linux

This document describes the packaging conventions for NVIDIA GPU driver
components on Azure Linux, covering both kernel modules and user-space
libraries/tools.

## Design Principles

1. **Kernel vs. user-space separation** — Kernel modules and user-space
   components are packaged independently. They share the same NVIDIA driver
   version but have no build-time dependency on each other.
2. **Headless / compute-only** — Azure Linux is a headless distro. Only
   compute, monitoring, and video encode/decode components are included.
   No X11, GLX, EGL, Vulkan, OptiX, or display-server libraries.
3. **Multi-kernel support** — Kernel modules can be built against multiple
   kernel versions using `component-templates` with a matrix axis. The
   user-space package works with any matching kernel module build.
4. **Three kernel module variants** — Kernel modules are available through
   three distinct sources, packaged as separate kmod variants:
   - **`kmod-nvidia-open`** — Open-source modules from NVIDIA's
     [open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
     repository (MIT+GPL). Default for CUDA compute on supported GPUs.
   - **`kmod-nvidia-closed`** — Proprietary modules from the NVIDIA
     datacenter `.run` installer. Same CUDA/datacenter driver branch as
     `open`, but required for GPUs not supported by the open-source modules.
   - **`kmod-nvidia-grid`** — Proprietary modules from the GRID/vGPU
     `-grid-azure.run` installer (published at `download.microsoft.com`).
     A separate driver branch with vGPU mediation support and embedded
     Azure licensing.
   
   All three variants conflict — only one can be installed at a time.

## Package Naming Conventions

### Kernel module packages: `kmod-nvidia-<variant>`

NVIDIA publishes kernel modules through three distinct channels. The `<variant>`
suffix identifies which **driver branch and source** the modules come from:

| Variant | Package name | Source | Description |
|---------|-------------|--------|-------------|
| `open` | `kmod-nvidia-open` | [open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules) (GitHub) | Open-source kernel modules (MIT+GPL). Default for CUDA compute on supported GPUs. |
| `closed` | `kmod-nvidia-closed` | NVIDIA datacenter `.run` installer | Proprietary kernel modules from the **CUDA/datacenter driver branch**. Required for GPUs not supported by the open-source modules, or when proprietary-only features are needed. |
| `grid` | `kmod-nvidia-grid` | GRID `-grid-azure.run` from `download.microsoft.com` | Proprietary kernel modules from the **GRID/vGPU driver branch**. Includes vGPU mediation support (`nvidia-vgpu-vfio.ko`). Azure licensing embedded. |

The variant names reflect the **driver branch**, not just the license:
- `open` vs `closed` distinguishes the source license within the same CUDA/datacenter branch
- `grid` identifies the entirely separate GRID/vGPU branch (different versions, different feature set)

All three **conflict** with each other — only one kmod variant can be installed at a time.

**Naming rules:**
- Prefix: `kmod-` (standard Linux convention for out-of-tree kernel modules)
- Driver name: `nvidia-<variant>` (identifies the source/branch)
- The kernel `uname -r` string is embedded in the **Release** tag, not the Name,
  so the same spec can build for any kernel version
- The component template name (e.g., `kmod-nvidia-open`) is expanded with a matrix
  suffix by azldev: `kmod-nvidia-open-6-18` is the component name for the
  6.18 kernel build

## Version and Release Conventions

### Shared version

Both `kmod-nvidia-open` and `nvidia-cuda-driver` use the **NVIDIA driver
version** as their RPM `Version:` tag:

```
Version:        595.58.03
```

This ensures `Requires: kmod-nvidia-open = %{version}` in the user-space
package pins to the correct driver release without caring about the kernel.

## Dependency Graph

```
nvidia-cuda-driver
├── Requires: (kmod-nvidia-open = 595.58.03 OR kmod-nvidia-closed = 595.58.03)
├── Requires: nvidia-cuda-driver-libs
└── Requires: nvidia-cuda-driver-firmware

kmod-nvidia-open (per kernel version)           kmod-nvidia-closed (per kernel version)
├── BuildRequires: kernel-devel                 ├── BuildRequires: kernel-devel
├── Requires: kernel-uname-r = <uname-r>       ├── Requires: kernel-uname-r = <uname-r>
├── Conflicts: kmod-nvidia-closed               ├── Conflicts: kmod-nvidia-open
├── Conflicts: kmod-nvidia-grid                 ├── Conflicts: kmod-nvidia-grid
├── Provides: kmod-nvidia-open = 595.58.03      ├── Provides: kmod-nvidia-closed = 595.58.03
└── Provides: kmod-nvidia-open-<uname-r>        └── Provides: kmod-nvidia-closed-<uname-r>
```

Key points:
- `nvidia-cuda-driver` works with **either** `kmod-nvidia-open` or
  `kmod-nvidia-closed` — both are the same CUDA/datacenter driver branch,
  just different kernel module sources (open-source vs proprietary)
- The dependency is **version-only** (matches on NVIDIA driver version,
  not kernel version)
- `kmod-nvidia-*` → `kernel-uname-r` is an **exact** dependency
  (must match the running kernel)
- All three kmod variants conflict with each other — only one can be installed
- Users install the kmod variant that matches their GPU and kernel; the
  user-space package works with any compatible kmod

## Component Definition Patterns

### Kernel modules: `component-templates` with matrix

The kmod uses `component-templates` with a `kernel` matrix axis. This causes
azldev to generate one component per kernel version:

```toml
[component-templates.kmod-nvidia-open]
description = "Out-of-tree driver built against multiple kernel versions"

[component-templates.kmod-nvidia-open.default-component-config]
spec = { type = "local", path = "kmod-nvidia-open.spec" }

[[component-templates.kmod-nvidia-open.matrix]]
axis = "kernel"

[component-templates.kmod-nvidia-open.matrix.values.6-18]
# No overlays needed — spec auto-detects kernel_uname_r from
# the installed kernel-devel headers at build time.
```

Resulting component name: `kmod-nvidia-open-6-18`

To add a new kernel version, add a new matrix value:

```toml
[component-templates.kmod-nvidia-open.matrix.values.6-12]
```

### User-space: standard `components`

The user-space driver is a normal (non-templated) component since it's
kernel-independent:

```toml
[components.nvidia-cuda-driver]
spec = { type = "local", path = "nvidia-cuda-driver.spec" }

[[components.nvidia-cuda-driver.source-files]]
filename = "NVIDIA-Linux-x86_64-595.58.03-no-compat32.run"
# ...

[[components.nvidia-cuda-driver.source-files]]
filename = "NVIDIA-Linux-aarch64-595.58.03.run"
# ...
```

Both x86_64 and aarch64 source files are listed; the spec uses `%ifarch`
to select the correct one at build time.

## Architecture Support

| Package | x86_64 | aarch64 |
|---------|--------|---------|
| `kmod-nvidia-open` | ✅ | ✅ |
| `nvidia-cuda-driver` | ✅ | ✅ |

The kernel module spec builds natively on both architectures using the
same source (NVIDIA's open-gpu-kernel-modules supports both).

## Kernel Version Auto-Detection

The `component-templates` matrix in the kmod TOML file defines which kernel
flavours to build against. When azldev expands the template, each matrix
value produces a distinct component (e.g., `kmod-nvidia-open-6-18`) whose
build configuration can specify the matching `kernel-<flavour>-devel`
package as a `BuildRequires`. This ensures the correct kernel headers are
pulled into the mock chroot for each flavour.

Once inside the chroot, the kmod spec auto-detects the exact kernel version
from the installed headers:

```rpm
%{!?kernel_uname_r: %global kernel_uname_r %(ls -1 /usr/src/kernels/ | sort -V | tail -1)}
```

This resolves to the `uname -r` string of whichever `kernel-devel` package
is installed in the mock chroot (e.g., `6.18.5-1.4.azl4.x86_64`).

To override manually:

```bash
rpmbuild --define 'kernel_uname_r 6.18.5-1.4.azl4.x86_64' ...
```

## Build Commands

```bash
# Build kernel (prerequisite — produces kernel-devel RPM)
azldev comp build -p kernel --local-repo-with-publish ./base/out -q

# Build kernel modules (uses kernel-devel from local repo)
azldev comp build -p kmod-nvidia-open --local-repo-with-publish ./base/out -q

# Build user-space driver
azldev comp build -p nvidia-cuda-driver --local-repo-with-publish ./base/out -q
```

Build order: `kernel` → `kmod-nvidia-open-*` → `nvidia-cuda-driver`
(the user-space package has no build-time dependency on the kmod, but
listing it after ensures the kmod RPM is available for integration testing).

## GRID / vGPU Packages

The open-source packages (`kmod-nvidia-open` + `nvidia-cuda-driver`) are for
**bare-metal GPU compute** (physical GPU or full GPU passthrough). They are
**not compatible** with NVIDIA GRID/vGPU workloads.

GRID/vGPU requires a separate set of packages built from proprietary `.run`
files redistributed by Microsoft. These `.run` files include Azure-specific
licensing for GRID Virtual GPU Software — **no separate NVIDIA vGPU license
server is required**. The drivers are published at `download.microsoft.com`
and are specific to Azure N-series VM families.

### GRID package split

| Package | Source | Contents |
|---------|--------|----------|
| `kmod-nvidia-grid` | GRID `-grid-azure.run` from `download.microsoft.com` | Proprietary kernel modules with vGPU mediation support (`nvidia.ko`, `nvidia-vgpu-vfio.ko`, etc.) |
| `nvidia-grid-driver` | GRID `-grid-azure.run` from `download.microsoft.com` | User-space GRID libraries, vGPU manager tools, and Azure licensing components |

### Naming conventions

- **`kmod-nvidia-grid`** — follows the `kmod-nvidia-<variant>` pattern with
  `grid` identifying the GRID/vGPU **driver branch**. This is distinct from
  `kmod-nvidia-closed` (proprietary CUDA/datacenter branch) and
  `kmod-nvidia-open` (open-source). The name reflects the branch, not just
  the license, because the CUDA and GRID branches carry different versions,
  different kernel modules (GRID includes `nvidia-vgpu-vfio.ko`), and target
  different workloads. All three kmod variants conflict with each other.
- **`nvidia-grid-driver`** — the user-space companion. Named `grid-driver`
  (not `cuda-driver`) to clearly indicate the GRID/vGPU purpose and avoid
  confusion with the bare-metal `nvidia-cuda-driver` package. These two
  user-space packages also conflict — a system runs either bare-metal compute
  or GRID, not both.

### Dependency graph (GRID)

```
nvidia-grid-driver
├── Requires: kmod-nvidia-grid = <grid-driver-version>
├── Requires: nvidia-grid-driver-libs
└── Requires: nvidia-grid-driver-firmware
    └── (GSP firmware + vGPU manager firmware)

kmod-nvidia-grid (per kernel version)
├── BuildRequires: kernel-devel
├── Requires: kernel-uname-r = <uname-r>
├── Conflicts: kmod-nvidia-open, kmod-nvidia-closed
└── Provides: kmod-nvidia-grid-<uname-r>
```

### Conflict matrix

| Installed | `kmod-nvidia-open` | `kmod-nvidia-closed` | `kmod-nvidia-grid` | `nvidia-cuda-driver` | `nvidia-grid-driver` |
|-----------|--------------------|-----------------------|--------------------|----------------------|----------------------|
| `kmod-nvidia-open` | — | ❌ Conflicts | ❌ Conflicts | ✅ | ❌ Conflicts |
| `kmod-nvidia-closed` | ❌ Conflicts | — | ❌ Conflicts | ✅ | ❌ Conflicts |
| `kmod-nvidia-grid` | ❌ Conflicts | ❌ Conflicts | — | ❌ Conflicts | ✅ |
| `nvidia-cuda-driver` | ✅ | ✅ | ❌ Conflicts | — | ❌ Conflicts |
| `nvidia-grid-driver` | ❌ Conflicts | ❌ Conflicts | ✅ | ❌ Conflicts | — |

A system installs **one** of three kmod variants and its matching user-space package:
- **`kmod-nvidia-open`** + `nvidia-cuda-driver` — open-source, bare-metal compute
- **`kmod-nvidia-closed`** + `nvidia-cuda-driver` — proprietary, bare-metal compute
- **`kmod-nvidia-grid`** + `nvidia-grid-driver` — proprietary, GRID/vGPU

Note that `nvidia-cuda-driver` pairs with **either** `kmod-nvidia-open` or
`kmod-nvidia-closed` (same CUDA/datacenter branch, different source license),
but `nvidia-grid-driver` **only** pairs with `kmod-nvidia-grid` (different
driver branch entirely).

### Build commands (GRID)

```bash
# Build GRID kernel modules
azldev comp build -p kmod-nvidia-grid --local-repo-with-publish ./base/out -q

# Build GRID user-space driver
azldev comp build -p nvidia-grid-driver --local-repo-with-publish ./base/out -q
```

> **Note:** Both `kmod-nvidia-grid` and `nvidia-grid-driver` use the
> same `.run` file as their source. The kmod spec extracts and builds only
> the kernel modules, while the user-space spec extracts only the libraries
> and tools (using `--no-kernel-modules`). The `-grid-azure` suffix in the
> filename distinguishes it from the public NVIDIA consumer/datacenter drivers.
