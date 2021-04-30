%global debug_package %{nil}
%global release_number 1
Summary:        First stage UEFI bootloader
Name:           shim
Version:        15.4
Release:        %{release_number}%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/shim
# This signed-shim tarball contains the shim binary signed with
# the Microsoft UEFI CA key
Source0:        signed-%{name}-%{version}-%{release_number}.tar.gz
# Currently, the tarball only contains a UEFI CA signed x86_64 shim binary.
# Upstream aarch64 shim 15.4 builds are in a bad state. They will break using
# binutils versions before 2.35, and even after that they may give
# unpredictable results. Due to this, aarch64 shims are not being accepted
# for shim signing at this time.
#
# Once upstream aarch64 shim builds stabilize and are being accepted for
# review/signing, we should update this spec to also include UEFI CA signed
# aarch64 shim binaries
ExclusiveArch:  x86_64

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments.

%prep
%autosetup

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
install -m644 shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi

%files
%defattr(-,root,root)
/boot/efi/EFI/BOOT/bootx64.efi

%changelog
* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
