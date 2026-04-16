---
applyTo: 'SPECS*/**/*.spec'
description: Always apply these instructions when editing `*.spec` files that build or repackage
**out-of-tree (OOT) kernel modules**. Such specs are identifiable by the
presence of `azl_kernel_*` macros (e.g., `azl_kernel_version`,
`azl_kernel_hwe_version`).
---

# Out-of-Tree (OOT) Kernel Module Spec File Conventions

## Instructions context

The specs to be analyzed with these instructions live under:

- `SPECS-NVIDIA/` and `SPECS-AMD/` — **unsigned** (build) specs.
- `SPECS-NVIDIA-SIGNED/` and `SPECS-AMD-SIGNED/` — **signed** (repackaging) specs.

Above directory pairs are only examples - there may be additional directories for OOT specs,
but they must follow the same conventions outlined in this document.

---

## 1. Kernel and Dependency Version Macros

### 1.1 Resolving the Target Kernel Version

Always use the `azl_kernel_*` macros provided by the build system. **Never** use
`rpm -q` shell queries to discover the kernel version at build time.

- Example for the **default kernel**:

  ```rpm
  %global target_kernel_version_full %{azl_kernel_version}-%{azl_kernel_release}%{?dist}
  %global release_suffix _%{azl_kernel_version}.%{azl_kernel_release}
  ```

- Example for the **HWE kernel**:

  ```rpm
  %global target_kernel_version_full %{azl_kernel_hwe_version}-%{azl_kernel_hwe_release}%{?dist}
  %global release_suffix _%{azl_kernel_hwe_version}.%{azl_kernel_hwe_release}
  ```

### 1.2 Extending the Release Suffix with Additional Version Components

When the OOT module is tied to both a specific kernel **and** another package
version (e.g., an NVIDIA driver version), the release suffix may be extended:

```rpm
%global release_suffix _%{azl_kernel_version}.%{azl_kernel_release}.%{NVIDIA_DRIVER_VERSION}
```

This is the exception, not the default. Use it only when the kernel module
binary is specific to that additional dependency's exact version.

### 1.3 Resolving Non-Kernel Package Version

When the spec also depends on non-kernel packages (i.e., MOFED packages), resolve the version through the
`azl_<pkg>_*` (i.e., `azl_mlnx_ofa_kernel_*`) macros:

- For the **default kernel**:

  ```rpm
  %{!?_mofed_full_version: %define _mofed_full_version %{azl_mlnx_ofa_kernel_version}-%{azl_mlnx_ofa_kernel_release}%{?dist}}
  ```

  Or simpler:
  ```rpm
  %define _mofed_full_version %{azl_mlnx_ofa_kernel_version}-%{azl_mlnx_ofa_kernel_release}%{?dist}
  ```

- For the **HWE kernel**:

  ```rpm
  %{!?_mofed_hwe_full_version: %define _mofed_hwe_full_version %{azl_mlnx_ofa_kernel_hwe_version}-%{azl_mlnx_ofa_kernel_hwe_release}%{?dist}}
  ```

  Or simpler:
  ```rpm
  %define _mofed_hwe_full_version %{azl_mlnx_ofa_kernel_hwe_version}-%{azl_mlnx_ofa_kernel_hwe_release}%{?dist}
  ``` 

---

## 2. Release Tag Format

### 2.1 Packages/Subpackages Containing OOT Modules

```rpm
Release:        [number][kernel_version_related_suffix]%{?dist}
```

Example from `gdrcopy-hwe-kmod` subpackage in `gdrcopy-hwe.spec`.
```rpm
Release:        %{_release}_%{target_azl_build_kernel_version}.%{target_kernel_release}.%{NVIDIA_DRIVER_VERSION}%{?dist}
```

### 2.2 Packages/Subpackages NOT Containing OOT Modules

```rpm
Release:        [number]%{?dist}
```

The `[kernel_version_related_suffix]` is **not needed** for subpackages that contain only
kernel-independent components (usermode binaries, libraries, services, docs).

Example from `gdrcopy` base subpackage in `gdrcopy.spec`.
```rpm
Release:        %{_release}%{?dist}
```

### 2.3 Reusing the Release Number Across Subpackages

When the same release number must appear in multiple subpackages, encode it as a
macro to avoid repetition:

```rpm
%{!?_release: %define _release 3}
```

Then reference it in each `Release:` tag:

```rpm
# kmod subpackage (kernel-tied)
Release: %{_release}%{release_suffix}%{?dist}

# service subpackage (kernel-independent)
Release: %{_release}%{?dist}
```

---

## 3. Subpackage Separation

### 3.1 Principle

Subpackages containing OOT kernel modules (`.ko` files) **must not** contain
components that are not tied to a specific kernel version. Kernel-independent
components include:

- Usermode binaries and scripts.
- Shared libraries (`.so` files).
- Systemd service units.
- udev rules.
- Configuration files not specific to the kernel module.
- Documentation and man pages.

### 3.2 Reference Implementation

The `gdrcopy` spec family is the current exemplar for proper separation:

