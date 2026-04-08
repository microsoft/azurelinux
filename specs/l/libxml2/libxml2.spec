# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libxml2
Version:        2.12.10
Release:        5%{?dist}
Summary:        Library providing XML and HTML support

# list.c, dict.c and few others use ISC-Veillard
# the conformance and test suite data in
# Source1, Source2 and Source3 is covered by W3C
License:        MIT AND ISC-Veillard AND W3C
URL:            https://gitlab.gnome.org/GNOME/libxml2/-/wikis/home
Source0:        https://download.gnome.org/sources/%{name}/2.12/%{name}-%{version}.tar.xz
# https://www.w3.org/XML/Test/xmlconf-20080827.html
Source1:        https://www.w3.org/XML/Test/xmlts20080827.tar.gz
# https://www.w3.org/XML/2004/xml-schema-test-suite/index.html
Source2:        https://www.w3.org/XML/2004/xml-schema-test-suite/xmlschema2002-01-16/xsts-2002-01-16.tar.gz
Source3:        https://www.w3.org/XML/2004/xml-schema-test-suite/xmlschema2004-01-14/xsts-2004-01-14.tar.gz
Patch0:         libxml2-multilib.patch
# Patch from openSUSE.
# See:  https://bugzilla.gnome.org/show_bug.cgi?id=789714
Patch1:         libxml2-2.12.0-python3-unicode-errors.patch

BuildRequires:  cmake-rpm-macros
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary:        Libraries, includes, etc. to develop XML and HTML applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel%{?_isa}
Requires:       xz-devel%{?_isa}

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary:        Static library for libxml2

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%package -n python3-%{name}
Summary:        Python 3 bindings for the libxml2 library
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python3 < %{version}-%{release}
Provides:       %{name}-python3 = %{version}-%{release}

%description -n python3-%{name}
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to use the
interface supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%prep
%autosetup -p1
find doc -type f -executable -print -exec chmod 0644 {} ';'

%build
# see https://bugzilla.redhat.com/show_bug.cgi?id=2139546 , several
# of these options are needed to (mostly) retain ABI compatibility
# with earlier versions
%configure \
    --enable-static \
    --with-legacy \
    --with-ftp \
    --with-python=%{__python3}
%make_build

%install
%make_install

# multiarch crazyness on timestamp differences or Makefile/binaries for examples
touch -m --reference=%{buildroot}%{_includedir}/libxml2/libxml/parser.h %{buildroot}%{_bindir}/xml2-config

