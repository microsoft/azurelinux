# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# RHEL 8 compatibility
%{!?version_no_tilde: %define version_no_tilde %{shrink:%(echo '%{version}' | tr '~' '-')}}

Name:    libnvme
Summary: Linux-native nvme device management library
Version: 1.16.1
Release: 1%{?dist}
License: LGPL-2.1-or-later
URL:     https://github.com/linux-nvme/libnvme
Source0: %{url}/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz

BuildRequires: gcc gcc-c++
BuildRequires: swig
BuildRequires: python3-devel

BuildRequires: meson >= 0.62
BuildRequires: json-c-devel >= 0.13
BuildRequires: openssl-devel
BuildRequires: dbus-devel
BuildRequires: keyutils-libs-devel
%if 0%{?fedora} || 0%{?rhel} > 9
BuildRequires: kernel-headers >= 5.15
%endif

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
%package doc
Summary: Reference manual for libnvme
BuildArch: noarch
BuildRequires: perl-interpreter
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme

%description doc
This package contains the reference manual for %{name}.

%package -n python3-libnvme
Summary:  Python3 bindings for libnvme
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  python3-nvme = %{version}-%{release}
Obsoletes: python3-nvme < 1.0~rc7
%{?python_provide:%python_provide python3-libnvme}

%description -n python3-libnvme
This package contains Python bindings for libnvme.

%prep
%autosetup -p1 -n %{name}-%{version_no_tilde}

%build
%meson -Dpython=enabled -Dlibdbus=enabled -Ddocs=all -Ddocs-build=true -Dhtmldir=%{_pkgdocdir} -Dliburing=disabled
%meson_build

%install
%meson_install
%{__install} -pm 644 README.md %{buildroot}%{_pkgdocdir}
%{__install} -pm 644 doc/config-schema.json %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_pkgdocdir}/nvme/html %{buildroot}%{_pkgdocdir}/html
rm -rf %{buildroot}%{_pkgdocdir}/nvme
mv %{buildroot}/usr/*.rst %{buildroot}%{_pkgdocdir}/
rm -r %{buildroot}%{_pkgdocdir}/html/{.buildinfo,.doctrees/}

%ldconfig_scriptlets

%files
%license COPYING ccan/licenses/*
%{_libdir}/libnvme.so.1
%{_libdir}/libnvme.so.1.16.1
%{_libdir}/libnvme-mi.so.1
%{_libdir}/libnvme-mi.so.1.16.1

%files devel
%{_libdir}/libnvme.so
%{_libdir}/libnvme-mi.so
%{_includedir}/libnvme.h
%{_includedir}/libnvme-mi.h
%dir %{_includedir}/nvme
%{_includedir}/nvme/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_pkgdocdir}
%{_mandir}/man2/*.2*

%files -n python3-libnvme
%dir %{python3_sitearch}/libnvme
%{python3_sitearch}/libnvme/*

%changelog
* Thu Dec 04 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.16.1-1
- Upstream v1.16.1 release

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.15-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.15-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.15-2
- Fix loop transport address matching (#2385228)

* Fri Jul 25 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.15-1
- Upstream v1.15 release

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.14-1
- Upstream v1.14 release
- Disable io_uring support per upstream suggestion

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.13-2
- Rebuilt for Python 3.14

* Fri Apr 11 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.13-1
- Upstream v1.13 release

* Thu Apr 03 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.12-2
- Fix iouring admin commands status codes

* Mon Mar 17 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.12-1
- Upstream v1.12 release

* Mon Mar 03 2025 Tomas Bzatek <tbzatek@redhat.com> - 1.11.1-3
- Fix build with Python 3.14 (#2325194)

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 15 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.11.1-1
- Upstream v1.11.1 release

* Thu Oct 31 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.11-1
- Upstream v1.11 release

* Mon Aug 05 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.10-1
- Upstream v1.10 release

* Tue Jul 30 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.9-5
- Avoid using OpenSSL Engine API (#2300907)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9-2
- Rebuilt for Python 3.13

* Fri May 03 2024 Tomas Bzatek <tbzatek@redhat.com> - 1.9-1
- Upstream v1.9 release

* Wed Feb 28 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 1.8-2
- Do not package doctrees to make the package build reproducible

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
