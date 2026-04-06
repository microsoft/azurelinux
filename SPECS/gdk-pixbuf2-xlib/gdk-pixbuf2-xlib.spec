# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           gdk-pixbuf2-xlib
Version:        2.40.2
Release:        12%{?dist}
Summary:        Deprecated Xlib integration for gdk-pixbuf2

License:        LGPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/Archive/gdk-pixbuf-xlib
Source0:        https://download.gnome.org/sources/gdk-pixbuf-xlib/2.40/gdk-pixbuf-xlib-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(x11)

%description
gdk-pixbuf2-xlib contains the deprecated API for integrating gdk-pixbuf2 with
Xlib data types.

This library was originally shipped by gdk-pixbuf2, and has
since been moved out of the original repository.

No newly written code should ever use this library.

If your existing code depends on gdk-pixbuf2-xlib, then you're strongly
encouraged to port away from it.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n gdk-pixbuf-xlib-%{version}


%build
%meson -Dgtk_doc=true
%meson_build


%install
%meson_install


%files
%license COPYING
%doc README.md
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.0*

%files devel
%{_includedir}/gdk-pixbuf-2.0/
%{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%{_datadir}/gtk-doc/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 2.40.2-2
- Use actual gdk-pixbuf2 package names in package description and summary

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 2.40.2-1
- Initial Fedora packaging, package split off from gdk-pixbuf2
