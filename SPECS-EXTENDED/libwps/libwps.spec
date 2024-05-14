%global apiversion 0.4

Name:		libwps
Version:	0.4.11
Release:	2%{?dist}
Summary:	A library for import of Microsoft Works documents

License:	LGPLv2+ or MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://libwps.sourceforge.net/
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	help2man
BuildRequires:	pkgconfig(librevenge-0.0)
BuildRequires:	pkgconfig(librevenge-generators-0.0)
BuildRequires:	pkgconfig(librevenge-stream-0.0)

%description
%{name} is a library for import of Microsoft Works text documents,
spreadsheets and (in a limited way) databases. Full list of supported
formats is available at
https://sourceforge.net/p/libwps/wiki/Home/#recognized-formats .

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:	Tools to transform Microsoft Works documents into other formats
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Microsoft Works documents into other formats.
Currently supported: CSV, HTML, raw, text

%package doc
Summary:	Documentation of %{name} API
BuildArch:	noarch

%description doc
The %{name}-doc package contains documentation files for %{name}

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR="%{buildroot}" 
rm -f %{buildroot}%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in wks2csv wks2raw wks2text wps2html wps2raw wps2text; do
    help2man -S '%{name} %{version}' -N -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 wks2*.1 wps2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%files
%doc CREDITS NEWS README
%license COPYING.LGPL COPYING.MPL
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files tools
%{_bindir}/wks2csv
%{_bindir}/wks2raw
%{_bindir}/wks2text
%{_bindir}/wps2html
%{_bindir}/wps2raw
%{_bindir}/wps2text
%{_mandir}/man1/wks2csv.1*
%{_mandir}/man1/wks2raw.1*
%{_mandir}/man1/wks2text.1*
%{_mandir}/man1/wps2html.1*
%{_mandir}/man1/wps2raw.1*
%{_mandir}/man1/wps2text.1*

%files doc
%license COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.11-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Apr 05 2020 David Tardon <dtardon@redhat.com> - 0.4.11-1
- new upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 David Tardon <dtardon@redhat.com> - 0.4.10-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 David Tardon <dtardon@redhat.com> - 0.4.9-1
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 27 2017 David Tardon <dtardon@redhat.com> - 0.4.8-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 David Tardon <dtardon@redhat.com> - 0.4.7-1
- new upstream release

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Mar 20 2017 David Tardon <dtardon@redhat.com> - 0.4.6-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.4.5-2
- Rebuilt for Boost 1.63

* Wed Jan 11 2017 David Tardon <dtardon@redhat.com> - 0.4.5-1
- new upstream release

* Mon Oct 17 2016 David Tardon <dtardon@redhat.com> - 0.4.4-1
- new upstream release

* Sun Feb 14 2016 David Tardon <dtardon@redhat.com> - 0.4.3-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.4.2-2
- Rebuilt for Boost 1.60

* Tue Oct 06 2015 David Tardon <dtardon@redhat.com> - 0.4.2-1
- new upstream release

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.4.1-2
- Rebuilt for Boost 1.59

* Tue Aug 25 2015 David Tardon <dtardon@redhat.com> - 0.4.1-1
- new upstream release

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.4.0-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 David Tardon <dtardon@redhat.com> - 0.4.0-1
- new upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.3.1-2
- Rebuild for boost 1.57.0

* Tue Dec 30 2014 David Tardon <dtardon@redhat.com> - 0.3.1-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.3.0-1
- new upstream release

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 0.2.9-8
- Rebuild for boost 1.55.0

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.2.9-7
- generate man pages

* Mon Sep 09 2013 David Tardon <dtardon@redhat.com> - 0.2.9-6
- Resolves: rhbz#1005711 do not compile in C++11 mode

* Mon Aug 19 2013 David Tardon <dtardon@redhat.com> - 0.2.9-5
- Resolves: rhbz#98166 Duplicated documentation

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 David Tardon <dtardon@redhat.com> - 0.2.9-3
- drop build req. on cppunit

* Thu May 30 2013 David Tardon <dtardon@redhat.com> - 0.2.9-2
- libwps does not have any test suite

* Sat May 25 2013 David Tardon <dtardon@redhat.com> - 0.2.9-1
- new release

* Sun Apr 21 2013 David Tardon <dtardon@redhat.com> - 0.2.8-1
- new release

* Tue Apr 16 2013 Caolán McNamara <caolanm@redhat.com> - 0.2.7-5
- Resolves: rhbz#925931 support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 David Tardon <dtardon@redhat.com> - 0.2.7-3
- rebuilt for boost 1.50

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 David Tardon <dtardon@redhat.com> - 0.2.7-1
- new release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 David Tardon <dtardon@redhat.com> - 0.2.4-1
- latest version

* Fri Nov 18 2011 David Tardon <dtardon@redhat.com> - 0.2.3-1
- latest version
- remove obsoleted patch

* Wed Jul 13 2011 David Tardon <dtardon@redhat.com> - 0.2.2-1
- latest version

* Tue Jun 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.2.0-3
- Remove -Werror from CFLAGS/CXXFLAGS (Add libwps-0.2.0-werror.patch)
  (Fix FTBFS BZ#715767).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.0-1
- latest version

* Sat Jan 30 2010 Chen Lei <supercyper@163.com> - 0.1.2-7
- Add noarch to -doc subpackage

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.1.2-5
- Correct DOC issues (again) RHBZ: #484933 / C14

* Sun Feb 15 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.1.2-4
- Correct path for CHECK section

* Sun Feb 15 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.1.2-3
- Add CHECK section
- Add cppunit-devel to BuildRequires

* Sun Feb 15 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.1.2-2
- Correct DOC issues
- Delete wrong pkgconfig pathes 

* Tue Feb 10 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.1.2-1
- Initial Package build 
