# kmod-nvidia-open.inc — NVIDIA open GPU kernel module subpackage
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase global + include from kernel.comp.toml overlays
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   nvidia_open_version  — NVIDIA driver version (e.g. 595.58.03)
#   SOURCE6000           — open-gpu-kernel-modules tarball
#   SOURCE6001           — kmod-nvidia-open-modprobe.conf

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
# Snapshot the kernel NVR, then give this subpackage its own Version (the NVIDIA
# driver version) and Release (the kernel NVR). Setting Version/Release clobbers
# the global %{version}/%{release} macros at parse time, so restore them right
# after the tags below — before %{KVERREL} (which expands %{release}) is used in
# the Requires and %description.
%global _azl_kver %{version}
%global _azl_krel %{release}
%package -n kmod-%{_kmod_name}
Summary:        NVIDIA open GPU kernel modules (driver %{nvidia_open_version})
Version:        %{nvidia_open_version}
Release:        %{_azl_kver}.%{_azl_krel}
# Restore kernel NVR macros clobbered by the Version/Release tags above.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
# Track the actual NVIDIA driver version via Provides for dependency resolution.
Provides:       nvidia-open-kmod-version = %{nvidia_open_version}
Provides:       nvidia-kmod = %{nvidia_open_version}
Provides:       kmod-nvidia-open-uname-r = %{KVERREL}
# Mark this kmod as install-only so multiple versions can coexist alongside
# their matching kernels (dnf/dnf5 default installonlypkgs includes the
# 'installonlypkg(kernel-module)' token).
Provides:       installonlypkg(kernel-module)
Requires:       %{name}-core-uname-r = %{KVERREL}
# TODO: Add userspace package dependency when package name/version contract is finalized.
# Requires:       <nvidia-userspace-package> = %{nvidia_open_version}
Requires(post): kmod
Requires(postun): kmod
Conflicts:      nvidia-closed-kmod

%description -n kmod-%{_kmod_name}
Open-source NVIDIA GPU kernel modules (driver version %{nvidia_open_version})
built from the official NVIDIA/open-gpu-kernel-modules repository for
kernel %{KVERREL}.

These modules support CUDA workloads on NVIDIA GPUs (Turing and later).
Each kernel version produces a separate kmod package
(kmod-nvidia-open-<nvidia_driver_version>-<KVERREL>) so that multiple kernel versions
can coexist with their own NVIDIA modules.
Use 'Requires: nvidia-open-kmod-version = %{nvidia_open_version}' to depend on a
specific NVIDIA driver version, or 'Requires: nvidia-kmod = %{nvidia_open_version}' to
depend on a specific NVIDIA driver package version.

%package -n kmod-nvidia-open-matched
Summary:        Meta package to ensure kmod-nvidia-open is installed for all kernels

%description -n kmod-nvidia-open-matched
This meta package provides a single reference that other packages can Require to have kmod-nvidia-open installed for all kernels. When installed, the kernel package automatically pulls in the version-matched kmod-nvidia-open for each kernel version on this machine (x86_64 and aarch64 only).

%endif

%endif

# =========================================================================
# Phase: prep — extract NVIDIA source tarball
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6000}
popd
%endif

%endif

# =========================================================================
# Phase: build — compile NVIDIA kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building NVIDIA open GPU kernel modules %{nvidia_open_version} for %{KVERREL}"}
pushd %{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}
# Unset LDFLAGS — NVIDIA kbuild invokes ld directly, not via gcc
unset LDFLAGS
# IGNORE_CC_MISMATCH=1: kmod is a kernel subpackage built in the same
# mock chroot with the same GCC. The flag suppresses NVIDIA's compiler-string
# comparison which can false-positive on path or version-string formatting
# differences even when the toolchain is identical.
# CONFIG_OBJTOOL_WERROR=: NVIDIA's precompiled binary blob (nv-kernel.o_binary)
# contains bare 'ret' instructions that fail objtool's rethunk validation when
# CONFIG_MITIGATION_RETHUNK=y. Clearing this config on the make command line
# propagates through GNU make's recursive $(MAKE) into kbuild, turning the
# objtool errors into non-fatal warnings. The kernel itself is already fully
# built and validated with objtool by this point.
# Ref: https://forums.developer.nvidia.com/t/360610
make %{?_smp_mflags} modules \
    KERNEL_UNAME="%{KVERREL}" \
    SYSSRC="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    SYSOUT="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    IGNORE_CC_MISMATCH=1 \
    IGNORE_XEN_PRESENCE=1 \
    IGNORE_PREEMPT_RT_PRESENCE=1 \
    NV_EXCLUDE_BUILD_MODULES="" \
    CONFIG_OBJTOOL_WERROR=
popd
%endif

%endif

# =========================================================================
# Phase: install — install modules, config, and license
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing NVIDIA open GPU kernel modules for %{KVERREL}"}
install -d %{buildroot}/lib/modules/%{KVERREL}/extra/nvidia
for mod in nvidia nvidia-modeset nvidia-drm nvidia-uvm nvidia-peermem; do
    ko="%{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}/kernel-open/${mod}.ko"
    install -m 0644 "${ko}" %{buildroot}/lib/modules/%{KVERREL}/extra/nvidia/
done
# Install modprobe config to blacklist conflicting modules. Lives under
# %{_modprobedir} (/usr/lib/modprobe.d) — vendor-supplied config, not
# admin-editable, so it is owned by the package without %config(noreplace).
# Path is keyed by %{KVERREL} (not the driver version) so that per-kernel kmod
# packages sharing the same driver version can coexist without file conflicts.
install -D -m 0644 %{SOURCE6001} %{buildroot}%{_modprobedir}/kmod-%{_kmod_name}-%{KVERREL}.conf
# Install NVIDIA license file (keyed by %{KVERREL} for the same coexistence reason)
install -D -m 0644 %{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}/COPYING \
    %{buildroot}%{_datadir}/licenses/kmod-%{_kmod_name}-%{KVERREL}/COPYING
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kmod-%{_kmod_name}
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kmod-%{_kmod_name}
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n kmod-%{_kmod_name}
%license %{_datadir}/licenses/kmod-%{_kmod_name}-%{KVERREL}/COPYING
/lib/modules/%{KVERREL}/extra/nvidia/nvidia.ko.%{compext}
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-modeset.ko.%{compext}
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-drm.ko.%{compext}
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-uvm.ko.%{compext}
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-peermem.ko.%{compext}
%{_modprobedir}/kmod-%{_kmod_name}-%{KVERREL}.conf

%files -n kmod-nvidia-open-matched
# empty sentinel package — no files

%endif

%endif
