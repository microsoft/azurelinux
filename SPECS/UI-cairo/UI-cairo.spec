%define tarname cairo
%define pixman_version 0.30.0
%define freetype_version 2.1.9
%define fontconfig_version 2.2.95

# This version of "cairo" uses the same sources as the "regular" one but builds
# with a dependency on some X11 and other graphics-related libraries, producing
# same-named binaries as the "regular" version, thus the "UI-" prefix.
# Due to this conflict "cairo*" and "UI-cairo*" packages CANNOT be installed
# on a single system.
Summary:        A 2D graphics library (UI libs dependent)
Name:           UI-cairo
Version:        1.16.0
Release:        12%{?dist}
# The sources for 'cairo' itself are available under the (LGPLv2 OR MPLv1.1) license.
# Test code and fonts are available under either the MIT or Public Domain license.
# The 'cairo-trace' tools are released under the GPLv3 license - 'License' tag added separately for that subpackage.
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://cairographics.org
Source0:        https://cairographics.org/releases/%{tarname}-%{version}.tar.xz

Patch3:         cairo-multilib.patch
# https://gitlab.freedesktop.org/cairo/cairo/merge_requests/1
Patch4:         0001-Set-default-LCD-filter-to-FreeType-s-default.patch
# https://gitlab.freedesktop.org/cairo/cairo/merge_requests/5
Patch5:         CVE-2018-19876.patch
# https://github.com/matthiasclasen/cairo/commit/79ad01724161502e8d9d2bd384ff1f0174e5df6e
Patch6:         cairo-composite_color_glyphs.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1817958
Patch7:         0001-cff-Allow-empty-array-of-operands-for-certain-operat.patch

BuildRequires:  fontconfig-devel >= %{fontconfig_version}
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrender-devel
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel >= %{pixman_version}
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(xext)

Requires:       expat
Requires:       glib
Requires:       libpng
Requires:       pixman

