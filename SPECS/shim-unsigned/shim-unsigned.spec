%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim-unsigned
Version:        15
Release:        3%{?dist}
URL:            https://github.com/rhboot/shim
License:        BSD
Vendor:         Microsoft
Distribution:   Mariner

%ifarch x86_64
BuildRequires:  shim-unsigned-x64
%endif

%ifarch aarch64
BuildRequires:  shim-unsigned-aarch64
%endif

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments.

%prep

%install
%ifarch x86_64
install -D -m 0744 /usr/share/shim-unsigned-x64/shimx64.efi %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi
%endif

%ifarch aarch64
install -D -m 0744 /usr/share/shim-unsigned-aarch64/shimaa64.efi %{buildroot}/boot/efi/EFI/BOOT/bootaa64.efi
%endif

%files
%defattr(-,root,root)
%ifarch x86_64
/boot/efi/EFI/BOOT/bootx64.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/bootaa64.efi
%endif

%changelog
* Tue Aug 25 2020 Chris Co <chrco@microsoft.com> 15-3
- Bump release to get patched shims
* Thu Jul 30 2020 Chris Co <chrco@microsoft.com> 15-2
- Update aarch64 source binary path
* Wed Jul 29 2020 Chris Co <chrco@microsoft.com> 15-1
- Original version for CBL-Mariner.