Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A general purpose sound file conversion tool
Name: sox
# A mistake in naming, 14.4.2rc2 breaks upgrade path.
# This workaround will go away with rebase to 14.4.3
# it affects Source, %%prep and Version
Version: 14.4.2.0
Release: 33%{?dist}
License: GPLv2+ and LGPLv2+ and MIT
# Modified source tarball with libgsm license, without unlicensed liblpc10:
# _Source: https://downloads.sourceforge.net/%%{name}/%%{name}-%%{version}.tar.gz
# _Source: %%{name}/%%{name}-%%{version}.modified.tar.gz
# _Source: %%{name}/%%{name}-14.4.2.modified.tar.bz2
Source0: https://github.com/i386x/sox-downstream/archive/%{name}-%{version}.modified.tar.gz
URL: https://sox.sourceforge.net/
# 0000 - 0099: General:
Patch0: sox-14.4.2-lsx_symbols.patch
Patch1: sox-14.4.2-lpc10.patch
Patch2: sox-14.4.2-fsf_address_fix.patch
# 0100 - 0999: Extensions:
# - no extensions yet
# 1000 - 8999: Bug fixes:
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1500570
# - upstream discussion: https://sourceforge.net/p/sox/mailman/sox-devel/thread/CAG_ZyaD8huzEm9cajDd63z1nGOTVRw=Y8vPE-t5pHB=9XmQ_Xw@mail.gmail.com/#msg36124536
# - patch origin: https://bogomips.org/sox.git/patch/?id=818bdd0ccc1e5b6cae742c740c17fd414935cf39
# - security fix for CVE-2017-15371
Patch1000: sox-14.4.2-bug_1500570_fix.patch
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1500554
# - upstream discussion: https://sourceforge.net/p/sox/mailman/sox-devel/thread/CAG_ZyaDcmDNEHRr2WBR2fPcXtu_kd5OdpRVTbhDe1YQZQA2c9w@mail.gmail.com/#msg36103130
# - patch origin: https://github.com/mansr/sox/commit/ef3d8be0f80cbb650e4766b545d61e10d7a24c9e.patch
# - security fix for CVE-2017-15370
Patch1001: sox-14.4.2-bug_1500554_fix.patch
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1500553
# - upstream discussion: https://sourceforge.net/p/sox/mailman/sox-devel/thread/CAG_ZyaBLxUKk_xmrvn2YfnVLNRE_Rzxe+cYBC5CJtK_xWrVvNw@mail.gmail.com/#msg36121067
# - patch origin: https://bogomips.org/sox.git/patch/?id=3f7ed312614649e2695b54b398475d32be4f64f3
# - security fix for CVE-2017-15372
Patch1002: sox-14.4.2-bug_1500553_fix.patch
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1510923
# - upstream discussion: https://sourceforge.net/p/sox/mailman/sox-devel/thread/CAG_ZyaA_WyTTEWeGYPUhG95M3wOv64vTqn8jeH4JYvgMnx83Tw@mail.gmail.com/#msg36128861
# - patch origin: https://sourceforge.net/p/sox/mailman/sox-devel/thread/20171120110535.14410-1-mans@mansr.com/#msg36129559
# - security fix for CVE-2017-15642
Patch1003: sox-14.4.2-bug_1510923_fix.patch
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1558887
# - upstream discussion: https://sourceforge.net/p/sox/bugs/308/
Patch1004: sox-14.4.2-hcom_stopwrite_big_endian_bug_fix.patch
# -rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1309426 [CLOSED DUPL]
#        https://bugzilla.redhat.com/show_bug.cgi?id=1226675
#        https://bugzilla.redhat.com/show_bug.cgi?id=1540762 [CLOSED DUPL]
#        https://bugzilla.redhat.com/show_bug.cgi?id=1492910 [CLOSED DUPL]
# - upstream discussion: https://sourceforge.net/p/sox/bugs/309/
Patch1005: sox-14.4.2-bug_1226675_fix.patch
# - security fix for CVE-2017-11332
#   * rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1480674
#   * upstream commit: https://sourceforge.net/p/sox/code/ci/6e177c455fb554327ff8125b6e6dde1568610abe/
# - security fix for CVE-2017-11358
#   * rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1480675
#   * upstream commit: https://sourceforge.net/p/sox/code/ci/e410d00c4821726accfbe1f825f2def6376e181f/
# - security fix for CVE-2017-11359
#   * rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1480676
#   * upstream commit: https://sourceforge.net/p/sox/code/ci/7b3f30e13e4845bafc93215a372c6eb7dcf04118/
# - rhbz tracker: https://bugzilla.redhat.com/show_bug.cgi?id=1480678
# - upstream discussion: https://sourceforge.net/p/sox/bugs/296/
Patch1006: sox-14.4.2-bug_1480678_fix.patch
# - rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1545867
# - upstream patch: https://sourceforge.net/p/sox/mailman/sox-devel/thread/20180426131552.29249-9-mans@mansr.com/#msg36303839
# - security fix for CVE-2017-18189
Patch1007: sox-14.4.2-bug_1545867_fix.patch
# 9000 - 9999: Tests:
Patch9000: sox-14.4.2-installcheck_fix.patch
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/IJFYI5Q2BYZKIGDFS2WLOBDUSEGWHIKV/
BuildRequires: make
BuildRequires: gcc
BuildRequires: libvorbis-devel
BuildRequires: alsa-lib-devel, libtool-ltdl-devel, libsamplerate-devel
BuildRequires: gsm-devel, wavpack-devel, ladspa-devel, libpng-devel
BuildRequires: flac-devel, libao-devel, libsndfile-devel, libid3tag-devel
BuildRequires: pulseaudio-libs-devel, opusfile-devel
BuildRequires: libtool, libmad-devel, lame-devel, twolame-devel

