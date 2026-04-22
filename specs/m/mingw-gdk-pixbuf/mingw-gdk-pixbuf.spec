# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-gdk-pixbuf
Version:        2.44.5
Release: 2%{?dist}
Summary:        MinGW Windows GDK Pixbuf library

License:        LGPL-2.0-or-later
URL:            http://www.gtk.org
Source0:        http://download.gnome.org/sources/gdk-pixbuf/%{release_version}/gdk-pixbuf-%{version}.tar.xz

# If you want to rebuild this, do:
# wine /usr/i686-w64-mingw32/sys-root/mingw/bin/gdk-pixbuf-query-loaders.exe | sed s@'Z:/usr/i686-w64-mingw32/sys-root/mingw'@'..'@ > gdk-pixbuf.loaders
Source1:        gdk-pixbuf.loaders

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils

BuildRequires:  mingw32-glib2
BuildRequires:  mingw64-glib2
BuildRequires:  mingw32-libjpeg
BuildRequires:  mingw64-libjpeg
BuildRequires:  mingw32-libpng
BuildRequires:  mingw64-libpng
BuildRequires:  mingw32-libtiff
BuildRequires:  mingw64-libtiff

BuildRequires:  gettext
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkg-config
# For glib-compile-resources
BuildRequires:  glib2-devel

%description
MinGW Windows GDK Pixbuf library.


%package -n mingw32-gdk-pixbuf
Summary:        MinGW Windows GDK Pixbuf library

%description -n mingw32-gdk-pixbuf
MinGW Windows GDK Pixbuf library.


%package -n mingw64-gdk-pixbuf
Summary:        MinGW Windows GDK Pixbuf library

%description -n mingw64-gdk-pixbuf
MinGW Windows GDK Pixbuf library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n gdk-pixbuf-%{version}


%build
%mingw_meson \
  -Drelocatable=true \
  -Dbuiltin_loaders=bmp,gif,ico,jpeg,tiff,png \
  -Dman=false \
  -Ddocumentation=false \
  -Dothers=enabled

# Copy the loaders.cache file to the source tree
install -m 0644 %{SOURCE1} build_win32/gdk-pixbuf/loaders.cache
install -m 0644 %{SOURCE1} build_win64/gdk-pixbuf/loaders.cache

%mingw_ninja


%install
%mingw_ninja_install

# The .dll.a files are import libraries, but as the regular .dll's are
# only dlopen'ed by GTK they provide no additional value so they can be dropped
rm -f %{buildroot}%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.dll.a
rm -f %{buildroot}%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.dll.a

# Install the loaders.cache file
install -m 0644 %{SOURCE1} %{buildroot}%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
install -m 0644 %{SOURCE1} %{buildroot}%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

%mingw_find_lang %{name} --all-name