- `gdrcopy` — userspace library and test binaries.
- `gdrcopy-service` — systemd service components.
- `gdrcopy-dkms-src` — DKMS source for runtime compilation.
- `gdrcopy-kmod` — prebuilt `gdrdrv.ko`, pinned to a specific kernel and NVIDIA
  driver version.

### 3.3 Known Gap

Most current specs (`cuda-open`, `cuda`, `amdgpu`, `amd-ama-driver`,
`nvidia-vgpu-guest-driver`) bundle kernel modules and usermode components in a
single package with `%{release_suffix}`. This is a known gap to be addressed in
future refactoring. New specs **must** follow the separated pattern from the
start.

---

## 4. Unsigned / Signed Spec Pair

Every OOT driver requires **two** specs:

### 4.1 Unsigned Spec (Build)

Located in `SPECS-NVIDIA/` or `SPECS-AMD/`. Responsibilities:

- Compile kernel modules from source.
- Install unsigned `.ko` files (useful for dev testing with kernel lockdown
  disabled).
- Place unlinked `.o` / `.ko` files in `kmod_o_dir` to be picked up by the
  signing pipeline.

### 4.2 Signed Spec (Repackaging)

Located in `SPECS-NVIDIA-SIGNED/` or `SPECS-AMD-SIGNED/`. Responsibilities:

- Take the unsigned RPM as `Source0`, referenced as
  `<name>-%{version}-%{release}.%{_arch}.rpm`.
- Strip unsigned `.ko` files from the extracted contents.
- Install signed `.ko` files provided as additional `Source` entries.
- Repackage everything into the final RPM.
- Repeat pre-/post-install scripts from the unsigned spec as needed for the subpackage they override from the unsigned spec.

**Mandatory** in signed specs — prevent RPM post-processing from stripping
module signatures:

```rpm
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}
```

Signed specs have an **empty `%build` section** — they never compile.

---

## 5. Build and Runtime Dependencies

### 5.1 Kernel Dependencies

```rpm
# Build-time
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}

# Runtime
Requires:       kernel = %{target_kernel_version_full}
```

For GPU drivers, also add:

```rpm
Requires:       kernel-drivers-gpu = %{target_kernel_version_full}
```

For **HWE kernel** variants, replace `kernel`/`kernel-devel`/`kernel-headers`
with `kernel-hwe`/`kernel-hwe-devel`/`kernel-hwe-headers`, and
`kernel-drivers-gpu` with `kernel-hwe-drivers-gpu`.

### 5.2 MOFED Dependencies

When InfiniBand / GPUDirect RDMA support is needed:

```rpm
BuildRequires:  mlnx-ofa_kernel-devel = %{_mofed_full_version}
BuildRequires:  mlnx-ofa_kernel = %{_mofed_full_version}
BuildRequires:  mlnx-ofa_kernel-modules = %{_mofed_full_version}
BuildRequires:  mlnx-ofa_kernel-source = %{_mofed_full_version}

Requires:       mlnx-ofa_kernel = %{_mofed_full_version}
Requires:       mlnx-ofa_kernel-modules = %{_mofed_full_version}
```

For **HWE kernel** variants, use `mlnx-ofa_kernel-hwe-*` package names and
`%{_mofed_hwe_full_version}`.

---

## 6. Common Boilerplate

### 6.1 Standard Tags

```rpm
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
```

### 6.2 Changelog Format

```
*   Day Mon DD YYYY Full Name <email@microsoft.com> - VERSION-RELEASE
-   Description of change.
```

Date format: `Day Mon DD YYYY` (e.g., `Tue Mar 24 2026`).

---

## 7. HWE Kernel Variant Naming Cheat Sheet

When creating an HWE variant of an existing spec, apply these substitutions
throughout the entire spec:

| Default kernel | HWE kernel |
|---|---|
| `%azl_kernel_version` | `%azl_kernel_hwe_version` |
| `%azl_kernel_release` | `%azl_kernel_hwe_release` |
| `%azl_mlnx_ofa_kernel_version` | `%azl_mlnx_ofa_kernel_hwe_version` |
| `%azl_mlnx_ofa_kernel_release` | `%azl_mlnx_ofa_kernel_hwe_release` |
| `kernel` (package name) | `kernel-hwe` |
| `kernel-devel` | `kernel-hwe-devel` |
| `kernel-headers` | `kernel-hwe-headers` |
| `kernel-drivers-gpu` | `kernel-hwe-drivers-gpu` |
| `mlnx-ofa_kernel-*` | `mlnx-ofa_kernel-hwe-*` |
| `_mofed_full_version` | `_mofed_hwe_full_version` |

---

## 8. Quick-Reference: Minimal Preamble Template

```rpm
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global driver_version <DRIVER_VERSION>

%global target_kernel_version_full %{azl_kernel_version}-%{azl_kernel_release}%{?dist}
%global release_suffix _%{azl_kernel_version}.%{azl_kernel_release}

# Only if MOFED is needed:
%{!?_mofed_full_version: %define _mofed_full_version %{azl_mlnx_ofa_kernel_version}-%{azl_mlnx_ofa_kernel_release}%{?dist}}

Name:           <package-name>
Version:        %{driver_version}
Release:        1%{release_suffix}%{?dist}
Summary:        <summary>
License:        <license>
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
```
