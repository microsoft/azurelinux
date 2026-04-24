# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           mjpegtools
Version:        2.2.1
Release: 12%{?dist}
Summary:        Tools to manipulate MPEG data
# Most sources are GPLv2+ except the following which don't mention "or later":
# mplex/*
# utils/yuv4mpeg_intern.h
# And scripts/lav2mpeg just says "GPL"
License:        GPL-2.0-or-later AND GPL-2.0-only AND GPL-1.0-or-later
URL:            https://mjpeg.sourceforge.io/
Source:         https://downloads.sourceforge.net/mjpeg/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch:          7b1989861157b1af5b98a797bd7a9080609a31f2.patch
Patch:          https://sources.debian.org/data/main/m/mjpegtools/1%3A2.1.0%2Bdebian-8.1/debian/patches/10_usr_local.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig(libquicktime) >= 0.9.8
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libdv) >= 0.9
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:  pkgconfig(sdl) >= 1.1.3
BuildRequires:  SDL_gfx-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# mencoder for lav2avi.sh
#Requires:       mencoder%%{?_isa}
# ffmpeg main package, y4mscaler and which for anytovcd.sh
Requires:       /usr/bin/ffmpeg
Requires:       which

%description
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains mjpegtools console
utilities.


%package        gui
Summary:        GUI tools to manipulate MPEG data
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-lav%{?_isa} = %{version}-%{release}

%description    gui
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains mjpegtools GUI
utilities.


%package        libs
Summary:        MJPEGtools libraries

%description    libs
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains libraries which are
used by mjpegtools and also by several other projects.


%package        lav
Summary:        MJPEGtools lavpipe libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    lav
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains libraries used by
mjpegtools.


%package        devel
Summary:        Development files for mjpegtools libraries 
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains development files
for building applications that use mjpegtools libraries.


%package        lav-devel
Summary:        Development files for mjpegtools lavpipe libraries 
Requires:       %{name}-lav%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    lav-devel
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains development files
for building applications that use mjpegtools lavpipe libraries.


%prep 
%autosetup -p1
autoreconf -fiv

for f in docs/yuvfps.1 ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
%configure --disable-static
%make_build