%description
SoX (Sound eXchange) is a sound file format converter. SoX can convert
between many different digitized sound formats and perform simple
sound manipulation functions, including sound effects.

%package -n  sox-devel
Summary: The SoX sound file format converter libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n sox-devel
This package contains the library needed for compiling applications
which will use the SoX sound file format converter.

%prep
%setup -q -n %{name}-downstream-%{name}-%{version}.modified
%patch 0 -p1
%patch 1 -p1 -b .lpc
%patch 2 -p1
%patch 1000 -p1
%patch 1001 -p1
%patch 1002 -p1
%patch 1003 -p1
%patch 1004 -p1
%patch 1005 -p1
%patch 1006 -p1
%patch 1007 -p1
%patch 9000 -p1
#regenerate scripts from older autoconf to support aarch64
autoreconf -vfi

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%configure --without-lpc10 \
           --with-gsm \
           --includedir=%{_includedir}/sox \
           --disable-static \
           --with-distro=Fedora \
           --with-dyn-default

%make_build

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libsox.la
rm -f $RPM_BUILD_ROOT%{_libdir}/sox/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/sox/*.a

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %doc}
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox
%{_bindir}/soxi
%{_libdir}/libsox.so.*
%dir %{_libdir}/sox/
%{_libdir}/sox/libsox_fmt_*.so
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n sox-devel
%{_includedir}/sox
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_mandir}/man3/*


%changelog
* Mon Mar 06 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 14.4.2.0-33
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License Verified

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-28
- fix CVE-2017-18189
  resolves #1545867

* Wed Jan 29 2020 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-27
- remove %%check (we use Fedora CI instead in a future)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Richard Shaw <hobbes1069@gmail.com> - 14.4.2.0-23
- Add twolame-devel to build requirements now that it's in Fedora.

* Wed Jun 06 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-22
- added patch that fixes:
  + "divide by zero in startread function in wav.c" (CVE-2017-11332)
  + "invalid memory read in read_samples function in hcom.c" (CVE-2017-11358)
  + "divide by zero in wavwritehdr function in wav.c" (CVE-2017-11359)
  resolves #1480674, #1480675, #1480676, and #1480678

* Sat Jun 02 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-21
- fix hunks in patches
- prevents division by zero in src/ao.c
  + fixes/prevents "sox killed by SIGFPE (signal 8)" kind of bugs that appear
    randomly, depending on reporter's HW/environment/OS components
  + related bugs: #1309426, #1226675, #1540762, #1492910

* Wed Mar 21 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-20
- added patch that fixes WAV to HCOM conversion abortion on 64 bit big endian
  machines
  + resolves #1558887

* Mon Mar 19 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-19
- CVEs presence tests beakerized and moved to tests/ directory as CI tests
- %%check section: creating of additional binaries for testing was replaced
  by the libsox binary patch workaround hack; during the testing the hardcoded
  path to the directory with sox plugins is replaced for non-root alternative
  and hence running the tests under the mock is possible (before the binary
  patching, the backup of libsox is made, and at the end of tests it is
  restored); this decrease the build time of the package, but may increase the
  fragility of the package build process (future features in gcc toolchain may
  make the binary patching impossible/not working)

* Thu Feb 22 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-18
- Added missing gcc dependency

* Tue Feb 06 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-17
- SOX_PLUGINS environment variable is now used only while running %%check
  during the package building; SOX_PLUGINS are now no longer available to
  users

* Thu Feb 01 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-16
- added patch that disables hcom conversion tests on big endian architectures
  due to SIGABRT issues

* Tue Jan 30 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-15
- added patch that fixes stack-overflow vulnerability in lsx_ms_adpcm_block_expand_i (CVE-2017-15372)
  + resolves #1500553, #1510919
- added patch that fixes use-after-free in lsx_aiffstartread (CVE-2017-15642)
  + resolves #1510923
- added patch that fixes incorrect FSF address in src/ladspa.h
- added patch that introduces SOX_PLUGINS environment variable that overrides
  standard sox location for plugins
- added patch that inserts $(DESTDIR) before ${bindir} in src/Makefile.am
  installcheck target
- added tests that checks if previously fixed bugs remain fixed in newer releases
- spec file changes:
  + suppressed rpmlint warning about bad Source URL
  + added comments to security patches
  + in %%description: added missing sentence period
  + in %%prep: suppressed "%%setup is not quite" rpmlint warning
  + in %%install: removed redundant slashes before %%{_libdir}
  + added %%check section

* Wed Jan 10 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-14
- add patch to fix the heap-based buffer overflow in the ImaExpandS function (CVE-2017-15370)
- resolves #1500554, #1510917
- sanitized macro-in-comment rpmlint warnings

* Wed Jan 03 2018 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-13
- add patch to fix reachable assertion abort in function sox_append_comment (CVE-2017-15371)
- resolves #1500570, #1510918

* Tue Dec 19 2017 Jiri Kucera <jkucera@redhat.com> - 14.4.2.0-12
- .gz suffix changed to .bz2 since the source archive is bzipped

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2.0-9
- built with lame-devel

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2.0-7
- play mp3 using libmad

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14.4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2.0-5
- temporary change in versioning to fix broken upgrade path

* Tue Nov 10 2015 Richard Shaw <hobbes1069@gmail.com> - 14.4.2-4
- Expose required lsx_* symbols so all plugins can build dynamically.
- Minor spec fixes for merge review, RHBZ#226425.

* Wed Aug 19 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2-3
- play opus files (added dependency on opusfile)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2-1
- rebase

* Thu Feb 12 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.2rc2-1
- rebase to rc because of https://access.redhat.com/security/cve/CVE-2014-8145
- with-dyn-default broken, link oss and flac statically

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jul 25 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-4
- removed liblpc10 from source tarball due to licensing uncertainity
- added license file to libgsm
- fixed bogus dates in changelog

* Tue Apr 02 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-3
- added autoreconf to replace old scripts => support aarch64

* Fri Feb 15 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-2
- added sox-mcompand_clipping.patch to prevent integer overflow

* Thu Feb 14 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-1
- rebase to 14.4.1

* Tue Sep 18 2012 Honza Horak <hhorak@redhat.com> - 14.4.0-3
- Minor spec file fixes

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Honza Horak <hhorak@redhat.com> - 14.4.0-1
- updated to upstream version 14.4.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> 14.3.2-2
- Rebuild for libpng 1.5

* Sat Mar 19 2011 Felix Kaechele <heffer@fedoraproject.org> - 14.3.2-1
- 14.3.2
- added PulseAudio support

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 02 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 14.3.1-2
- rebuild

* Mon Apr 12 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 14.3.1-1
- updated to upstream version

* Fri Feb 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 14.3.0-2
- fixed license tag

* Mon Nov 23 2009 Jiri Moskovcak <jmoskovc@redhat.com> - 14.3.0-1
- 14.3.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.2.0-1
- 14.2.0

* Mon Nov 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-7.20081105cvs
- patch for newer libtool

* Mon Nov 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-6.20081105cvs
- rebuild for libtool

* Wed Nov  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-5.20081105cvs
- forgot to add libtool as a BR

* Wed Nov  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-4.20081105cvs
- update to 20081105 cvs checkout (fixes many bugs, no longer creates _fmt_*.so.*)
- move _fmt_*.so to main package so support for file formats no longer requires devel

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-3
- missed a few BR, this should be all of them

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-2
- enable the full set of functionality with missing BR

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 14.1.0-1
- fix license tag
- update to 14.1.0
- disabled static libs (if something really needs them, re-enable them
  in a -static subpackage)

* Wed Apr 16 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 14.0.1-2
- enabled flac support
- Resolves: #442703

* Mon Feb 25 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 14.0.1-1
- New version 14.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 14.0.0-2
- Autorebuild for GCC 4.3

* Mon Oct 29 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 14.0.0-1
- New version 14.0.0
- Thanks to Chris Bagwell <chris at cnpbagwell dot com> for initial changes to spec file

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 13.0.0-3
- Rebuild for selinux ppc32 issue.

* Mon Jul 16 2007 Jiri Moskovcak <jmoskovc@redhat.com> 13.0.0-2
- uses external libgsm instead of local copy
- spec file update: added BuildRequires: gsm-devel
- Resolves: #239955

* Mon Feb 26 2007 Thomas Woerner <twoerner@redhat.com> 13.0.0-1
- new version 13.0.0
- spec file cleanup (#227429)
- new ldconfig calls for post and postun

* Mon Jul 24 2006 Thomas Woerner <twoerner@redhat.com> 12.18.1-1
- new version 12.18.1
- fixed multilib devel conflict in libst-config (#192751)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 12.17.9-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 12.17.9-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 12.17.9-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 12.17.9-1
- new version 12.17.9

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu May 12 2005 Thomas Woerner <twoerner@redhat.com> 12.17.7-3
- fixed bad link for man/man1/rec.1.gz (#154089)
- using /usr/include instead of kernel-devel includes

* Tue Apr 26 2005 Warren Togami <wtogami@redhat.com> 12.17.7-2
- overflow patch (#155224 upstream)

* Sun Apr 17 2005 Warren Togami <wtogami@redhat.com> 12.17.7-1
- 12.17.7
- BR alsa-lib-devel (#155224 thias)

* Sun Feb 27 2005 Florian La Roche <laroche@redhat.com>
- Copyright: -> License:

* Mon Nov 22 2004 Thomas Woerner <twoerner@redhat.com> 12.17.6-1
- new version 12.17.6

* Wed Sep 15 2004 Thomas Woerner <twoerner@redhat.com> 12.17.5-3
- moved libst-config to devel package (#132489)

* Thu Aug 26 2004 Thomas Woerner <twoerner@redhat.com> 12.17.5-2
- fixed initialization bug in wav file handler (#130968)

* Thu Aug 19 2004 Thomas Woerner <twoerner@redhat.com> 12.17.5-1
- new version 12.17.5

* Fri Jul 23 2004 Bill Nottingham <notting@redhat.com> 12.17.4-4.fc2
- add patch for buffer overflow in wav code (CAN-2004-0557, #128158)

* Fri Jul  9 2004 Bill Nottingham <notting@redhat.com> 12.17.4-4
- add patch for 64-bit problem (#127502)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct  7 2003 Bill Nottingham <notting@redhat.com> 12.17.4-1
- update to 12.17.4
- ship soxmix (#102499)
- fix soxplay to handle files with spaces (#91144)
- use LFS (#79151)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Elliot Lee <sopwith@redhat.com> 12.17.3-10
- Add sox-vorberr.patch to fix segfault in #81448
- _smp_mflags

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 12.17.3-8
- remoive unpackaged files from the buildroot
- lib64'ize

* Thu Jul 18 2002 Bill Nottingham <notting@redhat.com>
- build against current libvorbis

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require gsm-devel as it has been excluded from rawhide

* Fri Jan  4 2002 Bill Nottingham <notting@redhat.com> 12.17.3-1
- update to 12.17.3

* Tue Dec  4 2001 Bill Nottingham <notting@redhat.com>
- update to 12.17.2

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- add patch to fix recording (#41755)
- fix license (#50574)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- rebuild against new gsm-devel

* Tue Jan  2 2001 Bill Nottingham <notting@redhat.com>
- re-enable gsm stuff
- update to 12.17.1

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- update to 12.17
- yank out gsm stuff

* Mon Aug  7 2000 Bill Nottingham <notting@redhat.com>
- fix playing of sounds on cards that don't support mono

* Sat Aug  5 2000 Bill Nottingham <notting@redhat.com>
- fix playing of sounds on cards that don't support 8-bit

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Feb 03 2000 Bill Nottingham <notting@redhat.com>
- fix manpage link the Right Way(tm)

* Thu Feb 03 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix rec manpage link - now that man pages are compressed, it should point to
  play.1.gz, not play.1

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Tue Sep 28 1999 Bill Nottingham <notting@redhat.com>
- Grrr. Arrrrgh. Fix link.

* Fri Sep 24 1999 Bill Nottingham <notting@redhat.com>
- add some more files to devel

* Fri Sep 17 1999 Bill Nottingham <notting@redhat.com>
- fix link

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- update to 12.16

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Jan 20 1999 Bill Nottingham <notting@redhat.com>
- allow spaces in filenames for play/rec

* Wed Dec  9 1998 Bill Nottingham <notting@redhat.com>
- fix docs

* Mon Nov 23 1998 Bill Nottingham <notting@redhat.com>
- update to 12.15

* Sat Oct 10 1998 Michael Maher <mike@redhat.com>
- fixed broken spec file

* Mon Jul 13 1998 Michael Maher <mike@redhat.com>
- updated source from Chris Bagwell.

* Tue Jun 23 1998 Michael Maher <mike@redhat.com>
- made patch to fix the '-e' option. BUG 580
- added buildroot

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Nov 06 1997 Erik Troan <ewt@redhat.com>
- built against glibc
