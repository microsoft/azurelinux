# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_qt4 1
%if 0%{?rhel}
%global with_qt4 0
%endif

%global ubuntu 16.04
%global snapshot 20160218
# FIXME?  pkg-config files still report as 0.9.2
%global tarballversion 0.9.2

# set this until when/if we port to new cmake macros
%global __cmake_in_source_build 1

Summary: A Qt implementation of the DBusMenu protocol 
Name:    dbusmenu-qt
Version: 0.9.3
Release: 0.37.%{snapshot}%{?dist}

License: LGPL-2.0-or-later
URL: https://launchpad.net/libdbusmenu-qt/
%if 0%{?snapshot}
# bzr branch lp:libdbusmenu-qt && cd libdbusmenu-qt && bzr export --root=libdbusmenu-qt-%{version}-%{snapshot}bzr.tar.gz
#Source0:  libdbusmenu-qt-%{version}-%{snapshot}bzr.tar.gz
Source0:  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/libdbusmenu-qt/%{version}+%{ubuntu}.%{snapshot}-0ubuntu1/libdbusmenu-qt_%{version}+%{ubuntu}.%{snapshot}.orig.tar.gz
%else
Source0:  https://launchpad.net/libdbusmenu-qt/trunk/%{version}/+download/libdbusmenu-qt-%{version}.tar.bz2
%endif


## upstream patches

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: pkgconfig
%if 0%{?with_qt4}
BuildRequires: pkgconfig(QJson)
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtGui)
%endif # with_qt4
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Widgets)
# test-suite
BuildRequires: xorg-x11-server-Xvfb dbus-x11
BuildRequires: make

Provides: libdbusmenu-qt = %{version}-%{release}

%description
This library provides a Qt implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.

%if 0%{?with_qt4}
%package devel
Summary: Development files for %{name}
Provides: libdbusmenu-qt-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Development and API documentation for %{name}
BuildArch: noarch
# when -doc content was moved here
Conflicts: dbusmenu-qt-devel < 0.9.3
%description doc
%{summary}.
%endif # with_qt4

%package -n dbusmenu-qt5
Summary: A Qt implementation of the DBusMenu protocol
Provides: libdbusmenu-qt5 = %{version}-%{release}
%description -n dbusmenu-qt5
This library provides a Qt5 implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.

%package -n dbusmenu-qt5-devel
Summary: Development files for dbusmenu-qt5
Provides: libdbusmenu-qt5-devel = %{version}-%{release}
Requires: dbusmenu-qt5%{?_isa} = %{version}-%{release}
%description -n dbusmenu-qt5-devel
%{summary}.


%prep
%autosetup -n libdbusmenu-qt-%{version}+%{ubuntu}.%{snapshot}


%build
%if 0%{?with_qt4}
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DUSE_QT4:BOOL=ON \
  -DUSE_QT5:BOOL=OFF \
  -DWITH_DOC:BOOL=ON

popd

%make_build -C %{_target_platform}
%endif # with_qt4

mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%cmake .. \
  -DUSE_QT4:BOOL=OFF \
  -DUSE_QT5:BOOL=ON \
  -DWITH_DOC:BOOL=OFF

popd

%make_build -C %{_target_platform}-qt5


%install
%if 0%{?with_qt4}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%endif # with_qt4
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5

# unpackaged files
rm -rfv %{buildroot}%{_docdir}/libdbusmenu-qt*-doc


%check
# verify pkg-config version
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
%if 0%{?with_qt4}
test "$(pkg-config --modversion dbusmenu-qt)" = "%{tarballversion}"
%endif # with_qt4
test "$(pkg-config --modversion dbusmenu-qt5)" = "%{tarballversion}"
# test suite
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a dbus-launch --exit-with-session make -C %{_target_platform} check ARGS="--output-on-failure --timeout 300" ||:


%if 0%{?with_qt4}
%ldconfig_scriptlets

%files
%doc README
%license COPYING
%{_libdir}/libdbusmenu-qt.so.2*

%files devel
%doc %{_target_platform}/html/
%{_includedir}/dbusmenu-qt/
%{_libdir}/libdbusmenu-qt.so
%{_libdir}/cmake/dbusmenu-qt/
%{_libdir}/pkgconfig/dbusmenu-qt.pc

%files doc
%doc %{_target_platform}/html/
%endif # with_qt4

%ldconfig_scriptlets -n dbusmenu-qt5

%files -n dbusmenu-qt5
%doc README
%license COPYING
%{_libdir}/libdbusmenu-qt5.so.2*

%files -n dbusmenu-qt5-devel
%{_includedir}/dbusmenu-qt5/
%{_libdir}/libdbusmenu-qt5.so
%{_libdir}/pkgconfig/dbusmenu-qt5.pc
%{_libdir}/cmake/dbusmenu-qt5/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.37.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.36.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.35.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.34.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.33.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.32.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 12 2023 Than Ngo <than@redhat.com> - 0.9.3-0.31.20160218
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.30.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.29.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.28.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.27.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.26.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-0.25.20160218
- fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.24.20160218
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.23.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.22.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.21.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.20.20160218
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-0.19.20160218
- libdbusmenu-qt_0.9.3+16.04.20160218
- use %%autosetup %%make_build

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.18.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-0.17.20150604
- BR: gcc-c++
- use %%ldconfig_scriptlets 

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.16.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-0.15.20150604
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.14.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.13.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.12.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.11.20150604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-0.10.20150604
- consolidate dbusmenu-qt5 here (instead of using a separate module)
- fresh(er) 20150604 snapshot
- -doc noarch subpkg

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.2-9
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-6
- .spec cleanup, %%check harder

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 08 2012 Than Ngo <than@redhat.com> - 0.9.2-3
- fix url

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-2
- fix %%check

* Sat Oct 01 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- 0.9.0
- pkgconfig-style deps

* Thu Jun 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-2
- rebuild

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- 0.8.2

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 0.6.6-1
- 0.6.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.6.3-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Rex Dieter <rdieter@fedoraproject.org> 0.6.3-1
- dbusmenu-qt-0.6.3
- include kubuntu_00_external_contributions.diff 

* Fri Aug 06 2010 Rex Dieter <rdieter@fedoraproject.org> 0.5.2-1
- dbusmenu-qt-0.5.2

* Fri May 21 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- dbusmenu-qt-0.3.3

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-2
- pkg rename s/libdbusmenu-qt/dbusmenu-qt/
- Provides: libdbusmenu-qt(-devel)

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- dbusmenu-qt-0.3.2

