%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%endif
%define kernelver %{version}-%{release}
Summary:        Signed Unified Kernel Image for %{buildarch} systems
Name:           kernel-uki-signed-%{buildarch}
Version:        6.6.44.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-uki-%{kernelver}.%{buildarch}.rpm
Source1:        vmlinuz-uki-%{kernelver}.efi
ExclusiveArch:  x86_64

%description
This package contains the Unified Kernel Image (UKI) EFI binary signed for secure boot.
The package is specifically created for installing on %{buildarch} systems.

%package -n     kernel-uki
Summary:        Unified Kernel Image
Group:          System Environment/Kernel

%description -n kernel-uki
The kernel-uki package contains the Linux kernel packaged as a Unified
Kernel Image (UKI).

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed kernel-uki binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/vmlinuz-uki-%{kernelver}.efi

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n kernel-uki
/boot/vmlinuz-uki-%{kernelver}.efi
/lib/modules/%{kernelver}/vmlinuz-uki.efi

%changelog
* Wed Aug 14 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.44.1-1
- Auto-upgrade to 6.6.44.1

* Sat Aug 10 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-7
- Bump release to match kernel

* Wed Aug 07 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-6
- Bump release to match kernel

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
- Bump release to match kernel

* Fri Jul 05 2024 Gary Swalling <gaswal@microsoft.com> - 6.6.35.1-4
- Bump release to match kernel

* Mon Jul 01 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.35.1-3
- Bump release to match kernel

* Tue Jun 25 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.35.1-2
- Original version for Azure Linux.
- License verified.
