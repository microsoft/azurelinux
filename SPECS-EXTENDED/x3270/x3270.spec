Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global catalogue /etc/X11/fontpath.d

%global majorver 3.6
Summary: An X Window System based IBM 3278/3279 terminal emulator
Name: x3270
Version: 3.6ga10
Release: 2%{?dist}
License: BSD
URL: https://x3270.sourceforge.net/
Source0: https://downloads.sourceforge.net/%{name}/suite3270-%{version}-src.tgz
Source1: x3270.png
Source2: x3270.desktop
Patch0: x3270-3.5-paths.patch
Patch1: x3270-3.5-ibmhostpath.patch

BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: libtool
BuildRequires: desktop-file-utils
BuildRequires: fontpackages-devel

%package x11
Summary: IBM 3278/3279 terminal emulator for the X Window System
BuildRequires: xorg-x11-font-utils
BuildRequires: libXaw-devel
Requires: %{name} = %{version}

%package text
Summary: IBM 3278/3279 terminal emulator for text mode
Requires: %{name} = %{version}


%description
The x3270 package contains files needed for emulating the IBM 3278/3279
terminals, commonly used with mainframe applications.

You will also need to install a frontend for %{name}. Available frontends
are %{name}-x11 (for the X Window System) and %{name}-text (for text mode).

%description x11
The x3270 program opens a window in the X Window System which emulates
the actual look of an IBM 3278/3279 terminal, commonly used with
mainframe applications.  x3270 also allows you to telnet to an IBM
host from the x3270 window.

Install the %{name}-x11 package if you need to access IBM hosts using an IBM
3278/3279 terminal emulator from X11.

%description text
The c3270 program opens a 3270 terminal which emulates the actual look of an
IBM 3278/3279 terminal, commonly used with mainframe applications.
x3270 also allows you to telnet to an IBM host from the x3270 window.

Install the %{name}-text package if you need to access IBM hosts using an IBM
3278/3279 terminal emulator without running X.


%prep
%setup -q -n suite3270-%{majorver}
%patch 0 -p1 -b .paths
%patch 1 -p1 -b .ibmhosts

for d in c3270 pr3287 s3270 x3270; do
    for f in LICENSE README html; do
        mv $d/$f $f.$d
    done
done


%build
%configure --enable-x3270 --enable-c3270 --enable-s3270 --enable-pr3287
make %{?_smp_mflags} CCOPTIONS="$RPM_OPT_FLAGS" LIBX3270DIR=%{_sysconfdir}