%files -n mingw32-gdk-pixbuf -f mingw32-%{name}.lang
%license COPYING
%{mingw32_bindir}/gdk-pixbuf-csource.exe
%{mingw32_bindir}/gdk-pixbuf-pixdata.exe
%{mingw32_bindir}/gdk-pixbuf-query-loaders.exe
%{mingw32_bindir}/libgdk_pixbuf-2.0-0.dll
%dir %{mingw32_libdir}/gdk-pixbuf-2.0
%dir %{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-ani.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-icns.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-pnm.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-qtif.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-tga.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xbm.dll
%{mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xpm.dll
%{mingw32_libdir}/libgdk_pixbuf-2.0.dll.a
%{mingw32_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{mingw32_includedir}/gdk-pixbuf-2.0/

%files -n mingw64-gdk-pixbuf -f mingw64-%{name}.lang
%license COPYING
%{mingw64_bindir}/gdk-pixbuf-csource.exe
%{mingw64_bindir}/gdk-pixbuf-pixdata.exe
%{mingw64_bindir}/gdk-pixbuf-query-loaders.exe
%{mingw64_bindir}/libgdk_pixbuf-2.0-0.dll
%dir %{mingw64_libdir}/gdk-pixbuf-2.0
%dir %{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-ani.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-icns.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-pnm.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-qtif.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-tga.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xbm.dll
%{mingw64_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xpm.dll
%{mingw64_libdir}/libgdk_pixbuf-2.0.dll.a
%{mingw64_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{mingw64_includedir}/gdk-pixbuf-2.0/


%changelog
* Wed Feb 11 2026 Sandro Mani <manisandro@gmail.com> - 2.44.5-1
- Update to 2.44.5

* Tue Jan 20 2026 Richard W.M. Jones <rjones@redhat.com> - 2.44.4-4
- Fix paths and remove JPEG 2000 in loaders.cache (RHBZ#2431201)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 08 2025 Sandro Mani <manisandro@gmail.com> - 2.44.4-2
- Rebuild (libtiff)

* Fri Oct 24 2025 Sandro Mani <manisandro@gmail.com> - 2.44.4-1
- Update to 2.44.4

* Fri Oct 03 2025 Sandro Mani <manisandro@gmail.com> - 2.44.3-1
- Update to 2.44.3

* Sat Sep 27 2025 Sandro Mani <manisandro@gmail.com> - 2.44.2-1
- Update to 2.44.2

* Tue Sep 16 2025 Sandro Mani <manisandro@gmail.com> - 2.44.1-1
- Update to 2.44.1

* Sun Sep 14 2025 Sandro Mani <manisandro@gmail.com> - 2.44.0-1
- Update to 2.44.0

* Mon Sep 08 2025 Sandro Mani <manisandro@gmail.com> - 2.43.5-1
- Update to 2.43.5

* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 2.43.3-1
- Update to 2.43.3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 2.42.12-5
- Backport fix for CVE-2025-7345

* Tue Jun 24 2025 Sandro Mani <manisandro@gmail.com> - 2.42.12-4
- Backport fix for CVE-2025-6199

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 28 2024 Sandro Mani <manisandro@gmail.com> - 2.42.12-1
- Update to 2.42.12

* Sun Apr 21 2024 Sandro Mani <manisandro@gmail.com> - 2.42.11-1
- Update to 2.42.11

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 2.42.10-1
- Update to 2.42.10

* Tue Aug 16 2022 Sandro Mani <manisandro@gmail.com> - 2.42.9-1
- Update to 2.42.9

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 2.42.8-1
- Update to 2.42.8

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.42.6-5
- Rebuild with mingw-gcc-12

* Thu Feb 03 2022 Sandro Mani <manisandro@gmail.com> - 2.42.6-4
- Backport patch for CVE-2021-44648

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 10 2021 Sandro Mani <manisandro@gmail.com> - 2.42.6-1
- Update to 2.42.6

* Thu Mar 25 2021 Sandro Mani <manisandro@gmail.com> - 2.42.4-1
- Update to 2.42.4

* Sat Mar 06 2021 Sandro Mani <manisandro@gmail.com> - 2.42.2-1
- Update to 2.42.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 13:36:42 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.40.0-4
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 2.40.0-2
- Rebuild (gettext)

* Wed Jan 29 2020 Sandro Mani <manisandro@gmail.com> - 2.40.0-1
- Update to 2.40.0

* Tue Jan 28 2020 Kalev Lember <klember@redhat.com> - 2.36.12-1
- Update to 2.36.12

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.36.11-6
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.36.11-1
- Update to 2.36.11

* Mon Aug 21 2017 Kalev Lember <klember@redhat.com> - 2.36.9-1
- Update to 2.36.9

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 2.36.8-1
- Update to 2.36.8

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 2.36.7-1
- Update to 2.36.7

* Mon Jun 19 2017 Kalev Lember <klember@redhat.com> - 2.36.6-1
- Update to 2.36.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> - 2.36.0-2
- Rebuilt for mingw-jasper update

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0
- Don't set group tags

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 2.32.3-2
- Use global instead of define.

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 2.32.3-1
- Update to 2.32.3

* Wed Nov 18 2015 Kalev Lember <klember@redhat.com> - 2.32.2-1
- Update to 2.32.2

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Fri Sep 25 2015 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Kalev Lember <kalevlember@gmail.com> - 2.31.3-1
- Update to 2.31.3
- Use license macro for the COPYING file

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.31.1-1
- Update to 2.31.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.30.8-1
- Update to 2.30.8

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 2.30.7-1
- Update to 2.30.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.2-3
- Rebuild against libpng 1.6

* Sun Jun 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.2-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Sun Jun 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.28.2-1
- Update to 2.28.2

* Tue Mar 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.0-1
- Update to 2.28.0

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.3-1
- Update to 2.27.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.4-1
- Update to 2.26.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.0-1
- Update to 2.26.0

* Wed Mar 14 2012 Kalev Lember <kalevlember@gmail.com> - 2.25.2-5
- Build 64 bit Windows binaries

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.2-4
- Renamed the source package to mingw-gdk-pixbuf (RHBZ #800383)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.2-3
- Rebuild against the mingw-w64 toolchain

* Sun Feb 19 2012 Kalev Lember <kalevlember@gmail.com> - 2.25.2-2
- Include all GDI+ loaders in the main DLL (#795152)
- Also include the PNG loader, for consistency with native gdk-pixbuf2 package

* Wed Feb 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.25.2-1
- Update to 2.25.2
- Dropped upstreamed patches

* Tue Jan 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.0-1
- Update to 2.25.0
- Rebuild against libpng 1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 27 2011 Kalev Lember <kalevlember@gmail.com> - 2.24.0-1
- Update to 2.24.0

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.5-1
- Update to 2.23.5
- Rebuild against win-iconv

* Fri Jun  3 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.3-2
- Rebuild for libjpeg-turbo

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.3-1
- Update to 2.23.3
- Dropped the configure argument --enable-gdiplus as it's enabled by default
- Dropped upstreamed patch
- Dropped the proxy-libintl pieces

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.0-2
- Rebuild in order to have soft dependency on libintl
- Bump the BR: mingw32-filesystem to >= 61 because of mingw32(gdiplus.dll) provides

* Thu Sep 23 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Mon Sep 20 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.7-2
- Fixed a bug which caused the path /usr/i686-pc-mingw32/sys-root/mingw to get hardcoded
  in the resulting library resulting in runtime failures on Win32 environments
- Moved the file %%{_mingw32_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders to
  %%{_mingw32_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.7-1
- Initial release (split off from the mingw32-gtk2 package)
- Dropped the -static subpackage as it provides no added value
- Dropped all the .dll.a and .la files from the loaders as they provide no added value
- Dropped the libpng 1.4 hack as upstream has provided a proper fix

