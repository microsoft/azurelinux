# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Image loading, saving, rendering, and manipulation library
Name:           imlib2
Version:        1.12.3
Release:        3%{?dist}
License:        Imlib2
URL:            http://docs.enlightenment.org/api/imlib2/html/
Source0:        http://downloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.xz

BuildRequires:  doxygen
BuildRequires:  giflib-devel
BuildRequires:  freetype-devel >= 2.1.9-4
BuildRequires:  libtool
BuildRequires:  bzip2-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libheif-devel
BuildRequires:  libjxl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libspectre-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libwebp-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  pkgconfig
BuildRequires:  make

%description
Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       freetype-devel >= 2.1.9-4


%description devel
This package contains development files for %{name}.

Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%package id3tag-loader
Summary:        Imlib2 id3tag-loader
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description id3tag-loader
This package contains a plugin which makes imlib2 capable of parsing id3 tags
of mp3 files. This plugin is packaged separately because it links with
libid3tag which is GPLv2+, thus making imlib2 and apps using it subject to the
conditions of the GPL version 2 (or at your option) any later version.


%prep
%autosetup -p1

%build
asmopts="--disable-mmx --disable-amd64"
%ifarch x86_64
asmopts="--disable-mmx --enable-amd64"
%else
%ifarch %{ix86}
asmopts="--enable-mmx --disable-amd64"
%endif
%endif

# can be dropped once upstream moves to autoconf 2.69
autoreconf -ifv

# stop -L/usr/lib[64] getting added to imlib2-config
export x_libs=" "
%configure \
 --disable-static \
 --enable-doc-build \
 --with-pic \
 $asmopts
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{make_build}


%install
%{make_install}

# remove demos and their dependencies
rm $RPM_BUILD_ROOT%{_bindir}/imlib2_*
rm -rf $RPM_BUILD_ROOT%{_datadir}/imlib2/

# remove static libraries
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f \{\} \;



%ldconfig_scriptlets


%files
%doc AUTHORS README TODO
%license COPYING
%{_libdir}/libImlib2.so.*
%{_libdir}/imlib2/
%exclude %{_libdir}/imlib2/loaders/id3.*

%files devel
%doc doc/html
%{_includedir}/Imlib2*.h
%{_libdir}/libImlib2.so
%{_libdir}/pkgconfig/imlib2.pc

%files id3tag-loader
%{_libdir}/imlib2/loaders/id3.*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 1.12.3-2
- Rebuild for jpegxl (libjxl) 0.11.1

* Mon Jan 27 2025 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 1.12.3-1
- Update to 1.12.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.11.1-9
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 1.11.1-7
- Rebuild for jpegxl (libjxl) 0.10.2

* Wed Feb 14 2024 Sérgio Basto <sergio@serjux.com> - 1.11.1-6
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 1.11.1-2
- Mass rebuild for jpegxl-0.8.1

* Tue Jun 13 2023 Leigh Scott <leigh123linux@gmail.com> - 1.11.1-1
- New upstream version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 20 2021 Tomas Smetana <tsmetana@redhat.com> - 1.7.4-1
- New upstream version
- Fix rhbz#2015742 - Compile with WebP support

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Tomas Smetana <tsmetana@redhat.com> - 1.6.1-1
- New upstream version
- Fix rhbz#1834969 - CVE-2020-12761 integer overflow in ICO color maps handling

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 05 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-3
- Spec file cleanup

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Tomas Smetana <tsmetana@redhat.com> - 1.5.1-1
- New upstream version

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 1.4.9-6
- Rebuild (giflib)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 06 2016 Tomas Smetana <tsmetana@redhat.com> - 1.4.9-1
- New upstream bugfix version
- Fix rhbz#1323617 - CVE-2016-3993: off by one error in MergeUpdate
- Fix rhbz#1327478 - CVE-2016-4024: integer overflow resulting in insufficient heap allocation

