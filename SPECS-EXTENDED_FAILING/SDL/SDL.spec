Vendor:         Microsoft Corporation
Distribution:   Mariner
%if 0%{?rhel}
%bcond_with arts
%bcond_without esound
%bcond_with nas
%else
%bcond_with arts
%bcond_without esound
%bcond_with nas
%endif

Name:       SDL
Version:    1.2.15
Release:    44%{?dist}
Summary:    A cross-platform multimedia library
URL:        https://www.libsdl.org/
# The license of the file src/video/fbcon/riva_mmio.h is bad, but the contents
# of the file has been relicensed to MIT in 2008 by Nvidia for the 
# xf86_video-nv driver, therefore it can be considered ok.
# The license in the file src/stdlib/SDL_qsort.c is bad, but author relicensed
# it to zlib on 2016-02-21,
# <https://www.mccaughan.org.uk/software/qsort.c-1.14>, bug #1381888.
License:    LGPLv2+
# Source: %%{url}/release/%%{name}-%%{version}.tar.gz
# To create the repackaged archive use ./repackage.sh %%{version}
Source0:    %{name}-%{version}_repackaged.tar.gz
Source1:    %{url}/release/%{name}-%{version}.tar.gz.sig
Source2:    https://slouken.libsdl.org/slouken-pubkey.asc
Source3:    SDL_config.h
Source4:    repackage.sh
Patch0:     SDL-1.2.12-multilib.patch
# Rejected by upstream as sdl1155, rh480065
Patch1:     SDL-1.2.10-GrabNotViewable.patch
# Proposded to upstream as sdl1769
Patch2:     SDL-1.2.15-const_XData32.patch
# sdl-config(1) manual from Debian, rh948864
Patch3:     SDL-1.2.15-add_sdl_config_man.patch
# Upstream fix for sdl1486, rh990677
Patch4:     SDL-1.2.15-ignore_insane_joystick_axis.patch
# Do not use backing store by default, sdl2383, rh1073057, rejected by
# upstream
Patch5:     SDL-1.2.15-no-default-backing-store.patch
# Fix processing keyboard events if SDL_EnableUNICODE() is enabled, sdl2325,
# rh1126136, in upstream after 1.2.15
Patch6:     SDL-1.2.15-SDL_EnableUNICODE_drops_keyboard_events.patch
# Fix vec_perm() usage on little-endian 64-bit PowerPC, bug #1392465
Patch7:     SDL-1.2.15-vec_perm-ppc64le.patch
# Use system glext.h to prevent from clashing on a GL_GLEXT_VERSION definition,
# rh1662778
Patch8:     SDL-1.2.15-Use-system-glext.h.patch
# Fix CVE-2019-7577 (a buffer overread in MS_ADPCM_decode), bug #1676510,
# upstream bug #4492, in upstream after 1.2.15
Patch9:     SDL-1.2.15-CVE-2019-7577-Fix-a-buffer-overread-in-MS_ADPCM_deco.patch
# Fix CVE-2019-7575 (a buffer overwrite in MS_ADPCM_decode), bug #1676744,
# upstream bug #4493, in upstream after 1.2.15
Patch10:    SDL-1.2.15-CVE-2019-7575-Fix-a-buffer-overwrite-in-MS_ADPCM_dec.patch
# Fix CVE-2019-7574 (a buffer overread in IMA_ADPCM_decode), bug #1676750,
# upstream bug #4496, in upstream after 1.2.15
Patch11:    SDL-1.2.15-CVE-2019-7574-Fix-a-buffer-overread-in-IMA_ADPCM_dec.patch
# Fix CVE-2019-7572 (a buffer overread in IMA_ADPCM_nibble), bug #1676754,
# upstream bug #4495, in upstream after 1.2.15
Patch12:    SDL-1.2.15-CVE-2019-7572-Fix-a-buffer-overread-in-IMA_ADPCM_nib.patch
# Fix CVE-2019-7572 (a buffer overwrite in IMA_ADPCM_nibble), bug #1676754,
# upstream bug #4495, in upstream after 1.2.15
Patch13:    SDL-1.2.15-CVE-2019-7572-Fix-a-buffer-overwrite-in-IMA_ADPCM_de.patch
# Fix CVE-2019-7573, CVE-2019-7576 (buffer overreads in InitMS_ADPCM),
# bugs #1676752, #1676756, upstream bugs #4491, #4490,
# in upstream after 1.2.15
Patch14:    SDL-1.2.15-CVE-2019-7573-CVE-2019-7576-Fix-buffer-overreads-in-.patch
# Fix CVE-2019-7578, (a buffer overread in InitIMA_ADPCM), bug #1676782,
# upstream bug #4491, in upstream after 1.2.15
Patch15:    SDL-1.2.15-CVE-2019-7578-Fix-a-buffer-overread-in-InitIMA_ADPCM.patch
# Fix CVE-2019-7638, CVE-2019-7636 (buffer overflows when processing BMP
# images with too high number of colors), bugs #1677144, #1677157,
# upstream bugs #4500, #4499, in upstream after 1.2.15
Patch16:    SDL-1.2.15-CVE-2019-7638-CVE-2019-7636-Refuse-loading-BMP-image.patch
# Fix CVE-2019-7637 (an integer overflow in SDL_CalculatePitch), bug #1677152,
# upstream bug #4497, in upstream after 1.2.15
Patch17:    SDL-1.2.15-CVE-2019-7637-Fix-in-integer-overflow-in-SDL_Calcula.patch
# Fix CVE-2019-7635 (a buffer overread when blitting a BMP image with pixel
# colors out the palette), bug #1677159, upstream bug #4498,
# in upstream after 1.2.15
Patch18:    SDL-1.2.15-CVE-2019-7635-Reject-BMP-images-with-pixel-colors-ou.patch
# Reject 2, 3, 5, 6, 7-bpp BMP images (related to CVE-2019-7635),
# bug #1677159, upstream bug #4498, in upstream after 1.2.15
Patch19:    SDL-1.2.15-Reject-2-3-5-6-7-bpp-BMP-images.patch
# Fix CVE-2019-7577 (Fix a buffer overread in MS_ADPCM_nibble and
# MS_ADPCM_decode on an invalid predictor), bug #1676510, upstream bug #4492,
# in upstream after 1.2.15
Patch20:    SDL-1.2.15-CVE-2019-7577-Fix-a-buffer-overread-in-MS_ADPCM_nibb.patch
# Fix retrieving an error code after stopping and resuming a CD-ROM playback,
# upstream bug #4108, in upstream after 1.2.15
Patch21:    SDL-1.2.15-Fixed-bug-4108-Missing-break-statements-in-SDL_CDRes.patch
# Fix SDL_Surface reference counter initialization and a possible crash when
# opening a mouse device when using a framebuffer video output, bug #1602687
Patch22:    SDL-1.2.15-fix-small-errors-detected-by-coverity.patch
# Fix Windows drivers broken with a patch for CVE-2019-7637, bug #1677152,
# upstream bug #4497, in upstream after 1.2.15
Patch23:    SDL-1.2.15-fix_copy_paste_mistakes_in_commit_9b0e5c555c0f.patch
# Fix CVE-2019-13616 (a heap buffer over-read in BlitNtoN), bug #1747237,
# upstream bug #4538, in upstream after 1.2.15
Patch24:    SDL-1.2.15-CVE-2019-13616-validate_image_size_when_loading_BMP_files.patch

