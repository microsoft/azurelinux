# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global api_version 0.3

Name:           libcloudproviders
Summary:        Library for integration of cloud storage providers
Version:        0.3.6
Release:        2%{?dist}
License:        LGPL-3.0-or-later

URL:            https://gitlab.gnome.org/World/libcloudproviders
Source0:        https://ftp.gnome.org/pub/GNOME/sources/libcloudproviders/%{api_version}/libcloudproviders-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  vala

BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

%description
Cross desktop library for desktop integration of cloud storage providers
and sync tools.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%meson -Denable-gtk-doc=true
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc CHANGELOG README.md
%{_libdir}/libcloudproviders.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/CloudProviders-%{api_version}.typelib

%files devel
%{_includedir}/cloudproviders/
%{_libdir}/pkgconfig/cloudproviders.pc
%{_libdir}/libcloudproviders.so
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/CloudProviders-%{api_version}.gir
%{_datadir}/gtk-doc/
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/cloudproviders.*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 06 2025 Cole Robinson <crobinso@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Miroslav Suchý <msuchy@redhat.com> - 0.3.5-4
- convert license to SPDX

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 08 2023 Kalev Lember <klember@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Thu Sep 07 2023 Kalev Lember <klember@redhat.com> - 0.3.4-1
- Update to 0.3.4
- Fix directory ownership for gir and vapi directories

* Wed Aug 09 2023 Kalev Lember <klember@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Fabio Valentini <decathorpe@gmail.com> - 0.3.1-1
- Update to version 0.3.1.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Fabio Valentini <decathorpe@gmail.com> - 0.3.0-1
- Update to version 0.3.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Carlos Soriano <csoriano@redhat.com> - 0.2.5-0.1
- Initial RPM release

