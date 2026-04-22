# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable X11 for RHEL
%bcond x11 %[%{undefined rhel}]

%global		framework kidletime

Name:		kf6-%{framework}
Version:	6.23.0
Release: 2%{?dist}
Summary:	KDE Frameworks 6 Tier 1 integration module for idle time detection
License:	CC0-1.0 AND GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
URL:		https://invent.kde.org/frameworks/%{framework}
Source0:	https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz
Source1:	https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz.sig

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	extra-cmake-modules >= %{version}
BuildRequires:	kf6-rpm-macros
BuildRequires:	qt6-qtbase-devel
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols-devel
BuildRequires:	cmake(PlasmaWaylandProtocols)
BuildRequires:	cmake(Qt6WaylandClient)
Requires:	kf6-filesystem
%if %{with x11}
Recommends:	%{name}-x11%{?_isa} = %{version}-%{release}
%endif

%description
KDE Frameworks 6 Tier 1 integration module for idle time detection.

%if %{with x11}
%package	x11
Summary:	Idle time detection plugins for X11 environments
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-sync)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xkbcommon)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Conflicts:	%{name} < 6.6.0-1
# X11 is deprecated and this will be removed eventually...
Provides:	deprecated()

%description	x11
The %{name}-x11 package contains plugins for applications using
%{name} to detect idle time on X11 environments.
%endif

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	qt6-qtbase-devel
%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch
%description    doc
Developer Documentation files for %{name} for use with KDevelop or QtCreator.

%package        html
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch
%description    html
Developer Documentation files for %{name} in HTML format

%prep
%autosetup -n %{framework}-%{version} -p1

%build
%cmake_kf6 \
  -DWITH_X11=%{?with_x11:ON}%{?!with_x11:OFF}
%cmake_build_kf6

%install
%cmake_install_kf6

%files
%doc README.md
%license LICENSES/*.txt
%{_kf6_datadir}/qlogging-categories6/%{framework}.*
%{_kf6_libdir}/libKF6IdleTime.so.*
%dir %{_kf6_plugindir}/org.kde.kidletime.platforms/
%{_kf6_plugindir}/org.kde.kidletime.platforms/KF6IdleTimeWaylandPlugin.so

%if %{with x11}
%files x11
%{_kf6_plugindir}/org.kde.kidletime.platforms/KF6IdleTimeXcbPlugin0.so
%{_kf6_plugindir}/org.kde.kidletime.platforms/KF6IdleTimeXcbPlugin1.so
%endif

%files devel
%{_kf6_includedir}/KIdleTime/
%{_kf6_libdir}/libKF6IdleTime.so
%{_kf6_libdir}/cmake/KF6IdleTime/
%{_qt6_docdir}/*/*.tags
%{_qt6_docdir}/*/*.index

%files doc
%{_qt6_docdir}/*.qch

%files html
%{_qt6_docdir}/*/*
%exclude %{_qt6_docdir}/*/*.tags
%exclude %{_qt6_docdir}/*/*.index

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.23.0-1
- 6.23.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 02 2026 farchord@gmail.com - 6.22.0-1
- 6.22.0

* Fri Dec 05 2025 Steve Cossette <farchord@gmail.com> - 6.21.0-1
- 6.21.0

* Thu Nov 13 2025 Steve Cossette <farchord@gmail.com> - 6.20.0-1
- 6.20.0

* Sun Oct 05 2025 Steve Cossette <farchord@gmail.com> - 6.19.0-1
- 6.19.0

* Tue Sep 16 2025 farchord@gmail.com - 6.18.0-1
- 6.18.0

* Fri Aug 01 2025 Steve Cossette <farchord@gmail.com> - 6.17.0-1
- 6.17.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 05 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.16.0-1
- 6.16.0

* Tue Jun 17 2025 Marie Loise Nolden <loise@kde.org> - 6.15.0-2
- 6.15 and plasma 3.4 compatibility rebuild

* Sat Jun 07 2025 Steve Cossette <farchord@gmail.com> - 6.15.0-1
- 6.15.0

* Sat May 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.14.0-1
- 6.14.0

* Sun Apr 06 2025 Steve Cossette <farchord@gmail.com> - 6.13.0-1
- 6.13.0

* Fri Mar 07 2025 Steve Cossette <farchord@gmail.com> - 6.12.0-1
- 6.12.0

* Fri Feb 07 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.11.0-1
- 6.11.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Steve Cossette <farchord@gmail.com> - 6.10.0-1
- 6.10.0

* Sat Dec 14 2024 Steve Cossette <farchord@gmail.com> - 6.9.0-1
- 6.9.0

* Sat Nov 02 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.8.0-1
- 6.8.0

* Fri Oct 04 2024 Steve Cossette <farchord@gmail.com> - 6.7.0-1
- 6.7.0

* Wed Oct 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.6.0-3
- Enable X11 plugins and ship as subpackage in Fedora

* Wed Oct 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.6.0-2
- Drop unused qt6-qtbase-private-devel BR

* Mon Sep 16 2024 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Thu Sep 05 2024 Troy Dawson <tdawson@redhat.com> - 6.5.0-2
- Clean up X dependencies

* Sat Aug 10 2024 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Sat Jun 01 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Sat May 04 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Wed Apr 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.0.0-3
- Rebuild (qt6)

* Sat Mar 09 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-2
- add missing BuildArch: noarch to -doc package

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 5.249.0-2
- Rebuild (qt6)

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.249.0-1
- 5.249.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.248.0-1
- 5.248.0

* Tue Jan 09 2024 Marie Loise Nolden <loise@kde.org> - 5.247.0-2
- add doc package for KF6 API

* Wed Dec 20 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.247.0-1
- 5.247.0

* Sat Dec 02 2023 Justin Zobel <justin.zobel@gmail.com> - 5.246.0-1
- Update to 5.246.0

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 5.245.0-2
- Rebuild (qt6)

* Thu Nov 09 2023 Steve Cossette <farchord@gmail.com> - 5.245.0-1
- 5.245.0

* Tue Oct 17 2023 Jan Grulich <jgrulich@redhat.com> - 5.240.0^20230829.233116.5bf73aa-3
- Rebuild (qt6)

* Thu Oct 05 2023 Justin Zobel <justin.zobel@gmail.com> - 5.240.0^20230829.233116.5bf73aa-2
- Rebuild for Qt Private API

* Sun Sep 24 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20230829.233116.5bf73aa-1
- Initial release
