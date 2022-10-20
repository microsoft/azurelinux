Vendor:         Microsoft Corporation
Distribution:   Mariner
%if !0%{?bootstrap} && (0%{?fedora} || 0%{?rhel} > 6)
%global tests 1
%global python3 python%{python3_pkgversion}
%endif

Name:    lensfun
Version: 0.3.2
Summary: Library to rectify defects introduced by photographic lenses
Release: 26%{?dist}

License: LGPLv3 and CC-BY-SA
URL: http://lensfun.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

## upstream patches
Patch1: 0001-Only-require-glib-2.40-when-tests-are-build-without-.patch
Patch38: 0038-Only-use-proper-C-new-and-delete-syntax-for-object-c.patch
Patch58: 0058-Use-database-in-source-directory-while-running-tests.patch
Patch59: 0059-Patch-47-respect-DESTDIR-when-installing-python-stuf.patch
Patch60: 0060-Various-CMake-patches-from-the-mailing-list.patch
Patch113: 0113-Added-std-namespace-to-isnan.patch

## upstream patches (master branch)
Patch866: 0866-Pull-isnan-into-std-namespace-include-cmath-not-math.patch

## upstreamable patches
# install manpages only when INSTALL_HELPER_SCRIPTS=ON
Patch200: lensfun-0.3.2-INSTALL_HELPER_SCRIPTS.patch

BuildRequires: cmake >= 2.8
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(glib-2.0) 
BuildRequires: pkgconfig(libpng) 
BuildRequires: pkgconfig(zlib)
%if 0%{?python3:1}
BuildRequires: python3 python3-devel
%else
Obsoletes: lensfun-python3 < %{version}-%{release}
Obsoletes: lensfun-tools < %{version}-%{release}
%endif
# for rst2man, if INSTALL_HELPER_SCRIPTS != OFF
BuildRequires: /usr/bin/rst2man

%description
The lensfun library provides an open source database of photographic lenses and
their characteristics. It not only provides a way to read and search the
database, but also provides a set of algorithms for correcting images based on
detailed knowledge of lens properties. Right now lensfun is designed to correct
distortion, transversal (also known as lateral) chromatic aberrations,
vignetting and color contribution of a lens.

%package devel
Summary: Development toolkit for %{name}
License: LGPLv3
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains library and header files needed to build applications
using lensfun.

%package tools
Summary: Tools for managing %{name} data
License: LGPLv3
Requires: python3-lensfun = %{version}-%{release}
%description tools
This package contains tools to fetch lens database updates and manage lens
adapters in lensfun.

%package -n python3-lensfun
Summary:  Python3 lensfun bindings
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
## pkgname changed in epel7 from python34- to python36-
Obsoletes: python34-lensfun < %{version}-%{release}
%endif
%description -n python3-lensfun
%{summary}.


%prep
%setup -q

%patch1 -p1 -b .0001
%patch38 -p1 -b .0038
%patch58 -p1 -b .0058
%patch59 -p1 -b .0059
%patch60 -p1 -b .0060
%patch113 -p1 -b .0113

%patch866 -p1 -b .0866

%patch200 -p1 -b .INSTALL_HELPER_SCRIPTS

%if 0%{?python3:1}
sed -i.shbang \
  -e "s|^#!/usr/bin/env python3$|#!%{__python3}|g" \
  apps/lensfun-add-adapter \
  apps/lensfun-update-data
%endif


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DBUILD_DOC:BOOL=ON \
  -DBUILD_TESTS:BOOL=%{?tests:ON}%{!?tests:OFF} \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir} \
  %{?!python3:-DINSTALL_HELPER_SCRIPTS:BOOL=OFF}
popd

%make_build -C %{_target_platform}

make doc -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# create/own /var/lib/lensfun-updates
mkdir -p %{buildroot}/var/lib/lensfun-updates

## unpackaged files
# omit g-lensfun-update-data because it needs gksudo which we don't ship
rm -fv %{buildroot}%{_bindir}/g-lensfun-update-data \
       %{buildroot}%{_mandir}/man1/g-lensfun-update-data.*


%check
%if 0%{?tests}
pushd %{_target_platform}
export CTEST_OUTPUT_ON_FAILURE=1
ctest -vv
popd
%endif


%ldconfig_scriptlets

%files
%doc README.md
%license docs/cc-by-sa-3.0.txt docs/lgpl-3.0.txt
%{_datadir}/lensfun/
%{_libdir}/liblensfun.so.%{version}
%{_libdir}/liblensfun.so.1*
%dir /var/lib/lensfun-updates/

