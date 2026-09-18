# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Run-time libraries and programs
Name: motif
Version: 2.3.8
Release: 2%{?dist}
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
Source: http://downloads.sf.net/motif/motif-%{version}.tar.gz
Source1: xmbind
URL: http://www.motifzone.net/
Obsoletes: openmotif < 2.3.4
Provides: openmotif = %{version}-%{release}
Requires: xorg-x11-xbitmaps

BuildRequires: make
BuildRequires: automake, libtool, autoconf, flex
BuildRequires: flex-static
BuildRequires: byacc, pkgconfig
BuildRequires: libjpeg-devel libpng-devel
BuildRequires: libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel
BuildRequires: xorg-x11-xbitmaps
BuildRequires: perl-interpreter

Patch22: motif-2.3.4-no_demos.patch
Patch23: openMotif-2.2.3-uil_lib.patch
Patch43: openMotif-2.3.0-rgbtxt.patch
Patch45: motif-2.3.4-mwmrc_dir.patch
Patch46: motif-2.3.4-bindings.patch
Patch47: openMotif-2.3.0-no_X11R6.patch
# FTBFS #1448819
Patch48: motif-2.3.4-Fix-issues-with-Werror-format-security.patch
Patch49: motif-configure-c99.patch
Patch50: motif-c99-void-sprintf.patch
Patch51: motif-c99-string.patch
# CVE-2023-43788
Patch55: 0001-Fix-CVE-2023-43788-Out-of-bounds-read-in-XpmCreateXp.patch
# CVE-2023-43789
Patch56: 0001-Fix-CVE-2023-43789-Out-of-bounds-read-on-XPM-with-co.patch
# https://sourceforge.net/p/motif/code/merge-requests/9/
Patch58: 0001-build-Check-for-Xinerama-availability.patch
Patch59: 0002-Xm-Display-Add-optional-Xinerama-support.patch
Patch60: 0003-Xm-MenuShell-Use-Xinerama-to-place-menus.patch
Patch61: 0004-Xm-DropDown-Use-Xinerama-for-placement.patch
Patch62: 0005-Xm-RCMenu-Use-Xinerama-for-placement.patch
Patch63: 0006-Xm-Tooltip-Use-Xinerama-for-placement.patch
Patch64: 0007-Xm-ComboBox-Use-Xinerama-for-placement.patch
# https://sourceforge.net/p/motif/code/merge-requests/10/
Patch65: 0001-Xm-String-Fix-memory-leak.patch
# https://sourceforge.net/p/motif/code/merge-requests/11/
Patch66:  0001-Xm-Screen-Add-_NET_WORKAREA-support.patch
Patch67:  0002-Xm-Screen-Add-_GTK_WORKAREAS-support-for-multi-monit.patch

Patch68: includes.patch

Conflicts: lesstif <= 0.92.32-6

%description
This is the Motif %{version} run-time environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif and the Motif Window Manager mwm.

%package devel
Summary: Development libraries and header files
Conflicts: lesstif-devel <= 0.92.32-6
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libjpeg-devel%{?_isa} libpng-devel%{?_isa}
Requires: libXft-devel%{?_isa} libXmu-devel%{?_isa} libXp-devel%{?_isa}
Requires: libXt-devel%{?_isa} libXext-devel%{?_isa}
Obsoletes: openmotif-devel < 2.3.4
Provides: openmotif-devel = %{version}-%{release}

%description devel
This is the Motif %{version} development environment. It includes the
header files and also static libraries necessary to build Motif applications.

%package static
Summary: Static libraries
Conflicts: lesstif-devel <= 0.92.32-6
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains the static Motif libraries.

%prep
%setup -q
%patch -P 22 -p1 -b .no_demos
%patch -P 23 -p1 -b .uil_lib
%patch -P 43 -p1 -b .rgbtxt
%patch -P 45 -p1 -b .mwmrc_dir
%patch -P 46 -p1 -b .bindings
%patch -P 47 -p1 -b .no_X11R6
%patch -P 48 -p1 -b .format-security
%patch -P 49 -p1
%patch -P 50 -p1
%patch -P 51 -p1
%patch -P 55 -p1
%patch -P 56 -p1
%patch -P 58 -p1 -b .xinerama
%patch -P 59 -p1 -b .xinerama
%patch -P 60 -p1 -b .xinerama
%patch -P 61 -p1 -b .xinerama
%patch -P 62 -p1 -b .xinerama
%patch -P 63 -p1 -b .xinerama
%patch -P 64 -p1 -b .xinerama
%patch -P 65 -p1 -b .utf8-memleak
%patch -P 66 -p1 -b .net-workarea
%patch -P 67 -p1 -b .gtk-workareas

