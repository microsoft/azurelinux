Summary:        POSIX capability Library
Name:           libcap-ng
Version:        0.8.3
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://people.redhat.com/sgrubb/libcap-ng
Source0:        https://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  swig
Provides:       %{name}-utils = %{version}-%{release}

%description
The libcap-ng library is intended to make programming with posix capabilities much easier than the traditional libcap library. It includes utilities that can analyse all currently running applications and print out any capabilities and whether or not it has an open ended bounding set. An open bounding set without the securebits "NOROOT" flag will allow full capabilities escalation for apps retaining uid 0 simply by calling execve.

%package -n     python3-libcap-ng
Summary:        Python3 bindings for libaudit
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-libcap-ng
The python3-libcap-ng package contains the python3 bindings for libcap-ng.

%package        devel
Summary:        The libraries and header files needed for libcap-ng development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for libcap_ng development.

%prep
%autosetup

%build
%configure --with-python=no --with-python3
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%license COPYING
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man8/*
%{_mandir}/man7/*

%files -n python3-libcap-ng
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_datadir}/aclocal/*.m4
%{_libdir}/*.a

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.3-1
- Auto-upgrade to 0.8.3 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Rachel Menge <rachelmenge@microsoft.com> - 0.8.2-2
- Add libcap-ng to toolchain for util-linux

* Mon Mar 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.8.2-1
- Upgrade to 0.8.2
- License verified

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.7.9-4
- Add compatibility provides for utils subpackage
- Remove python2 subpackage
- Lint spec, modernize with macros

* Mon Oct 19 2020 Andrew Phelps <anphel@microsoft.com> - 0.7.9-3
- Fix check test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.9-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Added %%license line automatically

* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> - 0.7.9-1
- Updated to latest version

* Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.8-2
- Added python3 subpackage.

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> - 0.7.8-1
- Upgrade version to 0.7.8

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 0.7.7-3
- Moved man3 to devel subpackage.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.7.7-2
- GA - Bump release of all rpms

* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> - 0.7.7-1
- Initial version
