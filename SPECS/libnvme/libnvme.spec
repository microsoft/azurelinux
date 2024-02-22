Summary: Linux-native nvme device management library
Name:    libnvme
Version: 1.8
Release: 1%{?dist}
License: LGPL-2.1-or-later
URL:     https://github.com/linux-nvme/libnvme
Source0: https://github.com/linux-nvme/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: dbus-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: json-c-devel >= 0.13
BuildRequires: keyutils-libs-devel
BuildRequires: meson >= 0.50
BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: swig

%description
Provides type definitions for NVMe specification structures,
enumerations, and bit fields, helper functions to construct,
dispatch, and decode commands and payloads, and utilities to connect,
scan, and manage nvme devices on a Linux system.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides header files to include and libraries to link with
for Linux-native nvme device management.

%package -n python3-libnvme
Summary:  Python3 bindings for libnvme
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  python3-nvme = %{version}-%{release}
Obsoletes: python3-nvme < 1.0~rc7
%{?python_provide:%python_provide python3-libnvme}

%description -n python3-libnvme
This package contains Python bindings for libnvme.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson -Dpython=enabled -Dlibdbus=enabled
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%license COPYING ccan/licenses/*
%{_libdir}/libnvme.so.1
%{_libdir}/libnvme.so.1.8.0
%{_libdir}/libnvme-mi.so.1
%{_libdir}/libnvme-mi.so.1.8.0

%files devel
%{_libdir}/libnvme.so
%{_libdir}/libnvme-mi.so
%{_includedir}/libnvme.h
%{_includedir}/libnvme-mi.h
%dir %{_includedir}/nvme
%{_includedir}/nvme/*.h
%{_libdir}/pkgconfig/*.pc


%files -n python3-libnvme
%dir %{python3_sitearch}/libnvme
%{python3_sitearch}/libnvme/*

%changelog
* Wed Feb 21 2024 Adit Jha <aditjha@microsoft.com> - 1.8-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).  License verified.

* Wed Feb 14 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.8-1
- Upstream v1.8 release

* Fri Feb 09 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.7.1-4
- nbft: Fix SSNS HFI indexes parsing
- cleanup: Explicitly initialize auto-cleanup variables

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 28 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.7.1-1
- Upstream v1.7.1 release

* Tue Oct 24 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.6-2
- Backport stack smashing fixes (#2245707)

* Fri Sep 29 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.6-1
- Upstream v1.6 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 1.5-2
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.5-1
- Upstream v1.5 release

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.4-3
- Rebuilt for Python 3.12

* Thu Apr 20 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.4-2
- Backport the NBFT parser from git master

* Mon Apr 03 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.4-1
- Upstream v1.4 release

* Tue Jan 31 2023 Tomas Bzatek <tbzatek@redhat.com> - 1.3-1
- Upstream v1.3 release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.2-1
- Upstream v1.2 release

* Fri Aug 05 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.1-1
- Upstream v1.1 release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1~rc0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.1~rc0-1
- Upstream v1.1 Release Candidate 0

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0-2
- Rebuilt for Python 3.11

* Mon Apr 11 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0-1
- Upstream v1.0 release

* Fri Apr 01 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc8-1
- Upstream v1.0 Release Candidate 8

* Wed Mar 23 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc7-1
- Upstream v1.0 Release Candidate 7
- Renamed python3-nvme subpackage to python3-libnvme

* Mon Mar 14 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc6-1
- Upstream v1.0 Release Candidate 6

* Fri Mar 04 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc5-1
- Upstream v1.0 Release Candidate 5

* Mon Feb 28 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc4-1
- Upstream v1.0 Release Candidate 4

* Fri Feb 11 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc3-1
- Upstream v1.0 Release Candidate 3

* Tue Feb 01 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc2-1
- Upstream v1.0 Release Candidate 2

* Thu Jan 27 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc1-1
- Upstream v1.0 Release Candidate 1

* Mon Jan 17 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc0-1
- Upstream v1.0 Release Candidate 0

* Wed Oct 20 2021 Tomas Bzatek <tbzatek@redhat.com> - 0.0.1-1.git1fe38d6
- Initial packaging