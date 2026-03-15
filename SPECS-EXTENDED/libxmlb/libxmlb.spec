%bcond mingw %{defined fedora}
%bcond stemmer %{defined fedora}

%global glib2_version 2.45.8

Summary:   Library for querying compressed XML metadata
Name:      libxmlb
Version:   0.3.22
Release:   2%{?dist}
License:   LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:       https://github.com/hughsie/%{name}
Source0:   https://github.com/hughsie/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk-doc
%if %{with stemmer}
BuildRequires: libstemmer-devel
%endif
BuildRequires: meson
BuildRequires: gobject-introspection-devel
BuildRequires: xz-devel
BuildRequires: libzstd-devel
BuildRequires: python3-setuptools

%if %{with mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-glib2
BuildRequires: mingw32-xz
BuildRequires: mingw32-zstd

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-glib2
BuildRequires: mingw64-xz
BuildRequires: mingw64-zstd
%endif

# needed for the self tests
BuildRequires: shared-mime-info

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: shared-mime-info

%description
XML is slow to parse and strings inside the document cannot be memory mapped as
they do not have a trailing NUL char. The libxmlb library takes XML source, and
converts it to a structured binary representation with a deduplicated string
table -- where the strings have the NULs included.

This allows an application to mmap the binary XML file, do an XPath query and
return some strings without actually parsing the entire document. This is all
done using (almost) zero allocations and no actual copying of the binary data.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary: Files for installed tests

%description tests
Executable and data files for installed tests.

%if %{with mingw}
%package -n mingw32-libxmlb
Summary: MinGW library for querying compressed XML metadata
BuildArch: noarch

%description -n mingw32-libxmlb
MinGW32 libxmlb library.

%package -n mingw64-libxmlb
Summary: MinGW library for querying compressed XML metadata
BuildArch: noarch

%description -n mingw64-libxmlb
MinGW64 libxmlb library.

%{?mingw_debug_package}
%endif

%prep
%autosetup -p1

%build

%meson \
    -Dgtkdoc=true \
    -Dtests=true

%meson_build

%if %{with mingw}
%mingw_meson -Dintrospection=false -Dtests=false -Dgtkdoc=false
%mingw_ninja
%endif

%check
%meson_test

%install
%meson_install

%if %{with mingw}
%mingw_ninja_install
%mingw_debug_install_post
rm -f $RPM_BUILD_ROOT/%{mingw32_mandir}/man1/xb-tool.1*
rm -f $RPM_BUILD_ROOT/%{mingw64_mandir}/man1/xb-tool.1*
%endif

%files
%doc README.md
%license LICENSE
%{_bindir}/xb-tool
%{_mandir}/man1/xb-tool.1*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Xmlb-2.0.typelib
%{_libdir}/libxmlb.so.2*

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Xmlb-2.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libxmlb
%{_includedir}/libxmlb-2
%{_libdir}/libxmlb.so
%{_libdir}/pkgconfig/xmlb.pc

%files tests
%dir %{_libexecdir}/installed-tests/libxmlb
%{_libexecdir}/installed-tests/libxmlb/xb-self-test
%{_libexecdir}/installed-tests/libxmlb/test.*
%dir %{_datadir}/installed-tests/libxmlb
%{_datadir}/installed-tests/libxmlb/libxmlb.test

%if %{with mingw}
%files -n mingw32-libxmlb
%license LICENSE
%{mingw32_bindir}/xb-tool.exe
%{mingw32_bindir}/libxmlb-2.dll
%{mingw32_libdir}/libxmlb.dll.a
%{mingw32_includedir}/libxmlb-2
%{mingw32_libdir}/pkgconfig/xmlb.pc

%files -n mingw64-libxmlb
%license LICENSE
%{mingw64_bindir}/xb-tool.exe
%{mingw64_bindir}/libxmlb-2.dll
%{mingw64_libdir}/libxmlb.dll.a
%{mingw64_includedir}/libxmlb-2
%{mingw64_libdir}/pkgconfig/xmlb.pc
%endif

%changelog
* Wed Apr 4 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.3.22-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Wed Mar 12 2025 Richard Hughes <richard@hughsie.com> - 0.3.22-1
- New upstream release

* Tue Oct 15 2024 Richard Hughes <richard@hughsie.com> - 0.3.21-1
- New upstream release

* Mon Oct 14 2024 Richard Hughes <richard@hughsie.com> - 0.3.20-1
- New upstream release

* Fri Jul 19 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.19-5
- Disable libstemmer on RHEL

* Fri Jul 19 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.19-4
- Use bcond for mingw

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 25 2024 Richard Hughes <richard@hughsie.com> - 0.3.19-2
- Backport a mingw patch from upstream

* Mon Apr 22 2024 Richard Hughes <richard@hughsie.com> - 0.3.19-1
- New upstream release

* Tue Apr 09 2024 Richard Hughes <richard@hughsie.com> - 0.3.18-1
- New upstream release

* Fri Apr 05 2024 Richard Hughes <richard@hughsie.com> - 0.3.17-1
- New upstream release

* Wed Apr 03 2024 Richard Hughes <richard@hughsie.com> - 0.3.16-1
- New upstream release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Richard Hughes <richard@hughsie.com> - 0.3.15-1
- New upstream release

* Thu Aug 24 2023 Richard Hughes <richard@hughsie.com> - 0.3.14-1
- New upstream release

* Thu Aug 17 2023 Richard Hughes <richard@hughsie.com> - 0.3.13-1
- New upstream release

* Thu Aug 10 2023 Richard Hughes <richard@hughsie.com> - 0.3.12-1
- New upstream release

* Wed Jul 26 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3.11-4
- Add MinGW packages

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 0.3.11-2
- migrated to SPDX license

* Mon Feb 20 2023 Richard Hughes <richard@hughsie.com> - 0.3.11-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Sep 11 2022 Richard Hughes <richard@hughsie.com> - 0.3.10-1
- New upstream release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 24 2022 Richard Hughes <richard@hughsie.com> - 0.3.9-1
- New upstream release

* Wed Feb 16 2022 Richard Hughes <richard@hughsie.com> - 0.3.7-1
- New upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Richard Hughes <richard@hughsie.com> - 0.3.6-1
- New upstream release

* Wed Dec 01 2021 Richard Hughes <richard@hughsie.com> - 0.3.5-1
- New upstream release

* Mon Nov 29 2021 Richard Hughes <richard@hughsie.com> - 0.3.4-1
- New upstream release

* Wed Oct 06 2021 Richard Hughes <richard@hughsie.com> - 0.3.3-2
- trivial: Add missing BRs

* Wed Oct 06 2021 Richard Hughes <richard@hughsie.com> - 0.3.3-1
- New upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Richard Hughes <richard@hughsie.com> - 0.3.2-1
- New upstream release

* Thu May 06 2021 Richard Hughes <richard@hughsie.com> - 0.3.1-1
- New upstream release

* Fri Mar 12 2021 Richard Hughes <richard@hughsie.com> - 0.3.0-2
- Fix date in changelog

* Fri Mar 12 2021 Richard Hughes <richard@hughsie.com> - 0.3.0-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 07 2020 Richard Hughes <richard@hughsie.com> - 0.2.1-1
- New upstream release

* Tue Aug 18 2020 Richard Hughes <richard@hughsie.com> - 0.2.0-1
- New upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 04 2020 Richard Hughes <richard@hughsie.com> - 0.1.15-1
- New upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Richard Hughes <richard@hughsie.com> - 0.1.14-1
- New upstream release

* Thu Oct 17 2019 Richard Hughes <richard@hughsie.com> - 0.1.13-1
- New upstream release

* Fri Sep 27 2019 Richard Hughes <richard@hughsie.com> - 0.1.12-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Richard Hughes <richard@hughsie.com> - 0.1.11-1
- New upstream release

* Thu May 16 2019 Richard Hughes <richard@hughsie.com> - 0.1.10-1
- New upstream release

* Tue May 07 2019 Richard Hughes <richard@hughsie.com> - 0.1.9-1
- New upstream release

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.1.8-2
- Rebuild with Meson fix for #1699099

* Tue Mar 26 2019 Richard Hughes <richard@hughsie.com> - 0.1.8-1
- New upstream release

* Fri Mar 08 2019 Richard Hughes <richard@hughsie.com> - 0.1.7-1
- New upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 30 2018 Richard Hughes <richard@hughsie.com> - 0.1.6-1
- New upstream release

* Wed Nov 21 2018 Richard Hughes <richard@hughsie.com> - 0.1.5-1
- New upstream release

* Fri Nov 09 2018 Richard Hughes <richard@hughsie.com> - 0.1.4-1
- New upstream release

* Mon Oct 22 2018 Richard Hughes <richard@hughsie.com> - 0.1.3-1
- New upstream release

* Tue Oct 16 2018 Richard Hughes <richard@hughsie.com> - 0.1.2-1
- New upstream release

* Thu Oct 11 2018 Richard Hughes <richard@hughsie.com> - 0.1.1-1
- New upstream release

* Thu Oct 04 2018 Richard Hughes <richard@hughsie.com> - 0.1.0-1
- Initial import (1636169)

