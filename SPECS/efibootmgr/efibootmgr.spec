Summary:        Tools and libraries to manipulate EFI variables
Name:           efibootmgr
Version:        16
Release:        4%{?dist}
License:        GPLv2
URL:            https://github.com/rhboot/efibootmgr/
Group:          System Environment/System Utilities
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/rhboot/efibootmgr/releases/download/%{version}/%{name}-%{version}.tar.bz2
BuildRequires: efivar-devel
BuildRequires: pciutils
BuildRequires: zlib
%description
efibootmgr is a userspace application used to modify the Intel Extensible Firmware Interface (EFI) Boot Manager. This application can create and destroy boot entries, change the boot order, change the next running boot option, and more.
%prep
%setup -q
%build
make %{?_smp_mflags} PREFIX=%{_prefix} EFIDIR=BOOT EFI_LOADER=grubx64.efi \
    libdir=%{_libdir} \
    bindir=%{_bindir}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} EFIDIR=BOOT EFI_LOADER=grubx64.efi \
    install
gzip -9 %{buildroot}%{_mandir}/man8/%{name}.8
gzip -9 %{buildroot}%{_mandir}/man8/efibootdump.8

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 16-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 16-3
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 16-2
- Added %%license line automatically

*   Wed Mar 18 2020 Nicolas Ontiveros <niontive@microsoft.com> 16-1
-   Update to version 16. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 15-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 15-1
-   Version update.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-   GA - Bump release of all rpms
*   Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.12-1
-   Initial build. First version. Install steps from spec file in source.
