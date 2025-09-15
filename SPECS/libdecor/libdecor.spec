Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libdecor
Version:        0.2.2
Release:        4%{?dist}
Summary:        Wayland client side decoration library
 
License:        MIT
URL:            https://gitlab.freedesktop.org/libdecor/libdecor
Source:         %{url}/-/releases/%{version}/downloads/libdecor-%{version}.tar.xz
 
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  gtk3
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(gtk+-3.0)
 
%description
Libdecor provides a small helper library for providing client side decoration
to Wayland clients.
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
 
 
%prep
%autosetup -p1
 
 
%build
%meson -Ddemo=false
%meson_build
 
%install
%meson_install
 
%files
%license LICENSE
%doc README.md
%{_libdir}/libdecor-0.so.0*
%dir %{_libdir}/libdecor/
%dir %{_libdir}/libdecor/plugins-1
%{_libdir}/libdecor/plugins-1/libdecor-cairo.so
%{_libdir}/libdecor/plugins-1/libdecor-gtk.so
 
%files devel
%{_includedir}/libdecor-0/
%{_libdir}/libdecor-0.so
%{_libdir}/pkgconfig/libdecor-0.pc
 
 
%changelog
* Mon Jul 15 2024 Hideyuki Nagase <hideyukn@microsoft.com> - 0.2.2-4
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Mon Jan 15 2024 Jonas Ådahl <jadahl@redhat.com> - 0.2.2-1
- Bump version to 0.2.2
 
* Wed Dec 06 2023 Jonas Ådahl <jadahl@redhat.com> - 0.2.1-2
- Fix crash when hiding/showing
 
* Fri Dec 01 2023 Jonas Ådahl <jadahl@redhat.com> - 0.2.1-1
- Bump version to 0.2.1
 
* Mon Sep 25 2023 Jonas Ådahl <jadahl@redhat.com> - 0.2.0-1
- Bump version to 0.2.0
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Mon Oct 31 2022 Jonas Ådahl <jadahl@redhat.com> - 0.1.1-1
- Bump version to 0.1.1
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Fri Jul 23 2021 Jonas Ådahl <jadahl@redhat.com> - 0.1.0-1
- Initial Fedora packaging
Powered by Pagure 5.14.1
Documentation • File an Issue • About this Instance • SSH Hostkey/Fingerprint

