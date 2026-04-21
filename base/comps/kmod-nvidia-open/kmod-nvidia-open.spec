# Azure Linux NVIDIA open GPU kernel modules
# Built from: https://github.com/NVIDIA/open-gpu-kernel-modules

# Kernel modules are built via kbuild outside the normal RPM build tree,
# so automatic debuginfo extraction fails with empty debugsourcefiles.list.
%global debug_package %{nil}

# Detect the kernel version from the installed kernel-devel package at
# RPM build time. Uses Lua to suppress errors during SRPM build when
# kernel-devel is not yet installed.
%{!?kernel_uname_r: %{lua:
  local handle = io.popen("rpm -q --qf '%{VERSION}-%{RELEASE}.%{ARCH}' " .. rpm.expand("%{kernel_devel_pkg_name}") .. " 2>/dev/null")
  local result = handle:read("*a")
  handle:close()
  if result and result ~= "" and not result:match("^package") then
    rpm.define("kernel_uname_r " .. result)
  end
}}

%global kmod_install_dir /lib/modules/%{kernel_uname_r}/extra/nvidia

Name:           kmod-nvidia-open
Version:        595.58.03
Release:        3%{?dist}
Summary:        NVIDIA open GPU kernel modules for CUDA workloads
License:        MIT AND GPLv2
URL:            https://github.com/NVIDIA/open-gpu-kernel-modules
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64 aarch64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{version}.tar.gz#/open-gpu-kernel-modules-%{version}.tar.gz
Source1:        kmod-nvidia-open-modprobe.conf

BuildRequires:  %{kernel_devel_pkg_name}
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils

%{?kernel_uname_r:Requires:       kernel-uname-r = %{kernel_uname_r}}
Requires(post): kmod
Requires(postun): kmod

Provides:       nvidia-open-kmod = %{version}-%{release}
Provides:       kmod-nvidia-open = %{version}-%{release}
%{?kernel_uname_r:Provides:       kmod-nvidia-open-%{kernel_uname_r} = %{version}-%{release}}

# Prevent conflicting NVIDIA driver packages from being installed
# nvidia-closed-kmod is provided by Azure Linux; nvidia-open is provided by Nvidia
Conflicts:      nvidia-closed-kmod
Conflicts:      nvidia-open

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
