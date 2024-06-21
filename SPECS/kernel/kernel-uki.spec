%global debug_package %{nil}

# This should be a subpackage of the kernel package, but due to
# "circular dependencies" that is not possible, so this is instead a
# separate source package

# Note - while Fedora's kernel version includes the %%_target_cpu as a
# suffix, our kernel version does not.
%define kernelver %{version}-%{release}

# noxsaves: Azure CVM instances have trouble booting due to the hypervisor
# not reporting an available CPU feature - shadow stack (X86_FEATURE_SHSTK).
# We need to temporarily turn it off by disabling xsaves until the problem
# is fixed on Azure. Since shadow stack depends on xsaves, disabling xsaves
# ensures the feature bit for shadow stack is also turned off.
%define cmdline console=ttyS0 noxsaves

Summary:        Unified Kernel Image
Name:           kernel-uki
Version:        6.6.29.1
Release:        6%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Source0:        kernel-uki-dracut.conf

BuildRequires:  kernel = %{version}-%{release}
BuildRequires:  systemd-ukify
BuildRequires:  dracut
BuildRequires:  binutils
BuildRequires:  systemd-boot-unsigned
BuildRequires:  systemd-udev
BuildRequires:  system-release
BuildRequires:  tpm2-tools
BuildRequires:  cryptsetup
BuildRequires:  device-mapper
BuildRequires:  kbd

%description
The kernel-uki package contains the Linux kernel packaged as a Unified
Kernel Image (UKI).

%prep
%setup -c -T

%build
dracut --conf=%{SOURCE0} --confdir=$(mktemp -d) --logfile=$(mktemp) \
       --verbose \
       --kver %{kernelver} \
       --kernel-image /lib/modules/%{kernelver}/vmlinuz \
       --kernel-cmdline "%{cmdline}" initrd
ukify build \
      --uname %{kernelver} \
      --linux /lib/modules/%{kernelver}/vmlinuz \
      --initrd initrd \
      --cmdline "%{cmdline}" \
      --output vmlinuz-uki.efi

%install
install -D -t %{buildroot}/lib/modules/%{kernelver} vmlinuz-uki.efi

%files
/lib/modules/%{kernelver}/vmlinuz-uki.efi

%changelog
* Wed Jun 12 2024 Dan Streetman <ddstreet@microsoft.com> - 6.6.29.1-6
- include i18n (kbd package) in UKI, to provide loadkeys binary so
  systemd-vconsole-setup works

* Tue Jun 11 2024 Juan Camposeco <juanarturoc@microsoft.com> - 6.6.29.1-5
- Bump release to match kernel

* Thu Apr 25 2024 Dan Streetman <ddstreet@microsoft.com> - 6.6.29.1-4
- Original version for Azure Linux.
- License verified.
