%global tests 1
%global python3 python%{python3_pkgversion}

Name:    lensfun
Version: 0.3.4
Summary: Library to rectify defects introduced by photographic lenses
Release: 3%{?dist}

License: LGPLv3 and CC-BY-SA
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://lensfun.github.io/
Source0: https://github.com/lensfun/lensfun/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: https://lensfun.sourceforge.net/db/version_1.tar.bz2

## upstream patches

## upstreamable patches
# install manpages only when INSTALL_HELPER_SCRIPTS=ON
Patch200: lensfun-0.3.2-INSTALL_HELPER_SCRIPTS.patch

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(zlib)
%if 0%{?python3:1}
BuildRequires: %{python3} %{python3}-devel
BuildRequires: python3-setuptools
# we cannot use pyproject_buildrequires as setup.py is created in
# build phase
BuildRequires: python3-pip
BuildRequires: python3-wheel
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
Requires: %{python3}-lensfun = %{version}-%{release}
%description tools
This package contains tools to fetch lens database updates and manage lens
adapters in lensfun.

%package -n %{python3}-lensfun
Summary:  Python3 lensfun bindings
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n %{python3}-lensfun
%{summary}.

%prep
%autosetup -p1
# extract the updated data
pushd data/db
tar xvf %{SOURCE1} > /dev/null
popd

# disable calls to setup.py, we use our own python build/install macros
# this is the 0.3.4 version...
sed -i -e '/${PYTHON} ${SETUP_PY}/d' apps/CMakeLists.txt
# ...this is how it is on master branch, for future-proofing
sed -i -e '/${Python3_EXECUTABLE} ${SETUP_PY}/d' apps/CMakeLists.txt
# creating a timestamp doesn't work with build step disabled
sed -i -e '/touch/d' apps/CMakeLists.txt

%if 0%{?python3:1}
sed -i.shbang \
  -e "s|^#!/usr/bin/env python3$|#!%{__python3}|g" \
  apps/lensfun-add-adapter \
  apps/lensfun-update-data
%endif

%build
%cmake \
  -DBUILD_DOC:BOOL=ON \
  -DBUILD_TESTS:BOOL=%{?tests:ON}%{!?tests:OFF} \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir} \
  %{?!python3:-DINSTALL_HELPER_SCRIPTS:BOOL=OFF}

%cmake_build

%cmake_build --target doc

# do a proper guideline-compliant build of the python library
pushd apps
%py3_build
popd

%install
%cmake_install

# do a proper guideline-compliant install of the python library
pushd apps
%py3_install
popd

# create/own /var/lib/lensfun-updates
mkdir -p %{buildroot}/var/lib/lensfun-updates

## unpackaged files
# omit g-lensfun-update-data because it needs gksudo which we don't ship
rm -fv %{buildroot}%{_bindir}/g-lensfun-update-data \
       %{buildroot}%{_mandir}/man1/g-lensfun-update-data.* \
       %{buildroot}%{_docdir}/%{name}/doxygen.svg


%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
%ctest
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
%{_pkgdocdir}/*.html
%{_pkgdocdir}/*.png
%{_pkgdocdir}/*.css
%{_pkgdocdir}/*.js
# seems like we install no SVGs on EPEL <= 9
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

%files -n %{python3}-lensfun
%{python3_sitelib}/lensfun-*.egg-info/
%{python3_sitelib}/lensfun/
%endif

%changelog
* Mon Feb 11 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.3.4-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 27 2024 Adam Williamson <awilliam@redhat.com> - 0.3.4-1
- Update to 0.3.4, drop merged and no-longer-needed patches
- Fix Python build/install so Python subpackage works
- Fix build on EPEL 8 and 9
- Include latest database from upstream

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 9 2023 Tom Rix <trix@redhat.com> - 0.3.3-5
- Fix *.egg-info to *.egg

* Wed Jun 28 2023 Michael J Gruber <mjg@fedoraproject.org> - 0.3.3-4
- fix FTBFS pre py 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.3-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 04 2022 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- lensfun-0.3.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.2-37
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-35
- better FTBFS fix

* Tue Aug 03 2021 Graham White <graham_alton@hotmail.com> - 0.3.2-34
- Fix FTBFS (#1987636)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.2-32
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 07 2020 Than Ngo <than@redhat.com> - 0.3.2-30
- Fix FTBFS

* Tue Aug 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-29
- fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-28
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-26
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

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
