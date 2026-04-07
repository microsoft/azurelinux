# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond qt5 %[%{undefined rhel} || 0%{?rhel} < 10]

Name:           libportal
Version:        0.9.1
Release:        3%{?dist}
Summary:        Flatpak portal library
# doc/urlmap.js is LGPL-2.1-or-later
# everything else is LGPL-3.0-only
License:        LGPL-3.0-only AND LGPL-2.1-or-later
Url:            https://github.com/flatpak/libportal
Source:         https://github.com/flatpak/libportal/releases/download/%{version}/%{name}-%{version}.tar.xz

# https://github.com/flatpak/libportal/pull/200
Patch0:         libportal-fix-build-with-qt-6_9.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%if %{with qt5}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
%endif

%description
libportal provides GIO-style asynchronous APIs for most Flatpak portals.

%package gtk3
Summary: GTK+ 3 libraries for %name
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gtk3
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for GTK+ 3 and %name.

%package gtk4
Summary: GTK 4 libraries for %name
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gtk4
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for GTK 4 and %name.

%package qt6
Summary: Qt6 libraries for %name
Requires: %{name}%{?_isa} = %{version}-%{release}

%description qt6
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for Qt 6 and %name.

%if %{with qt5}
%package qt5
Summary: Qt5 libraries for %name
Requires: %{name}%{?_isa} = %{version}-%{release}

%description qt5
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for Qt 5 and %name.
%endif

%package devel
Summary: Development files and libraries for %name
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for development with %name.

%package gtk3-devel
Summary: GTK+ 3 development files and libraries for %name
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-gtk3%{?_isa} = %{version}-%{release}

%description gtk3-devel
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for development with GTK+ 3 and %name.

%package gtk4-devel
Summary: GTK 4 development files and libraries for %name
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-gtk4%{?_isa} = %{version}-%{release}

%description gtk4-devel
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for development with GTK 4 and %name.

%package qt6-devel
Summary: Qt 6 development files and libraries for %name
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-qt6%{?_isa} = %{version}-%{release}

%description qt6-devel
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for development with Qt 6 and %name.

%if %{with qt5}
%package qt5-devel
Summary: Qt 5 development files and libraries for %name
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}

%description qt5-devel
%name provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides files for development with Qt 5 and %name.
%endif

%package devel-doc
Summary: Development documentation for libportal
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts
BuildArch: noarch

%description devel-doc
libportal provides GIO-style asynchronous APIs for most Flatpak portals.

This package provides development documentations for libportal.

%prep
%autosetup -p1

%build
%meson \
  -Dbackend-gtk3=enabled \
  -Dbackend-gtk4=enabled \
  -Dbackend-qt6=enabled \
%if %{with qt5}
  -Dbackend-qt5=enabled \
%else
  -Dbackend-qt5=disabled \
%endif
  %{nil}
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md NEWS
%{_libdir}/girepository-1.0/Xdp-1.0.typelib
%{_libdir}/libportal.so.1*

%files gtk3
%{_libdir}/girepository-1.0/XdpGtk3-1.0.typelib
%{_libdir}/libportal-gtk3.so.1*

%files gtk4
%{_libdir}/girepository-1.0/XdpGtk4-1.0.typelib
%{_libdir}/libportal-gtk4.so.1*

%if %{with qt5}
%files qt5
%{_libdir}/libportal-qt5.so.1*
%endif

%files qt6
%{_libdir}/libportal-qt6.so.1*

%files devel
%{_datadir}/gir-1.0/Xdp-1.0.gir
%{_datadir}/vala/vapi/libportal.deps
%{_datadir}/vala/vapi/libportal.vapi
%{_includedir}/libportal
%{_libdir}/libportal.so
%{_libdir}/pkgconfig/libportal.pc

%files gtk3-devel
%{_datadir}/gir-1.0/XdpGtk3-1.0.gir
%{_datadir}/vala/vapi/libportal-gtk3.deps
%{_datadir}/vala/vapi/libportal-gtk3.vapi
%{_includedir}/libportal-gtk3
%{_libdir}/libportal-gtk3.so
%{_libdir}/pkgconfig/libportal-gtk3.pc

%files gtk4-devel
%{_datadir}/gir-1.0/XdpGtk4-1.0.gir
%{_datadir}/vala/vapi/libportal-gtk4.deps
%{_datadir}/vala/vapi/libportal-gtk4.vapi
%{_includedir}/libportal-gtk4
%{_libdir}/libportal-gtk4.so
%{_libdir}/pkgconfig/libportal-gtk4.pc

%if %{with qt5}
%files qt5-devel
%{_includedir}/libportal-qt5
%{_libdir}/libportal-qt5.so
%{_libdir}/pkgconfig/libportal-qt5.pc
%endif

%files qt6-devel
%{_includedir}/libportal-qt6
%{_libdir}/libportal-qt6.so
%{_libdir}/pkgconfig/libportal-qt6.pc

%files devel-doc
%{_datadir}/doc/libportal-1

%changelog
* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 0.9.1-3
- Rebuild (qt6)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Apr 5 2025 Tomi Lähteenmäki <lihis@lihis.net> - 0.9.1-1
- Update to 0.9.1 (fedora#2345185)

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 0.9.0-4
- Rebuild (qt6)

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 22 2024 David King <amigadave@amigadave.com> - 0.9.0-1
- Update to 0.9.0 (#2333636)

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 0.8.1-2
- Rebuild (qt6)

* Sun Sep 29 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Tue Sep 03 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0
- Add Qt6 bindings

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Kalev Lember <klember@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.6-7
- Disable qt5 in RHEL 10 builds

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Bastien Nocera <bnocera@redhat.com> - 0.6-5
- Backport post-0.6 bug fixes

* Thu Dec 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6-4
- Ensure correct fonts are installed for HTML docs

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Bastien Nocera <bnocera@redhat.com> - 0.6-2
+ libportal-0.6-2
- Disable Qt tests, see https://github.com/flatpak/libportal/issues/86

* Thu Jun 09 2022 Bastien Nocera <bnocera@redhat.com> - 0.6-1
+ libportal-0.6-1
- Update to 0.6

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 David King <amigadave@amigadave.com> - 0.5-1
- Update to 0.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 06 2021 David King <amigadave@amigadave.com> - 0.4-1
- Update to 0.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Bastien Nocera <bnocera@redhat.com> - 0.3-3
+ libportal-0.3-3
- Add forgotten dist tag to Release (#1790258)

* Mon Jan 06 2020 Bastien Nocera <bnocera@redhat.com> - 0.3-2
+ libportal-0.3-2
- Add COPYING file to package

* Mon Jan 06 2020 Bastien Nocera <bnocera@redhat.com> - 0.3-1
+ libportal-0.3-1
- Update to 0.3

* Wed Dec 11 2019 Bastien Nocera <bnocera@redhat.com> - 0.1-0.1.20191211git7355b1e
+ libportal-0.1-0.20191211git7355b1e
