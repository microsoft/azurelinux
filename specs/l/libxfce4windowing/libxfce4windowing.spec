# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global prerel pre1
%global xfceversion 4.20

# Disable X11 for RHEL 10+
%bcond x11 %[%{undefined rhel} || 0%{?rhel} < 10]

%global glib2_minver 2.68.0
%global gtk3_minver 3.24.10
%global gdk_pixbuf_minver 2.40.8
%global wl_minver 1.20

%global api_majorver 0

Name:           libxfce4windowing
Version:        4.20.3
Release: 3%{?dist}
Summary:        Windowing concept abstraction library for X11 and Wayland

License:        LGPL-2.1-or-later
URL:            https://docs.xfce.org/xfce/libxfce4windowing/start
#VCS:            git:https://gitlab.xfce.org/xfce/{name}.git
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2

BuildRequires:  bzip2
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  meson >= 0.56
BuildRequires:  tar
BuildRequires:  xfce4-dev-tools >= 4.19.4
# Generic deps
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_minver}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_minver}
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib2_minver}
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_minver}
BuildRequires:  pkgconfig(gdk-3.0) >= %{gtk3_minver}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_minver}
BuildRequires:  pkgconfig(gtk-doc) >= 1.30
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.66.0
# Wayland deps
BuildRequires:  pkgconfig(gdk-wayland-3.0) >= %{gtk3_minver}
BuildRequires:  pkgconfig(wayland-scanner) >= %{wl_minver}
BuildRequires:  pkgconfig(wayland-client) >= %{wl_minver}
BuildRequires:  pkgconfig(wayland-protocols) >= 1.25
BuildRequires:  pkgconfig(wlr-protocols)
%if %{with x11}
# X11 deps
BuildRequires:  pkgconfig(libdisplay-info) >= 0.1.1
BuildRequires:  pkgconfig(x11) >= 1.6.7
BuildRequires:  pkgconfig(gdk-x11-3.0) >= %{gtk3_minver}
BuildRequires:  pkgconfig(libwnck-3.0) >= 3.14
BuildRequires:  pkgconfig(xrandr) >= 1.5.0
%endif

# Require gdk-pixbuf2-modules-extra for loaders needed for icons
# https://bugzilla.redhat.com/show_bug.cgi?id=2359089
Requires: gdk-pixbuf2-modules-extra

%description
Libxfce4windowing is an abstraction library that attempts to present
windowing concepts (screens, toplevel windows, workspaces, etc.) in a
windowing-system-independent manner.

Currently, X11 is fully supported, via libwnck.  Wayland is partially
supported, through various Wayland protocol extensions.  However, the
full range of operations available on X11 is not available on Wayland,
due to missing features in these protocol extensions.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -S git_am


%conf
%meson %{!?with_x11:-Dx11=false}

%build
%meson_build

%install
%meson_install

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc NEWS
%{_libdir}/%{name}*.so.%{api_majorver}{,.*}
%{_libdir}/girepository-1.0/Libxfce4windowing*-%{api_majorver}.0.typelib

%files devel
# Co-own the directory for now
%dir %{_includedir}/xfce4
%{_includedir}/xfce4/%{name}*/
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_datadir}/gir-1.0/Libxfce4windowing*-%{api_majorver}.0.gir


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 01 2025 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.20.3-1
- Update to v4.20.3

* Sat Apr 12 2025 Kevin Fenzi <kevin@scrye.com> - 4.20.2-2
- Add a Requires on gdk-pixbuf2-modules-extra. Fixes rhbz#2359089

* Sat Feb 15 2025 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.20.2-1
- Update to v4.20.2
- Update source to correct location

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 21 2024 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.20.0-1
- Update to v4.20.0

* Sun Nov 10 2024 Neal Gompa <ngompa@fedoraproject.org> - 4.19.9-1
- Update to 4.19.9

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.3^git20240317.0a487d7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 24 2024 Joshua Strobl <joshua@buddiesofbudgie.org> - 4.19.3^git20240317.0a487d7-1
- Update to 4.19.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.2^git20231104.1fbbf17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.2^git20231104.1fbbf17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 Neal Gompa <ngompa@fedoraproject.org> - 4.19.2^git20231104.1fbbf17-1
- Initial package