BuildRequires:  alsa-lib-devel
%if %{with arts}
BuildRequires:  arts-devel
%endif
BuildRequires:  coreutils
%if %{with esound}
BuildRequires:  esound-devel
%endif
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  make
%if %{with nas}
BuildRequires:  nas-devel
%endif
%ifarch %{ix86}
BuildRequires:  nasm
%endif
BuildRequires:  pulseaudio-libs-devel
%if %{with esound}
BuildRequires:  sed
%endif
# Autotools
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:    Files needed to develop Simple DirectMedia Layer applications
Requires:   SDL%{?_isa} = %{version}-%{release}
Requires:   alsa-lib-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:    Files needed to develop static Simple DirectMedia Layer applications
Requires:   SDL-devel%{?_isa} = %{version}-%{release}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the static libraries needed for developing static SDL
applications.

%prep
%setup -q -b0
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
for F in CREDITS; do 
    iconv -f iso8859-1 -t utf-8 < "$F" > "${F}.utf"
    touch --reference "$F" "${F}.utf"
    mv "${F}.utf" "$F"
done
%if %{without esound}
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.in
%endif

%build
aclocal
libtoolize
autoconf
%configure \
    --enable-video-opengl \
    --disable-video-svga \
    --disable-video-ggi \
    --disable-video-aalib \
    --enable-sdl-dlopen \
