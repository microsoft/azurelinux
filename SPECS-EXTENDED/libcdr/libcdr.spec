Vendor:         Microsoft Corporation
Distribution:   Mariner
%global apiversion 0.1

Name: libcdr
Version: 0.1.6
Release: 2%{?dist}
Summary: A library for import of CorelDRAW drawings

# the only Public Domain source is src/lib/CDRColorProfiles.h
License: MPLv2.0 and Public Domain
URL: http://wiki.documentfoundation.org/DLP/Libraries/libcdr
Source: http://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz
Patch0: icu-68-1-build-fix.patch

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: help2man
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: pkgconfig(zlib)

%description
Libcdr is library providing ability to interpret and import CorelDRAW
drawings into various applications. You can find it being used in
libreoffice.

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
Summary: Tools to transform CorelDRAW drawings into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform CorelDRAW drawings into other formats.
Currently supported: XHTML, text, raw.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# rhbz#1001251 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in cdr2raw cmx2raw cdr2xhtml cmx2xhtml cdr2text cmx2text; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 0644 cdr2*.1 cmx2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS ChangeLog README
%license COPYING.MPL
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING.MPL
%doc docs/doxygen/html

%files tools
%{_bindir}/cdr2raw
%{_bindir}/cdr2text
%{_bindir}/cdr2xhtml
%{_bindir}/cmx2raw
%{_bindir}/cmx2text
%{_bindir}/cmx2xhtml
%{_mandir}/man1/cdr2raw.1*
%{_mandir}/man1/cdr2text.1*
%{_mandir}/man1/cdr2xhtml.1*
%{_mandir}/man1/cmx2raw.1*
%{_mandir}/man1/cmx2text.1*
%{_mandir}/man1/cmx2xhtml.1*

%changelog
* Wed May 19 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.1.6-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Apply build fix for break caused by icu package upgrade

* Fri Feb 07 2020 David Tardon <dtardon@redhat.com> - 0.1.6-1
- new upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 0.1.5-6
- Rebuild for ICU 65

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.1.5-3
- Rebuilt for Boost 1.69

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 0.1.5-2
- Rebuild for ICU 63

* Sat Dec 29 2018 David Tardon <dtardon@redhat.com> - 0.1.5-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0.1.4-6
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 0.1.4-5
- Rebuild for ICU 61.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.1.4-3
- Rebuilt for Boost 1.66

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0.1.4-2
- Rebuild for ICU 60.1

* Fri Sep 15 2017 David Tardon <dtardon@redhat.com> - 0.1.4-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.3-5
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.3-2
- Rebuilt for Boost 1.63

* Thu Jul 21 2016 David Tardon <dtardon@redhat.com> - 0.1.3-1
- new upstream release

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 0.1.2-4
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.1.2-2
- Rebuilt for Boost 1.60

* Sun Dec 27 2015 David Tardon <dtardon@redhat.com> - 0.1.2-1
- new upstream release

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 0.1.1-9
- rebuild for ICU 56.1

* Sun Aug 30 2015 Jonathan Wakely <jwakely@redhat.com> - 0.1.1-8
- Rebuilt for Boost 1.59

* Sun Aug 30 2015 David Tardon <dtardon@redhat.com> - 0.1.1-7
- Resolves: rhbz#1258127 fix build with boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.1.1-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.1.1-2
- Rebuild for boost 1.57.0

* Tue Nov 25 2014 David Tardon <dtardon@redhat.com> - 0.1.1-1
- new upstream release

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-4
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-1
- new upstream release

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.0.16-2
- Rebuild for boost 1.55.0

* Thu Apr 10 2014 David Tardon <dtardon@redhat.com> - 0.0.16-1
- new upstream release

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.0.15-2
- generate man pages

* Sat Apr 05 2014 David Tardon <dtardon@redhat.com> - 0.0.15-1
- new upstream release

* Thu Feb 13 2014 David Tardon <dtardon@redhat.com> - 0.0.14-6
- rebuild for new ICU

* Fri Aug 30 2013 David Tardon <dtardon@redhat.com> - 0.0.14-5
- Resolves: rhbz#1001251 duplicate documentation files / potentially conflicting

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.0.14-3
- Rebuild for boost 1.54.0

* Tue May 21 2013 David Tardon <dtardon@redhat.com> - 0.0.14-2
- add public domain to licenses

* Fri May 17 2013 David Tardon <dtardon@redhat.com> - 0.0.14-1
- new release

* Tue Apr 23 2013 David Tardon <dtardon@redhat.com> - 0.0.13-1
- new relese

* Mon Apr 08 2013 David Tardon <dtardon@redhat.com> - 0.0.12-1
- new release

* Sat Mar 02 2013 David Tardon <dtardon@redhat.com> - 0.0.11-1
- new release

* Thu Jan 31 2013 David Tardon <dtardon@redhat.com> - 0.0.10-2
- rebuild for ICU change

* Mon Jan 28 2013 David Tardon <dtardon@redhat.com> - 0.0.10-1
- new release

* Tue Jan 08 2013 David Tardon <dtardon@redhat.com> - 0.0.9-2
- Resolves: rhbz#891082 libreoffice Impress constantly crashes

* Mon Oct 08 2012 David Tardon <dtardon@redhat.com> - 0.0.9-1
- new upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 David Tardon <dtardon@redhat.com> 0.0.8-1
- new upstream release
- adds basic initial primitive uncomplete text support

* Thu Apr 26 2012 David Tardon <dtardon@redhat.com> 0.0.7-1
- new upstream release

* Tue Apr 03 2012 David Tardon <dtardon@redhat.com> 0.0.6-1
- new upstream release

* Mon Mar 19 2012 David Tardon <dtardon@redhat.com> 0.0.5-1
- new upstream release
- fix license

* Sat Mar 10 2012 David Tardon <dtardon@redhat.com> 0.0.3-2
- remove Requires: of main package from -doc subpackage

* Thu Mar 01 2012 David Tardon <dtardon@redhat.com> 0.0.3-1
- initial import
