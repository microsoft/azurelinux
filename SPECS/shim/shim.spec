%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim
Version:        15.4
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/shim
# This shim binary is signed with the Microsoft UEFI CA key
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments.

%prep
%autosetup

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
cp shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi

%files
%defattr(-,root,root)
/boot/efi/EFI/BOOT/bootx64.efi

%changelog
* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