%files devel
%{_pkgdocdir}/*.css
%{_pkgdocdir}/*.html
%{_pkgdocdir}/*.js
%{_pkgdocdir}/*.png
%{_pkgdocdir}/*.svg
%{_includedir}/lensfun/
%{_libdir}/liblensfun.so
%{_libdir}/pkgconfig/lensfun.pc

%if 0%{?python3:1}
%files tools
%{_bindir}/lensfun-add-adapter
%{_bindir}/lensfun-update-data
%{_mandir}/man1/lensfun-add-adapter.1*
%{_mandir}/man1/lensfun-update-data.1*

%files -n python3-lensfun
%{python3_sitelib}/lensfun/
%{python3_sitelib}/lensfun*.egg-info
%endif


%changelog
* Thu Oct 20 2022 Muhammad Falak R Wani <mwani@microsoft.com> - 0.3.2-26
- License verified

* Wed Jul 07 2021 Muhammad Falak R Wani <mwani@microsoft.com> - 0.3.2-25
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Fix usage of %{python3} macro. Use python3 instead of %{python3}.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-24
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-23
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Kalev Lember <klember@redhat.com> - 0.3.2-21
- Avoid using the bindir macro in BuildRequires

* Wed Jun 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-20
- use %%python3_pkgversion
- epel7: Obsoletes: python34-lensfun (#1721810)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-18
- BR: %_bindir/rst2man (#1604549)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-16
- use %%make_build %%ldconfig_scriptlets (#1600022)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-15
- Rebuilt for Python 3.7

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> 0.3.2-14
- require gcc, gcc-c++ for building

* Mon Feb 12 2018 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-13
- -tools: make buildable on epel7/python34

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.2-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-9
- epel7 compatibility (#1454359)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-7
- lensfun-tools package should depend on python3-lensfun (#1409893)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-6
- Rebuild for Python 3.6

* Thu Dec 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-5
- more upstream fixes... from the right branch (0.3)

* Thu Dec 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-4
- support BUILD_FOR_SSE/SSE2 on %%ix86/x86_64 (#1400481)
- enable/fix python bindings
- pull in upstream fixes (tests, buildsys)

* Tue Nov 15 2016 Germano Massullo <germano.massullo@gmail.com> - 0.3.2-3
- Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 03 2016 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- lensfun-0.3.2 (#1295216), %%check: enable tests

* Tue Jul 14 2015 Rex Dieter <rdieter@fedoraproject.org> 0.3.1-3
- lensfun-update-data: Root privileges needed (#1242826)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Nils Philippsen <nils@redhat.com> - 0.3.1-1
- version 0.3.1 (with API/ABI changes)
- fix source URL (no tar.bz2 available)
- update patches

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Nov 19 2014 Nils Philippsen <nils@redhat.com> 0.3.0-4
- reenable helper scripts
- install man pages into their correct place
- correct typo

* Mon Nov 17 2014 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-3
- enable sse only in %%ix86 x86_64, sse2 on x86_64, disable elsewhere

* Mon Nov 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.3.0-2
- -DINSTALL_HELPER_SCRIPTS=OFF (with patch)
- -DCMAKE_BUILD_TYPE=Release (defaults to Debug otherwise)
- disable SSE2 on %%ix86 (fedora base i686 platform doesn't support it)
- use %%buildroot consistently

* Mon Nov 17 2014 Nils Philippsen <nils@redhat.com> - 0.3.0-1
- version 0.3.0

* Tue Nov 04 2014 Nils Philippsen <nils@redhat.com> - 0.3.0-1
- Lensfun moved from Berlios to SourceForge (#1159993)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Rex Dieter <rdieter@fedoraproject.org> 0.2.8-1
- 0.2.8 (#1048784)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.2.7-1
- 0.2.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 25 2012 Nils Philippsen <nils@redhat.com> - 0.2.6-3
- pkgconfig: fix cflags so lensfun.h is found

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.2.6-1
- lensfun-0.2.6 (#836156)
- use cmake
- use pkgconfig-style deps

* Thu Jun 21 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-8
- don't modify doxygen configuration anymore as doxygen carries fixes now
  (#831399)

* Fri Jun 15 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-7
- multilib: don't embed creation dates in generated docs (#831399)

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-6
- rebuild for gcc 4.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.5-4
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Nils Philippsen <nils@redhat.com> 0.2.5-3
- backport cpuid fixes (#631674)

* Mon Jul 26 2010 Dan Horák <dan[at]danny.cz> 0.2.5-2
- disable SSE vectorization on non x86 arches

* Mon Jun 07 2010 Nils Philippsen <nils@redhat.com> 0.2.5-1
- lensfun-0.2.5
- add CC-BY-SA to main package license tag for lens data
- don't ship GPLv3 text as nothing is licensed under it currently
- mark documentation files as such
- shorten summaries, expand package descriptions

* Sun Oct 18 2009 Rex Dieter <rdieter@fedoraproject.orG> 0.2.4-1
- lensfun-0.2.4 (#529506)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-3
- rebuild for pkgconfig deps

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-2
- -devel: Requires: pkgconfig

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-1
- lensfun-0.2.3
- fix SOURCE Url
- configure --target=..generic

* Mon Oct 13 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-3
- BR: doxygen

* Mon Oct 13 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-2
- fix subpkg deps

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-1
- adapt for fedora

* Tue Jun 24 2008 Helio Chissini de Castro <helio@mandriva.com> 0.2.2b-1mdv2009.0
+ Revision: 228769
- Added missing buildrequires
- import lensfun