* Fri Apr 01 2016 Tomas Smetana <tsmetana@redhat.com> - 1.4.8-1
- New upstream bugfix version
- Fix rhbz#1323062 - out of bound read in GIF loader
- Fix rhbz#1323082 - divide by zero on 2x1 ellipse

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Tomas Smetana <tsmetana@redhat.com> - 1.4.7-1
- Rebase to 1.4.7
- Fixes CVE-2014-9762, CVE-2014-9763, CVE-2014-9764

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Tomas Smetana <tsmetana@redhat.com> - 1.4.6-3
- Fix output of imlib2-config --libs (rhbz #1184166)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Tomas Smetana <tsmetana@redhat.com> - 1.4.6-1
- New upstream bugfix version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Tomas Smetana <tsmetana@redhat.com> - 1.4.5-9
- fix #925586: call autoreconf -ifv during build to add support for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.4.5-7
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.4.5-6
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Tomas Smetana <tsmetana@redhat.com> - 1.4.5-4
- Rebuild for new libtiff

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.4.5-2
- Rebuild for new libpng

* Mon Sep 19 2011 Tomas Smetana <tsmetana@redhat.com> - 1.4.5-1
- new upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 07 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.4-1
- new upstream version

* Fri Apr 23 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.3-1
- new upstream version
- patch for CVE-2010-0991

* Mon Feb 01 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.2-6
- fix #542607 - remove static libraries

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Tomas Smetana <tsmetana@redhat.com> 1.4.2-3
- fix #477400 - remove fonts
- remove demo programs and images

* Sun Nov 23 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.2-2
- patch for CVE-2008-5187

* Tue Oct 21 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.2-1
- new upstream version 1.4.2

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.1-1
- New upstream release 1.4.1
- Stop shipping static lib in -devel

* Fri May 30 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.0-7
- patch for CVE-2008-2426

* Tue Mar 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-6
- Disable amd64 assembly optimization. (Kills idesk - #222998, #436924)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.0-5
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-4
- Fix building on ia64 (bz 349171)

* Thu Sep  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-3
- Update license tag

* Wed Aug  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-2
- put the id3tag loader in its own imlib2-id3tag-loader subpackage as it links
  to libid3tag, which is GPLv2+, and we don't want the imlib2 main package to
  become GPLv2+ (bz 251054) (WIP) (*)
- fix the URL tag (bz 251277)
- Update License tag for new Licensing Guidelines compliance (WIP) (*)
(*) waiting for feedback from Spot, do not build yet!!

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-1
- New upstream release 1.4.0

* Thu Nov  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-3
- Fix CVE-2006-4806, CVE-2006-4807, CVE-2006-4808, CVE-2006-4809, thanks to
  Ubuntu for the patch (bug 214676)

* Thu Oct 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-2
- Multilib devel goodness (make -devel i386 and x86_64 parallel installable)
- Fix bug 212469
- Add libid3tag-devel to the BR's so id3tag support gets build in

* Tue Oct 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-1
- New upstream release 1.3.0

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-2
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-1
- New upstream release 1.2.2

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-6
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5 (bug 185871)

* Thu Nov 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-5
- Make XPM loader use /usr/share/X11/rgb.txt.
- Drop no longer needed multilib configure options.

* Sun Nov 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-4
- Adapt to modular X.Org (#172613).

* Wed Sep 21 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.1-3
- Make XPM loader use /usr/lib/X11/rgb.txt instead of /usr/X11R6/...

* Sun Aug 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-2
- 1.2.1, patches applied/obsoleted upstream.
- Improve summary and description, fix URL.
- Move HTML docs to -devel.
- Build with dependency tracking disabled.
- Drop x86_64 freetype rpath hack, require a fixed freetype-devel.

* Mon May  9 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-8.fc4
- Fix segfault in XPM loader (#156058).

* Tue Apr  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-7.fc4
- Fix broken pkgconfig file.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-6
- Include imlib2 directory in datadir and libdir.

* Wed Feb  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-5
- Link loaders with the main lib, fixes load/save problems with some apps.

* Tue Jan 18 2005 Michael Schwendt <mschwendt[AT[users.sf.net> - 0:1.2.0-4
- Really include libtool archives to fix fedora.us bug #2284.

* Fri Jan 14 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-3
- Move filters and loaders back into main package where they belong

* Mon Jan 10 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-2
- Don't ship *.?.a in {_libdir}/imlib/filters/ and loaders/

* Sun Jan 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-1
- Ship .la files ue to a bug in kdelibs; see
  https://bugzilla.fedora.us/show_bug.cgi?id=2284
  http://bugzilla.redhat.com/bugzilla/142244
  http://bugs.kde.org/93359
- Use make param LIBTOOL=/usr/bin/libtool - fixes hardcoded rpath on x86_64
- fix hardcoded rpath im Makefiles on x86_64 due to freetype-config --libs
  returning "-L/usr/lib64 -Wl,--rpath -Wl,/usr/lib64 -lfreetype -lz"
- Update to 1.2.0 -- fixes several security issues
- remove explicit libdir=_libdir - 1.2.9 does not need it anymore
- removeddemo compile/install;
- use configure param --x-libraries={_prefix}/X11R6/{_lib} and patch to fix
  "cannot find -lX11"

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.1.2-2
- Disable mmx on x86_64 (fixes Build error)
- Add explicit libdir=_libdir to make calls to avoid install errors on x86_64
- Add --with-pic configure option (taken from Matthias Saou's package)

* Sat Sep 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.1
- Update to 1.1.2, fixes CAN-2004-0802.
- Enable MMX on all ix86, x86_64 and ia64, it seems runtime-detected.
- Update URL.

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.3
- s#_prefix/lib#_libdir#

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.2
- Moved some binaries and loaders into main package
- Added missing Requires and BuildRequires

* Sun Oct 26 2003 Dams <anvil[AT]livna.org>
- Initial build.
