# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-atk
Version:        2.38.0
Release: 11%{?dist}
Summary:        MinGW Windows Atk library

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            http://projects.gnome.org/accessibility/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/atk/%{release_version}/atk-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-glib2

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-gettext
BuildRequires:  mingw64-glib2

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig
# Need native one too for msgfmt
BuildRequires:  gettext
# Need native one too for  glib-genmarshal
BuildRequires:  glib2-devel


%description
MinGW Windows Atk library.


# Win32
%package -n mingw32-atk
Summary:        MinGW Windows Atk library
Requires:       pkgconfig

%description -n mingw32-atk
MinGW Windows Atk library.

%package -n mingw32-atk-static
Summary:        Static version of the MinGW Windows Atk library
Requires:       mingw32-atk = %{version}-%{release}

%description -n mingw32-atk-static
Static version of the MinGW Windows Atk library.

# Win64
%package -n mingw64-atk
Summary:        MinGW Windows Atk library
Requires:       pkgconfig

%description -n mingw64-atk
MinGW Windows Atk library.

%package -n mingw64-atk-static
Summary:        Static version of the MinGW Windows Atk library
Requires:       mingw64-atk = %{version}-%{release}

%description -n mingw64-atk-static
Static version of the MinGW Windows Atk library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n atk-%{version}


%build
%mingw_meson --default-library=both -Dintrospection=false
%mingw_ninja


%install
%mingw_ninja_install

%mingw_find_lang atk10


# Win32
%files -n mingw32-atk -f mingw32-atk10.lang
%license COPYING
%{mingw32_bindir}/libatk-1.0-0.dll
%{mingw32_includedir}/atk-1.0
%{mingw32_libdir}/libatk-1.0.dll.a
%{mingw32_libdir}/pkgconfig/atk.pc

%files -n mingw32-atk-static
%{mingw32_libdir}/libatk-1.0.a

# Win64
%files -n mingw64-atk -f mingw64-atk10.lang
%license COPYING
%{mingw64_bindir}/libatk-1.0-0.dll
%{mingw64_includedir}/atk-1.0
%{mingw64_libdir}/libatk-1.0.dll.a
%{mingw64_libdir}/pkgconfig/atk.pc

%files -n mingw64-atk-static
%{mingw64_libdir}/libatk-1.0.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.38.0-8
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.36.0-9
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 13:44:01 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.36.0-5
- Rebuild (mingw-gettext)

* Wed Aug 12 13:31:51 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.36.0-4
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 2.36.0-2
- Rebuild (gettext)

* Thu Apr 02 2020 Sandro Mani <manisandro@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Sat Mar 28 2020 Sandro Mani <manisandro@gmail.com> - 2.35.1-1
- Update to 2.35.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.34.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 2.34.1-1
- Update to 2.34.1

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 2.33.3-1
- Update to 2.33.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Kalev Lember <klember@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.22.0-1
- Update to 2.22.0
- Don't set group tags

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 2.18.0-2
- Use global instead of define.

* Fri Sep 25 2015 Kalev Lember <klember@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.16.0-1
- Update to 2.16.0
- Use license macro for the COPYING file

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.15.3-1
- Update to 2.15.3

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.0-1
- Update to 2.14.0

* Sun Sep 21 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.13.90-1
- Update to 2.13.90

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 2.12.0-1
- Update to 2.12.0

* Thu Dec  5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.11.3-1
- Update to 2.11.3
- Export the symbol atk_object_get_object_locale (required by webkitgtk)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.11.2-1
- Update to 2.11.2

* Tue Sep 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.10.0-1
- Update to 2.10.0

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.9.4-1
- Update to 2.9.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.9.3-1
- Update to 2.9.3

* Tue Mar 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.7.91-1
- Update to 2.7.91

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct  5 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Sat Aug 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.5.4-1
- Update to 2.5.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.0-1
- Update to 2.4.0
- Don't run autoreconf, the 64 bit builds work fine without it

* Sun Mar 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.3.93-2
- Added win64 support

* Thu Mar  8 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.3.93-1
- Update to 2.3.93
- Dropped .la files

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.2.0-4
- Renamed the source package to mingw-atk (RHBZ #800371)

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.2.0-3
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Kalev Lember <kalevlember@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Tue Aug 30 2011 Kalev Lember <kalevlember@gmail.com> - 2.1.5-1
- Update to 2.1.5

* Sun Jul 10 2011 Kalev Lember <kalevlember@gmail.com> - 2.0.1-1
- Update to 2.0.1
- Switched to xz compressed tarballs
- Use automatic mingw dep extraction
- Cleaned up the spec file for modern rpmbuild
- Dropped upstreamed AtkHyperlinkImpl patch

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 1.32.0-6
- Rebuilt against win-iconv

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.32.0-5
- Dropped the proxy-libintl pieces

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.32.0-3
- Export the AtkHyperlinkImpl functions (required for webkitgtk)

* Sun Nov  7 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.32.0-2
- Rebuild in order to have soft dependency on libintl

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.32.0-1
- Update to 1.32.0
- Drop upstreamed patch

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.30.0-2
- Export the function atk_value_get_minimum_increment (required by GTK 2.21.7)

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.30.0-1
- Update to 1.30.0

* Wed Dec  2 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.29.3-1
- Update to 1.29.3

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.27.90-1
- Update to 1.27.90
- Automatically generate debuginfo subpackage

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.26.0-1
- Update to 1.26.0
- Use %%global instead of %%define

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Erik van Pienbroek <info@nntpgrab.nl> - 1.25.2-7
- Added -static subpackage
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-5
- Include license file.

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-4
- Remove gtk-doc.
- Fix defattr line.
- Requires pkgconfig.
- Remove the atk*.def file.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-1
- Rebase to latest Fedora native version 1.25.2.
- Use find_lang macro.
- Use smp_mflags.
- Fix URL.
- Fix Source URL.

* Wed Sep 24 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-1
- Update to 1.24.0 release

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-2
- Added dep on pkgconfig and glib2-devel (native)

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-1
- Initial RPM release
