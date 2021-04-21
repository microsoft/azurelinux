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
