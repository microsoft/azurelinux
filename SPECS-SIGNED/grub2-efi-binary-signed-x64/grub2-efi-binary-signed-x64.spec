%global debug_package %{nil}
Summary:        Signed GRand Unified Bootloader for x86_64 systems
Name:           grub2-efi-binary-signed-x64
Version:        2.02
Release:        24%{?dist}
URL:            https://www.gnu.org/software/grub
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner

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
Source0:        grub2-efi-unsigned-%{version}-%{release}.x86_64.rpm
Source1:        grubx64.efi

ExclusiveArch:  x86_64

Conflicts:      grub2-efi-binary

%description
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on x86_64 systems

%prep

%build

%install
mkdir -p %{buildroot}/boot/efi/EFI/BOOT
cp %{SOURCE1} %{buildroot}/boot/efi/EFI/BOOT/grubx64.efi

%files
/boot/efi/EFI/BOOT/grubx64.efi

%changelog
* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> 2.02-24
- Original version for CBL-Mariner.