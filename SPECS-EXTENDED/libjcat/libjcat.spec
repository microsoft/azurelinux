Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global glib2_version 2.45.8
%global json_glib_version 1.1.1

Summary:   Library for reading Jcat files
Name:      libjcat
Version:   0.2.2
Release:   2%{?dist}
License:   LGPL-2.1-or-later
URL:       https://github.com/hughsie/libjcat
Source0:   https://github.com/hughsie/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: %{_bindir}/xsltproc
BuildRequires: meson
BuildRequires: gobject-introspection-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: gnutls-devel
BuildRequires: gnutls-utils
BuildRequires: gpgme-devel
BuildRequires: vala
BuildRequires: help2man

Requires: glib2%{?_isa} >= %{glib2_version}

%description
This library allows reading and writing gzip-compressed JSON catalog files,
which can be used to store GPG, PKCS-7 and SHA-256 checksums for each file.

This provides equivalent functionality to the catalog files supported in
Microsoft Windows.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary: Files for installed tests

%description tests
Executable and data files for installed tests.

%prep
%autosetup -p0

%build

%meson \
    -Dgtkdoc=false \
    -Dtests=true

%meson_build

%install
%meson_install

%check
%meson_test

%files
%doc README.md
%license LICENSE
%{_bindir}/jcat-tool
%{_datadir}/man/man1/*.1*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib
%{_libdir}/libjcat.so.1*

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir
%{_includedir}/libjcat-1
%{_libdir}/libjcat.so
%{_libdir}/pkgconfig/jcat.pc
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/jcat.deps
%{_datadir}/vala/vapi/jcat.vapi

%files tests
%doc README.md
%{_libexecdir}/installed-tests/libjcat/*
%{_datadir}/installed-tests/libjcat/*
%dir %{_datadir}/installed-tests/libjcat

%changelog
## START: Generated by rpmautospec
*  Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.2.2-2
- Integrating the latest version of the library into Azure Linux
- Initial CBL-Mariner import from Fedora 42 (license: MIT).
- License verified.

* Mon Oct 14 2024 Richard Hughes <richard@hughsie.com> - 0.2.2-1
- New upstream release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Richard Hughes <richard@hughsie.com> - 0.2.1-1
- New upstream release

* Tue Jan 02 2024 Richard Hughes <richard@hughsie.com> - 0.2.0-1
- New upstream release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Richard Hughes <richard@hughsie.com> - 0.1.14-1
- New upstream release

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 0.1.13-1
- New upstream release

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 0.1.12-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Sep 11 2022 Richard Hughes <richard@hughsie.com> - 0.1.12-1
- New upstream release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.6-3
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Wed Feb 16 2022 Richard Hughes <richard@hughsie.com> - 0.1.10-1
- New upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 28 2021 Richard Hughes <richard@hughsie.com> - 0.1.9-1
- New upstream release

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.6-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Richard Hughes <richard@hughsie.com> - 0.1.8-1
- New upstream release

* Thu May 06 2021 Richard Hughes <richard@hughsie.com> - 0.1.7-1
- New upstream release

* Mon Feb 08 2021 Richard Hughes <richard@hughsie.com> - 0.1.6-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Richard Hughes <richard@hughsie.com> - 0.1.5-1
- New upstream release

* Fri Oct 23 2020 Richard Hughes <richard@hughsie.com> - 0.1.4-1
- New upstream release

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Richard Hughes <richard@hughsie.com> - 0.1.3-1
- New upstream release

* Fri Jun 05 2020 Richard Hughes <richard@hughsie.com> - 0.1.2-2
- Security fix for CVE-2020-10759

* Mon Apr 27 2020 Richard Hughes <richard@hughsie.com> - 0.1.2-1
- New upstream release

* Tue Apr 14 2020 Richard Hughes <richard@hughsie.com> - 0.1.1-1
- New upstream release

* Mon Mar 23 2020 Richard Hughes <richard@hughsie.com> - 0.1.0-1
- Initial release for Fedora package review
## END: Generated by rpmautospec
