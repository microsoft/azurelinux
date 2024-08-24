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
Version:        6.6.47.1
Release:        1%{?dist}
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
BuildRequires:  systemd-boot
BuildRequires:  systemd-udev
BuildRequires:  system-release
BuildRequires:  tpm2-tools
BuildRequires:  cryptsetup
BuildRequires:  device-mapper
BuildRequires:  kbd
ExclusiveArch:  x86_64

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
install -vdm 700 %{buildroot}/boot
install -vdm 700 %{buildroot}/lib/modules/%{kernelver}
install -vm 600 vmlinuz-uki.efi %{buildroot}/boot/vmlinuz-uki-%{kernelver}.efi
ln -s /boot/vmlinuz-uki-%{kernelver}.efi %{buildroot}/lib/modules/%{kernelver}/vmlinuz-uki.efi

%files
/boot/vmlinuz-uki-%{kernelver}.efi
/lib/modules/%{kernelver}/vmlinuz-uki.efi

%changelog
* Thu Aug 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.47.1-1
- Auto-upgrade to 6.6.47.1

* Wed Aug 14 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.44.1-1
- Auto-upgrade to 6.6.44.1

* Sat Aug 10 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-7
- Include systemd-cryptsetup in UKI

* Wed Aug 07 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-6
- Rebuild UKI with new initrd

* Tue Aug 06 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-5
- Bump release to match kernel

* Sat Aug 03 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-4
- Bump release to match kernel

* Thu Aug 01 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.43.1-3
- Bump release to match kernel

* Wed Jul 31 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-2
- Bump release to match kernel

* Tue Jul 30 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.43.1-1
- Auto-upgrade to 6.6.43.1

* Tue Jul 30 2024 Chris Co <chrco@microsoft.com> - 6.6.39.1-2
- Bump release to match kernel

* Fri Jul 26 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.39.1-1
- Auto-upgrade to 6.6.39.1

* Tue Jul 16 2024 Kelsey Steele <kelseysteele@microsoft.com> - 6.6.35.1-6
- Bump release to match kernel

* Wed Jul 10 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.35.1-5
- Add tag to build exclusively on x86_64

* Fri Jul 05 2024 Gary Swalling <gaswal@microsoft.com> - 6.6.35.1-4
- Bump release to match kernel

* Mon Jul 01 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.35.1-3
- Bump release to match kernel

* Fri Jun 28 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.35.1-2
- Bump release to match kernel

* Tue Jun 25 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.35.1-1
- Auto-upgrade to 6.6.35.1

* Wed Jun 12 2024 Dan Streetman <ddstreet@microsoft.com> - 6.6.29.1-6
- include i18n (kbd package) in UKI, to provide loadkeys binary so
  systemd-vconsole-setup works

* Tue Jun 11 2024 Juan Camposeco <juanarturoc@microsoft.com> - 6.6.29.1-5
- Bump release to match kernel

* Thu Apr 25 2024 Dan Streetman <ddstreet@microsoft.com> - 6.6.29.1-4
- Original version for Azure Linux.
- License verified.
