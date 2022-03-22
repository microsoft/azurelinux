Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib2_version 2.45.8

Summary:   Library for querying compressed XML metadata
Name:      libxmlb
Version:   0.1.14
Release:   4%{?dist}
License:   LGPLv2+
URL:       https://github.com/hughsie/libxmlb
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz

BuildRequires: %{_bindir}/xsltproc
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libstemmer-devel
BuildRequires: meson
BuildRequires: gobject-introspection-devel
BuildRequires: python-setuptools

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

%prep
%setup -q

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
%{_libexecdir}/xb-tool
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib
%{_libdir}/libxmlb.so.1*

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir
%{_includedir}/libxmlb-1
%{_libdir}/libxmlb.so
%{_libdir}/pkgconfig/xmlb.pc

%files tests
%{_libexecdir}/installed-tests/libxmlb/xb-self-test
%{_datadir}/installed-tests/libxmlb/libxmlb.test
%{_datadir}/installed-tests/libxmlb/test.xml.gz.gz.gz
%dir %{_datadir}/installed-tests/libxmlb

%changelog
* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.14-4
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.14-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Richard Hughes <richard@hughsie.com> 0.1.14-1
- New upstream release
- Do not use libuuid
- Ignore adaptors added with xb_builder_source_add_converter()

* Thu Oct 17 2019 Richard Hughes <richard@hughsie.com> 0.1.13-1
- New upstream release
- Export xb_silo_query_full()
- Show the XPath that was used in the query in the error message

* Fri Sep 27 2019 Richard Hughes <richard@hughsie.com> 0.1.12-1
- New upstream release
- Add xb_node_transmogrify to allow changing XML format
- Do not escape a single quote with &apos;
- Don't invalidate the silo for a GIO temp file
- Fix up two memory leaks if using libxmlb from an introspected binding

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Richard Hughes <richard@hughsie.com> 0.1.11-1
- New upstream release
- Add xb_node_query_first_full() API
- Rebuild the XbMachine parser to support 'and' and 'or' predicates

* Thu May 16 2019 Richard Hughes <richard@hughsie.com> 0.1.10-1
- New upstream release
- Do not mistake gzipped files as being application/x-zerosize content type
- Fix running the installed tests with no checkout directory

* Tue May 07 2019 Richard Hughes <richard@hughsie.com> 0.1.9-1
- New upstream release
- Correctly implement building a silo with _SINGLE_LANG set

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.1.8-2
- Rebuild with Meson fix for #1699099

* Tue Mar 26 2019 Richard Hughes <richard@hughsie.com> 0.1.8-1
- New upstream release
- Add some installed tests
- Always add all children when importing parent-less XML data

* Fri Mar 08 2019 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream release
- Add XB_BUILDER_COMPILE_FLAG_IGNORE_GUID
- Allow nesting XbBuilderSource content type handlers

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 30 2018 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream release
- Allow controlling how the XbQuery is parsed

* Wed Nov 21 2018 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release
- Add xb_builder_node_export() for gnome-software
- Ignore calls to xb_silo_query_build_index() with no results
- Lazy load the stemmer when required

* Fri Nov 09 2018 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream release
- Add support for bound variables and indexed strings
- Optionally optimize predicates
- Use INTE:INTE for comparison where available

* Mon Oct 22 2018 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream release
- Add more API for fwupd and gnome-software
- Switch from GPtrArray to XbStack for performance reasons

* Tue Oct 16 2018 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream release
- Add more API for fwupd and gnome-software
- Fix a crash when using xb_builder_node_set_text() in a fixup
- Only run the XbBuilderSourceConverterFunc if the silo needs rebuilding
- Return an error when the XPath predicate has invalid syntax

* Thu Oct 11 2018 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream release
- Add support for more XPath funtions
- Add new API required for gnome-software and fwupd

* Thu Oct 04 2018 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial release for Fedora package review
