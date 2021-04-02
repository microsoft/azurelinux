%global debug_package %{nil}
Summary:        Signed GRand Unified Bootloader for x86_64 systems
Name:           grub2-efi-binary-signed-x64
Version:        2.06~rc1
Release:        3%{?dist}
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
Source0:        grub2-efi-unsigned-%{version}-%{release}.x86_64.rpm
Source1:        grubx64.efi
Conflicts:      grub2-efi-binary
ExclusiveArch:  x86_64

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
* Fri Apr 02 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.06~rc1-3
- Update release to be aligned with unsigned version

* Fri Mar 26 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-2
- Update release to be aligned with unsigned version

* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-1
- Update to 2.06-rc1
- Incorporate SBAT data

* Wed Dec 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-26
- Updating release to be aligned with the unsigned bits.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Updating release to be aligned with the unsigned bits.

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> 2.02-24
- Original version for CBL-Mariner.
