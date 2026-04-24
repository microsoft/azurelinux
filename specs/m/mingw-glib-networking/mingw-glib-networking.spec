# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-glib-networking
Version:        2.80.1
Release: 5%{?dist}
Summary:        MinGW Windows glib-networking library

License:        LGPL-2.1-or-later
URL:            http://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glib-networking/%{release_version}/glib-networking-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  intltool
BuildRequires:  meson
BuildRequires:  pkgconfig

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-gnutls >= 2.10
BuildRequires:  mingw32-gsettings-desktop-schemas

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-glib2
BuildRequires:  mingw64-gnutls >= 2.10
BuildRequires:  mingw64-gsettings-desktop-schemas


%description
This package contains modules that extend the networking support in GIO.


%package -n mingw32-glib-networking
Summary:        MinGW Windows glib-networking library
Requires:       mingw32-gsettings-desktop-schemas

%description -n mingw32-glib-networking
This package contains modules that extend the networking support in GIO.


%package -n mingw64-glib-networking
Summary:        MinGW Windows glib-networking library
Requires:       mingw64-gsettings-desktop-schemas

%description -n mingw64-glib-networking
This package contains modules that extend the networking support in GIO.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n glib-networking-%{version}


%build
%mingw_meson -Dlibproxy=disabled -Denvironment_proxy=enabled
%mingw_ninja


%install
%mingw_ninja_install

rm -f %{buildroot}%{mingw32_libdir}/gio/modules/*.dll.a
rm -f %{buildroot}%{mingw64_libdir}/gio/modules/*.dll.a
rm -f %{buildroot}%{mingw32_libdir}/gio/modules/*.la
rm -f %{buildroot}%{mingw64_libdir}/gio/modules/*.la

%mingw_find_lang glib-networking


%files -n mingw32-glib-networking -f mingw32-glib-networking.lang
%license COPYING
%{mingw32_libdir}/gio/modules/libgiognutls.dll
%{mingw32_libdir}/gio/modules/libgioenvironmentproxy.dll
%{mingw32_libdir}/gio/modules/libgiognomeproxy.dll

%files -n mingw64-glib-networking -f mingw64-glib-networking.lang
%license COPYING
%{mingw64_libdir}/gio/modules/libgiognutls.dll
%{mingw64_libdir}/gio/modules/libgioenvironmentproxy.dll
%{mingw64_libdir}/gio/modules/libgiognomeproxy.dll


%changelog
* Thu Jan 22 2026 Sandro Mani <manisandro@gmail.com> - 2.80.1-4
- Add Requires: mingw32-gsettings-desktop-schemas (#2431589)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 25 2025 Sandro Mani <manisandro@gmail.com> - 2.80.1-1
- Update to 2.80.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Mar 23 2024 Sandro Mani <manisandro@gmail.com> - 2.80.0-1
- Update to 2.80.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.78.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Sandro Mani <manisandro@gmail.com> - 2.78.0-1
- Update to 2.78.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.76.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Sandro Mani <manisandro@gmail.com> - 2.76.1-1
- Update to 2.76.1

* Sun Mar 19 2023 Sandro Mani <manisandro@gmail.com> - 2.76.0-1
- Update to 2.76.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 21 2022 Sandro Mani <manisandro@gmail.com> - 2.74.0-1
- Update to 2.74.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Sandro Mani <manisandro@gmail.com> - 2.72.1-1
- Update to 2.72.1

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 2.72.0-1
- Update to 2.72.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.70.1-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.70.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Sandro Mani <manisandro@gmail.com> - 2.70.1-1
- Update to 2.70.1

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 2.70.0-1
- Update to 2.70.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.68.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Sandro Mani <manisandro@gmail.com> - 2.68.1-1
- Update to 2.68.1

* Fri Apr 16 2021 Sandro Mani <manisandro@gmail.com> - 2.68.0-1
- Update to 2.68.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Sandro Mani <manisandro@gmail.com> - 2.66.0-1
- Update to 2.66.0

* Wed Aug 12 13:37:20 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.64.3-3
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 31 2020 Sandro Mani <manisandro@gmail.com> - 2.64.3-1
- Update to 2.64.3

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 2.64.2-2
- Rebuild (gettext)

* Thu Apr 16 2020 Sandro Mani <manisandro@gmail.com> - 2.64.2-1
- Update to 2.64.2

* Sat Mar 28 2020 Sandro Mani <manisandro@gmail.com> - 2.64.1-1
- Update to 2.64.1

* Fri Mar 06 2020 Sandro Mani <manisandro@gmail.com> - 2.64.0-1
- Update to 2.64.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.62.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Sandro Mani <manisandro@gmail.com> - 2.62.3-1
- Update to 2.62.3

* Tue Dec 10 2019 Sandro Mani <manisandro@gmail.com> - 2.62.2-1
- Update to 2.62.2

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.62.1-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.62.1-1
- Update to 2.62.1

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 2.62.0-1
- Update to 2.62.0

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 2.61.2-1
- Update to 2.61.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.57.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.57.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 28 2018 Christophe Fergeau <cfergeau@redhat.com> - 2.57.90-1
- Sync with native rawhide package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.54.0-1
- Update to 2.54.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0
- Don't set group tags

* Mon May 09 2016 Kalev Lember <klember@redhat.com> - 2.48.2-1
- Update to 2.48.2

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.46.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 16 2015 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Fri Sep 25 2015 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Sun Aug 23 2015 Kalev Lember <klember@redhat.com> - 2.45.1-1
- Update to 2.45.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-2
- Rebuilt for mingw-gnutls 3.4 ABI change

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0
- Use license macro for the COPYING file

* Fri Oct 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.38.2-1
- Update to 2.38.2

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.5-1
- Update to 2.37.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.4-1
- Update to 2.37.4

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.1-1
- Update to 2.37.1

* Fri Mar 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.36.0-1
- Update to 2.36.0

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.9-1
- Update to 2.35.9

* Fri Feb  8 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.6-1
- Update to 2.35.6

* Wed Nov 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.2-1
- Update to 2.34.2

* Sat Oct 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.0-1
- Update to 2.34.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.1-1
- Update to 2.32.1

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.0-1
- Update to 2.32.0
- Dropped upstreamed patch

* Fri Mar 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.16-3
- Build 64 bit Windows binaries

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.16-2
- Renamed the source package to mingw-glib-networking (RHBZ #800391)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.16-1
- Update to 2.31.16
- Patch to fix linking against pkcs11-enabled gnutls

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.6-1
- Update to 2.31.6
- Dropped upstreamed patch
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Kalev Lember <kalevlember@gmail.com> - 2.30.1-1
- Update to 2.30.1
- Added a patch to fix build without gnome-proxy

* Sun Oct 02 2011 Kalev Lember <kalevlember@gmail.com> - 2.30.0-1
- Update to 2.30.0
- Use automatic mingw dep extraction
- Switch to .xz tarballs

* Thu Apr 28 2011 Kalev Lember <kalev@smartlink.ee> - 2.28.6.1-2
- Dropped Requires: pkgconfig (#700348)

* Wed Apr 27 2011 Kalev Lember <kalev@smartlink.ee> - 2.28.6.1-1
- Initial RPM release