%patch -P 68 -p1 -b .includes

%build
export CFLAGS="$CFLAGS -std=gnu17"
touch AUTHORS NEWS
autoreconf -fi
%configure --enable-static --enable-xft --enable-jpeg --enable-png

make clean %{?_smp_mflags}
make -C include
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}/etc/X11/xinit/xinitrc.d
install -m 755 %{SOURCE1} %{buildroot}/etc/X11/xinit/xinitrc.d/xmbind.sh

rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

%files
%doc COPYING README RELEASE RELNOTES
/etc/X11/xinit/xinitrc.d/xmbind.sh
%dir /etc/X11/mwm
%config(noreplace) /etc/X11/mwm/system.mwmrc
%{_bindir}/mwm
%{_bindir}/xmbind
%{_includedir}/X11/bitmaps/*
%{_libdir}/libMrm.so.*
%{_libdir}/libUil.so.*
%{_libdir}/libXm.so.*
%{_datadir}/X11/bindings
%{_mandir}/man1/mwm*
%{_mandir}/man1/xmbind*
%{_mandir}/man4/mwmrc*

%files devel
%{_bindir}/uil
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_libdir}/lib*.so
%{_mandir}/man1/uil.1*
%{_mandir}/man3/*
%{_mandir}/man5/*

%files static
%{_libdir}/lib*.a

%changelog
* Thu Dec 11 2025 Olivier Fourdan <ofourdan@redhat.com> - 2.3.8-2
- Fix memleak in XmString from:
  https://sourceforge.net/p/motif/code/merge-requests/10/
- Add NET_WORKAREA and GTK_WORKAREAS support from:
  https://sourceforge.net/p/motif/code/merge-requests/11/

* Thu Aug 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.3.8-1
- 2.3.8

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun  2 2025 Olivier Fourdan <ofourdan@redhat.com> - 2.3.4-38
- Add Xinerama support from https://sourceforge.net/p/motif/code/merge-requests/9/

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.3.4-36
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 14 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.3.4-34
- Drop xorg-x11-xinit dependency

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Florian Weimer <fweimer@redhat.com> - 2.3.4-32
- Backport upstream patch to fix incompatible-pointer-types issues

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 José Expósito <jexposit@redhat.com> - 2.3.4-30
- Fix CVE-2023-43788: out of bounds read in XpmCreateXpmImageFromBuffer()
- Fix CVE-2023-43789: out of bounds read on XPM with corrupted colormap

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 14 2023 Florian Weimer <fweimer@redhat.com> - 2.3.4-28
- Port to C99 (#2186773)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 03 2022 Adam Jackson <ajax@redhat.com> - 2.3.4-25
- Fix invoking autogen/configure so the default CFLAGS actually get applied

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Petr Šabata <contyk@redhat.com> - 2.3.4-13
- Fix issues with -Werror=format-security (#1448819)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.3.4-6
- fix missing BuildRequires flex-static (RHBZ#889175)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.3.4-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Oct 26 2012 Thomas Woerner <twoerner@redhat.com> 2.3.4-3
- do not use _isa for build requires

* Fri Oct 26 2012 Thomas Woerner <twoerner@redhat.com> 2.3.4-2
- fixed requirements according to review (RHBZ#870049)
- flex-static has been renamed to flex-devel with Fedora-18 and RHEL-7

* Thu Oct 25 2012 Thomas Woerner <twoerner@redhat.com> 2.3.4-1
- new version 2.3.4 with LGPL license
- fixed some rpmlint warnings
- new sub package for static libraries
- added /etc/X11/mwm directory
- removed defattrs

* Fri May 25 2012 Thomas Woerner <twoerner@redhat.com> 2.3.3-5
- dropped file requires for /usr/share/X11/XKeysymDB, not needed and not 
  available anymore
- added flex-static build requirement, because of flex package split

* Mon Aug 15 2011 Thomas Woerner <twoerner@redhat.com> 2.3.3-4
- fixed Label draws Xft text over border of its parent (rhbz#584300#c3)
  (MotifZone bug #1521 refixed)

* Wed Aug 10 2011 Thomas Woerner <twoerner@redhat.com> 2.3.3-3
- fixed regression introduced with upstream FIX #1521 (rhbz#729346)

* Mon Aug  1 2011 Thomas Woerner <twoerner@redhat.com> 2.3.3-2
- fixed LabelGadget draws background over border of its parent (rhbz#584300)
  (MotifZone bug #1517)
- fixed LabelGadget draws Xft text over border of its parent (rhbz#584300#c3)
  (MotifZone bug #1521)

* Tue Mar 23 2010 Thomas Woerner <twoerner@redhat.com> 2.3.3-1
- new version 2.3.3 (bugfix release)
  see RELNOTES file for the list of the bug fixes

* Fri Feb 26 2010 Thomas Woerner <twoerner@redhat.com> 2.3.2-1.1
- fixes according to review:
- fixed buildroot
- removed dot from summary
- removed dist tag from changelog
- added source download link

* Wed Jan 13 2010 Thomas Woerner <twoerner@redhat.com> 2.3.2-1
- new version 2.3.2 with upstream bug fixes: #1212, #1277, #1473, #1476
- spec file cleanup
- make build work with libtool
- all man pages are utf-8, no need to convert them anymore
- enabled EditRes support with upstream fix
- fixed parallel build
- fixed patches for fuzz 0
  Related: rhbz#543948

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-3.1
- Rebuilt for RHEL 6

* Wed Sep 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-3
- update the bindings patch

* Wed Nov 12 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-2
- more fixes for unreliable pasting into XmTextField (MotifZone bug #1321)
  Resolves: rhbz#405941
- the fix for MotifZone bug #1400 is not working for remote displays

* Thu Oct  2 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-1
- using final 2.3.1 dist archive

* Wed Sep 17 2008 Thomas Woerner <twoerner@redhat.com> 2.3.1-0
- rebase to 2.3.1 (CVS dist release)
  Resolves: rhbz#455736
- fixes OpenMotif XmList problem
  Resolves: rhbz#405801
- fixes List.c/ReplaceItem() segfaults when item selected
  Resolves: rhbz#431460
- fixes [motifzone 1400 ] openmotif/ BadFont on multiple display application
  Resolves: rhbz#438910
- fixes applications dump core in non-UTF8 environment
  Resolves: rhbz#453722
- fixes lots of additional bugs: see release notes

* Tue Apr  1 2008 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.5
- fixed SEGV error moving mouse over window related to XmToolTipGetLabel
  (MotifZone bug fix #1388)
  Resolves: rhbz#277381

* Thu Nov  8 2007 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.4
- fixed title bar problem using XmNdialogTitle (MotifZone bug fix #1380)
  Resolves: rhbz#353251

* Fri Dec  1 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.3
- fixed path to xmbind in /etc/X11/xinit/xinitrc.d/xmbind.sh
  Resolves: rhbz#218032

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.2.1
- rebuild

* Tue Jun  6 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.2
- new CVS version 2006-06-06
- new buildprereq for pkgconfig

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.1.9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.0-0.1.9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.9
- new CVS version 2006-02-02
- fixed CVE-2005-3964: libUil buffer overflows (#174814)
- fixed XmList out of bound accesses (#167701)
- fixed pasting into TextField (#179549)

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.coM> 2.3.0-0.1.2
- Rebuilt on new gcc

* Fri Dec  9 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.1
- moved mwmrc to /etc/X11/mwm
- moved bindings to /usr/share/X11
- fixed paths in man pages containing /usr/X11R6

* Thu Dec  8 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1.1
- enabled Xft, jpeg and png support
- patch for missing xft-config
- dropped duplicate include path in devel package

* Fri Dec  2 2005 Thomas Woerner <twoerner@redhat.com> 2.3.0-0.1
- new 2.3.0 (beta1)
- patch for new rgb.txt location (#174210)
  Thanks to Ville Skyttä for the patch

* Fri Nov 18 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-15
- moved man pages to /usr/share/man (#173604)

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-14
- X11R6 stuff is gone

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-13
- also buildrequire xbitmaps

* Wed Nov 16 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-12
- rebuild for modular X

* Fri Sep  2 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-11
- fixed mrm initialization error in MrmOpenHierarchyPerDisplay (#167094)
  Thanks to Arjan van de Ven for the patch.

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-10
- fixed possible libXpm overflows (#151642)

* Mon Feb 28 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-9
- Upstream Fix: Multiscreen mode
- Upstream Fix: Crash when restarting by a session manager (motifzone#1193)
- Upstream Fix: Crash when duplicating a window menu containing f.circle_up
  (motifzone#1202)
- fixed divide by zero error in ComputeVizCount() (#144420)
- Xpmcreate: define LONG64 on 64 bit architectures (#143689)

* Mon Nov 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-8.1
- allow to write XPM files with absolute path names again (#140815)

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> 2.2.3-8
- Convert man pages to UTF-8

* Mon Nov 22 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-7
- latest Xpm patches: CAN-2004-0914 (#134631)
- new patch for tmpnam in imake (only used for build)

* Thu Sep 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-6
- fixed CAN-2004-0687 (integer overflows) and CAN-2004-0688 (stack overflows)
  in embedded Xpm library

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.2
- replaced libtoolize and autofoo* calls with a patch (autofoo)

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.1
- use new autofoo

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5
- libXp now moved to xorg-x11-deprecated-libs, therefore no compatibility 
  with XFree86 packages anymore.

* Mon Aug 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.3
- devel package: added requires for XFree86-devel (#131202)

* Thu Jun 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.2
- rebuilt for fc3

* Wed Jun 16 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.1
- renamed xmbind script to xmbind.sh (#126116)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-3
- fixed popup menus fail on Tarantella/VNC (#123027)
- fixed character not supported problem (#124960)
- fixed data out of bounds bug (#124961)

* Wed Apr 14 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-2
- 2.2.3 final version

* Tue Mar 23 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.2
- final CVS version

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.1
- new openmotif 2.2.3 beta version

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-17
- fixed popdown problem in ToolTip (#75730)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.3
- rebuilt

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- added missing BuildRequires for XFree86-devel

* Thu Nov 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.2
- removed rpath

* Mon Aug 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16
- fixed ToggleBG (#101159)

* Thu Jul 31 2003  <timp@redhat.com> 2.2.2-15.2
- rebuild for RHEL

* Wed Jul 30 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-15
- fixed ToggleB (#101159)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-13
- fix for Xmu/EditRes conflict (bug #80777)
- fix for wml and utf-8 (bug #80271)
- fix for Ext18List (bug #74502)

* Thu Nov 14 2002 Than Ngo <than@redhat.com> 2.2.2-12.2
- add buildprereq byacc and flex (bug #77860)

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 2.2.2-12.1
- fix some build problem

* Mon Aug 27 2002 Than Ngo <than@redhat.com> 2.2.2-12
- Fixed a segmentation fault in mkcatdefs (bug #71955)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 2.2.2-11
- Added missing symlinks (bug #69117)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 2.2.2-10
- build using gcc-3.2-0.1

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 2.2.2-9
- fix to build openmotif (bug #64176)

* Thu Jun 13 2002 Than Ngo <than@redhat.com> 2.2.2-8
- rebuild in new enviroment

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- patched ltmain.sh to link properly

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- specified libraries by full name in files section 
  (libMrm was missing on alpha)

* Tue Mar 26 2002 Than Ngo <than@redhat.com> 2.2.2-5
- update new 2.2.2 from ICS

* Sun Mar 24 2002 Than Ngo <than@redhat.com> 2.2.2-4
- add missing uil

* Fri Mar 22 2002 Tim Powers <timp@redhat.com>
- rebuilt to try and shake some broken deps in the devel package

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-2
- rebuild

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-1
- update to 2.2.2 release

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-3
- conflict with older lesstif

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-2
- fix bug #60816

* Fri Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-1
- update to 2.2.1 release
- remove somme patches, which are included in 2.2.1

* Fri Feb 22 2002 Tim Powers <timp@redhat.com>
- rebuilt in new environment

* Fri Jan 25 2002 Tim Powers <timp@redhat.com>
- don't obsolete lesstif anymore, play nicely together
- rebuild against new toolchain

* Wed Jan 21 2002 Than Ngo <than@redhat.com> 2.1.30-11
- add some patches from Darrell Commander (supporting largefile)
- fix to build on s390

* Thu Jan 17 2002 Than Ngo <than@redhat.com> 2.1.30-10
- rebuild in 8.0

* Wed Sep  6 2001 Than Ngo <than@redhat.com>
- rebuild for ExtraBinge 7.2

* Thu May 03 2001 Than Ngo <than@redhat.com>
- add 3 official motif patches 
- add rm -rf $RPM_BUILD_ROOT in install section
- remove some old patches which are now in official patches

* Fri Dec 29 2000 Than Ngo <than@redhat.com>
- don't build static debug libraries

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- bzip2 source

* Mon Jul 24 2000 Than Ngo <than@redhat.de>
- rebuilt against gcc-2.96-44

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Sun Jun 11 2000 Than Ngo <than@redhat.de>
- fix imake to built with gcc-2.96 (thanks Jakup)
- put bitmaps in /usr/X11R6/include/X11/bitmaps
- put bindings in /usr/X11R6/lib/Xm/bindings
- add define -D_GNU_SOURCE to build Motif
- gzip man pages
- cleanup specfile

* Mon May 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to patchlevel 2
- remove bindings patch, it's included in pl2

* Tue May 16 2000 Matt Wilson <msw@redhat.com>
- use -fPIC on sparc
- fixed Ngo's "fixes"

* Mon May 15 2000 Ngo Than <than@redhat.de>
- added description.
- fixed spec, added uil stuff.

* Mon May 15 2000 Matt Wilson <msw@redhat.com>
- initialization of spec file.
