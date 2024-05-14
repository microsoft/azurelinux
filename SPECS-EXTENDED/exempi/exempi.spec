Summary:	Library for easy parsing of XMP metadata
Name:		exempi
Version:	2.6.1
Release:	2%{?dist}
License:	BSD
URL:		https://libopenraw.freedesktop.org/wiki/Exempi
Source0:	https://gitlab.freedesktop.org/libopenraw/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		exempi-e23c213-typeinfos.patch
BuildRequires:	gcc-c++
BuildRequires:	boost-devel expat-devel zlib-devel pkgconfig
# Work around for aarch64 support (https://bugzilla.redhat.com/show_bug.cgi?id=925327)
BuildRequires:	autoconf automake libtool
BuildRequires: make
Provides:	bundled(md5-polstra)

%description
Exempi provides a library for easy parsing of XMP metadata. It is a port of 
Adobe XMP SDK to work on UNIX and to be build with GNU automake.
It includes XMPCore and XMPFiles.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with exempi.

%prep
%autosetup -p1

%build
libtoolize -vi
NOCONFIGURE=1 ./autogen.sh
# BanEntityUsage needed for #888765
%configure CPPFLAGS="-I%{_includedir} -fno-strict-aliasing -DBanAllEntityUsage=1"

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%check
make check

%install
%make_install

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.a

%files
%license COPYING LICENSE
%doc AUTHORS ChangeLog README.md
%{_bindir}/exempi
%{_libdir}/libexempi.so.8*
%{_mandir}/man1/exempi.1*

%files devel
%{_includedir}/exempi-2.0/
%{_libdir}/libexempi.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Aug 16 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.6.1-2
- Bump to rebuild with zlib 1.2.1-2 (fixes CVE-2022-37434)

* Thu Mar 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.1-1
- Updating to version 2.6.1.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Nikola Forró <nforro@redhat.com> - 2.5.1-1
- Update to version 2.5.1
  Resolves #1747391

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct  9 2018 Owen Taylor <otaylor@redhat.com> - 2.4.5-5
- Set NOCONFIGURE when running autogen.sh to avoid running configure twice

* Wed Sep 26 2018 Nikola Forró <nforro@redhat.com> - 2.4.5-4
- Fix CVE-2018-12648
  Resolves #1594643

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Nikola Forró <nforro@redhat.com> - 2.4.5-2
- Remove ldconfig from scriptlets

* Tue Mar 13 2018 Nikola Forró <nforro@redhat.com> - 2.4.5-1
- Update to version 2.4.5
  Resolves #1553140

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 2.4.4-2
- Add missing gcc-c++ build dependency

* Tue Feb 06 2018 Nikola Forró <nforro@redhat.com> - 2.4.4-1
- Update to version 2.4.4
  Resolves #1541818

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 2.4.2-5
- Rebuilt for Boost 1.64

* Thu Jun 1 2017 Owen Taylor <otaylor@redhat.com> - 2.4.2-4
- Make manpage installation agnostic of compression
  https://fedoraproject.org/wiki/Packaging:Guidelines#Manpages

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Feb 06 2017 Kalev Lember <klember@redhat.com> - 2.4.2-2
- Rebuilt for Boost 1.63

* Mon Jan 30 2017 Nikola Forró <nforro@redhat.com> - 2.4.2-1
- Update to version 2.4.2
  Resolves #1417497

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 2.4.1-3
- Rebuilt for Boost 1.63

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 2.4.1-2
- Rebuilt for Boost 1.63

* Tue Jan 24 2017 Nikola Forró <nforro@redhat.com> - 2.4.1-1
- Update to version 2.4.1
  Resolves #1415672

* Mon Jan 09 2017 Nikola Forró <nforro@redhat.com> - 2.4.0-1
- Update to version 2.4.0
  Resolves #1411059

* Thu Mar 17 2016 Nikola Forró <nforro@redhat.com> - 2.3.0-1
- Update to version 2.3.0
  Resolves #1318279

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 2.2.1-14
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2.2.1-13
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 2.2.1-11
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.2.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 2.2.1-8
- Rebuild for boost 1.57.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 2.2.1-5
- Rebuild for boost 1.55.0

* Fri Jan 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-4
- Run libtoolize before autogen.sh
- Resolves: rhbz#1051186

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 2.2.1-2
- Rebuild for boost 1.54.0

* Mon Jul 22 2013 Deji Akingunola <dakingun@gmail.com> - 2.2.1-1
- Update to version 2.2.1

* Wed Jan 30 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.0-6
- Get rid of unnecessary LDFLAGS definition overwriting RPM flags

* Wed Jan 02 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.0-5
- Make sure we respect RPM_OPT_FLAGS and simplify configure (#889554)

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.0-4
- Add BanAllEntityUsage into macro definitions (#888765)

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.0-3
- Add bundled(md5-polstra) provides
- Update to current guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 22 2012 Deji Akingunola <dakingun@gmail.com> - 2.2.0-1
- Update to version 2.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Add testsuite execution
- Removed build patch for gcc-4.4 (fixed in upstream)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 2.1.0-2
- Add patch to build with gcc-4.4

* Tue Jan 06 2009 Deji Akingunola <dakingun@gmail.com> - 2.1.0-1
- Update to 2.1.0
    
* Sat May 17 2008 Deji Akingunola <dakingun@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Wed Apr 02 2008 Deji Akingunola <dakingun@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Fri Feb 08 2008 Deji Akingunola <dakingun@gmail.com> - 1.99.9-1
- Update to 1.99.9

* Sun Jan 13 2008 Deji Akingunola <dakingun@gmail.com> - 1.99.7-1
- Update to 1.99.7

* Mon Dec 03 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.5-1
- Update to 1.99.5

* Wed Sep 05 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.4-2
- Rebuild for expat 2.0

* Wed Aug 22 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.4-1
- Update tp 1.99.4

* Tue Jul 10 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.3-1
- Initial packaging for Fedora