Conflicts:       cairo

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, in-memory image buffers, and image files (PDF, PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available.

NOTE: this is an extended version of 'cairo' built with multiple dependencies on X11
and other graphics-related libraries compiled into its binaries. It CONFLICTS
with the non-UI version.

%package devel
Summary:        Development files for cairo
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Conflicts:      cairo-devel

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       fontconfig-devel
Requires:       freetype-devel
Requires:       libpng-devel
Requires:       pixman-devel

Provides:       pkconfig(cairo-fc) = %{version}-%{release}
Provides:       pkconfig(cairo-ft) = %{version}-%{release}
Provides:       pkconfig(cairo) = %{version}-%{release}
Provides:       pkconfig(cairo-pdf) = %{version}-%{release}
Provides:       pkconfig(cairo-png) = %{version}-%{release}
Provides:       pkconfig(cairo-ps) = %{version}-%{release}
Provides:       pkconfig(cairo-svg) = %{version}-%{release}
Provides:       pkconfig(cairo-tee) = %{version}-%{release}
Provides:       pkconfig(cairo-xlib) = %{version}-%{release}
Provides:       pkconfig(cairo-xlib-xrender) = %{version}-%{release}
Provides:       pkconfig(cairo-script) = %{version}-%{release}
Provides:       pkconfig(cairo-xcb-shm) = %{version}-%{release}
Provides:       pkconfig(cairo-xcb) = %{version}-%{release}

%description devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary:        GObject bindings for cairo
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Conflicts:      cairo-gobject

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary:        Development files for cairo-gobject
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Conflicts:      cairo-gobject-devel

Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-gobject%{?_isa} = %{version}-%{release}

Provides:       pkconfig(cairo-gobject) = %{version}-%{release}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary:        Development tools for cairo
License:        GPLv3

Conflicts:      cairo-tools

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%autosetup -p1 -n %{tarname}-%{version}

%build
%configure \
    --disable-gl \
    --disable-gtk-doc \
    --disable-static \
    --enable-ft \
    --enable-gobject \
    --enable-pdf \
    --enable-ps \
    --enable-svg \
    --enable-tee \
    --enable-xlib

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%doc AUTHORS BIBLIOGRAPHY BUGS NEWS README
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*
%{_bindir}/cairo-sphinx

%files devel
%doc ChangeLog PORTING_GUIDE
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-xlib-xrender.h
%{_includedir}/cairo/cairo-xlib.h
%{_includedir}/cairo/cairo-script.h
%{_includedir}/cairo/cairo-xcb.h
%{_libdir}/libcairo.so
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-xlib.pc
%{_libdir}/pkgconfig/cairo-xlib-xrender.pc
%{_libdir}/pkgconfig/cairo-script.pc
%{_libdir}/pkgconfig/cairo-xcb-shm.pc
%{_libdir}/pkgconfig/cairo-xcb.pc
%{_datadir}/gtk-doc/html/cairo

%files gobject
%{_libdir}/libcairo-gobject.so.*

%files gobject-devel
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc

%files tools
%license util/cairo-trace/COPYING util/cairo-trace/COPYING-GPL-3
%{_bindir}/cairo-trace
%{_libdir}/cairo/

%changelog
* Thu Jun 10 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.0-12
- Added missing 'Conflicts' for all 'cairo' subpackges.

* Tue Apr 20 2021 Henry Li <lihl@microsoft.com> - 1.16.0-11
- Add pixman, glib, libpng and expat as runtime requirement for UI-cairo
- Add freetype-devel, pixman-devel, libpng-devel and fontconfig-devel as runtime requirements for UI-cairo-devel

* Tue Jan 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.0-10
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Removing BR on "librsvg2-devel" missing in CBL-Mariner. This disables build-time tests for SVG.
- Renamed package to "UI-cairo" to avoid conflicts with core CBL-Mariner's version of "cairo".
- Renamed patch file for a CVE-2018-19876 fix to align it with CBL-Mariner's tooling.
- Added "GPLv3" license for the '*-tools' subpackage.
- Added explicit "Provides" for "pkgconfig(*)".
- Added explicit calls to ldconfig.
- Added missing BR on "pkgconfig(xext)".

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Apr 24 2020 Marek Kasik <mkasik@redhat.com> - 1.16.0-8
- Allow empty array of operands for certain operators in CFF fonts
- Resolves: #1817958

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Kalev Lember <klember@redhat.com> - 1.16.0-5
- Fix a thinko in composite_color_glyphs

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec  7 2018 Marek Kasik <mkasik@redhat.com> - 1.16.0-3
- Use FT_Done_MM_Var instead of free when available in
- cairo_ft_apply_variations

* Fri Dec  7 2018 Marek Kasik <mkasik@redhat.com> - 1.16.0-2
- Set default LCD filter to FreeType's default
- Resolves: #1645763

* Mon Oct 22 2018 Kalev Lember <klember@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Sat Sep 22 2018 Kalev Lember <klember@redhat.com> - 1.15.14-1
- Update to 1.15.14
- Drop ldconfig scriptlets

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Apr 21 2018 Kalev Lember <klember@redhat.com> - 1.15.12-2
- Fix assertion failure in the freetype backend (#1567633)

* Thu Apr 12 2018 Kalev Lember <klember@redhat.com> - 1.15.12-1
- Update to 1.15.12

* Mon Mar 19 2018 Adam Jackson <ajax@redhat.com> - 1.15.10-5
- Update the description to reflect dropping the OpenGL backend.

* Thu Mar 15 2018 Adam Jackson <ajax@redhat.com> - 1.15.10-4
- Drop cairo-gl in RHEL too.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.10-2
- Switch to %%ldconfig_scriptlets

* Tue Dec 12 2017 Kalev Lember <klember@redhat.com> - 1.15.10-1
- Update to 1.15.10

* Thu Aug 31 2017 Kalev Lember <klember@redhat.com> - 1.15.8-1
- Update to 1.15.8

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Adam Jackson <ajax@redhat.com> - 1.14.10-2
- Disable cairo-gl in F27+

* Fri Jun 16 2017 Kalev Lember <klember@redhat.com> - 1.14.10-1
- Update to 1.14.10

* Wed Apr 19 2017 Kalev Lember <klember@redhat.com> - 1.14.8-3
- Remove all libtool .la files from cairo private directories as well

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Kalev Lember <klember@redhat.com> - 1.14.8-1
- Update to 1.14.8

* Mon Jul 25 2016 Kalev Lember <klember@redhat.com> - 1.14.6-2
- xlib: Fix double free in _get_image_surface() (#1331021)
- Minor spec file cleanups

* Mon Apr 04 2016 Kalev Lember <klember@redhat.com> - 1.14.6-1
- Update to 1.14.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 31 2015 Kalev Lember <klember@redhat.com> - 1.14.4-1
- Update to 1.14.4
- Use license macro for COPYING*

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Kalev Lember <kalevlember@gmail.com> - 1.14.2-1
- Update to 1.14.2

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.14.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 29 2015 Kevin Fenzi <kevin@scrye.com> 1.14.0-2
- Add patch to fix crashes in dot. Fixes bug #1183242

* Sun Nov 23 2014 Kalev Lember <kalevlember@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.13.1-0.5.git337ab1f
- Minor spec file cleanup:
- Drop manual -devel subpackage deps
- Tighten deps with the _isa macro

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1-0.4.git337ab1f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.1-0.3.git337ab1f
- Enable make check but don't (currently) fail the build on failure

* Fri Jun  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.1-0.2.git337ab1f
- Compile with -flto -ffat-lto-objects CFLAGS to fix FTBFSF with gcc 4.9

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 1.13.1-0.1.git337ab1f
- Update to 1.13.1 git snapshot for device scale support

* Wed Aug 28 2013 Kalev Lember <kalevlember@gmail.com> - 1.12.16-1
- Update to 1.12.16

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Matthias Clasen <mclasen@redhat.com> 1.12.14-3
- Fix a multilib issue in /usr/bin/cairo-trace

* Sat May 25 2013 Kalev Lember <kalevlember@gmail.com> 1.12.14-2
- Backport an upstream patch for eog get_buddy() crashes (#912030)

* Tue Feb 12 2013 Adam Jackson <ajax@redhat.com> 1.12.14-1
- cairo 1.12.14

* Mon Jan 28 2013 Adam Jackson <ajax@redhat.com> 1.12.10-2
- cairo-1.12.10-xlib-regression-fix.patch: Fix a regression caused by
  mit-shm surfaces.

* Wed Jan 16 2013 Adam Jackson <ajax@redhat.com> 1.12.10-1
- cairo 1.12.10
- 0001-xlib-shm-Fix-memory-leak.patch: Drop, merged.

* Wed Jan  2 2013 Matthias Clasen <mclasen@redhat.com> - 1.12.8-3
- Make inter-subpackage deps explicit

* Tue Dec 18 2012 Adam Jackson <ajax@redhat.com> 1.12.8-2
- 0001-xlib-shm-Fix-memory-leak.patch: Fix a memory leak with shm image
  surfaces. (#882976)

* Mon Nov  5 2012 Matthias Clasen <mclasen@redhat.com> - 1.12.8-1
- Update to 1.12.8, including a fix for screenshots in fallback mode

* Wed Oct 31 2012 Adam Jackson <ajax@redhat.com> 1.12.6-2
- *-x{c,li}b-Don-t-crash-when-swapping-a-0-sized-glyph.patch: Fix some
  crashes when client and server endian don't match.

* Thu Oct 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.6-1
- Update to 1.12.6

* Fri Oct 12 2012 Matthias Clasen <mclasen@redhat.com> - 1.12.4-1
- 1.12.4
- drop obsolete patch

* Wed Sep 19 2012 Thorsten Leemhuis <fedora@leemhuis.info> - 1.12.2-4.1
- rebuild for f18

* Tue Sep 18 2012 Thorsten Leemhuis <fedora@leemhuis.info> - 1.12.2-4
- add patch from master to fix issues with weston

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.12.2-2
- Add ldconfig scriptlet calls to -gobject.
- Fix rpmlint's spaces vs tabs warnings.

* Fri May 18 2012 Matthias Clasen <mclasen@redhat.com> - 1.12.2-1
- Update to 1.12.2

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 1.12.0-1
- Update to latest stable release
- Enable the GL backend

* Thu Mar 15 2012 Benjamin Otte <otte@redhat.com> - 1.10.2-7
- Add patch to make eclipse not crash (#803878)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 1.10.2-5
- Rebuild for new libpng

* Fri Jul 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.10.2-4
- cairo-devel doesn't own /usr/include/cairo (#716611)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Christopher Aillon <caillon@redhat.com> - 1.10.2-2
- Enable tee support

* Mon Jan 03 2011 Benjamin Otte <otte@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Thu Nov 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.10.0-4
- add missing BuildRequires: librsvg2 for SVG support

* Wed Sep 29 2010 jkeating - 1.10.0-3
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Matthias Clasen <mclasen@redhat.com> - 1.10.0-2
- Drop the explicit dep on the wrong package from -gobject-devel

* Tue Sep 07 2010 Benjamin Otte <otte@redhat.com> - 1.10.0-1
- Update to 1.10.0
- Add cairo-gobject package

* Mon Jul 26 2010 Benjamin Otte <otte@redhat.com> - 1.9.14-1
- Update to 1.9.14 snapshot

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.12-1
- Update to 1.9.12 snapshot
- Remove now unnecessary patch

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-3
- Add patch to force linking with gcc, not g++. (#606523)

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-2
- Don't use silent rules, we want verbose output in builders

* Sun Jun 27 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-1
- Update to 1.9.10 snapshot

* Thu Jun 17 2010 Benjamin Otte <otte@redhat.com> - 1.9.8-1
- Update to 1.9.8 snapshot

* Sun Feb 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.8.10-1
- Update to 1.8.10

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.8.8-3
- Move ChangeLog to -devel to save space

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Matthias Clasen <mclasen@redhat.com> 1.8.8-1
- Update to 1.8.8

* Wed Apr 08 2009 Adam Jackson <ajax@redhat.com> 1.8.6-3
- cairo-1.8.6-repeat-modes.patch: Enable the repeat and pad blend modes in
  the xlib backend to make firefox performance slightly less dire.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Matthias Clasen <mclasen@redhat.com> 1.8.6-1
- Update to 1.8.6

* Sun Dec 14 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.0-3
- Rebuild for pkgconfig provides

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> 1.8.0-2
- Tweak %%summary and %%documentation

* Thu Sep 25 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.8.0-1
- Update to 1.8.0
- Update dep versions

* Mon Sep 22 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.7.6-1
- Update to 1.7.6

* Mon Aug 11 2008 Matthias Clasen <mclasen@redhat.com> 1.7.4-1
- Update to 1.7.4

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-3
- fix license tag

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> 1.6.4-2
- Fix source url

* Fri Apr 11 2008 Carl Worth <cworth@redhat.com> 1.6.2-1
- Update to 1.6.2

* Thu Apr 10 2008 Carl Worth <cworth@redhat.com> 1.6.0-1
- Update to 1.6.0

* Tue Apr  8 2008 Carl Worth <cworth@redhat.com> 1.5.20-1
- Update to 1.5.20

* Sun Apr  6 2008 Carl Worth <cworth@redhat.com> 1.5.18-1
- Update to 1.5.18

* Thu Apr  3 2008 Matthias Clasen <mclasen@redhat.com> 1.5.16-1
- Update to 1.5.16

* Fri Mar 21 2008 Matthias Clasen <mclasen@redhat.com> 1.5.14-1
- Update to 1.5.14

* Wed Feb 20 2008 Behdad Esfahbod <besfahbo@redhat.com>
- Point Source to cairographics.org/snapshots.  Change back to /releases
  when 1.6.0 is out.

* Wed Jan 30 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.8-2
- Remove TODO and ROADMAP as they were removed from tarball upstream.

* Wed Jan 30 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.8-1
- Update to 1.5.8

* Thu Jan 17 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.6-1
- Update to 1.5.6

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 1.5.2-1
- Update to 1.5.2
- Switch to external pixman.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.4.10-2
- Rebuild for PPC toolchain bug

* Wed Jun 27 2007 Carl Worth <cworth@redhat.com> 1.4.10-1
- Update to 1.4.10

* Sat Jun 9 2007 Behdad Esfahbod <besfahbo@redhat.com> 1.4.8-1
- Update to 1.4.8

* Tue May  1 2007 Carl Worth <cworth@redhat.com> 1.4.6-1
- Update to 1.4.6

* Mon Apr 16 2007 Carl Worth <cworth@redhat.com> 1.4.4-1
- Update to 1.4.4

* Tue Mar 20 2007 Carl Worth <cworth@redhat.com> 1.4.2-1
- Update to 1.4.2

* Tue Mar  6 2007 Carl Worth <cworth@redhat.com> 1.4.0-1
- Update to 1.4.0

* Wed Feb 14 2007 Carl Worth <cworth@redhat.com> 1.3.14-1
- Update to 1.3.14

* Sat Jan 20 2007 Carl Worth <cworth@redhat.com> 1.3.12-1
- Update to 1.3.12

* Sat Dec 23 2006 Carl Worth <cworth@redhat.com> 1.3.10-1
- Update to 1.3.10

* Thu Dec 14 2006 Carl Worth <cworth@redhat.com> 1.3.8-1
- Update to 1.3.8

* Sat Dec  9 2006 Matthias Clasen <mclasen@redhat.com> 1.3.6-2
- Small spec file cleanups

* Wed Dec  6 2006 Matthias Clasen <mclasen@redhat.com> 1.3.6-1
- Update to 1.3.6

* Thu Nov 23 2006 Matthias Clasen <mclasen@redhat.com> 1.3.4-1
- Update to 1.3.4

* Wed Nov 15 2006 Carl Worth <cworth@redhat.com> 1.3.2-1
- Update to 1.3.2

* Sun Nov  5 2006 Matthias Clasen <mclasen@redhat.com> 1.2.6-1
- Update to 1.2.6

* Sun Aug 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.4-1
- Update to 1.2.4
- Drop libXt-devel BuildReq as it shouldn't need it anymore.

* Wed Aug  9 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.2-3
- Remove unnecessary --disable-* arguments to configure, add --enable-*
  for those backends we really want to make sure are enabled.

* Wed Aug  9 2006 Ray Strode <rstrode@redhat.com> - 1.2.2-2
- add lame libXt-devel BuildReq to get things building again.
- small spec tweaks to follow conventions

* Wed Aug  9 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.2-1
- Update to 1.2.2

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 1.2.0-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.1
- rebuild

* Mon Jul  3 2006 Matthias Clasen <mclasen@redhat.com> 1.2.0-1
- Update to 1.2.0

* Fri Jun 16 2006 Carl Worth <cworth@redhat.com> 1.1.10-1
- Update to 1.1.10 (fixes crash on 16-bit X servers like Xvnc)

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> 1.1.8-1
- Update to 1.1.8

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 1.1.6-6
- buildrequire libxml2-devel

* Fri May  5 2006 Carl Worth <cworth@redhat.com> - 1.1.6-2
- Refuse to build pdf2svg to avoid depending on newer poppler

* Fri May  5 2006 Carl Worth <cworth@redhat.com> - 1.1.6-1
- Update to new upstream 1.1.6

* Wed May  3 2006 Carl Worth <cworth@redhat.com> - 1.1.4-2
- Revert upstream commit that introduced a dependency on a newer
  poppler version for the PDF tests.

* Wed May  3 2006 Carl Worth <cworth@redhat.com> - 1.1.4-1
- Update to new upstream 1.1.4
- Drop both embedded-bitmaps and XRenderAddGlyphs patches as both now
  have upstream versions

* Fri Apr 28 2006 Carl Worth <cworth@redhat.com> - 1.1.2-2
- Add suggested patch for XRenderAddGlyphs crash of bug #4705
  https://bugs.freedesktop.org/show_bug.cgi?id=4705

* Tue Apr 25 2006 Carl Worth <cworth@redhat.com> - 1.1.2-1
- Update to new upstream 1.1.2
- Port forward the embedded bitmaps patch (now committed upstream to
  1.1.3)
- Drop build-fix and chunk-glyphs patches which now come from upstream

* Wed Mar 15 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.4-1
- Update to 1.0.4
- Drop upstreamed patches

* Fri Mar  3 2006 Carl Worth <cworth@redhat.com> - 1.0.2-5
- add patch to chunk Xlib glyph compositing (bug 182416 and
  CVE-20060528)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Ray Strode <rstrode@redhat.com> 1.0.2-4
- add patch from Tim Mayberry to support embbedded bitmap
  fonts (bug 176910)

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-3.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Matthias Clasen <mclasen@redhat.com> 1.0.2-3
- Require libXrender-devel instead of xorg-X11-devel

* Tue Oct 11 2005 Kristian Høgsberg <krh@redhat.com> 1.0.2-2
- Rebuild against freetype-2.10 to pick up FT_GlyphSlot_Embolden.

* Thu Oct  6 2005 Kristian Høgsberg <krh@redhat.com> - 1.0.2-1
- Update to cairo-1.0.2.

* Wed Aug 24 2005 Kristian Høgsberg <krh@redhat.com> - 1.0.0-1
- Update to cairo-1.0.0.
- Drop cairo-0.9.2-cache-eviction-fix.patch and
  cairo-0.9.2-dont-hash-null-string.patch.

* Fri Aug 19 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-3
- Add cairo-0.9.2-dont-hash-null-string.patch to avoid crash when
  creating a cairo font from a FT_Face.

* Tue Aug 16 2005 Kristian Høgsberg <krh@redhat.com> - 0.9.2-2
- Rebuild against new freetype to get rid of --rpath in cairo.pc.

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-1
- Also obsolete libpixman-debuginfo.
- Add cairo-0.9.2-cache-eviction-fix.patch to fix ft font cache eviction.

* Sun Aug 14 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-1
- Update to cairo 0.9.2.  Add Obsoletes: for libpixman <= 0.1.6.
- Drop cairo-0.6.0-font-options-to-scaled-font.patch.

* Tue Aug  2 2005 Kristian Høgsberg <krh@redhat.com> - 0.6.0-2
- Add cairo-0.6.0-font-options-to-scaled-font.patch to make sure font
  cache eviction works correctly (#164664).

* Thu Jul 28 2005 Owen Taylor <otaylor@devserv.devel.redhat.com> 0.6.0-1
- Update to cairo-0.6.0

* Mon Jul 18 2005 Kristian Høgsberg <krh@redhat.com> 0.5.2-1
- Update to cairo-0.5.2 and drop bitmap font patch.

* Wed Jul  6 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-5
- Fix typo in use of libpixman_version macro (Thanks to Michael
  Schwendt, #162550).

* Sun Jun 26 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-4
- Add more missing devel package requires (libpng-devel and
  xorg-x11-devel) (#161688)
- Add Owens patch (cairo-0.5.1-bitmap-fonts.patch) to make bitmap
  fonts work with cairo (#161653).

* Wed Jun 22 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-3
- Add requirement on libpixman-devel for devel package.

* Tue Jun 21 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-2
- Package gtk docs as part of devel package.
- Nuke static library.
- Update devel files so /usr/include/cairo is owned by devel package.

* Mon Jun 20 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-1
- Update to cairo 0.5.1.
- Remove gtk-doc files, since --disable-gtk-doc doesn't work.
- Disable gtk-doc and add freetype and fontconfig BuildRequires.

* Tue Jun 14 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.0-2
- Add libpixman-devel BuildRequires.
- Explicitly disable win32 backend.

* Tue May 17 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.0-1
- Update to 0.5.0.

* Sun Jan 23 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.0-1
- Update to 0.3.0, explicitly disable more backends.

* Tue Nov 16 2004 Kristian Høgsberg <krh@redhat.com> - 0.2.0-1
- Incorporate changes suggested by katzj: Require: ldconfig and run it
  in %%post and %%postun, don't pass CFLAGS to make.

* Mon Aug  9 2004 Kristian Høgsberg <krh@redhat.com> - 0.2.0-1
- Update license, explicitly disable glitz.
- Create package.
