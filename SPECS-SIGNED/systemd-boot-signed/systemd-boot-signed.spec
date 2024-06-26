%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%endif
Summary:        Signed systemd-boot for %{buildarch} systems
Name:           systemd-signed-%{buildarch}
Version:        255
Release:        14%{?dist}
License:        LGPL-2.1-or-later AND MIT AND GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://systemd.io
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
Source0:        systemd-boot-unsigned-%{version}-%{release}.%{buildarch}.rpm
Source1:        systemd-bootx64.efi
ExclusiveArch:  x86_64

%description
This package contains the systemd-boot EFI binary signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     systemd-boot
Summary:        UEFI boot manager (signed version)

%description -n systemd-boot
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the signed version that works with Secure Boot.

%prep

%build
mkdir rpm_contents
push rpm_contents

# This spec's whole purpose is to inject the signed systemd-boot binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./lib/systemd/boot/efi/systemd-bootx64.efi

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n systemd-boot
/lib/systemd/boot/efi/systemd-bootx64.efi

%changelog
* Tue June 25 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.29.1-6
- Original version for Azure Linux.
- License verified.
