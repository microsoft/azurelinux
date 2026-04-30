# kmod-nvidia-open.inc — NVIDIA open GPU kernel module subpackage
#
# Phases: package, prep, build, install, files
# Activated by: %{run_kmod_phase <phase>} from kmod-macros.inc
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   %{nvidia_open_version}  — NVIDIA driver version (e.g. 595.58.03)
#   %{SOURCE6000}           — open-gpu-kernel-modules tarball
#   %{SOURCE6001}           — kmod-nvidia-open-modprobe.conf

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package"

%package -n kmod-%{_kmod_name}
Summary:        NVIDIA open GPU kernel modules (driver %{nvidia_open_version})
# NOTE: Version is inherited from kernel (%{version}), NOT nvidia_open_version.
# Track the actual NVIDIA driver version via Provides for dependency resolution.
Provides:       nvidia-open-kmod-version = %{nvidia_open_version}
Provides:       kmod-%{_kmod_name} = %{version}-%{release}
Provides:       kmod-%{_kmod_name}-%{KVERREL} = %{version}-%{release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod
Conflicts:      nvidia-closed-kmod
Conflicts:      nvidia-open
ExclusiveArch:  x86_64 aarch64

%description -n kmod-%{_kmod_name}
Open-source NVIDIA GPU kernel modules (driver version %{nvidia_open_version})
built from the official NVIDIA/open-gpu-kernel-modules repository for
kernel %{KVERREL}.

These modules support CUDA workloads on NVIDIA GPUs (Turing and later).
Modules: nvidia.ko, nvidia-modeset.ko, nvidia-drm.ko, nvidia-uvm.ko,
nvidia-peermem.ko.

NOTE: This subpackage has the kernel version (%{version}-%{release}), not the
NVIDIA driver version. Use 'Requires: nvidia-open-kmod-version = %{nvidia_open_version}'
to depend on a specific NVIDIA driver version.

%endif

# =========================================================================
# Phase: prep — extract NVIDIA source tarball
# =========================================================================
%if "%{_kmod_phase}" == "prep"

%ifnarch noarch %nobuildarches
cd %{_builddir}
tar -xf %{SOURCE6000}
cd -
%endif

%endif

# =========================================================================
# Phase: build — compile NVIDIA kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build"

%if %{with_up_base}
%ifnarch noarch %nobuildarches
%{log_msg "Building NVIDIA open GPU kernel modules %{nvidia_open_version} for %{KVERREL}"}
pushd %{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}
# Unset LDFLAGS — NVIDIA kbuild invokes ld directly, not via gcc
unset LDFLAGS
make %{?_smp_mflags} modules \
    KERNEL_UNAME="%{KVERREL}" \
    SYSSRC="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    SYSOUT="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    IGNORE_CC_MISMATCH=1 \
    IGNORE_XEN_PRESENCE=1 \
    IGNORE_PREEMPT_RT_PRESENCE=1 \
    NV_EXCLUDE_BUILD_MODULES=""
popd
%endif
%endif

%endif

# =========================================================================
# Phase: install — install modules, config, and license
# =========================================================================
%if "%{_kmod_phase}" == "install"

%if %{with_up_base}
%ifnarch noarch %nobuildarches
%{log_msg "Installing NVIDIA open GPU kernel modules for %{KVERREL}"}
install -d $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/extra/nvidia
for mod in nvidia nvidia-modeset nvidia-drm nvidia-uvm nvidia-peermem; do
    ko="%{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}/kernel-open/${mod}.ko"
    if [ -f "${ko}" ]; then
        install -m 0644 "${ko}" $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/extra/nvidia/
    fi
done
# Install modprobe config to blacklist conflicting modules
install -D -m 0644 %{SOURCE6001} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/kmod-%{_kmod_name}.conf
# Install depmod override config
install -d $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/kmod-%{_kmod_name}.conf << 'DEPMOD_EOF'
override nvidia %{KVERREL} extra/nvidia
override nvidia-modeset %{KVERREL} extra/nvidia
override nvidia-drm %{KVERREL} extra/nvidia
override nvidia-uvm %{KVERREL} extra/nvidia
override nvidia-peermem %{KVERREL} extra/nvidia
DEPMOD_EOF
# Install NVIDIA license file
install -D -m 0644 %{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}/COPYING \
    $RPM_BUILD_ROOT%{_datadir}/licenses/kmod-%{_kmod_name}/COPYING
%endif
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files"

%post -n kmod-%{_kmod_name}
/usr/sbin/depmod -a %{KVERREL} || :

%postun -n kmod-%{_kmod_name}
/usr/sbin/depmod -a %{KVERREL} || :

%files -n kmod-%{_kmod_name}
%license %{_datadir}/licenses/kmod-%{_kmod_name}/COPYING
/lib/modules/%{KVERREL}/extra/nvidia/nvidia.ko.xz
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-modeset.ko.xz
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-drm.ko.xz
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-uvm.ko.xz
/lib/modules/%{KVERREL}/extra/nvidia/nvidia-peermem.ko.xz
%config(noreplace) %{_sysconfdir}/modprobe.d/kmod-%{_kmod_name}.conf
%{_sysconfdir}/depmod.d/kmod-%{_kmod_name}.conf

%endif
