Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global apiversion 0.3

Name: libmwaw
Version: 0.3.22
Release: 1%{?dist}
Summary: A library for import of many old Mac document formats

License: LGPL-2.1-or-later OR MPL-2.0
URL: http://sourceforge.net/projects/libmwaw/
Source: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: help2man
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: make

%description
%{name} is a library for import of old Mac documents. It supports many
kinds of text documents, spreadsheets, databases, vector and bitmap
images. Supported are, for example, documents created by BeagleWorks,
ClarisWorks, MacPaint, MacWrite or Microsoft Word for Mac. A full list
of supported formats is available at
https://sourceforge.net/p/libmwaw/wiki/Home/ .

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform the supported formats into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform the supported document formats into other formats.
Supported output formats are CSV, HTML, SVG, plain text and raw.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-werror --disable-zip --enable-docs
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
%make_build

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'convert Mac spreadsheet into CSV' -o mwaw2csv.1 ./src/conv/csv/.libs/mwaw2csv
help2man -N -n 'debug the conversion library' -o mwaw2raw.1 ./src/conv/raw/.libs/mwaw2raw
help2man -N -n 'convert Mac text document into HTML' -o mwaw2html.1 ./src/conv/html/.libs/mwaw2html
help2man -N -n 'convert Mac drawing into SVG' -o mwaw2svg.1 ./src/conv/svg/.libs/mwaw2svg
help2man -N -n 'convert Mac text document into plain text' -o mwaw2text.1 ./src/conv/text/.libs/mwaw2text

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.la
# it seems this tool is only useful on MacOS
rm -f %{buildroot}/%{_bindir}/mwawFile
# rhbz#1001297 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 mwaw2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%files
%doc CHANGES README
%license COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc HACKING
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING.*
%doc docs/doxygen/html

%files tools
%{_bindir}/mwaw2csv
%{_bindir}/mwaw2html
%{_bindir}/mwaw2raw
%{_bindir}/mwaw2svg
%{_bindir}/mwaw2text
%{_mandir}/man1/mwaw2csv.1*
%{_mandir}/man1/mwaw2html.1*
%{_mandir}/man1/mwaw2raw.1*
%{_mandir}/man1/mwaw2svg.1*
%{_mandir}/man1/mwaw2text.1*

%changelog
* Mon nov 18 2024 Akarsh Chaudhary  <v-akarshc@microsoft.com> - 0.3.22-1
- upgrade to version 0.3.22
-License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.17-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Sep 21 2020 David Tardon <dtardon@redhat.com> - 0.3.17-1
- new upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.3.16-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sun Apr 05 2020 David Tardon <dtardon@redhat.com> - 0.3.16-1
- new upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 18 2019 David Tardon <dtardon@redhat.com> - 0.3.15-1
- new upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 David Tardon <dtardon@redhat.com> - 0.3.14-1
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 David Tardon <dtardon@redhat.com> - 0.3.13-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 David Tardon <dtardon@redhat.com> - 0.3.12-1
- new upstream release

* Thu Jun 15 2017 David Tardon <dtardon@redhat.com> - 0.3.11-3
- Resolves: rhbz#1461763 CVE-2017-9433 Out-of-bounds write in the
  MsWrd1Parser::readFootnoteCorrespondence function

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Mar 31 2017 David Tardon <dtardon@redhat.com> - 0.3.11-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 David Tardon <dtardon@redhat.com> - 0.3.10-1
- new upstream release

* Tue Nov 22 2016 David Tardon <dtardon@redhat.com> - 0.3.9-1
- new upstream release

* Thu Jun 16 2016 David Tardon <dtardon@redhat.com> - 0.3.8-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.3.7-2
- Rebuilt for Boost 1.60

* Thu Nov 26 2015 David Tardon <dtardon@redhat.com> - 0.3.7-1
- new upstream release

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.3.6-2
- Rebuilt for Boost 1.59

* Mon Aug 24 2015 David Tardon <dtardon@redhat.com> - 0.3.6-1
- new upstream release

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.3.5-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 David Tardon <dtardon@redhat.com> - 0.3.5-1
- new upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.4-4
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.3.4-3
- Rebuild for boost 1.57.0

* Wed Jan 07 2015 David Tardon <dtardon@redhat.com> - 0.3.4-2
- Resolves: fdo#88098 ClarisWorks: import empty starting lines/columns

* Sun Jan 04 2015 David Tardon <dtardon@redhat.com> - 0.3.4-1
- new upstream release

* Tue Oct 14 2014 David Tardon <dtardon@redhat.com> - 0.3.3-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 David Tardon <dtardon@redhat.com> - 0.3.2-1
- new upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.3.1-1
- new upstream release

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.2.0-5
- rebuild for boost 1.55.0

* Thu Apr 24 2014 David Tardon <dtardon@redhat.com> - 0.2.0-4
- avoid out-of-bounds access
- ... and other fixes from upstream 0.2 branch

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.2.0-3
- generate man pages

* Wed Jan 22 2014 David Tardon <dtardon@redhat.com> - 0.2.0-2
- update licenses to current (simpler) state

* Sat Nov 02 2013 David Tardon <dtardon@redhat.com> - 0.2.0-1
- new release

* Mon Sep 09 2013 David Tardon <dtardon@redhat.com> - 0.1.11-1
- new upstream release

* Fri Aug 30 2013 David Tardon <dtardon@redhat.com> - 0.1.10-3
- Resolves: rhbz#1001297 duplicate documentation files / potentially conflicting

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 David Tardon <dtardon@redhat.com> - 0.1.10-1
- new release

* Tue May 14 2013 David Tardon <dtardon@redhat.com> - 0.1.9-1
- new release

* Tue Apr 30 2013 David Tardon <dtardon@redhat.com> - 0.1.8-1
- new upstream release

* Sat Apr 27 2013 David Tardon <dtardon@redhat.com> - 0.1.7-2
- minor fixes

* Tue Mar 19 2013 David Tardon <dtardon@redhat.com> 0.1.7-1
- initial import
