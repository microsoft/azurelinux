# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global snap0 20150318
#global commit0 d0f62e65f0b79fb7724d8d551dc9ff11d085127b
#global gittag0 GIT-TAG
#global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Always build out-of-source
%undefine __cmake_in_source_build

# define to support qjson-qt5(-devel)
%if 0%{?fedora} || 0%{?rhel} > 6
%global qt5 1
%endif

Name:           qjson
Version:        0.9.0
Release:        23%{?dist}
Summary:        A qt-based library that maps JSON data to QVariant objects

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://github.com/flavio/qjson
%if 0%{?commit0:1}
Source0:        https://github.com/flavio/qjson/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%else
Source0:        https://github.com/flavio/qjson/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

## upstream patches

## upstreamable patches
Patch100: qjson-0.9.0-static.patch

BuildRequires: make
BuildRequires:  cmake >= 2.8.8
BuildRequires:  doxygen
BuildRequires:  pkgconfig(QtCore)
%if 0%{?qt5}
BuildRequires:  pkgconfig(Qt5Core)
%endif

# %%check
BuildRequires: xorg-x11-server-Xvfb

%description
JSON is a lightweight data-interchange format. It can represents integer, real
number, string, an ordered sequence of value, and a collection of
name/value pairs.QJson is a qt-based library that maps JSON data to
QVariant objects.

%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package qt5
Summary: A Qt5-based library that maps JSON data to QVariant objects
%description qt5
%{summary}.

%package qt5-devel
Summary: Development files for %{name}-qt5
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
%description qt5-devel
%{summary}.


%prep
%setup -q %{?commit0:-n %{name}-%{commit0}}

%patch -P100 -p1 -b .static


%build
%global _vpath_builddir %{_target_platform}
%{cmake} .. \
  -DQJSON_BUILD_TESTS:BOOL=ON \
  -DQT4_BUILD:BOOL=ON

%cmake_build

%if 0%{?qt5}
%global _vpath_builddir %{_target_platform}-qt5
%{cmake} .. \
  -DQJSON_BUILD_TESTS:BOOL=ON \
  -DQT4_BUILD:BOOL=OFF

%cmake_build
%endif

# build docs
pushd doc
doxygen
popd


%install
%if 0%{?qt5}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5
%endif
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion QJson)" = "%{version}"
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a make test -C %{_target_platform} ||:
%if 0%{?qt5}
test "$(pkg-config --modversion QJson-qt5)" = "%{version}"
xvfb-run -a make test -C %{_target_platform}-qt5 ||:
%endif


%ldconfig_scriptlets

%files
%license COPYING.lib
%doc README.md README.license
%{_libdir}/libqjson.so.%{version}
%{_libdir}/libqjson.so.0*

%files devel
%doc doc/html
%{_includedir}/qjson/
%{_libdir}/libqjson.so
%{_libdir}/pkgconfig/QJson.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/qjson/

%if 0%{?qt5}
%files qt5
%license COPYING.lib
%doc README.md README.license
%{_libdir}/libqjson-qt5.so.%{version}
%{_libdir}/libqjson-qt5.so.0*

%files qt5-devel
%doc doc/html
%{_includedir}/qjson-qt5/
%{_libdir}/libqjson-qt5.so
%{_libdir}/pkgconfig/QJson-qt5.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/qjson-qt5/
%endif


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 0.9.0-21
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.0-1
- 0.9.0, update URL, upstreamable -static.patch to fix FTBFS

* Sun Feb 14 2016 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-16
- %%check: make tests non-fatal xvfb-run isn't working "cannot connect to X server" (#1307965)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-15.20150318.d0f62e6git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-14
- pull in another Qt5-related upstream fix, enable -qt5 (#1292093)

* Sun Nov 08 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.8.1-13
- use parallel-installable patch from upstream pull request
- make -qt5 support optional (default off), turns out no one wants/needs it... yet.
- .spec cosmetics, cleanup rpm warnings

* Sat Nov 07 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-12
- qjson-qt5(-devel) support (#1234207), use %%license tag

* Mon Aug 03 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-11.20150318.d0f62e6git
- 20150318 snapshot

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.8.1-8
- rebuild (gcc5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 13 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-5
- %%check: CTEST_OUTPUT_ON_FAILURE

* Thu Aug 22 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-4
- .spec cleanup

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-1
- 0.8.1

* Fri Nov 23 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- %%files: track soname
- -devel: own %%_libdir/cmake

* Thu Nov 22 2012 Jan Grulich <jgrulich@redhat.com> - 0.8.0-1
- 0.8.0

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-9
- rebuild

* Sat Jul 21 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-8
- skip stripping some compiler flags (undocumented)
- %%files: track files closer (lib soname in particular)
- -devel: avoid dep on cmake 
- %%check: +make test, pkgconfig check

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.7.1-3
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 0.7.1-2
-0.7.1
- Fixed dependancy issue

* Sat Dec 12 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.7.1-1
-0.7.1
- Version upgrade
- Fixed doxygen documentation (Thanks again Orcan)

* Tue Dec 8 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-6
-0.6.3
- Fixed capitalization of the summary 

* Tue Dec 8 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-5
-0.6.3
- Moved Doxygen docs to the development package.
- Corrected placement of the cmake project file (Thanks Orcan)
- Fixed the running of the build tests
- Corrected column length of the descriptions
- Changed description of the devlepment package

* Sun Dec 6 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-4
-0.6.3
- Additional placment of library files fix

* Fri Dec 4 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-3
-0.6.3
- Fixed placment of library files
- Activated build tests
- Corrected ownership of include directory
- Corrected dependacies
- Added doxygen documentation
- Fixed reported version in the changelogs

* Sun Nov 22 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-2
-0.6.3
- Split off development libraries to its own package
- Modified licensing in spec file to reflect GPL2 code though docs state that qjson
-   licensed under LPGL
- Uncommeted and corrected sed line in this spec file

* Sun Nov 22 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-1
-0.6.3
- Initial Build
