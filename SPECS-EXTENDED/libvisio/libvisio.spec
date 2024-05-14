Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global apiversion 0.1

Name: libvisio
Version: 0.1.7
Release: 4%{?dist}
Summary: A library for import of Microsoft Visio diagrams

License: MPLv2.0
URL: https://wiki.documentfoundation.org/DLP/Libraries/libvisio
Source: https://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: help2man
BuildRequires: perl-interpreter
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: pkgconfig(libxml-2.0)

%description
%{name} is library providing ability to interpret and import
Microsoft Visio diagrams into various applications. You can find it
being used in LibreOffice.

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
Summary: Tools to transform Microsoft Visio diagrams into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Microsoft Visio diagrams into other formats.
Currently supported: XHTML, raw, plain text.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-silent-rules
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# rhbz#1001240 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in vsd2raw vss2text vsd2xhtml vss2raw vsd2text vss2xhtml; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 vsd2*.1 vss2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make check %{?_smp_mflags}

%files
%doc AUTHORS README NEWS
%license COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING.*
%doc docs/doxygen/html

%files tools
%{_bindir}/vsd2raw
%{_bindir}/vsd2text
%{_bindir}/vsd2xhtml
%{_bindir}/vss2raw
%{_bindir}/vss2text
%{_bindir}/vss2xhtml
%{_mandir}/man1/vsd2raw.1*
%{_mandir}/man1/vsd2text.1*
%{_mandir}/man1/vsd2xhtml.1*
%{_mandir}/man1/vss2raw.1*
%{_mandir}/man1/vss2text.1*
%{_mandir}/man1/vss2xhtml.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.7-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 0.1.7-2
- Rebuild for ICU 65

* Sat Aug 17 2019 David Tardon <dtardon@redhat.com> - 0.1.7-1
- new upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 0.1.6-7
- Rebuild for ICU 63

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0.1.6-5
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 0.1.6-4
- Rebuild for ICU 61.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0.1.6-2
- Rebuild for ICU 60.1

* Sat Oct 21 2017 David Tardon <dtardon@redhat.com> - 0.1.6-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.5-6
- Rebuilt for Boost 1.63

* Tue Dec 13 2016 David Tardon <dtardon@redhat.com> - 0.1.5-5
- fix char background color in some cases
- fix handling of bitmaps in Windows Bitmap format that contain a color
  palette

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 0.1.5-4
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.1.5-2
- Rebuilt for Boost 1.60

* Wed Dec 30 2015 David Tardon <dtardon@redhat.com> - 0.1.5-1
- new upstream release

* Wed Dec 23 2015 David Tardon <dtardon@redhat.com> - 0.1.4-1
- new upstream release

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 0.1.3-5
- rebuild for ICU 56.1

* Sun Aug 30 2015 David Tardon <dtardon@redhat.com> - 0.1.3-4
- fix build with boost 1.59

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.1.3-3
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Sat Jul 25 2015 David Tardon <dtardon@redhat.com> - 0.1.3-1
- new upstream release

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.1.1-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.1.1-2
- Rebuild for boost 1.57.0

* Fri Jan 02 2015 David Tardon <dtardon@redhat.com> - 0.1.1-1
- new upstream release

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-4
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-1
- new upstream release

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 0.0.31-4
- Rebuild for boost 1.55.0

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.0.31-3
- generate man pages

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 0.0.31-2
- rebuild (libicu)

* Mon Sep 02 2013 David Tardon <dtardon@redhat.com> - 0.0.31-1
- new release

* Fri Aug 30 2013 David Tardon <dtardon@redhat.com> - 0.0.30-4
- Resolves: rhbz#1001240 duplicate documentation files / potentially conflicting

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.0.30-2
- Rebuild for boost 1.54.0

* Mon Jul 15 2013 David Tardon <dtardon@redhat.com> - 0.0.30-1
- new release

* Tue Jul 02 2013 David Tardon <dtardon@redhat.com> - 0.0.29-1
- new release

* Wed Jun 05 2013 David Tardon <dtardon@redhat.com> - 0.0.28-1
- new release

* Thu May 16 2013 David Tardon <dtardon@redhat.com> - 0.0.27-1
- new release

* Tue Apr 23 2013 David Tardon <dtardon@redhat.com> - 0.0.26-1
- new release

* Thu Feb 28 2013 David Tardon <dtardon@redhat.com> - 0.0.25-1
- new release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 David Tardon <dtardon@redhat.com> - 0.0.24-1
- new release

* Mon Dec 03 2012 David Tardon <dtardon@redhat.com> - 0.0.23-1
- new release

* Thu Nov 29 2012 David Tardon <dtardon@redhat.com> - 0.0.22-1
- new upstream release

* Wed Nov 21 2012 David Tardon <dtardon@redhat.com> - 0.0.21-1
- new upstream release

* Tue Nov 06 2012 David Tardon <dtardon@redhat.com> - 0.0.20-1
- new upstream version

* Fri Jul 27 2012 David Tardon <dtardon@redhat.com> - 0.0.19-2
- rebuilt for boost 1.50

* Thu Jul 26 2012 David Tardon <dtardon@redhat.com> - 0.0.19-1
- new upstream version

* Tue Jul 24 2012 David Tardon <dtardon@redhat.com> - 0.0.18-3
- fix endless loop with text fields in VSD6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 David Tardon <dtardon@redhat.com> 0.0.18-1
- new upstream version

* Fri Jun 01 2012 David Tardon <dtardon@redhat.com> 0.0.17-1
- new upstream version

* Tue Apr 17 2012 David Tardon <dtardon@redhat.com> 0.0.16-1
- new upstream version

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.15-2
- Rebuilt for c++ ABI breakage

* Tue Feb 21 2012 David Tardon <dtardon@redhat.com> 0.0.15-1
- new upstream version

* Wed Jan 25 2012 David Tardon <dtardon@redhat.com> 0.0.14-1
- bump version

- initial import
* Wed Dec 21 2011 David Tardon <dtardon@redhat.com> 0.0.11-1
- initial import