find %{buildroot} -type f -name '*.la' -print -delete
rm -vf %{buildroot}{%{python2_sitearch},%{python3_sitearch}}/*.a
rm -vrf %{buildroot}%{_datadir}/doc/
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz

%check
# Tests require the XML conformance suite.
tar -xzvf %{SOURCE1}
%make_build check
rm -rf xmlconf
# Schema tests use the schema test suite.
cp %{SOURCE2} %{SOURCE3} xstc/
pushd xstc
mkdir Tests
%make_build tests
popd
# As the directory is copied to the devel subpackage, remove any build
# artifacts.
(cd doc/examples ; make clean ; rm -rf .deps Makefile)

%ldconfig_scriptlets

%files
%license Copyright
%doc NEWS README.md
%{_libdir}/libxml2.so.2*
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog.1*
%{_mandir}/man1/xmllint.1*

%files devel
%doc doc/*.html
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/aclocal/libxml.m4
%{_datadir}/gtk-doc/html/libxml2/
%{_includedir}/libxml2/
%{_libdir}/libxml2.so
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/
%{_bindir}/xml2-config
%{_mandir}/man1/xml2-config.1*

%files static
%license Copyright
%{_libdir}/libxml2.a

%files -n python3-%{name}
%doc doc/*.py
%{python3_sitearch}/libxml2mod.so
%{python3_sitelib}/libxml2.py
%{python3_sitelib}/__pycache__/libxml2.*
%{python3_sitelib}/drv_libxml2.py
%{python3_sitelib}/__pycache__/drv_libxml2.*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.12.10-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.12.10-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.12.10-2
- Rebuilt for Python 3.14

* Thu Mar 13 2025 David King <amigadave@amigadave.com> - 2.12.10-1
- Update to 2.12.10

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 24 2024 David King <amigadave@amigadave.com> - 2.12.9-1
- Update to 2.12.9 (#2333939)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 David King <amigadave@amigadave.com> - 2.12.8-1
- Update to 2.12.8 (#2292029)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.12.7-2
- Rebuilt for Python 3.13

* Thu May 16 2024 David King <amigadave@amigadave.com> - 2.12.7-1
- Update to 2.12.7 (#2280532)

* Fri Mar 15 2024 David King <amigadave@amigadave.com> - 2.12.6-1
- Update to 2.12.6 (#2269695)

* Mon Feb 05 2024 David King <amigadave@amigadave.com> - 2.12.5-1
- Update to 2.12.5 (#2262648)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 David King <amigadave@amigadave.com> - 2.12.4-1
- Update to 2.12.4 (#2258493)

* Tue Dec 12 2023 David King <amigadave@amigadave.com> - 2.12.3-1
- Update to 2.12.3 (#2254194)

* Sat Dec 09 2023 David King <amigadave@amigadave.com> - 2.12.2-2
- Upstream patch to add extra includes

* Wed Dec 06 2023 David King <amigadave@amigadave.com> - 2.12.2-1
- Update to 2.12.2 (#2137281)
- Enable W3C XML Conformance and Schema test suites

* Fri Nov 24 2023 David King <amigadave@amigadave.com> - 2.12.1-1
- Update to 2.12.1 (#2250062)

* Thu Nov 16 2023 David King <amigadave@amigadave.com> - 2.12.0-1
- Update to 2.12.0 (#2250062)

* Thu Nov 16 2023 David King <amigadave@amigadave.com> - 2.11.6-1
- Update to 2.11.6

* Wed Aug 16 2023 David King <amigadave@amigadave.com> - 2.11.5-1
- Update to 2.11.5 (#2190441)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.10.4-2
- Rebuilt for Python 3.12

* Wed Apr 12 2023 David King <amigadave@amigadave.com> - 2.10.4-1
- Update to 2.10.4 (#2185870)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 03 2022 Adam Williamson <awilliam@redhat.com> - 2.10.3-2
- Set build options to maintain (most) symbols from 2.9.14 (#2139546)

* Thu Oct 20 2022 David King <amigadave@amigadave.com> - 2.10.3-1
- Update to 2.10.3 (#2119077)

* Tue Aug 30 2022 David King <amigadave@amigadave.com> - 2.10.2-1
- Update to 2.10.2 (#2119077)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.9.14-2
- Rebuilt for Python 3.11

* Mon May 02 2022 David King <amigadave@amigadave.com> - 2.9.14-1
- Update to 2.9.14 (#2080961)

* Mon Feb 21 2022 David King <amigadave@amigadave.com> - 2.9.13-1
- Update to 2.9.13

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.9.12-5
- Rebuilt for Python 3.10

* Sat May 29 2021 David King <amigadave@amigadave.com> - 2.9.12-4
- Fix xmlNodeDumpOutputInternal regression (#1965662)

* Tue May 25 2021 David King <amigadave@amigadave.com> - 2.9.12-3
- Fix multiarch conflict in devel subpackage

* Wed May 19 2021 David King <amigadave@amigadave.com> - 2.9.12-2
- Fix python-lxml regression with 2.9.12

* Thu May 13 2021 David King <amigadave@amigadave.com> - 2.9.12-1
- Update to 2.9.12 (#1960153)

* Thu May 06 2021 David King <amigadave@amigadave.com> - 2.9.10-12
- Fix CVE-2021-3537 (#1956524)

* Wed May 05 2021 David King <amigadave@amigadave.com> - 2.9.10-11
- Fix CVE-2021-3516 (#1954227)
- Fix CVE-2021-3517 (#1954234)
- Fix CVE-2021-3518 (#1954243)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 11:57:41 CET 2020 Victor Stinner <vstinner@python.org> - 2.9.10-9
- Build the Python extension with the PY_SSIZE_T_CLEAN macro to make it
  compatible with Python 3.10.
- Fixes: rhbz#1890878.

* Wed Nov 11 2020 Richard W.M. Jones <rjones@redhat.com> - 2.9.10-8
- Add correct fix for CVE-2020-24977 (RHBZ#1877788), thanks: Jan de Groot.

* Fri Sep 11 2020 Richard W.M. Jones <rjones@redhat.com> - 2.9.10-7
- Add fix for CVE-2020-24977 (RHBZ#1877788).

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9.10-5
- Rebuilt for Python 3.9

* Mon Feb 10 2020 David King <amigadave@amigadave.com> - 2.9.10-4
- Fix CVE-2019-20388 (#1799736)
- Fix CVE-2020-7595 (#1799786)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 03 2020 Jan Pokorny <jpokorny@fedoraproject.org> - 2.9.10-2
- Fix relaxed approach to nested documents on object disposal (#1780573)

* Fri Nov 01 2019 David King <amigadave@amigadave.com> - 2.9.10-1
- Update to 2.9.10 (#1767151)

* Thu Oct 31 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9.9-7
- Subpackage python2-libxml2 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9.9-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 23 2019 Florian Weimer <fweimer@redhat.com> - 2.9.9-5
- Rebuild to fix corrupted libxml2-static package on aarch64 (#1745020)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9.9-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 David King <amigadave@amigadave.com> - 2.9.9-1
- Update to 2.9.9

* Sun Jan 06 2019 Björn Esser <besser82@fedoraproject.org> - 2.9.8-5
- Add patch to fix crash: xmlParserPrintFileContextInternal mangles utf8

* Thu Aug 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.8-4
- Backport patches from upstream

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.8-2
- Rebuilt for Python 3.7

* Tue Apr 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.8-1
- Update to 2.9.8

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 2.9.7-4
- Rebuild with new LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.7-2
- Switch to %%ldconfig_scriptlets

* Wed Jan 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.7-1
- Update to 2.9.7
- Cleanups in packaging

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.9.5-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Sep 22 2017 Petr Pisar <ppisar@redhat.com> - 2.9.5-2
- Fix reporting error about undefined XPath variables (bug #1493613)

* Mon Sep  4 2017 Daniel Veillard <veillard@redhat.com> - 2.9.5-1
- update to 2.9.5

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.9.4-5
- Python 2 binary package renamed to python2-libxml2
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 2.9.4-1
- Update to 2.9.4.
- Apply very hacky patch that removes the no longer in python-3.6 PyVerify_fd symbol.

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.9.3-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Kalev Lember <klember@redhat.com> - 2.9.3-2
- Fix obsoletes versions now that F22 has libxml2 2.9.3 (#1287262)

* Fri Nov 20 2015 Daniel Veillard <veillard@redhat.com> - 2.9.2-1
- upstream release of 2.9.3
- Fixes for CVE-2015-8035, CVE-2015-7942, CVE-2015-7941, CVE-2015-1819
  CVE-2015-7497, CVE-2015-7498, CVE-2015-5312, CVE-2015-7499, CVE-2015-7500
  and CVE-2015-8242
- many other bug fixes

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 2.9.2-9
- Rebuilt for Python3.5 rebuild
- Python3.5 has new naming convention for byte compiled files

* Tue Nov  3 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 2.9.2-8
- Remove executable permissions from documentation.  Complies with packaging
  guidelines and solves issue of libxml2-python3 package depending on python2

* Thu Aug 27 2015 Miro Hrončok <mhroncok@redhat.com> - 2.9.2-7
- Remove dependency on python2 from python3 subpackage, rhbz#1250940

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 2.9.2-6
- Rename the Python 3 subpackage to python3-libxml2 as per guidelines

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.9.2-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 21 2015 Tomas Radej <tradej@redhat.com> - 2.9.2-3
- Added Python 3 subpackage

* Thu Oct 16 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.9.2-2
- Avoid corrupting the xml catalogs

* Thu Oct 16 2014 Daniel Veillard <veillard@redhat.com> - 2.9.2-1
- upstream release of 2.9.2
- Fix for CVE-214-3660 billion laugh DOS
- many other bug fixes

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.9.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Daniel Veillard <veillard@redhat.com> - 2.9.1-1
- upstream release of 2.9.1
- a couple more API entry point
- compatibility with python3
- a lot of bug fixes

* Mon Feb 11 2013 Daniel Veillard <veillard@redhat.com> - 2.9.0-4
- fix --nocheck build which I broke in october rhbz#909767

* Mon Nov 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.9.0-3
- workaround for crc/len check failure, rhbz#877567

* Thu Oct 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-2
- remaining cleanups from merge bug rhbz#226079
- do not put the docs in the main package, only in -devel rhbz#864731

* Tue Sep 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-1
- upstream release of 2.9.0
- A few new API entry points
- More resilient push parser mode
- A lot of portability improvement
- Faster XPath evaluation
- a lot of bug fixes and smaller improvement

* Fri Aug 10 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-0rc1
- upstream release candidate 1 of 2.9.0
- introduce a small API change, but ABI compatible, see
  https://mail.gnome.org/archives/xml/2012-August/msg00005.html
  patches for php, gcc/libjava and evolution-data-connector are upstream
  Grab me in cases of problems veillard@redhat.com
- many bug fixes including security aspects and small improvements

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Daniel Veillard <veillard@redhat.com> - 2.8.0-1
- upstream release of 2.8.0
- add lzma compression support
- many bug fixes and small improvements

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar  4 2011 Daniel Veillard <veillard@redhat.com> - 2.7.8-6
- fix a double free in XPath CVE-2010-4494 bug 665965

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-4
- reactivate shared libs versionning script

* Thu Nov  4 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-1
- Upstream release of 2.7.8
- various bug fixes, including potential crashes
- new non-destructive formatting option
- date parsing updated to RFC 5646

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 15 2010 Daniel Veillard <veillard@redhat.com> - 2.7.7-1
- Upstream release of 2.7.7
- fix serious trouble with zlib >= 1.2.4
- xmllint new option --xpath
- various HTML parser improvements
- includes a number of nug fixes

* Tue Oct  6 2009 Daniel Veillard <veillard@redhat.com> - 2.7.6-1
- Upstream release of 2.7.6
- restore thread support off by default in 2.7.5

* Thu Sep 24 2009 Daniel Veillard <veillard@redhat.com> - 2.7.5-1
- Upstream release of 2.7.5
- fix a couple of Relax-NG validation problems
- couple more fixes

* Tue Sep 15 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-2
- fix a problem with little data at startup affecting inkscape #523002

* Thu Sep 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-1
- upstream release 2.7.4
- symbol versioning of libxml2 shared libs
- very large number of bug fixes

* Mon Aug 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-4
- two patches for parsing problems CVE-2009-2414 and CVE-2009-2416

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-1
- new release 2.7.3
- limit default max size of text nodes
- special parser mode for PHP
- bug fixes and more compiler checks

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-7
- Pull back into Python 2.6

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-6
- AutoProvides requires BuildRequires pkgconfig

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-5
- rebuild to get provides(libxml-2.0) into HEAD rawhide

* Mon Dec  1 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-4
- Rebuild for pkgconfig logic

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-3
- Rebuild for Python 2.6

* Wed Nov 12 2008 Daniel Veillard <veillard@redhat.com> - 2.7.2-2.fc11
- two patches for size overflows problems CVE-2008-4225 and CVE-2008-4226

* Fri Oct  3 2008 Daniel Veillard <veillard@redhat.com> 2.7.2-1.fc10
- new release 2.7.2
- Fixes the known problems in 2.7.1
- increase the set of options when saving documents

* Thu Oct  2 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-2.fc10
- fix a nasty bug in 2.7.x, http://bugzilla.gnome.org/show_bug.cgi?id=554660

* Mon Sep  1 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-1.fc10
- fix python serialization which was broken in 2.7.0
- Resolve: rhbz#460774

* Sat Aug 30 2008 Daniel Veillard <veillard@redhat.com> 2.7.0-1.fc10
- upstream release of 2.7.0
- switch to XML 1.0 5th edition
- switch to RFC 3986 for URI parsing
- better entity handling
- option to remove hardcoded limitations in the parser
- more testing
- a new API to allocate entity nodes
- and lot of fixes and clanups

* Mon Aug 25 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-4.fc10
- fix for entities recursion problem
- Resolve: rhbz#459714

* Fri May 30 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-3.fc10
- cleanup based on Fedora packaging guidelines, should fix #226079
- separate a -static package

* Thu May 15 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-2.fc10
- try to fix multiarch problems like #440206

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-1.fc9
- upstream release 2.6.32 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6.31-2
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Daniel Veillard <veillard@redhat.com> 2.6.31-1.fc9
- upstream release 2.6.31 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Aug 23 2007 Daniel Veillard <veillard@redhat.com> 2.6.30-1
- upstream release 2.6.30 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Tue Jun 12 2007 Daniel Veillard <veillard@redhat.com> 2.6.29-1
- upstream release 2.6.29 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed May 16 2007 Matthias Clasen <mclasen@redhat.com> 2.6.28-2
- Bump revision to fix N-V-R problem

* Tue Apr 17 2007 Daniel Veillard <veillard@redhat.com> 2.6.28-1
- upstream release 2.6.28 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.6.27-2
- rebuild against python 2.5

* Wed Oct 25 2006 Daniel Veillard <veillard@redhat.com> 2.6.27-1
- upstream release 2.6.27 see http://xmlsoft.org/news.html
- very large amount of bug fixes reported upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1
- rebuild

* Wed Jun  7 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-2
- fix bug #192873
* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-1
- upstream release 2.6.26 see http://xmlsoft.org/news.html

* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 2.6.25 broken, do not ship !

