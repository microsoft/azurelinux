# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

Summary: The client for the Trivial File Transfer Protocol (TFTP)
Name: tftp
Version: 5.3
Release: 2%{?dist}
License: BSD-4-Clause-UC
URL: http://www.kernel.org/pub/software/network/tftp/
Source0: https://git.kernel.org/pub/scm/network/tftp/tftp-hpa.git/snapshot/tftp-hpa-%{version}.tar.gz
Source1: tftp.socket
Source2: tftp.service

Patch0: tftp-0.40-remap.patch
Patch2: tftp-hpa-0.39-tzfix.patch
Patch3: tftp-0.42-tftpboot.patch
Patch4: tftp-0.49-chk_retcodes.patch
Patch5: tftp-hpa-0.49-fortify-strcpy-crash.patch
Patch6: tftp-hpa-5.3-cmd_arg.patch
Patch7: tftp-hpa-0.49-stats.patch
Patch8: tftp-hpa-5.3-pktinfo.patch
Patch9: tftp-doc.patch
Patch10: tftp-enhanced-logging.patch
Patch12: tftp-off-by-one.patch
Patch14: tftp-hpa-5.2-osh.patch
# https://git.kernel.org/pub/scm/network/tftp/tftp-hpa.git/patch/?id=b9f2335e88dcb3939015843c7143f1533c755a46
Patch15: tftp-hpa-5.3-setjmp.patch

BuildRequires: autoconf
BuildRequires: gcc
BuildRequires: make
BuildRequires: readline-devel
BuildRequires: systemd-rpm-macros

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine.  This program and TFTP provide very little security,
and should not be enabled unless it is expressly needed.

%package server
Summary: The server for the Trivial File Transfer Protocol (TFTP)
Requires: systemd-units
Requires(post): systemd-units
Requires(postun): systemd-units

%description server
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp-server package provides the
server for TFTP, which allows users to transfer files to and from a
remote machine. TFTP provides very little security, and should not be
enabled unless it is expressly needed.  The TFTP server is run by using
systemd socket activation, and is disabled by default.

%prep
%setup -q -n tftp-hpa-%{version}
%patch -P0 -p1 -b .zero
%patch -P2 -p1 -b .tzfix
%patch -P3 -p1 -b .tftpboot
%patch -P4 -p1 -b .chk_retcodes
%patch -P5 -p1 -b .fortify-strcpy-crash
%patch -P6 -p1 -b .cmd_arg
%patch -P7 -p1 -b .stats
%patch -P8 -p1 -b .pktinfo
%patch -P9 -p1 -b .doc
%patch -P10 -p1 -b .logging
%patch -P12 -p1 -b .off-by-one
%patch -P14 -p1 -b .osh
%patch -P15 -p1 -b .setjmp

%build
autoreconf
%configure
%make_build

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,8}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tftpboot
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}

%make_install INSTALLROOT=%{buildroot} SBINDIR=%{_sbindir} MANDIR=%{_mandir}

install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_unitdir}
install -p -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_unitdir}

%post server
%systemd_post tftp.socket

%preun server
%systemd_preun tftp.socket

%postun server
%systemd_postun_with_restart tftp.socket


%files
%doc README README.security CHANGES
%{_bindir}/tftp
%{_mandir}/man1/tftp.1*

%files server
%doc README README.security CHANGES
%dir %{_localstatedir}/lib/tftpboot
%{_sbindir}/in.tftpd
%{_mandir}/man8/in.tftpd.8*
%{_mandir}/man8/tftpd.8*
%{_unitdir}/tftp.service
%{_unitdir}/tftp.socket

