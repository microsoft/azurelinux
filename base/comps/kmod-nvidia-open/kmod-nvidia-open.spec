# Azure Linux NVIDIA open GPU kernel modules
# Built from: https://github.com/NVIDIA/open-gpu-kernel-modules

# Kernel modules are built via kbuild outside the normal RPM build tree,
# so automatic debuginfo extraction fails with empty debugsourcefiles.list.
%global debug_package %{nil}

# Auto-detect the kernel version from the installed kernel-devel package.
# The kernel-devel package installs headers to /usr/src/kernels/<uname-r>.
# This is resolved at RPM build time (inside mock), after BuildRequires
# are installed — so the directory will exist.
#
# To override: rpmbuild --define 'kernel_uname_r 6.18.5-1.4.azl4.x86_64'
%{!?kernel_uname_r: %global kernel_uname_r %(ls -1 /usr/src/kernels/ 2>/dev/null | sort -V | tail -1)}

%global kmod_install_dir /lib/modules/%{kernel_uname_r}/extra/nvidia

Name:           kmod-nvidia-open
Version:        595.58.03
Release:        3_%{kernel_uname_r}%{?dist}
Summary:        NVIDIA open GPU kernel modules for CUDA workloads
License:        MIT AND GPLv2
URL:            https://github.com/NVIDIA/open-gpu-kernel-modules
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64 aarch64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{version}.tar.gz#/open-gpu-kernel-modules-%{version}.tar.gz
Source1:        kmod-nvidia-open-modprobe.conf

BuildRequires:  kernel-%{kernel_flavour-}devel # macro expands by azldev. if not set it falls back to the default kernel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils

Requires:       kernel-uname-r = %{kernel_uname_r}
Requires(post): kmod
Requires(postun): kmod

Provides:       nvidia-open-kmod = %{version}-%{release}
Provides:       kmod-nvidia-open = %{version}-%{release}
Provides:       kmod-nvidia-open-%{kernel_uname_r} = %{version}-%{release}

# Prevent conflicting NVIDIA driver packages from being installed
Conflicts:      nvidia-closed-kmod # provided by Azure Linux
Conflicts:      nvidia-open # provided by Nvidia

%description
Open-source NVIDIA GPU kernel modules built from the official
NVIDIA/open-gpu-kernel-modules repository for kernel %{kernel_uname_r}.

These modules support CUDA workloads on NVIDIA GPUs with compute
capability 5.0 and later. The modules are built using the open-source
kernel module variant (nvidia-open).

Modules included:
  - nvidia.ko          (core driver)
  - nvidia-modeset.ko  (modesetting support)
  - nvidia-drm.ko      (DRM/KMS support)
  - nvidia-uvm.ko      (unified virtual memory)
  - nvidia-peermem.ko   (GPU peer memory for RDMA)

%prep
%autosetup -n open-gpu-kernel-modules-%{version}

%build
# Unset LDFLAGS — NVIDIA's kbuild invokes ld directly (not via gcc),
# so it doesn't understand the -Wl, prefix in RPM's default hardening flags.
unset LDFLAGS

# Build the open kernel modules
# KERNEL_UNAME must match the target kernel exactly
make %{?_smp_mflags} modules -j$(nproc) \
    KERNEL_UNAME="%{kernel_uname_r}" \
    SYSSRC="/usr/src/kernels/%{kernel_uname_r}" \
    SYSOUT="/usr/src/kernels/%{kernel_uname_r}" \
    IGNORE_CC_MISMATCH=1 \
    IGNORE_XEN_PRESENCE=1 \
    IGNORE_PREEMPT_RT_PRESENCE=1 \
    NV_EXCLUDE_BUILD_MODULES="" \
    INSTALL_MOD_DIR="extra/nvidia"

%install
install -d %{buildroot}%{kmod_install_dir}

# Install the built kernel modules
for mod in nvidia nvidia-modeset nvidia-drm nvidia-uvm nvidia-peermem; do
    ko="kernel-open/${mod}.ko"
    if [ -f "${ko}" ]; then
        install -m 0644 "${ko}" %{buildroot}%{kmod_install_dir}/
    fi
done

# Install modprobe configuration to blacklist conflicting modules
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/modprobe.d/kmod-nvidia-open.conf

# Generate modules.dep metadata at build time (weak-modules support)
install -d %{buildroot}%{_sysconfdir}/depmod.d
cat > %{buildroot}%{_sysconfdir}/depmod.d/kmod-nvidia-open.conf << 'EOF'
# Ensure NVIDIA modules in extra/ override any in-tree modules
override nvidia %{kernel_uname_r} extra/nvidia
override nvidia-modeset %{kernel_uname_r} extra/nvidia
override nvidia-drm %{kernel_uname_r} extra/nvidia
override nvidia-uvm %{kernel_uname_r} extra/nvidia
override nvidia-peermem %{kernel_uname_r} extra/nvidia
EOF

%post
/usr/sbin/depmod -a %{kernel_uname_r} || :

%postun
/usr/sbin/depmod -a %{kernel_uname_r} || :

%files
%license COPYING
%{kmod_install_dir}/nvidia.ko
%{kmod_install_dir}/nvidia-modeset.ko
%{kmod_install_dir}/nvidia-drm.ko
%{kmod_install_dir}/nvidia-uvm.ko
%{kmod_install_dir}/nvidia-peermem.ko
%config(noreplace) %{_sysconfdir}/modprobe.d/kmod-nvidia-open.conf
%{_sysconfdir}/depmod.d/kmod-nvidia-open.conf

%changelog
* Thu Apr 10 2026 Elaheh Dehghani <edehghani@microsoft.com> - 595.58.03-2
- Auto-detect kernel version from installed kernel-devel package
- Remove hardcoded kernel_version macro dependency

* Thu Apr 09 2026 Elaheh Dehghani <edehghani@microsoft.com> - 595.58.03-1
- Initial Azure Linux 4.0 package
- Built from NVIDIA/open-gpu-kernel-modules upstream source
- Open-source kernel modules for CUDA workloads
