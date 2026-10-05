# kmod-nvidia-open.inc — NVIDIA open GPU kernel module subpackages
#   kmod-nvidia-open          — nvidia, nvidia-modeset, nvidia-drm, nvidia-uvm
#   kmod-nvidia-open-peermem  — nvidia-peermem (opt-in; requires MLNX OFED)
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
%global _azl_kver %{version}
%global _azl_krel %{release}
%package -n kmod-%{_kmod_name}
Summary:        NVIDIA open GPU kernel modules (driver %{nvidia_open_version})
License:        MIT OR GPL-2.0-only
Version:        %{nvidia_open_version}
Release:        %{_azl_kver}.%{_azl_krel}
# Restore kernel NVR macros clobbered by the Version/Release tags above.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       nvidia-open-kmod-version = %{nvidia_open_version}
Provides:       nvidia-kmod = %{nvidia_open_version}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod
Conflicts:      nvidia-closed-kmod

%description -n kmod-%{_kmod_name}
Open-source NVIDIA GPU kernel modules (driver version %{nvidia_open_version})
built from the official NVIDIA/open-gpu-kernel-modules repository for
kernel %{KVERREL}.

# AZL: nvidia-peermem is split out because it needs the MLNX OFED stack, which
# replaces the in-tree RDMA stack. Installing the GPU driver must not pull it in.
%package -n kmod-%{_kmod_name}-peermem
Summary:        NVIDIA peer memory (GPUDirect RDMA) kernel module (driver %{nvidia_open_version})
License:        MIT OR GPL-2.0-only
Version:        %{nvidia_open_version}
Release:        %{_azl_kver}.%{_azl_krel}
# Restore kernel NVR macros clobbered by the Version/Release tags above.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Requires:       kmod-%{_kmod_name}%{?_isa} = %{nvidia_open_version}-%{_azl_kver}.%{_azl_krel}
Requires:       mlnx-ofa_kernel-modules%{?_isa} = %{ofa_version}-%{ofa_release}.%{_azl_kver}.%{_azl_krel}
Requires(post): kmod
Requires(postun): kmod
# Pulled in automatically once the MLNX OFED stack is installed for this kernel.
Supplements:    (kmod-%{_kmod_name} = %{nvidia_open_version}-%{_azl_kver}.%{_azl_krel} and mlnx-ofa_kernel-modules-uname-r = %{KVERREL})

%description -n kmod-%{_kmod_name}-peermem
nvidia-peermem kernel module (driver version %{nvidia_open_version}) for
kernel %{KVERREL}. It registers NVIDIA GPU memory with the MLNX OFED
peer-memory interface for GPUDirect RDMA. Installing it pulls in the MLNX
OFED kernel stack (mlnx-ofa_kernel-modules), which replaces the in-tree
RDMA stack for this kernel.

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
patch -p1 -d %{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version} < %{SOURCE6003}
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
make %{?_smp_mflags} modules \
    KERNEL_UNAME="%{KVERREL}" \
    SYSSRC="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    SYSOUT="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    MLNX_OFED_KERNEL_DIR="%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj" \
    KBUILD_EXTRA_SYMBOLS="%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default/Module.symvers" \
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
install -D -m 0644 %{SOURCE6001} %{buildroot}%{_modprobedir}/kmod-%{_kmod_name}-%{KVERREL}.conf
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
%{_modprobedir}/kmod-%{_kmod_name}-%{KVERREL}.conf

%post -n kmod-%{_kmod_name}-peermem
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kmod-%{_kmod_name}-peermem
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n kmod-%{_kmod_name}-peermem
%license %{_datadir}/licenses/kmod-%{_kmod_name}-%{KVERREL}/COPYING
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-peermem.ko.%{compext}

%endif

%endif
