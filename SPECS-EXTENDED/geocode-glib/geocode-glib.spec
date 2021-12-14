Vendor:         Microsoft Corporation
Distribution:   Mariner
%global json_glib_version 0.99.2

Name:           geocode-glib
Version:        3.26.2
Release:        2%{?dist}
Summary:        Geocoding helper library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/%{name}/3.26/%{name}-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(libsoup-2.4)

Requires:       json-glib%{?_isa} >= %{json_glib_version}

%description
geocode-glib is a convenience library for the geocoding (finding longitude,
and latitude from an address) and reverse geocoding (finding an address from
coordinates). It uses Nominatim service to achieve that. It also caches
(reverse-)geocoding requests for faster results and to avoid unnecessary server
load.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%meson -Denable-installed-tests=false
%meson_build


%install
%meson_install


%ldconfig_scriptlets


%files
%license COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/libgeocode-glib.so.*
%{_libdir}/girepository-1.0/GeocodeGlib-1.0.typelib
%{_datadir}/icons/gnome/scalable/places/*.svg

%files devel
%{_includedir}/geocode-glib-1.0/
%{_libdir}/libgeocode-glib.so
%{_libdir}/pkgconfig/geocode-glib-1.0.pc
%{_datadir}/gir-1.0/GeocodeGlib-1.0.gir
%doc %{_datadir}/gtk-doc/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.26.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Mar 09 2020 Bastien Nocera <bnocera@redhat.com> - 3.26.2-1
+ geocode-glib-3.26.2-1
- Update to 3.26.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.26.1-2
- Rebuild with Meson fix for #1699099

* Thu Mar 14 2019 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.25.4.1-2
- Switch to %%ldconfig_scriptlets

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 3.25.4.1-1
- Update to 3.25.4.1
- Switch to the meson build system

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Feb 15 2016 David King <amigadave@amigadave.com> - 3.19.90-1
- Update to 3.19.90
- Use pkgconfig for BuildRequires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 20 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Sun Aug 16 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-2
- Use license macro for COPYING.LIB

* Fri May 01 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 3.15.3.1-1
- Update to 3.15.3.1

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Wed Jun 25 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.2-1
- Update to 3.12.2

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Ship icons in the main package, instead of -devel

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Wed Mar 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92.2-1
- Update to 3.11.92.2

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4.1-1
- Update to 3.11.4.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0
- Specify minimum json-glib version

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.4-1
- Update to 0.99.4

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.3-1
- Update to 0.99.3

* Sat Aug 31 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.2-2
- Move the pkgconfig file to -devel

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.2-1
- Initial Fedora packaging