# build playback tool
( cd Playback; make CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS" )


%install
make install DESTDIR=$RPM_BUILD_ROOT CIFONTDIR=%{_fontdir} LIBX3270DIR=%{_sysconfdir}
make install.man DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{_fontdir} $RPM_BUILD_ROOT%{catalogue}/x3270

install -p -m755 Playback/playback $RPM_BUILD_ROOT%{_bindir}
install -p -m644 Playback/playback.man $RPM_BUILD_ROOT%{_mandir}/man1/playback.1

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
desktop-file-install \
        --dir $RPM_BUILD_ROOT/%{_datadir}/applications \
        %{SOURCE2}


%files
%doc LICENSE.s3270 README.s3270 html.s3270
%doc LICENSE.pr3287 README.pr3287 html.pr3287
%{_bindir}/s3270
%{_bindir}/pr3287
%{_bindir}/x3270if
%{_bindir}/playback
%{_mandir}/man1/s3270.1*
%{_mandir}/man1/pr3287.1*
%{_mandir}/man1/x3270if.1*
%{_mandir}/man1/x3270-script.1*
%{_mandir}/man1/playback.1*
%{_mandir}/man5/ibm_hosts.5*
%config(noreplace) %{_sysconfdir}/ibm_hosts

%files x11
%doc LICENSE.x3270 README.x3270 html.x3270
%{_bindir}/x3270
%{_fontdir}/
%{catalogue}/x3270
%{_mandir}/man1/x3270.1*
%{_datadir}/icons/hicolor/48x48/apps/x3270.png
%{_datadir}/applications/x3270.desktop

%files text
%doc LICENSE.c3270 README.c3270 html.c3270
%{_bindir}/c3270
%{_mandir}/man1/c3270.1*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6ga10-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 24 2020 Dan Horák <dan[at]danny.cz> - 3.6ga10-1
- updated to 3.6ga10 (#1806341)

* Fri Feb 21 2020 Dan Horák <dan[at]danny.cz> - 3.6ga9-1
- updated to 3.6ga9 (#1803972)

* Wed Feb 05 2020 Than Ngo <than@redhat.com> - 3.6ga8-5
- fixed FTBFS against gcc10

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6ga8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 3.6ga8-3
- Fix symbol with multiple incompatible definitions which triggers
  an error with LTO

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6ga8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Dan Horák <dan[at]danny.cz> - 3.6ga8-1
- updated to 3.6ga8 (#1716585)

* Tue Mar 26 2019 Dan Horák <dan[at]danny.cz> - 3.6ga6-1
- updated to 3.6ga6 (#1692775)

* Fri Mar 08 2019 Dan Horák <dan[at]danny.cz> - 3.6ga5-6
- drop scriptlets

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6ga5-5
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6ga5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Adam Jackson <ajax@redhat.com> - 3.6ga5-3
- Drop BuildRequires: imake, no longer needed

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6ga5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 12 2018 Dan Horák <dan[at]danny.cz> - 3.6ga5-1
- updated to 3.6ga5 (#1544168)

* Fri Feb  9 2018 Florian Weimer <fweimer@redhat.com> - 3.6ga4-3
- Build playback with LDFLAGS from redhat-rpm-config

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Remove obsolete scriptlets

* Sun Dec 31 2017 Dan Horák <dan[at]danny.cz> - 3.6ga4-1
- updated to 3.6ga4 (#1529910)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5ga11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5ga11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Dan Horák <dan[at]danny.cz> - 3.5ga11-1
- updated to 3.5ga11 (#1465201)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5ga10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Dan Horák <dan[at]danny.cz> - 3.5ga10-1
- updated to 3.5ga10 (#1413799)

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.5ga9-2
- Rebuild for readline 7.x

* Tue Dec 27 2016 Dan Horák <dan[at]danny.cz> - 3.5ga9-1
- updated to 3.5ga9 (#1408735)

* Mon May 16 2016 Dan Horák <dan[at]danny.cz> - 3.5ga8-1
- updated to 3.5ga8 (#1335153)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.15ga9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Dan Horák <dan[at]danny.cz> - 3.3.15ga9-1
- updated to 3.3.15ga9
- fix FTBFS in s3270 due hardening

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.15ga8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 04 2015 Dan Horák <dan[at]danny.cz> - 3.3.15ga8-1
- updated to 3.3.15ga8 (#1178449)

* Wed Dec 17 2014 Dan Horák <dan[at]danny.cz> - 3.3.15ga7-1
- updated to 3.3.15ga7 (#1175247)

* Sat Dec 06 2014 Dan Horák <dan[at]danny.cz> - 3.3.15ga6-1
- updated to 3.3.15ga6 (#1171097)

* Fri Oct 17 2014 Dan Horák <dan[at]danny.cz> - 3.3.15ga5-1
- updated to 3.3.15ga5 (#1154010)

* Fri Oct 10 2014 Dan Horák <dan[at]danny.cz> - 3.3.15ga4-1
- updated to 3.3.15ga4 (#1150568)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.14ga11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.14ga11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Dan Horák <dan[at]danny.cz> - 3.3.14ga11-1
- updated to 3.3.14ga11 (#1095670)

* Mon Apr 14 2014 Dan Horák <dan[at]danny.cz> - 3.3.14ga9-1
- updated to 3.3.14ga9 (#1087398)

* Thu Mar 13 2014 Dan Horák <dan[at]danny.cz> - 3.3.14ga7-1
- updated to 3.3.14ga7 (#1075007)

* Mon Sep 16 2013 Dan Horák <dan[at]danny.cz> - 3.3.13ga7-1
- updated to 3.3.13ga7 (#1008442)

* Tue Sep 10 2013 Dan Horák <dan[at]danny.cz> - 3.3.13ga6-1
- updated to 3.3.13ga6 (#1006023)

* Fri Aug 23 2013 Dan Horák <dan[at]danny.cz> - 3.3.12ga13-1
- updated to 3.3.12ga13 (#959961)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.12ga12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Samantha N. Bueno <sbueno[at]redhat.com> - 3.3.12ga12-2
- Rebuilt to include fix for #926737

* Mon Mar 25 2013 Samantha N. Bueno <sbueno[at]redhat.com> - 3.3.12ga12-1
- updated to 3.3.12ga12
- fixes CVE-2012-5662 (#889373, #924228)
- add support for aarch64 to build system (#926737)

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 3.3.12ga11-5
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077
- Cleanup spec as per recently changed packaging guidelines

* Thu Nov 22 2012 Dan Horák <dan[at]danny.cz> - 3.3.12ga11-4
- fix license (BSD instead of MIT)

* Thu Sep 27 2012 Dan Horák <dan[at]danny.cz> - 3.3.12ga11-3
- cleanup of BuildRequires

* Fri Sep 21 2012 Dan Horák <dan[at]danny.cz> - 3.3.12ga11-2
- enable DBCS character sets (#801139)

* Fri Sep 07 2012 Dan Horák <dan[at]danny.cz> - 3.3.12ga11-1
- updated to 3.3.12ga11

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.12ga7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 3.3.12ga7-1
- updated to 3.3.12ga7
- spec cleanup

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.10ga4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.10ga4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 08 2009 Karsten Hopp <karsten@redhat.com> 3.3.10ga4-1
- update to 3.3.10ga4-1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.6-10
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 3.3.6-7
- rebuild with new openssl

* Thu Oct 02 2008 Karsten Hopp <karsten@redhat.com> 3.3.6-6
- update redhat patch for fuzz=0 (#465087)

* Thu Mar 20 2008 Karsten Hopp <karsten@redhat.com> 3.3.6-5
- fix compiler flags for FORTIFY_SOURCE

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.3.6-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Karsten Hopp <karsten@redhat.com> 3.3.6-3
- rebuild with new openssl libs

* Tue Aug 21 2007 Karsten Hopp <karsten@redhat.com> 3.3.6-2
- drop chkfontpath dependency (#252274)

* Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 3.3.6-1
- version 3.3.6
- fix font resize issue
- enable app-defaults

* Sun Aug 27 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p7-5
- rebuild

* Tue Aug 15 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p7-4
- fix requirements of -X11 subpackage

* Wed Jul 12 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p7-3
- fix fileconflicts in subpackages

* Wed Jul 05 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p7-2
- silence chkconfig
- rpmlint fixes:
 - replace PreReq/BuildPrereq with Requires/BuildRequires
 - move ibm_hosts to %%{_sysconfdir}
 - fix end of line encodings in docs

* Tue Jun 13 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p6-6
- update to 3.3.4p7
- buildrequire libtool

* Fri Feb 17 2006 Karsten Hopp <karsten@redhat.de> 3.3.4p6-5
- rebuild

* Mon Dec 19 2005 Karsten Hopp <karsten@redhat.de> 3.3.4p6-4
- test build without modular-X patch

* Wed Nov 23 2005 Karsten Hopp <karsten@redhat.de> 3.3.4p6-3
- update release again

* Wed Nov 23 2005 Karsten Hopp <karsten@redhat.de> 3.3.4p6-2
- update release

* Thu Nov 17 2005 Karsten Hopp <karsten@redhat.de> 3.3.4p6-1
- update to patchlevel 6
- drop obsolete segfault patch
- build with modular X
- build with current openssl
- gccmakedep is gone, use makedepend wrapper instead

* Wed Oct 19 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-6
- move x3270-x11 files from /usr/X11R6 to /usr (#170938)
  
* Thu Sep 08 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-5
- add missing buildrequires so that x3270 will be built with SSL support
  (#159527)

* Wed Jul 20 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-4
- buildrequires xorg-x11-font-utils (#160737)
- add disttag

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com>
- silence gtk-update-icon-cache in %%post

* Wed Apr 20 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-3
- more fixes, enable StartupNotify

* Wed Apr 20 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-2
- spec file cleanups from Chris Ricker <kaboom@oobleck.net>
- remove backup files from rpm patch process

* Mon Apr 18 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-1
- rpmlint fix
- buildroot fix
- use _smp_mflags

* Tue Apr 12 2005 Karsten Hopp <karsten@redhat.de> 3.3.4-1
- Version 3.3.4, fixes mouse selection and timing problems with scripted
  logins in ~/.ibm_hosts

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 3.3.3.b2-2
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 08 2005 Karsten Hopp <karsten@redhat.de> 3.3.3.b2-1
- update to b2, which fixes a segfault when login is done with 
  an entry in .ibm_hosts (via emulate_input)

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 3.3.3.b1-2
- build with gcc-4

* Thu Jan 13 2005 Karsten Hopp <karsten@redhat.de> 3.3.3.b1-1 
- update to fix ibm_hosts file parsing and c3270 color support

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 3.3.2.p1-10
- Rebuilt for new readline.

* Wed Dec 08 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-9
- add icon (#141599, #125577)
- fix variable usage (local variable overwrite) (#116660)

* Wed Dec 08 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-8
- rebuild 

* Thu Oct 21 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-7
- enable builds on ppc(64) again (#136703)

* Wed Jul 07 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-6
- rebuild with new gcc

* Mon Jul 05 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-5 
- update c3270 package to patchlevel2
- fix buildrequires (#124280)
- fix compiler warnings (#106312, #78479)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-3 
- include license file

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 15 2004 Karsten Hopp <karsten@redhat.de> 3.3.2.p1-1
- update to 3.3.2.p1

* Wed Dec 03 2003 Karsten Hopp <karsten@redhat.de> 3.3.2-1
- update to latest stable release, now with SSL and DBCS support

* Tue Aug 12 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-4.2
- check for libncursesw and use it if available

* Wed Jul 09 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-4.1
- rebuilt

* Wed Jul 09 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-4
- fix segfault when ~/.x3270connect isn't writable by the user

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-3.1
- rebuilt

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-3
- rebuild 

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 05 2003 Karsten Hopp <karsten@redhat.de> 3.2.20-1
- update to 3.2.20

* Tue Apr  1 2003 Thomas Woerner <twoerner@redhat.com>
- fixed inclusion of time header file (sys/time.h -> time.h)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Karsten Hopp <karsten@redhat.de> 3.2.19-3
- update to patchlevel 4:
  Re-enable the automatic font switching when the
  x3270 window is resized

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild for all arches
- remove cruft from the buildroot we aren't shipping

* Wed Jul 24 2002 Karsten Hopp <karsten@redhat.de>
- 3.2.19
- use desktop-file-utils

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.2.18-2
- Update to 3.2.18 patchlevel 14

* Wed Jan 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.2.18-1
- 3.2.18
- Don't ship x3270-tcl anymore

* Mon Jul 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.2.16-4
- Add build dependencies (#48930)

* Sat Jun 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove all provides/requires for x3270-frontend

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.2.16-2
- Rebuild with new readline

* Thu May 10 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.2.16-1
- 3.2.16
- adapt patches
- get rid of the **** pdksh requirement
- split the tcl version into a different package, no need to require tcl for
  normal use
- split the x11 frontend into a separate package.
  We don't necessarily have X on a machine where we want to run
  3270 sessions (e.g. s390...)

* Fri Dec 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.2.14
- Add c3270 (textmode x3270) in x3270-text package
- Fix build
- Make ibm_hosts a %%config(noreplace)

* Tue Oct 24 2000 Jeff Johnson <jbj@redhat.com>
- remove /usr/local paths in Examples.

* Sun Oct 22 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.2.13.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for 7.0

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.1.1.9 (see URL for pending 3.2alpha version).

* Fri Sep 24 1999 Preston Brown <pbrown@redhat.com>
- change to directory before doing a mkfontdir

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- ibm_hosts needed %%config (#788)

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 22 1997 Marc Ewing <marc@redhat.com>
- new version
- added wmconfig entry

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
