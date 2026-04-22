# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:		mingw-libsoup
Version:	2.74.3
Release: 18%{?dist}
Summary:	MinGW library for HTTP and XML-RPC functionality

License:	LGPL-2.0-only
URL:		https://wiki.gnome.org/Projects/libsoup
Source0:	https://download.gnome.org/sources/libsoup/%{release_version}/libsoup-%{version}.tar.xz
# Fix initialization from incompatible pointer type
Patch0:         libsoup-incompat-pointer-type.patch
# Backport fix for CVE-2024-52532
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/6adc0e3eb74c257ed4e2a23eb4b2774fdb0d67be
Patch1:         CVE-2024-52532.patch
# Backport fix for CVE-2024-52530
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/04df03bc092ac20607f3e150936624d4f536e68b
Patch2:         CVE-2024-52530.patch
# Backport fix for CVE-2025-32050
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/9bb0a55de55c6940ced811a64fbca82fe93a9323
Patch3:         CVE-2025-32050.patch
# Backport fix for CVE-2025-32052
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/f182429e5b1fc034050510da20c93256c4fa9652
Patch4:         CVE-2025-32052.patch
# Backport fix for CVE-2025-32053
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/eaed42ca8d40cd9ab63764e3d63641180505f40a
Patch5:         CVE-2025-32053.patch
# Backport fix for CVE-2025-32906
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/af5b9a4a3945c52b940d5ac181ef51bb12011f1f
Patch6:         CVE-2025-32906.patch
# Backport fix for CVE-2025-32907
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/452
Patch7:         CVE-2025-32907.patch
# Backport fix for CVE-2025-32909
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/ba4c3a6f988beff59e45801ab36067293d24ce92
Patch8:         CVE-2025-32909.patch
# Backport fix for CVE-2025-32910
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/ea16eeacb052e423eb5c3b0b705e5eab34b13832
Patch9:         CVE-2025-32910.patch
# Backport fix for CVE-2025-32911 + CVE-2025-32913
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/f4a761fb66512fff59798765e8ac5b9e57dceef0
Patch10:         CVE-2025-32911.patch
# Backport fix for CVE-2025-4476
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/e64c221f9c7d09b48b610c5626b3b8c400f0907c
Patch11:         CVE-2025-4476.patch
# Backport fix for CVE-2025-4948
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/f2f28afe0b3b2b3009ab67d6874457ec6bac70c0
Patch12:         CVE-2025-4948.patch
# Backport fix for CVE-2025-4969
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/b5b4dd10d4810f0c87b4eaffe88504f06e502f33
Patch13:         CVE-2025-4969.patch
# Backport fix for CVE-2025-46420
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/c9083869ec2a3037e6df4bd86b45c419ba295f8e
Patch14:         CVE-2025-46420.patch
# Backport fix for CVE-2025-46421
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/3e5c26415811f19e7737238bb23305ffaf96f66b
Patch15:         CVE-2025-46421.patch
# Backport proposed fix for CVE-2025-4945
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/462
Patch16:         CVE-2025-4945.patch
# Backport fix for CVE-2025-11021
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/9e1a427d2f047439d0320defe1593e6352595788
Patch17:         CVE-2025-11021.patch
# Backport patch for CVE-2025-14523
# https://gitlab.gnome.org/GNOME/libsoup/-/commit/2137d6f75a32a6facb2ffc2062f11a8d9748e0c2
Patch18:        CVE-2025-14523.patch
# Backport fix for CVE-2026-0716
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/494
Patch19:        CVE-2026-0716.patch
# Backport fix for CVE-2026-0719
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/493
Patch20:        CVE-2026-0719.patch

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  meson

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-brotli
BuildRequires:  mingw32-libpsl
BuildRequires:  mingw32-sqlite

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-glib2
BuildRequires:  mingw64-libxml2
BuildRequires:  mingw64-brotli
BuildRequires:  mingw64-libpsl
BuildRequires:  mingw64-sqlite

# For glib-genmarshal
BuildRequires: glib2-devel
BuildRequires: intltool

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

This is the MinGW build of Libsoup


# Win32
%package -n mingw32-libsoup
Summary:	MinGW library for HTTP and XML-RPC functionality
Requires:       pkgconfig
Requires:       mingw32-glib-networking
# Dropped in F25
Obsoletes:      mingw32-libsoup-static < 2.54.1

%description -n mingw32-libsoup
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

This is the MinGW build of Libsoup

