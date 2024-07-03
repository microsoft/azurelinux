%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%endif

# Support for quick builds with rpmbuild --build-in-place.
# See README.build-in-place
%bcond inplace 0
Summary:        Signed systemd-boot for %{buildarch} systems
Name:           systemd-boot-%{buildarch}
%if %{without inplace}
Version:        255
%else
# determine the build information from local checkout
Version:        %(tools/meson-vcs-tag.sh . error | sed -r 's/-([0-9])/.^\1/; s/-g/_g/')
%endif
Release:        15%{?dist}
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
Source0:        systemd-boot-%{version}-%{release}.%{buildarch}.rpm
Source1:        systemd-bootx64.efi
ExclusiveArch:  x86_64

%description
This package contains the systemd-boot EFI binary signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     systemd-boot
Summary:        UEFI boot manager (signed version)

Provides: systemd-boot-%{efi_arch} = %version-%release
Provides: systemd-boot = %version-%release
Provides: systemd-boot%{_isa} = %{version}-%{release}
# A provides with just the version, no release or dist, used to build systemd-boot
Provides: version(systemd-boot) = %version
Provides: version(systemd-boot)%{_isa} = %version

# self-obsoletes to install both packages after split of systemd-boot
Obsoletes: systemd-udev < 252.2^

%description -n systemd-boot
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the signed version that works with Secure Boot.

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed systemd-boot binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./usr/lib/systemd/boot/efi/systemd-bootx64.efi

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n systemd-boot
/usr/lib/systemd/boot/efi/*
/usr/share/man/man5/loader.conf.5.gz
/usr/share/man/man7/sd-boot.7.gz
/usr/share/man/man7/systemd-boot.7.gz

%changelog
* Tue Jun 25 2024 Thien Trung Vuong <tvuong@microsoft.com> - 255-15
- Original version for Azure Linux.
- License verified.