%changelog
* Fri Dec 26 2025 Dominik Mierzejewski <dominik@greysector.net> - 5.3-1
- Updated to 5.3 (resolves rhbz#2419684)
- drop obsolete patch
- backport fix for compiler warning about setjmp
- make file lists more explicit
- use modern make macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 16 2024 Lukáš Zaoral <lzaoral@redhat.com> - 5.2-43
- apply fixes to true positives reported by static analyzers from RHEL

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Lukáš Zaoral <lzaoral@redhat.com> - 5.2-40
- migrate to SPDX license format

* Sun Feb 05 2023 Florian Weimer <fweimer@redhat.com> - 5.2-39
- Fix C99 compatibility issue (#2148911)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 29 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.2-36
- fix the --mapfile/--map-file discrepancy in the manual page (Lukáš Zaoral)
- fix off-by-one reads and writes when filename remapping with macro \x is used
  (Lukáš Zaoral)
- use correct dependency for systemd rpm macros and sort deps alphabetically

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.2-33
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 03 2020 Dominik Mierzejewski <rpm@greysector.net> - 5.2-30
- fix build with gcc 10 (#1800195)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.2-27
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.2-24
- Escape macros in %%changelog

* Mon Dec  4 2017 Jan Synáček <jsynacek@redhat.com> - 5.2-23
- remove build dependency on tcp_wrappers (#1518793)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 5.2-19
- Rebuild for readline 7.x

* Thu Mar  3 2016 Jan Synáček <jsynacek@redhat.com> - 5.2-18
- enhance in.tftpd logging capabilities

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Jan Synáček <jsynacek@redhat.com> - 5.2-13
- add documentation reference to the service file

* Wed Feb 19 2014 Jan Synáček <jsynacek@redhat.com> - 5.2-12
- start socket as well when starting the service

* Thu Feb 13 2014 Jan Synáček <jsynacek@redhat.com> - 5.2-11
- don't depend on xinetd anymore (#1059641)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Jan Synáček <jsynacek@redhat.com> - 5.2-9
- harden the package (#955197)

* Fri Apr 19 2013 Jan Synáček <jsynacek@redhat.com> - 5.2-8
- documentation fixes

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 5.2-6
- add systemd-rpm macros
- Resolves: #850338

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Jan Synáček <jsynacek@redhat.com> - 5.2.4
- make fedora-review-friendly

* Wed Jul 18 2012 Jan Synáček <jsynacek@redhat.com> - 5.2-4
- update spec: fix Source0

* Wed May 30 2012 Jan Synáček <jsynacek@redhat.com> - 5.2-4
- use systemd instead of xinetd as a default

* Tue May 22 2012 Jan Synáček <jsynacek@redhat.com> - 5.2-3
- provide native systemd service files
- Resolves: #737212

* Wed Jan 04 2012 Jiri Skala <jskala@redhat.com> - 5.2-2
- fixes #739534 - TFTP to an IP alias of FC15 tftp server failed

* Wed Dec 14 2011 Jiri Skala <jskala@redhat.com> - 5.2-1
- updated to latest upstream - 5.2

* Thu Oct 06 2011 Jiri Skala <jskala@redhat.com> - 5.1-1
- updated to latest upstream - 5.1

* Mon Jun 20 2011 Jiri Skala <jskala@redhat.com> - 0.49-9
- fixes #714261 - CVE-2011-2199: buffer overflow when setting utimeout option

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Jiri Skala <jskala@redhat.com> - 0.49-7
- fixes #666746 - Packaging mistake: confusing %%doc files patched+unpatched
- fixes printing statistics using -v option

* Fri May 28 2010 Jiri Skala <jskala@redhat.com> - 0.49-6
- patched handling arguments of commands (put)

* Wed Aug 05 2009 Warren Togami <wtogami@redhat.com> - 0.49-5
- Bug #515361 tftp FORTIFY_SOURCE strcpy crash 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Jiri Skala <jskala@redhat.com> - 0.49-2
- #473487 - unchecked return values

* Tue Nov 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.49-1
- update to 0.49

* Wed May 21 2008 Warren Togami <wtogami@redhat.com. - 0.48-6
- undo symlink stuff completely because they are problematic
  See Bug #447135 for details.

* Wed May 21 2008 Martin Nagy <mnagy@redhat.com> - 0.48-5
- fix troubles caused by added symlink

* Tue May 20 2008 Martin Nagy <mnagy@redhat.com> - 0.48-4
- add symlink to /var/lib/tftpboot

* Mon Mar 03 2008 Martin Nagy <mnagy@redhat.com> - 0.48-3
- changed description (#234099)

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 0.48-2
- rebuild for gcc-4.3

* Tue Jan 22 2008 Martin Nagy <mnagy@redhat.com> - 0.48-1
- upgrade to 0.48
- remove the old sigjmp patch (fixed in upstream)
- make some changes in spec file (#226489)

* Tue Jan 22 2008 Martin Nagy <mnagy@redhat.com> - 0.42-6
- changed the location of tftpboot directory to /var/lib/

* Fri Aug 31 2007 Maros Barabas <mbarabas@redhat.com> - 0.42-5
- rebuild

* Mon Feb 19 2007 Maros Barabas <mbarabas@redhat.com> - 0.42-4
- make some changes in spec file (review)
- Resolves #226489

* Mon Dec 04 2006 Maros Barabas <mbarabas@redhat.com> - 0.42-3.2
- change BuildRequires from tcp_wrappers to tcp_wrappers-devel

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.42-3.1
- rebuild

* Mon Apr 10 2006 Radek Vokál <rvokal@redhat.com> 0.42-3
- show localtime instead of GMT (#172274)

* Wed Mar 22 2006 Radek Vokál <rvokal@redhat.com> 0.42-2
- fix double free error when hitting ^C (#186201)

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> 0.42-1
- upgrade to 0.42

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.41-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.41-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 03 2005 Radek Vokal <rvokal@redhat.com> 0.41-1
- upstream update (patterns fixes)

* Tue Apr 19 2005 Radek Vokal <rvokal@redhat.com> 0.40-6
- fix remap rules convert error <pjones@redhat.com>

* Wed Mar 23 2005 Radek Vokal <rvokal@redhat.com> 0.40-5
- use tftp-xinetd from tarball (#143589)

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 0.40-4
- gcc4 rebuilt

* Sun Feb 27 2005 Florian La Roche <laroche@redhat.com>
- Copyright: -> License

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 0.40-2
- Rebuilt for new readline.

* Mon Nov 15 2004 Radek Vokal <rvokal@redhat.com> 0.40-1
- Update to new upstream version, fixes #139328

* Mon Sep 13 2004 Elliot Lee <sopwith@redhat.com> 0.39-1
- Update to new version makes tftp work, says upstream.
- Remove malta patch

* Mon Sep 13 2004 Elliot Lee <sopwith@redhat.com> 0.38-1
- Update to new version fixes #131736

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 03 2004 Elliot Lee <sopwith@redhat.com> 0.36-1
- Update version

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com>
- 0.33
- Add /tftpboot directory (#88204)

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 23 2003 Tim Powers <timp@redhat.com>
- add BuildPreReq on tcp_wrappers

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Elliot Lee <sopwith@redhat.com> 0.32-1
- Update to 0.32

* Wed Oct 23 2002 Elliot Lee <sopwith@redhat.com> 0.30-1
- Fix #55789
- Update to 0.30

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com>
- Try applying HJ's patch from #65476

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Elliot Lee <sopwith@redhat.com>
- Update to 0.29

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Dec 18 2001 Elliot Lee <sopwith@redhat.com> 0.17-15
- Add patch4: netkit-tftp-0.17-defaultport.patch for bug #57562
- Update to tftp-hpa-0.28 (bug #56131)
- Remove include/arpa/tftp.h to fix #57259
- Add resource limits in tftp-xinetd (#56722)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Jun 12 2001 Helge Deller <hdeller@redhat.de> (0.17-13)
- updated tftp-hpa source to tftp-hpa-0.17
- tweaked specfile with different defines for tftp-netkit and tftp-hpa version
- use hpa's tftpd.8 man page instead of the netkits one

* Mon May 07 2001 Helge Deller <hdeller@redhat.de>
- rebuilt in 7.1.x

* Wed Apr 18 2001 Helge Deller <hdeller@redhat.de>
- fix tftp client's put problems (#29529)
- update to tftp-hpa-0.16

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Thu Feb 08 2001 Helge Deller <hdeller@redhat.de>
- changed "wait" in xinetd file to "yes" (hpa-tftpd forks and exits) (#26467)
- fixed hpa-tftpd to handle files greater than 32MB (#23725)
- added "-l" flag to hpa-tftpd for file-logging (#26467)
- added description for "-l" to the man-page 

* Thu Feb 08 2001 Helge Deller <hdeller@redhat.de>
- updated tftp client to 0.17 stable (#19640),
- drop dependency on xinetd for tftp client (#25051),

* Wed Jan 17 2001 Jeff Johnson <jbj@redhat.com>
- xinetd shouldn't wait on tftp (which forks) (#23923).

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- fix to permit tftp put's (#18128).
- startup as root with chroot to /tftpboot with early reversion to nobody
  is preferable to starting as nobody w/o ability to chroot.
- %%post is needed by server, not client. Add %%postun for erasure as well.

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- default to being disabled

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- correct group.

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- change user from root to nobody

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- update to tftp-hpa-0.14 (#14003).
- add server_args (#14003).
- remove -D_BSD_SOURCE (#14003).

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- cook up an xinetd config file for tftpd

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Fri May  5 2000 Matt Wilson <msw@redhat.com>
- use _BSD_SOURCE for hpa's tftpd so we get BSD signal semantics.

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- fix description

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages (again).

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description and summary

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Sat Aug 28 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.15.

* Wed Apr  7 1999 Jeff Johnson <jbj@redhat.com>
- tftpd should truncate file when overwriting (#412)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added check for getpwnam() failure

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