# Win64
%package -n mingw64-libsoup
Summary:        MinGW library for HTTP and XML-RPC functionality
Requires:       pkgconfig
Requires:       mingw64-glib-networking
# Dropped in F25
Obsoletes:      mingw64-libsoup-static < 2.54.1

%description -n mingw64-libsoup
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

This is the MinGW build of Libsoup


%{?mingw_debug_package}


%prep
%autosetup -p1 -n libsoup-%{version}

%build
%mingw_meson \
    -Dgtk_doc=false \
    -Dgssapi=disabled \
    -Dintrospection=disabled \
    -Dtests=false \
    -Dtls_check=false \
    -Dvapi=disabled
%mingw_ninja

%install
%mingw_ninja_install

# Remove the .la files
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la

%mingw_find_lang libsoup

# Win32
%files -n mingw32-libsoup -f mingw32-libsoup.lang
%license COPYING
%{mingw32_bindir}/libsoup-2.4-1.dll
%{mingw32_bindir}/libsoup-gnome-2.4-1.dll
%{mingw32_includedir}/libsoup-2.4
%{mingw32_includedir}/libsoup-gnome-2.4
%{mingw32_libdir}/libsoup-2.4.dll.a
%{mingw32_libdir}/libsoup-gnome-2.4.dll.a
%{mingw32_libdir}/pkgconfig/libsoup-2.4.pc
%{mingw32_libdir}/pkgconfig/libsoup-gnome-2.4.pc

# Win64
%files -n mingw64-libsoup -f mingw64-libsoup.lang
%license COPYING
%{mingw64_bindir}/libsoup-2.4-1.dll
%{mingw64_bindir}/libsoup-gnome-2.4-1.dll
%{mingw64_includedir}/libsoup-2.4
%{mingw64_includedir}/libsoup-gnome-2.4
%{mingw64_libdir}/libsoup-2.4.dll.a
%{mingw64_libdir}/libsoup-gnome-2.4.dll.a
%{mingw64_libdir}/pkgconfig/libsoup-2.4.pc
%{mingw64_libdir}/pkgconfig/libsoup-gnome-2.4.pc

%changelog
* Sat Feb 07 2026 Sandro Mani <manisandro@gmail.com> - 2.74.3-17
- Backport fixes for CVE-2026-0716 and CVE-2026-0719

* Sat Jan 17 2026 Sandro Mani <manisandro@gmail.com> - 2.74.3-16
- Backport patch for CVE-2025-14523

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Dec 14 2025 Sandro Mani <manisandro@gmail.com> - 2.74.3-14
- Backport fix for CVE-2025-11021

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 30 2025 Sandro Mani <manisandro@gmail.com> - 2.74.3-12
- Backport fixes for CVE-2025-4476, CVE-2025-4948, CVE-2025-4969,
  CVE-2025-46420, CVE-2025-46421, CVE-2025-4945

* Wed Apr 16 2025 Sandro Mani <manisandro@gmail.com> - 2.74.3-11
- Backport fixes for CVE-2025-32910, CVE-2025-32911, CVE-2025-32913

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 2.74.3-10
- Backport fixes for CVE-2025-32050 CVE-2025-32052 CVE-2025-32053 CVE-2025-32906
  CVE-2025-32907 CVE-2025-32909

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Sandro Mani <manisandro@gmail.com> - 2.74.3-8
- Backport fix for CVE-2024-52530 and CVE-2024-52532

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.74.3-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 2.74.3-1
- Update to 2.74.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Sandro Mani <manisandro@gmail.com> - 2.74.2-1
- Update to 2.74.2

* Thu Oct 28 2021 Sandro Mani <manisandro@gmail.com> - 2.74.1-1
- Update to 2.74.1

* Fri Sep 10 2021 Sandro Mani <manisandro@gmail.com> - 2.74.0-1
- Update to 2.74.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Sandro Mani <manisandro@gmail.com> - 2.72.0-1
- Update to 2.72.0

* Tue Sep 08 2020 Sandro Mani <manisandro@gmail.com> - 2.71.1-1
- Update to 2.71.1

* Wed Aug 12 13:43:26 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.71.0-2
- Rebuild (mingw-gettext)

* Fri Jul 31 2020 Sandro Mani <manisandro@gmail.com> - 2.71.0-1
- Update to 2.71.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.70.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 2.70.0-2
- Rebuild (gettext)