%if %{with arts}
    --enable-arts-shared \
%else
    --disable-arts \
%endif
%if %{with esound}
    --enable-esd-shared \
%else
    --disable-esd \
%endif
%if %{with nas}
    --enable-nas-shared \
%else
    --disable-nas \
%endif
    --enable-pulseaudio-shared \
    --enable-alsa \
    --disable-video-ps3 \
    --disable-rpath
%{make_build}

%install
%{make_install}

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}/%{_includedir}/SDL/SDL_config.h %{buildroot}/%{_includedir}/SDL/SDL_config-%{_arch}.h
install -m644 %{SOURCE3} %{buildroot}/%{_includedir}/SDL/SDL_config.h

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la

%files
%license COPYING
%doc BUGS CREDITS README-SDL.txt
%{_libdir}/libSDL-1.2.so.*

%files devel
%doc README docs.html docs/html docs/index.html TODO WhatsNew
%{_bindir}/*-config
%{_libdir}/libSDL.so
%{_libdir}/pkgconfig/sdl.pc
%{_includedir}/SDL
%{_datadir}/aclocal/*
%{_mandir}/man1/*
%{_mandir}/man3/SDL*.3*

%files static
%{_libdir}/lib*.a

%changelog
* Thu Mar 25 2021 Henry Li <lihl@microsoft.com> - 1.2.15-44
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove x11 and graphics-related dependencies

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-42
- Fix CVE-2019-13616 (a heap buffer over-read in BlitNtoN) (bug #1747237)

* Fri Aug 02 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-41
- Fix Windows drivers broken with a patch for CVE-2019-7637 (bug #1677152)
- Update URL to use secured HTTP protocol

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-39
- Fix retrieving an error code after stopping and resuming a CD-ROM playback
  (upstream bug #4108)
- Fix SDL_Surface reference counter initialization and a possible crash when
  opening a mouse device when using a framebuffer video output (bug #1602687)

* Tue Mar 12 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-38
- Fix CVE-2019-7577 completely (a buffer overread in MS_ADPCM_nibble and
  MS_ADPCM_decode on an invalid predictor) (bug #1676510)

* Fri Feb 15 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-37
- Fix CVE-2019-7577 (a buffer overread in MS_ADPCM_decode) (bug #1676510)
- Fix CVE-2019-7575 (a buffer overwrite in MS_ADPCM_decode) (bug #1676744)
- Fix CVE-2019-7574 (a buffer overread in IMA_ADPCM_decode) (bug #1676750)
- Fix CVE-2019-7572 (a buffer overread in IMA_ADPCM_nibble) (bug #1676754)
- Fix CVE-2019-7572 (a buffer overwrite in IMA_ADPCM_nibble) (bug #1676754)
- Fix CVE-2019-7573, CVE-2019-7576 (buffer overreads in InitMS_ADPCM)
  (bugs #1676752, #1676756)
- Fix CVE-2019-7578 (a buffer overread in InitIMA_ADPCM) (bug #1676782)
- Fix CVE-2019-7638, CVE-2019-7636 (buffer overflows when processing BMP
  images with too high number of colors) (bugs #1677144, #1677157)
- Fix CVE-2019-7637 (an integer overflow in SDL_CalculatePitch) (bug #1677152)
- Fix CVE-2019-7635 (a buffer overread when blitting a BMP image with pixel
  colors out the palette) (bug #1677159)
- Reject 2, 3, 5, 6, 7-bpp BMP images (bug #1677159)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Petr Pisar <ppisar@redhat.com> - 1.2.15-35
- Remove manual updating of config.{guess,sub} - this has been part of
  %%configure since 2013
- Use system glext.h to prevent from clashing on a GL_GLEXT_VERSION definition
  (bug #1662778)

* Tue Aug 28 2018 Petr Pisar <ppisar@redhat.com> - 1.2.15-34
- Remove useless build-time dependency on audiofile-devel

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 27 2018 David Abdurachmanov <david.abdurachmanov@gmail.com> - 1.2.15-32
- Add riscv64 to SDL_config.h

* Thu Mar 22 2018 Petr Pisar <ppisar@redhat.com> - 1.2.15-31
- Remove post scriptlets with ldconfig

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Petr Pisar <ppisar@redhat.com> - 1.2.15-29
- Fix vec_perm() usage on little-endian 64-bit PowerPC (bug #1392465)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.2.15-27
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Petr Pisar <ppisar@redhat.com> - 1.2.15-25
- Rebuild with newer GCC to fix miscompilation on PowerPC (bug #1427880)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Petr Pisar <ppisar@redhat.com> - 1.2.15-23
- Enable setting gamma by programing palette as supported by xorg-server
  1.19.0 again (bug #891973)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 22 2015 Petr Pisar <ppisar@redhat.com> - 1.2.15-20
- Enable support for ESound

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 1.2.15-19
- Add support for MIPS architecture to SDL_config.h
- Disable support for ESound

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Petr Pisar <ppisar@redhat.com> - 1.2.15-16
- Fix processing keyboard events if SDL_EnableUNICODE() is enabled
  (bug #1126136)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Petr Pisar <ppisar@redhat.com> - 1.2.15-14
- Do not harness backing store by default. Export SDL_VIDEO_X11_BACKINGSTORE
  environment variable to enable it. (bug #1073057)

* Fri Jan 17 2014 Petr Pisar <ppisar@redhat.com> - 1.2.15-13
- Add support for ppc64le architecture (bug #1054397)

* Thu Dec 05 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-12
- Ignore joystick axis events if they aren't in a sane range (bug #990677)

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-11
- Fix a typo in controlling NAS support

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-10
- Add esound and arts support (bug #851349)
- Add NAS support

* Wed Jun 19 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-9
- Add sdl-config(1) manual page (bug #948864)

* Thu May 23 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-8
- Update header files to support aarch64 (bug #966115)

* Wed Mar 27 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-7
- Update config.sub to support aarch64 (bug #926510)
- Adapt to libX11-1.5.99.901

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15-5
- Work around bug in Xorg to allow changing gamma on X11 (bug #891973)

* Mon Sep 10 2012 Petr Pisar <ppisar@redhat.com> - 1.2.15-4
- GL and GLU headers have been moved to mesa-GL-devel and mesa-GLU-devel

* Thu Aug 23 2012 Matthias Clasen <mclasen@redhat.com> - 1.2.15-3
- Drop esound and arts support (bug #851349)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Petr Pisar <ppisar@redhat.com> - 1.2.15-1
- Beautify spec code
- 1.2.15 bump

* Thu Jan 19 2012 Petr Pisar <ppisar@redhat.com> - 1.2.14-16
- Replace my patch with upstream one (bug #782251)

* Tue Jan 17 2012 Petr Pisar <ppisar@redhat.com> - 1.2.14-15
- Restore compatibility with libX11-1.4.99.1 (bug #782251)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 26 2011 Petr Pisar <ppisar@redhat.com> - 1.2.14-13
- Don't block SDL_WM_GrabInput() if window is not viewable (bug #480065)

* Thu Feb 24 2011 Petr Pisar <ppisar@redhat.com> - 1.2.14-12
- Adapt to nasm-2.09 (bug #678818)

* Fri Feb 18 2011 Petr Pisar <ppisar@redhat.com> - 1.2.14-11
- Correct patch application
- Make intradependecies architecture specific

* Fri Feb 18 2011 Petr Pisar <ppisar@redhat.com> - 1.2.14-10
- Do not call memcpy() on overlapping areas (bug #669844)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 16 2010 Petr Pisar <ppisar@redhat.com> - 1.2.14-8
- Kernel joystick structure has grown in unknown 2.6 Linux version (rh624241,
  sdl900)

* Thu Aug 12 2010 Petr Pisar <ppisar@redhat.com> - 1.2.14-7
- Fix left button press event in windowed mode (rh556608, sdl894)
- Remove unrecognized --disable-debug and --enable-dlopen configure options
  (rh581056)

* Mon Aug 02 2010 Petr Pisar <ppisar@redhat.com> - 1.2.14-6
- Make repacked source tar ball relative
- Remove useless src/joystick/darwin/10.3.9-FIX/IOHIDLib.h because of APSL-2.0
  license
- Apply SDL-1.2.14-xio_error-rh603984.patch (rh603984, sdl1009)
- Escape spec file comments
- Convert CREDITS to UTF-8

* Wed Jun 23 2010 Hans de Goede <hdegoede@redhat.com> 1.2.14-5
- Don't crash when trying to exit because of an xio-error (rh603984, sdl1009)

* Wed Mar 24 2010 Thomas Woerner <twoerner@redhat.com> 1.2.14-4
- added repackage.sh script to remove joyos2,h and symbian.zip because of
  licensing problems
- added comment about riva_mmio.h license

* Tue Feb 16 2010 Josh Boyer <jwboyer@gmail.com> 1.2.14-3
- disable ps3 video support that was added in 2.14.  It fails to
  build on ppc/ppc64

* Fri Feb 12 2010 Thomas Woerner <twoerner@redhat.com> 1.2.14-2
- fixed build for libtool 2.2.6 in F-13 (rhbz#555501)

* Tue Oct 27 2009 Thomas Woerner <twoerner@redhat.com> 1.2.14-1
- new version 1.2.14
- dropped patches for upstream fixes: libdir, dynamic-esd, x11dyn64,
  dynamic-pulse, pa-rewrite, rh484362 and rh487720

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr  7 2009 Thomas Woerner <twoerner@redhat.com> 1.2.13-9
- fixed qemu-kvm segfaults on startup in SDL_memcpyMMX/SSE (rhbz#487720)
  upstream patch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Hans de Goede <hdegoede@redhat.com> 1.2.13-7
- Rewrite pulseaudio support to stop the crackle crackle with the
  new glitch free pulseaudio, this also gives us much better latency,
  as good as with directly using alsa (rh 474745, sdl 698)
- Workaround an obscure bug in the inline-asm revcpy function (by disabling it) 
  This fixes Ri-li crashing on i386 (rh 484121, rh 484362, sdl 699)

* Tue Sep  2 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-6
- dropped pulseaudio hack (rhbz#448270)
- pulseaudio is now used by default
- simplified spec file for new architecture support (rhbz#433618)

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.13-5
- fix license tag

* Wed May 28 2008 Dennis Gilmore <dennis@ausil.us> 1.2.13-4
- fix sparc multilib handling

* Mon Apr  7 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-3
- updated PulseAudio driver (rhbz#439847)
  Thanks to Lennart Poettering for the patch

* Fri Feb  1 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-2
- new static sub package for static libraries

* Mon Jan  7 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-1
- new version 1.2.13
  - fixes i810 video overlay problem (rhbz#310841)
  - fixes c++ style comments in header files (rhbz#426475)
- review fixes: spec file cleanup, dropped static libs (rhbz#226402)
- fixed pulseaudio hack scripts from Warren for multilib systems (rhbz#426579)
- fixed pulseaudio detection in configure to enable dynamic use of pulseaudio
  libraries

* Fri Dec 21 2007 Warren Togami <wtogami@redhat.com> 1.2.12-5
- correct stupid mistake that broke SDL-devel
  RPM should error out if a SourceX is defined twice...

* Wed Dec 19 2007 Warren Togami <wtogami@redhat.com> 1.2.12-4
- Build with --enable-pulseaudio-shared for testing purposes (#343911)
  It is known to not work in some cases, so not enabled by default.
- Move pulseaudio enabler hack from SDL_mixer (#426275)
- Make pulseaudio enabler hack conditional.  It will only attempt to use it if
  alsa-plugins-pulseaudio is installed.

* Tue Nov  6 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-3
- fixed latest multiarch conflicts: dropped libdir from sdl-config completely
  (rhbz#343141)

* Tue Aug 28 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-2
- use uname -m in multilib patch instead of arch

* Mon Aug 27 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-1
- new version 1.2.12
  fixes TEXTRELs (rhbz#179407)
- added arm support (rhbz#245411)
  Thanks to Lennert Buytenhek for the patch
- added alpha support (rhbz#246463)
  Thanks to Oliver Falk for the patch
- disabled yasm for SDL (rhbz#234823)
  Thanks to Nikolay Ulyanitsky for the patch

* Tue Mar 20 2007 Thomas Woerner <twoerner@redhat.com> 1.2.11-2
- use X11 dlopen code for 64 bit architectures (rhbz#207903)

* Mon Mar 19 2007 Thomas Woerner <twoerner@redhat.com> 1.2.11-1
- new version 1.2.11
- fixed man page SDL_ListModes (rhbz#208212)
- fixed spurious esound, audiofile dependencies (rhbz#217389)
  Thanks to Ville Skyttä for the patch
- dropped requirements for imake and libXt-devel (rhbz#226402)
- made nasm arch %%{ix86} only (rhbz#226402)
- dropped O3 from options (rhbz#226402)
- dropped tagname environment variable (rhbz#226402)

* Thu Nov  2 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-9
- fixed arch order in SDL_config.h wrapper

* Fri Oct 27 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-8
- fixed multilib conflicts for SDL (#212288)

* Wed Jul 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6.2
- setting the X11 lib and include paths hard to get shared X11 support on all
  architectures

* Wed Jul 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6.1
- added build requires for automake and autoconf

* Tue Jul 25 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6
- dropped libXt build requires, because libSDL does not need libXt at all - 
  this was an autofoo bug (fixed already)
- fixed multilib devel conflicts (#192749)
- added buidrequires for imake: AC_PATH_X needs imake currently

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.10-5
- rebuild
- use %%configure macro

* Tue Jun 20 2006 Christopher Stone <chris.stone@gmail.com> 1.2.10-4
- added missing (build) requires for libXt libXrender libXrandr
- remove %%makeinstall macro (bad practice)
- use %%{buildroot} macro consistantly

* Tue Jun  6 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-2
- added missing (build) requires for GL and GLU

* Mon May 22 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-1
- new version 1.2.10
- dropped the following patches because they are not needed anymore:
  ppc_modes, gcc4, yuv_mmx_gcc4 and no_exec_stack
- new pagesize patch (drop PAGE_SIZE, use sysconf(_SC_PAGESIZE) instead)

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-5
- added upstream no exec stack patch

* Thu Jan 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-4
- prefer alsa sound output, then artsd and esd

* Tue Jan 24 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-3
- dropped libtool .la files from devel package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Thomas Woerner <twoerner@redhat.com> 1.2.9-2.1
- fixed build requires

* Tue Nov 15 2005 Warren Togami <wtogami@redhat.com> 1.2.9-2
- -devel req actual X libs

* Mon Nov  7 2005 Thomas Woerner <twoerner@redhat.com> 1.2.9-1
- new version 1.2.9 with additional gcc4 fixes
- using xorg-x11-devel instead of XFree86-devel

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 1.2.8-3.2
- fix configure script for libdir so library deps are identical on all
  arches (#158346)

* Thu Apr 14 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-3.1
- new version of the gcc4 fix

* Tue Apr 12 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-3
- fixed gcc4 compile problems
- fixed x86_64 endian problem

* Wed Feb  9 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-2
- rebuild

* Fri Dec 17 2004 Thomas Woerner <twoerner@redhat.com> 1.2.8-1
- new version 1.2.8

* Thu Oct 14 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-8
- added patch from SDL CVS for arts detection/initialization problem (#113831)

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-7.1
- moved to new autofoo utils

* Fri Jul  9 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-7
- fixed resolution switching for ppc (#127254)

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-6
- fixed gcc34 build problems

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-4
- added requires for alsa-lib-devel (#123374)

* Wed Mar 31 2004 Harald Hoyer <harald@redhat.com> - 1.2.7-3
- fixed gcc34 compilation issues

* Wed Mar 10 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-2.1
- added buildrequires for alsa-lib-devel
- now using automake 1.5

* Tue Mar  9 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-2
- Fixed SDL requires for devel package

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt
- Revive SDL-ppc64.patch

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-1
- new version 1.2.7

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 1.2.6-3.1
- disabled several video modes, hopefuilly fixes (#113831)

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 1.2.6-3
- fix for alsa 1.0

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 1.2.6-2
- removed rpath
- using O3 instead of O2, now (SDL_RLEaccel.c compile error)
- added BuildRequires for nasm

* Tue Sep  2 2003 Thomas Woerner <twoerner@redhat.com> 1.2.6-1
- new version 1.2.6

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 1.2.5-9
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  4 2003 Than Ngo <than@redhat.com> 1.2.5-7
- fix build problem with gcc 3.3
- clean up specfile

* Mon May 19 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-5
- rebuild

* Tue Apr 15 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-4
- X11 modes fix (use more than 60 Hz, when possible)

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 1.2.5-3.5
- ppc64 fix

* Mon Feb 10 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-3
- added -fPIC to LDFLAGS

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Thomas Woerner <twoerner@redhat.com> 1.2.5-1
- new version 1.2.5
- disabled conflicting automake16 patch
- dgavideo modes fix (#78861)

* Sun Dec 01 2002 Elliot Lee <sopwith@redhat.com> 1.2.4-7
- Fix unpackaged files by including them.
- _smp_mflags

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.2.4-6
- remove unpackaged files from the buildroot
- lib64'ize

* Sat Jul 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require nasm for mainframe

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-4
- Fix bug #67255

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-1
- 1.2.4
- Fix build with automake 1.6

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-7
- Fix AM_PATH_SDL automake macro with AC_LANG(c++) (#60533)

* Thu Feb 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-6
- Rebuild in current environment

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-5
- dlopen() aRts and esd rather than linking directly to them.
- make sure aRts and esd are actually used if they're running.

* Mon Jan 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-4
- Don't crash without xv optimization: BuildRequire a version of nasm that
  works.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Dec 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-2
- Rebuild with new aRts, require arts-devel rather than kdelibs-sound-devel
- Temporarily exclude alpha (compiler bugs)

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-1
- 1.2.3

* Sat Nov 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-5
- Add workaround for automake 1.5 asm bugs

* Tue Oct 30 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-4
- Make sure -fPIC is used on all architectures (#55039)
- Fix build with autoconf 2.5x

* Fri Aug 31 2001 Bill Nottingham <notting@redhat.com> 1.2.2-3
- rebuild (fixes #50750??)

* Thu Aug  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-2
- SDL-devel should require esound-devel and kdelibs-sound-devel (#44884)

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-1
- Update to 1.2.2; this should fix #47941
- Add build dependencies

* Tue Jul 10 2001 Elliot Lee <sopwith@redhat.com> 1.2.1-3
- Rebuild to eliminate libXv/libXxf86dga deps.

* Fri Jun 29 2001 Preston Brown <pbrown@redhat.com>
- output same libraries for sdl-config whether --libs or --static-libs 
  selected.  Fixes compilation of most SDL programs.
- properly packaged new HTML documentation

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.1-1
- 1.2.1

* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.0-2
- Add Bill's byteorder patch

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2.0

* Tue Feb 27 2001 Karsten Hopp <karsten@redhat.de>
- SDL-devel requires SDL

* Tue Jan 16 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Require arts rather than kdelibs-sound

* Sun Jan  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.7

* Tue Oct 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.6

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- build against new DGA
- update to 1.1.4, remove patches (they're now in the base release)

* Tue Aug  1 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- %%post -p /sbin/ldconfig (Bug #14928)
- add URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- replace patch that fell out of SRPM

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths
- use 1.1 (development) version; everything even from Loki links to it!

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- autoconf fixes for ia64

* Mon Apr 24 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.8

* Tue Feb 15 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.4, fixes problems when run in 8bpp

* Tue Feb 01 2000 Tim  Powers <timp@redhat.com>
- applied patch from Hans de Goede <hans@highrise.nl> for fullscreen toggling.
- using  --enable-video-x11-dgamouse since it smoothes the mouse some.

* Sun Jan 30 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.3, bugfix update

* Fri Jan 28 2000 Tim Powers <timp@redhat.com>
- fixed group etc

* Fri Jan 21 2000 Tim Powers <timp@redhat.com>
- build for 6.2 Powertools

* Wed Jan 19 2000 Sam Lantinga <slouken@devolution.com>
- Re-integrated spec file into SDL distribution
- 'name' and 'version' come from configure 
- Some of the documentation is devel specific
- Removed SMP support from %%build - it doesn't work with libtool anyway

* Tue Jan 18 2000 Hakan Tandogan <hakan@iconsult.com>
- Hacked Mandrake sdl spec to build 1.1

* Sun Dec 19 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Sat Dec 18 1999 John Buswell <johnb@mandrakesoft.com>
- Add symlink for libSDL-1.0.so.0 required by sdlbomber
- Added docs

* Thu Dec 09 1999 Lenny Cartier <lenny@mandrakesoft.com>
- v 1.0.0

* Mon Nov  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First spec file for Mandrake distribution.

# end of file
