# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libmanette
Version:        0.2.13
Release: 2%{?dist}
Summary:        Game controller library

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/libmanette
Source0:        https://download.gnome.org/sources/libmanette/0.2/libmanette-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  vala

%description
libmanette is a small GObject library giving you simple access to game
controllers.

This library is intended for software needing a painless access to game
controllers from any programming language and with little dependencies.

It supports the de-facto standard gamepads as defined by the W3C standard
Gamepad specification or as implemented by the SDL GameController. More game
controller kinds could be supported in the future if needed. Mapping of the
devices is handled transparently and internally by the library using the
popular SDL mapping string format.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc NEWS README.md
%{_libdir}/girepository-1.0/
%{_libdir}/libmanette-0.2.so.0*

%files devel
%{_bindir}/manette-test
%{_includedir}/libmanette/
%{_libdir}/libmanette-0.2.so
%{_libdir}/pkgconfig/manette-0.2.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/

%changelog
* Fri Oct 10 2025 Petr Schindler <pschindl@redhat.com> - 0.2.13-1
- Update to 0.2.13

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 14 2025 nmontero <nmontero@redhat.com> - 0.2.12-1
- Update to 0.2.12

* Wed Mar 19 2025 nmontero <nmontero@redhat.com> - 0.2.11-1
- Update to 0.2.11

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 nmontero <nmontero@redhat.com> - 0.2.9-1
- Update to 0.2.9

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 10 2024 David King <amigadave@amigadave.com> - 0.2.7-1
- Update to 0.2.7

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan  5 2021 Kalev Lember <klember@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 0.2.5-1
- Update to 0.2.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Apr 05 2020 Kalev Lember <klember@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 0.2.2-1
- Initial Fedora packaging
