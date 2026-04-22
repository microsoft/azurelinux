# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libqrtr-glib
Version: 1.2.2
Release: 9%{?dist}
Summary: Support library to use and manage the QRTR (Qualcomm IPC Router) bus.
License: LGPL-2.1-or-later
URL: https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib
Source: https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires: meson >= 0.53
BuildRequires: gcc
BuildRequires: glib2-devel >= 2.56
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: pkgconfig(gudev-1.0) >= 147
BuildRequires: python3

%description
This package contains the libraries that make it easier to use and
manage the QRTR (Qualcomm IPC Router) bus.


%package devel
Summary: Header files for adding QRTR support to applications that use glib
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description devel
This package contains the header and pkg-config files for development
applications using QRTR functionality from applications that use glib.


%prep
%autosetup -p1


%build
%meson
%meson_build


%install
%meson_install
find %{buildroot}%{_datadir}/gtk-doc |xargs touch --reference meson.build


%check
%meson_test


%ldconfig_scriptlets


%files
%license LICENSES/LGPL-2.1-or-later.txt
%doc NEWS AUTHORS README.md
%{_libdir}/libqrtr-glib.so.*
%{_libdir}/girepository-1.0/Qrtr-1.0.typelib


%files devel
%{_includedir}/libqrtr-glib/
%{_libdir}/libqrtr-glib.so
%{_libdir}/pkgconfig/qrtr-glib.pc
%{_datadir}/gtk-doc/html/libqrtr-glib/
%{_datadir}/gir-1.0/Qrtr-1.0.gir


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.2.2-1
- Update to 1.2.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 13 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-1
- Initial package
