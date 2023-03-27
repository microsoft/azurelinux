%global glib2_version 2.45.8
%global gtk_doc 0
Summary:        Library for querying compressed XML metadata
Name:           libxmlb
Version:        0.3.11
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/hughsie/%{name}
Source0:        https://github.com/hughsie/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  glib2-devel >= %{glib2_version}
%if %{with gtk_doc}
BuildRequires:  gtk-doc
%endif
BuildRequires:  libstemmer-devel
BuildRequires:  meson
BuildRequires:  gobject-introspection-devel
BuildRequires:  xz-devel
BuildRequires:  libzstd-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  shared-mime-info
%endif
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       shared-mime-info

%description
XML is slow to parse and strings inside the document cannot be memory mapped as
they do not have a trailing NUL char. The libxmlb library takes XML source, and
converts it to a structured binary representation with a deduplicated string
table -- where the strings have the NULs included.

This allows an application to mmap the binary XML file, do an XPath query and
return some strings without actually parsing the entire document. This is all
done using (almost) zero allocations and no actual copying of the binary data.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary:        Files for installed tests

%description tests
Executable and data files for installed tests.

%prep
%autosetup -p1

%build

%meson \
    -Dgtkdoc=false \
    -Dtests=true

%meson_build

%check
%meson_test

%install
%meson_install

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
%if %{with gtk_doc}
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libxmlb
%endif
%{_includedir}/libxmlb-2
%{_libdir}/libxmlb.so
%{_libdir}/pkgconfig/xmlb.pc

%files tests
%dir %{_libexecdir}/installed-tests/libxmlb
%{_libexecdir}/installed-tests/libxmlb/xb-self-test
%{_libexecdir}/installed-tests/libxmlb/test.xml.gz.gz.gz
%dir %{_datadir}/installed-tests/libxmlb
%{_datadir}/installed-tests/libxmlb/libxmlb.test

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 0.3.11-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Disable gtk-doc
- license verified

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 0.3.11-1
- New upstream release

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
