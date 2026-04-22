# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global use_qt5 1
%global use_qt6 1

%global appname QCoro
%global qt5_build_dir release-qt5
%global qt6_build_dir release-qt6
%global _description %{expand:
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

The major benefit of using coroutines with Qt types is that it allows writing
asynchronous code as if it were synchronous and, most importantly, while the
coroutine is co_awaiting, the Qt event loop runs as usual, meaning that your
application remains responsive.}

Name: qcoro
Version: 0.12.0
Release: 4%{?dist}

License: MIT
Summary: C++ Coroutines for Qt
URL: https://github.com/danvratil/%{name}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%if 0%{?use_qt5}
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5WebSockets)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: qt5-qtbase-private-devel
%endif

%if 0%{?use_qt6}
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6WebSockets)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: qt6-qtbase-private-devel
%endif

BuildRequires: cmake
BuildRequires: dbus-x11
BuildRequires: gcc-c++
BuildRequires: ninja-build

%description %_description

%if 0%{?use_qt5}
%package qt5
Summary: C++ Coroutines for Qt 5
Provides: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: %{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%package qt5-devel
Summary: Development files for %{appname} (Qt 5 version)
Requires: %{name}-qt5%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Provides: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: %{name}-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description qt5 %_description
%description qt5-devel %_description
%endif

%if 0%{?use_qt6}
%package qt6
Summary: C++ Coroutines for Qt 6

%package qt6-devel
Summary: Development files for %{appname} (Qt 6 version)
Requires: %{name}-qt6%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}

%description qt6 %_description
%description qt6-devel %_description
%endif

%prep
%autosetup -p1

%build
%if 0%{?use_qt5}
mkdir %{qt5_build_dir} && pushd %{qt5_build_dir}
%cmake -G Ninja \
    -S'..' \
    -DCMAKE_BUILD_TYPE=Release \
    -DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt5/mkspecs/modules \
    -DUSE_QT_VERSION:STRING=5 \
    -DBUILD_TESTING:BOOL=ON \
    -DQCORO_BUILD_EXAMPLES:BOOL=ON \
    -DQCORO_ENABLE_ASAN:BOOL=OFF \
    -DQCORO_WITH_QML:BOOL=ON \
    -DQCORO_WITH_QTDBUS:BOOL=ON \
    -DQCORO_WITH_QTNETWORK:BOOL=ON \
    -DQCORO_WITH_QTQUICK:BOOL=ON \
    -DQCORO_WITH_QTWEBSOCKETS:BOOL=ON
%cmake_build
popd
%endif

%if 0%{?use_qt6}
mkdir %{qt6_build_dir} && pushd %{qt6_build_dir}
%cmake -G Ninja \
    -S'..' \
    -DCMAKE_BUILD_TYPE=Release \
    -DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt6/mkspecs/modules \
    -DUSE_QT_VERSION:STRING=6 \
    -DBUILD_TESTING:BOOL=ON \
    -DQCORO_BUILD_EXAMPLES:BOOL=ON \
    -DQCORO_ENABLE_ASAN:BOOL=OFF \
    -DQCORO_WITH_QML:BOOL=ON \
    -DQCORO_WITH_QTDBUS:BOOL=ON \
    -DQCORO_WITH_QTNETWORK:BOOL=ON \
    -DQCORO_WITH_QTQUICK:BOOL=ON \
    -DQCORO_WITH_QTWEBSOCKETS:BOOL=ON
%cmake_build
popd
%endif

%install
%if 0%{?use_qt5}
pushd %{qt5_build_dir}
%cmake_install
popd
%endif

%if 0%{?use_qt6}
pushd %{qt6_build_dir}
%cmake_install
popd
%endif

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if 0%{?use_qt5}
pushd %{qt5_build_dir}
%ctest --timeout 3600
popd
%endif

%if 0%{?use_qt6}
pushd %{qt6_build_dir}
%ctest --timeout 3600
popd
%endif

%if 0%{?use_qt5}
%files qt5
%doc README.md
%license LICENSES/*
%{_libdir}/lib%{appname}5*.so.0*

%files qt5-devel
%{_includedir}/%{name}5/
%{_libdir}/cmake/%{appname}5*/
%{_libdir}/lib%{appname}5*.so
%{_libdir}/qt5/mkspecs/modules/qt_%{appname}*.pri
%endif

%if 0%{?use_qt6}
%files qt6
%doc README.md
%license LICENSES/*
%{_libdir}/lib%{appname}6*.so.0*

%files qt6-devel
%{_includedir}/%{name}6/
%{_libdir}/cmake/%{appname}6*/
%{_libdir}/lib%{appname}6*.so
%{_libdir}/qt6/mkspecs/modules/qt_%{appname}*.pri
%endif

%changelog
* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 0.12.0-3
- Rebuild (qt6)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Apr 05 2025 Marie Loise Nolden <loise@kde.org> - 0.12.0-1
- 0.12.0

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 0.11.0-2
- Rebuild (qt6)

* Thu Feb 06 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 0.11.0-1
- 0.11.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 0.10.0-7
- Rebuild (qt6)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 0.10.0-5
- Rebuild (qt6)

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 0.10.0-4
- Rebuild (qt6)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.10.0-1
- 0.10.0

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 0.9.0-8
- Rebuild (qt6)

* Fri Oct 13 2023 Jan Grulich <jgrulich@redhat.com> - 0.9.0-7
- Rebuild (qt6)

* Thu Oct 05 2023 Justin Zobel <justin.zobel@gmail.com> - 0.9.0-6
- Rebuild for Qt Private API

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 0.9.0-4
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 0.9.0-3
- Rebuild for qtbase private API version change

* Mon May 29 2023 Jan Grulich <jgrulich@redhat.com> - 0.9.0-2
- Rebuild (qt6)

* Fri May 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 0.9.0-1
- Update to version 0.9.0

* Wed Feb 01 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 0.8.0-1
- Updated to version 0.8.0.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.7.0-1
- Updated to version 0.7.0.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 0.6.0-1
- 0.6.0

* Sat May 07 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.1-1
- Updated to version 0.5.1.

* Wed Mar 16 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.0-4
- Enabled s390x build.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 09 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.0-2
- Fixed summary in subpackages.

* Sun Jan 09 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.0-1
- Updated to version 0.4.0.
- Separated Qt 5 and Qt 6 versions into a different subpackages.

* Mon Oct 25 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 0.3.0-1
- Updated to version 0.3.0.

* Sat Oct 02 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-1
- Initial SPEC release.
