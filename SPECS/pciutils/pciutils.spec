Summary:        System utilities to list pci devices
Name:           pciutils
Version:        3.7.0
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/System Utilities
URL:            https://www.kernel.org/pub/software/utils/pciutils/
Source0:        https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.gz

%description
The pciutils package contains a set of programs for listing PCI devices, inspecting their status and setting their configuration registers.

%package devel
Summary:        Linux PCI development library
Group:          Development/Libraries
Requires:       pciutils = %{version}-%{release}

%description devel
Library files for doing development with pciutils.

%package libs
Summary:        Linux PCI library

%description libs
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%prep
%setup -q

%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes \
    install install-lib
chmod -v 766 %{buildroot}%{_libdir}/libpci.so

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so.*
%{_datadir}/misc/*
%{_mandir}/*

%files libs
%license COPYING
%{_libdir}/libpci.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Wed Dec 29 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 3.7.0-1
- Upgrading to 3.7.0
- Adding libs subpackage.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.2-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.6.2-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.6.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.6.2-1
-   Upgraded to 3.6.2 version

*   Wed Mar 29 2017 Robert Qi <qij@vmware.com> 3.5.4-1
-   Upgraded to 3.5.4 version.

*   Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.1-3
-   Added devel package and removed packaging of debug files

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.1-2
-   GA - Bump release of all rpms

*   Thu Jul 2 2015 Sharath George <sharathg@vmware.com> 3.3.1-1
-   Initial build.	First version
