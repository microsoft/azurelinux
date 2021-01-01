%global debug_package %{nil}
Summary:        Signed GRand Unified Bootloader for aarch64 systems
Name:           grub2-efi-binary-signed-aarch64
Version:        2.02
Release:        26%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/grub
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
Source0:        grub2-efi-unsigned-%{version}-%{release}.aarch64.rpm
Source1:        grubaa64.efi
Conflicts:      grub2-efi-binary
ExclusiveArch:  aarch64

%description
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on aarch64 systems

%prep

%build

%install
mkdir -p %{buildroot}/boot/efi/EFI/BOOT
cp %{SOURCE1} %{buildroot}/boot/efi/EFI/BOOT/grubaa64.efi

%files
/boot/efi/EFI/BOOT/grubaa64.efi

%changelog
* Wed Dec 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-26
- Updating release to be aligned with the unsigned bits.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Updating release to be aligned with the unsigned bits.

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> 2.02-24
- Original version for CBL-Mariner.
