# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libgudev
Version:        238
Release: 9%{?dist}
Summary:        GObject-based wrapper library for libudev

License:        LGPL-2.1-or-later
URL:            https://wiki.gnome.org/Projects/libgudev
Source0:        https://download.gnome.org/sources/libgudev/%{version}/libgudev-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  pkgconfig
BuildRequires:  libudev-devel
BuildRequires:  gtk-doc
BuildRequires:  meson
# For tests
BuildRequires:  umockdev-devel
BuildRequires:  glibc-langpack-fr

# Upstream promises to remove libgudev from systemd before this version
Provides:       libgudev1 = %{version}-%{release}
Obsoletes:      libgudev1 < 230

%description
This library makes it much simpler to use libudev from programs
already using GObject. It also makes it possible to easily use libudev
from other programming languages, such as Javascript, because of
GObject introspection support.

%package devel
Summary:   Header files for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}

Provides:       libgudev1-devel = %{version}-%{release}
Obsoletes:      libgudev1-devel < 230

%description devel
This package is necessary to build programs using %{name}.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=true -Dtests=enabled -Dvapi=disabled
%meson_build

%install
%meson_install

%check
%meson_test

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libgudev-1.0.so.*
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files devel
%{_libdir}/libgudev-1.0.so
%dir %{_includedir}/gudev-1.0
%dir %{_includedir}/gudev-1.0/gudev
%{_includedir}/gudev-1.0/gudev/*.h
%{_datadir}/gir-1.0/GUdev-1.0.gir
%dir %{_datadir}/gtk-doc/html/gudev
%{_datadir}/gtk-doc/html/gudev/*
%{_libdir}/pkgconfig/gudev-1.0*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 238-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 238-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 238-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 238-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 238-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Lukáš Zaoral <lzaoral@redhat.com> - 238-3
- migrate to SPDX license format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 238-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Bastien Nocera <bnocera@redhat.com> - 238-1
- Update to 238

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 237-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 237-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 237-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 14 2021 Bastien Nocera <bnocera@redhat.com> - 237-1
+ libgudev-237-1
- Update to 237

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 236-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 16 2021 Bastien Nocera <bnocera@redhat.com> - 236-1
+ libgudev-236-1
- Update to 236

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 234-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Bastien Nocera <bnocera@redhat.com> - 234-1
+ libgudev-234-1
- Update to 234

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 232-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 232-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 232-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 232-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 232-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 24 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-3
- Pull in patch from upstream to fix build

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 232-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 232-2
- Switch to %%ldconfig_scriptlets

* Fri Sep 01 2017 Kalev Lember <klember@redhat.com> - 232-1
- Update to 232
- Enable self tests

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 230-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 230-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 230-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 230-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 230-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-1
- Initial packaging