%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%if 0%{?rhel} && 0%{?rhel} < 10
rm -f %{buildroot}%{_libdir}/*.la
%endif
# too broken/outdated to be useful in 1.[89].0 (and would come with dep chain)
rm -f %{buildroot}%{_bindir}/mpegtranscode
# requires mencoder
rm -f %{buildroot}%{_bindir}/lav2avi.sh


%files
%doc CHANGES ChangeLog AUTHORS BUGS README.lavpipe NEWS TODO
%{_bindir}/anytovcd.sh
%{_bindir}/jpeg2yuv
%{_bindir}/lav*
%{_bindir}/*.flt
%{_bindir}/mjpeg_simd_helper
%{_bindir}/mp*2enc
%{_bindir}/mplex
%{_bindir}/*toy4m
%{_bindir}/png2yuv
%{_bindir}/y4m*
%{_bindir}/ypipe
%{_bindir}/yuv*
%exclude %{_bindir}/glav
%exclude %{_bindir}/lavplay
%exclude %{_bindir}/qttoy4m
%exclude %{_bindir}/y4mhist
%exclude %{_bindir}/y4mtoqt
%exclude %{_bindir}/yuvplay
%{_mandir}/man1/jpeg2yuv.1*
%{_mandir}/man1/lav*.1*
%{_mandir}/man1/mjpegtools.1*
%{_mandir}/man1/mp*2enc.1*
%{_mandir}/man1/mplex.1*
%{_mandir}/man1/*toy4m.1*
%{_mandir}/man1/png2yuv.1*
%{_mandir}/man1/y4m*.1*
%{_mandir}/man1/yuv*.1*
%exclude %{_mandir}/man1/lavplay.1*
%exclude %{_mandir}/man1/yuvplay.1*
%{_mandir}/man5/yuv4mpeg.5*
%{_infodir}/mjpeg-howto.info*

%files gui
%{_bindir}/glav
# lavplay and yuvplay won't save console util users from X11 and SDL
# dependencies as long as liblavplay is in -lav, but they're inherently
# GUI tools -> include them here
%{_bindir}/lavplay
%{_bindir}/qttoy4m
%{_bindir}/y4mhist
%{_bindir}/y4mtoqt
%{_bindir}/yuvplay
%{_mandir}/man1/lavplay.1*
%{_mandir}/man1/yuvplay.1*

%files libs
%license COPYING
%{_libdir}/libmjpegutils-2.2.so.0{,.*}
%{_libdir}/libmpeg2encpp-2.2.so.0{,.*}
%{_libdir}/libmplex2-2.2.so.0{,.*}

%files lav
%{_libdir}/liblavfile-2.2.so.0{,.*}
%{_libdir}/liblavjpeg-2.2.so.0{,.*}
%{_libdir}/liblavplay-2.2.so.0{,.*}

%files devel
%{_includedir}/%{name}
%exclude %{_includedir}/%{name}/*lav*.h
%{_libdir}/libmjpegutils.so
%{_libdir}/libmpeg2encpp.so
%{_libdir}/libmplex2.so
%{_libdir}/pkgconfig/%{name}.pc

%files lav-devel
%{_includedir}/%{name}/*lav*.h
%{_libdir}/liblavfile.so
%{_libdir}/liblavjpeg.so
%{_libdir}/liblavplay.so


%changelog
* Wed Aug 27 2025 Vitaly <vitaly@easycoding.org> - 2.2.1-11
- Fixed installation with alternative versions of ffmpeg package.

* Mon Aug 11 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.1-10
- Import to Fedora (rhbz#2387676)

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
- Add GCC-15 patch from upstream

* Tue Oct 08 2024 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-7
- Rebuilt

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 19 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-1
- Update to 2.2.1

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 17 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 12 2020 Leigh Scott <leigh123linux@gmail.com> - 2.1.0-19
- Rebuilt for i686

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Xavier Bachelot <xavier@bachelot.org> - 2.1.0-17
- Disable use of SDL_gfx on EL8.
- Minor spec cleanup.

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.1.0-14
- Rebuild for ffmpeg-3.4.5 on el7
- infodir scriptlets deprecated

* Fri Oct 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-13
- Remove Group tag
- Add missing isa on Requires
- Update scriptlets and buildroot  macro

* Fri Oct 12 2018 Sérgio Basto <sergio@serjux.com> - 2.1.0-12
- Add BuildRequires: gcc-c++

* Fri Oct 12 2018 Sérgio Basto <sergio@serjux.com> - 2.1.0-11
- Build with libquicktime again

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-8
- Build without libquicktime for F28
- Disable AltiVec for ppc64

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 2.1.0-5
- Rebuilt for FFmpeg 2.4.3

* Sat Jul 26 2014 Sérgio Basto <sergio@serjux.com> - 2.1.0-4
- Rebuild for new libSDL_gfx, need by mjpegtools-gui
- Fix FTBFS for errors "format not a string literal and no format arguments" because 
    FESCO decided Enable "-Werror=format-security" by default
    https://fedorahosted.org/fesco/ticket/1185
- Bring and add two patches from Gentoo: mjpegtools-2.1.0-pic.patch and mjpegtools-2.1.0-sdl-cflags.patch

* Tue Nov 19 2013 Sérgio Basto <sergio@serjux.com> - 2.1.0-3
- Better obsoletes/provides for y4mscaler.

* Tue Nov 19 2013 Sérgio Basto <sergio@serjux.com> - 2.1.0-2
- Fix rfbz #3022, Obsoletes: y4mscaler, because already integrate into
  mjpegtools-2.1.0

* Thu Nov 07 2013 Sérgio Basto <sergio@serjux.com> - 2.1.0-1
- Update to 2.1.0
- Drop upstreamed patches.

* Wed Nov 06 2013 Sérgio Basto <sergio@serjux.com> - 2.0.0-9
- Rebuilt for x264/FFmpeg

* Mon Sep 30 2013 Sérgio Basto <sergio@serjux.com> - 2.0.0-8
- Rebuilt for x264/FFmpeg

* Sat May 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-7
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-6
- Mass rebuilt for Fedora 19 Features

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-5
- Rebuilt for FFmpeg

* Wed May 02 2012 Sérgio Basto <sergio@serjux.com> - 2.0.0-4
- Add patch for gcc 4.7

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug  1 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 2.0.0-1
- Update to new upstream 2.0.0 final release

* Fri Sep  3 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9.0-2
- Fix a memleak which is causing issues for LiVES

* Wed Apr 15 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9.0-1
- Update to upstream 1.9.0 final release

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.9.0-0.7.rc3
- rebuild for new F11 features

* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9.0-0.6.rc3
- Release bump for rpmfusion
- Sync with freshrpms (no changes)

* Tue Apr 22 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.5.rc3
- Apply patch from Gentoo to fix build with GCC 4.3 (#1941).

* Tue Dec  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.4.rc3
- 1.9.0rc3.

* Sat Sep 29 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.4.rc2
- Requires: which

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.3.rc2
- License: GPLv2

* Thu Jun 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.2.rc2
- Rebuild.

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.1.rc2
- 1.9.0rc2.

* Sat Nov 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-7
- Split GUI utilities into -gui subpackage.
- Don't ship mpegtranscode, it's broken/outdated.
- Require mencoder for lav2avi.sh.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.8.0-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-5
- Specfile cleanup.

* Sun Jun  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-4
- Get rid of undefined non-weak symbols in liblav*.
- Apply upstream fix for compiling with libquicktime 0.9.8.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sat Jan 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-0.lvn.3
- Include license text in -libs, it can be installed without the main package.
- Convert yuvfps man page to UTF-8.
- Fix -devel Group tag.

* Thu Jan 19 2006 Adrian Reber <adrian@lisas.de> - 1.8.0-0.lvn.2
- Added patch to compile with gcc 4.1
- Dropped 0 Epoch

* Mon Sep 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.8.0-0.lvn.1
- 1.8.0.

* Sat Aug 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.3-0.lvn.0.1.rc3
- 1.6.3-rc3, Altivec fixes applied upstream.

* Fri Aug 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.3-0.lvn.0.1.rc2
- 1.6.3-rc2, clean up obsolete pre-FC2 stuff.
- Fix Altivec build, kudos to upstream.

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6,3-0.lvn.0.1.rc1
- 1.6.3-rc1 (1.7.0 snapshot package not released, so no Epoch bump).

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.7.0-0.lvn.0.2.cvs20050521
- PPC: disable Altivec due to gcc4 build failure, honor $RPM_OPT_FLAGS.

* Sat May 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.7.0-0.lvn.0.1.cvs20050521
- Pre-1.7.0 snapshot as of today, all patches applied or obsoleted upstream.
- Require pkgconfig in -devel.

* Wed Feb  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.7
- Add corrected -fPIC tweak from Thorsten.

* Mon Jan 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.6
- Include PNG input support.
- Remove no-op $RPM_OPT_FLAGS setting from %%build.
- Remove bogus optimization settings from configure script.

* Fri Dec 31 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.6.2-0.lvn.5
- CFLAGS="$CFLAGS -fPIC" on non x86; Fixes build error on x86_64; The 
  option --with-pic is not enough

* Sat Dec 18 2004 Dams <anvil[AT]livna.org> - 0:1.6.2-0.lvn.4
- Disabling static libraries building

* Tue Dec 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.3
- Include quicktime support.
- Apply patch from ALT Linux to fix info pages, fix typo in %%post.
- Require /sbin/install-info.
- Add "--without static" rpmbuild option to work around an issue with FC3 strip
- Always enable SIMD accelerations, CPU capabilities detected at runtime.
- Always disable use of cmov.

* Thu Nov 11 2004 Dams <anvil[AT]livna.org> 0:1.6.2-0.lvn.2
- Added patch to fix gcc3.4 build
- Detected race condition in Makefiles (disabling _smp_mflags use)
- Added info files & scriptlets
- Dropped patch0 and patch1

* Tue Jun  8 2004 Dams <anvil[AT]livna.org> 0:1.6.2-0.lvn.1
- Updated to 1.6.2

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.6
- Removed comment after scriptlets

* Fri Aug 22 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.5
- buildroot -> RPM_BUILD_ROOT

* Sun Aug 10 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.4
- Applied upstream patches to fix build on gcc3.3 systems

* Tue Apr 29 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.3
- Now test arch for configure options (from Ville)
- Removed ImageMagick-devel BuildRequires

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.2
- Added missing BuildRequires 
- Added post/postun scriplets for libs package

* Wed Apr 23 2003 Dams <anvil[AT]livna.org> 
- Initial build.