* Sat Mar 07 2020 Sandro Mani <manisandro@gmail.com> - 2.70.0-1
- Update to 2.70.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.68.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Sandro Mani <manisandro@gmail.com> - 2.68.3-1
- Update to 2.68.3

* Thu Nov 14 2019 Sandro Mani <manisandro@gmail.com> - 2.68.2-1
- Update to 2.68.2

* Thu Nov 07 2019 Fabiano Fidêncio <fidencio@redhat.com> - 2.68.0-3
- Enable GNOME support

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.68.0-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Aug 15 2019 Fabiano Fidêncio <fidencio@redhat.com> - 2.68.0-1
- Update to its native counter-part version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.59.90.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.59.90.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.59.90.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.59.90.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.59.90.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 2.59.90.1-2
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Kalev Lember <klember@redhat.com> - 2.59.90.1-1
- Update to 2.59.90.1 (CVE-2017-2885)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Kalev Lember <klember@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Sat Feb 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.56.0-3
- Add BR python.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.56.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.56.0-1
- Update to 2.56.0

* Wed Sep 07 2016 Kalev Lember <klember@redhat.com> - 2.54.1-1
- Update to 2.54.1
- Drop static subpackage as the static libs don't build any more
- Don't set group tags
- Update project URLs

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.52.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 2.52.2-2
- Use global instead of define.

* Wed Nov 18 2015 Kalev Lember <klember@redhat.com> - 2.52.2-1
- Update to 2.52.2

* Fri Oct 16 2015 Kalev Lember <klember@redhat.com> - 2.52.1-1
- Update to 2.52.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.50.0-1
- Update to 2.50.0
- Use license macro for the COPYING file

* Mon Dec 01 2014 Fabiano Fidêncio <fidencio@redhat.com> - 2.48.0-2
- Add mingw-glib-networking as dep (#1169185)

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.48.0-1
- Update to 2.48.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.46.0-1
- Update to 2.46.0

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.44.2-1
- Update to 2.44.2

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.90-1
- Update to 2.43.90

* Sat Aug  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.5-1
- Update to 2.43.5
- Make sure translations get installed to the correct folder (intltool bug #398571)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.43.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.4-1
- Update to 2.43.4

* Sun Jun 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.1-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.1-1
- Update to 2.43.1

* Fri Mar 29 2013 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.41.92-1
- Update to 2.41.92

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Kalev Lember <kalevlember@gmail.com> - 2.40.2-1
- Update to 2.40.2

* Sat Oct 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.40.1-1
- Update to 2.40.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.38.1-1
- Update to 2.38.1

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Sun Mar 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.90-3
- Added win64 support

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 2.37.90-2
- Renamed the source package to mingw-libsoup (#800433)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.37.90-1
- Update to 2.37.90
- Remove the .la files

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.5-2
- Rebuild against the mingw-w64 toolchain

* Tue Feb 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.37.5-1
- Update to 2.37.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Sun Oct 02 2011 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0
- Spec cleanup for recent rpmbuild

* Thu Jul 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.34.1-2
- Rebuilt against win-iconv

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.34.1-1
- Update to 2.34.1
- Build with --with-gnome
- Dropped the BR: mingw32-gnutls as support for TLS connections has
  moved to glib-networking

* Sun Apr 24 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.34.0-1
- Update to 2.34.0

* Fri Apr 22 2011 Kalev Lember <kalev@smartlink.ee> - 2.32.0-3
- Rebuilt for pseudo-reloc version mismatch (#698827)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov  7 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.32.0-1
- Update to 2.32.0

* Fri Nov 20 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.1-1
- Update to 2.28.1

* Sat Sep 19 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.92-2
- Rebuild because of broken mingw32-gcc/mingw32-binutils
- Added a patch to workaround GNOME BZ #595176

* Thu Sep 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.92-1
- Update to 2.27.92
- Dropped the workaround for GNOME BZ #593845

* Tue Sep  1 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.91-1
- Update to 2.27.91

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.90-1
- Update to 2.27.90
- Automatically generate debuginfo subpackage
- Added BR: mingw32-gnutls for SSL support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.27.1-1
- Update to 2.27.1

* Fri May 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.1-2
- Fixed license typo
- Use %%global instead of %%define
- Fixed mixed-use-of-spaces-and-tabs rpmlint warning

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.1-1
- Update to 2.26.1

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-2
- Added -static subpackage

* Fri Mar 20 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-1
- Update to 2.26.0

* Sat Feb 14 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.5-1
- Initial release

