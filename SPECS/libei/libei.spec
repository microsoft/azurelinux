# Note to packagers:
# libei-the-repo comes with three libraries, all independent of each other and
# processes that use one may not use the other.
# Here there are packaged as libei, libeis and liboeffis plus respective subpackages.
 
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libei
Version:        1.2.1
Release:        2%{?dist}
Summary:        Library for Emulated Input
 
License:        MIT
URL:            http://gitlab.freedesktop.org/libinput/libei
Source0:        https://gitlab.freedesktop.org/libinput/libei/-/archive/%{version}/libei-%{version}.tar.bz2
 
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  libxml2
BuildRequires:  meson
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  python3-attrs
BuildRequires:  python3-jinja2
BuildRequires:  python3-rpm-macros
BuildRequires:  systemd-devel
 
# libei packages
%description
libei is a library to Emulate Input. It allows clients to talk to
an EIS implementatation (Emulated Input Server), typically a Wayland compositor
and send input events via that connection. The EIS implementation
replays those events as if they came from physical devices.
 
%package devel
Summary:        Library for Emulated Input Development Package
Requires:       libei%{?_isa} = %{version}-%{release}
 
%description devel
Library for Emulated Input Development Package.
 
%package utils
Summary:        Library for Emulated Input Utilities Package
Requires:       libei%{?_isa} = %{version}-%{release}
 
%description utils
Utilities to test and/or debug emulated input devices.
 
# libeis packages
%package -n libeis
Summary:        Library for Emulated Input Servers
 
%description -n libeis
libeis is a library to provide logical devices that other applications
can then use to emulate input. This library is typically used by
a Wayland compositor that provides an EIS implementation.
 
%package -n libeis-devel
Summary:        Library for Emulated Input Servers Development Package
Requires:       libeis%{?_isa} = %{version}-%{release}
 
%description -n libeis-devel
Library for Emulated Input Servers Development Package.
 
# liboeffis packages
%package -n liboeffis
Summary:        Library for XDG RemoteDesktop Portal Setup
 
%description -n liboeffis
liboeffis is a helper library to contact the XDG RemoteDesktop portal
and obtain an EIS socket through the portal.
 
%package -n liboeffis-devel
Summary:        Library for XDG RemoteDesktop Portal Setup Development Package
Requires:       liboeffis%{?_isa} = %{version}-%{release}
 
%description -n liboeffis-devel
Library for XDG RemoteDesktop Portal Setup Development Package
 
%prep
%autosetup -S git
# Replace whatever the source uses with the approved call
%py3_shebang_fix $(git grep -l  '#!/usr/bin/.*python3')
 
%build
%meson -Dtests=disabled -Ddocumentation='[]' -Dliboeffis=enabled
%meson_build
%install
%meson_install
%files
%license COPYING
%{_libdir}/libei.so.1{,.*}
 
%files -n libeis
%license COPYING
%{_libdir}/libeis.so.1{,.*}
 
%files -n liboeffis
%license COPYING
%{_libdir}/liboeffis.so.1{,.*}
 
%files devel
%dir %{_includedir}/libei-1.0/
%{_includedir}/libei-1.0/libei.h
%{_libdir}/libei.so
%{_libdir}/pkgconfig/libei-1.0.pc
 
%files -n libeis-devel
%dir %{_includedir}/libei-1.0/
%{_includedir}/libei-1.0/libeis.h
%{_libdir}/libeis.so
%{_libdir}/pkgconfig/libeis-1.0.pc
 
%files -n liboeffis-devel
%dir %{_includedir}/libei-1.0/
%{_includedir}/libei-1.0/liboeffis.h
%{_libdir}/liboeffis.so
%{_libdir}/pkgconfig/liboeffis-1.0.pc
 
%files utils
%{_bindir}/ei-debug-events
 
%changelog
* Mon Jul 15 2024 Hideyuki Nagase <hideyukn@microsoft.com> - 1.2.1-2
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Mon Feb 05 2024 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-1
- libei 1.2.1
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Wed Dec 13 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-2
- Handle OEFFIS_DEVICE_ALL_DEVICES correctly
 
* Wed Dec 06 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-1
- libei 1.2.0
 
* Thu Sep 07 2023 Kalev Lember <klember@redhat.com> - 1.1.0-2
- Rebuild
 
* Thu Sep 07 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.0-1
- libei 1.1.0
 
* Thu Aug 31 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.901-1
- libei 1.0.901
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Thu Jun 08 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.0-1
- libei 1.0.0
 
* Tue May 23 2023 Peter Hutterer <peter.hutterer@redhat.com> - 0.99.2-1
- libei 0.99.2
 
* Wed May 17 2023 Peter Hutterer <peter.hutterer@redhat.com> - 0.99.1-1
- Initial package (#2207838)
Powered by Pagure 5.14.1
Documentation • File an Issue • About this Instance • SSH Hostkey/Fingerprint
© 
