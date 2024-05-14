Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _hardened_build 1

Summary: The client program for the Telnet remote login protocol
Name: telnet
Version: 0.17
Release: 81%{?dist}
License: BSD
Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{version}.tar.gz
Url: https://web.archive.org/web/20070819111735/www.hcs.harvard.edu/~dholland/computers/old-netkit.html
# telnet-client tarball is snapshot of the OpenBSD client telnet
Source2: telnet-client.tar.gz
Source4: telnet.wmconfig
Source5: telnet@.service
Source6: telnet.socket
Patch1: telnet-client-cvs.patch
Patch5: telnetd-0.17.diff
Patch6: telnet-0.17-env.patch
Patch7: telnet-0.17-issue.patch
Patch8: telnet-0.17-sa-01-49.patch
Patch10: telnet-0.17-pek.patch
Patch11: telnet-0.17-8bit.patch
Patch12: telnet-0.17-argv.patch
Patch13: telnet-0.17-conf.patch
Patch14: telnet-0.17-cleanup_race.patch
Patch15: telnetd-0.17-pty_read.patch
Patch16: telnet-0.17-CAN-2005-468_469.patch
Patch18: telnet-gethostbyname.patch
Patch19: netkit-telnet-0.17-ipv6.diff
Patch20: netkit-telnet-0.17-nodns.patch
Patch21: telnet-0.17-errno_test_sys_bsd.patch
Patch22: netkit-telnet-0.17-reallynodns.patch
Patch23: telnet-rh678324.patch
Patch24: telnet-rh674942.patch
Patch25: telnet-rh704604.patch
Patch26: telnet-rh825946.patch
Patch27: telnet-0.17-force-ipv6-ipv4.patch
Patch28: netkit-telnet-0.17-core-dump.patch
Patch29: netkit-telnet-0.17-gcc7.patch
Patch30: netkit-telnet-0.17-manpage.patch
Patch31: netkit-telnet-0.17-telnetrc.patch
Patch32: telnet-log-address.patch
Patch33: telnet-0.17-overflow-exploit.patch

BuildRequires: ncurses-devel systemd gcc gcc-c++
BuildRequires: perl-interpreter

%description
Telnet is a popular protocol for logging into remote systems over the
Internet. The package provides a command line Telnet client

%package server
Requires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Summary: The server program for the Telnet remote login protocol

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet. The package includes a daemon that supports Telnet remote
logins into the host machine. The daemon is disabled by default.
You may enable the daemon by editing /etc/xinetd.d/telnet

%prep
%setup -q -n netkit-telnet-%{version}

mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}

%patch 1 -p0 -b .cvs
%patch 5 -p0 -b .fix
%patch 6 -p1 -b .env
%patch 10 -p0 -b .pek
%patch 7 -p1 -b .issue
%patch 8 -p1 -b .sa-01-49
%patch 11 -p1 -b .8bit
%patch 12 -p1 -b .argv
%patch 13 -p1 -b .confverb
%patch 14 -p1 -b .cleanup_race 
%patch 15 -p0 -b .pty_read
%patch 16 -p1 -b .CAN-2005-468_469
#%patch17 -p1 -b .linemode
%patch 18 -p1 -b .gethost
%patch 19 -p1 -b .gethost2
%patch 20 -p1 -b .nodns
%patch 21 -p1 -b .errnosysbsd
%patch 22 -p1 -b .reallynodns
%patch 23 -p1 -b .rh678324
%patch 24 -p1 -b .rh674942
%patch 25 -p1 -b .rh704604
%patch 26 -p1 -b .rh825946
%patch 27 -p1 -b .ipv6-support
%patch 28 -p1 -b .core-dump
%patch 29 -p1 -b .gcc7
%patch 30 -p1 -b .manpage
%patch 31 -p1 -b .telnetrc
%patch 32 -p1 -b .log-address
%patch 33 -p1 -b .overflow

%build
%ifarch s390 s390x
    export CC_FLAGS="$RPM_OPT_FLAGS -fPIE"
%else
    export CC_FLAGS="$RPM_OPT_FLAGS -fpie"
%endif

export LD_FLAGS="$LD_FLAGS -z now -pie"

sh configure --with-c-compiler=gcc 
perl -pi -e '
    s,-O2,\$(CC_FLAGS),;
    s,LDFLAGS=.*,LDFLAGS=\$(LD_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

# remove stripping
perl -pi -e 's|install[ ]+-s|install|g' \
    ./telnet/GNUmakefile \
    ./telnetd/Makefile \
    ./telnetlogin/Makefile \
    ./telnet-NETKIT/Makefile

make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

make INSTALLROOT=${RPM_BUILD_ROOT} install

install -p -m644 %SOURCE5 ${RPM_BUILD_ROOT}%{_unitdir}/telnet@.service
install -p -m644 %SOURCE6 ${RPM_BUILD_ROOT}%{_unitdir}/telnet.socket

%post server
%systemd_post telnet.socket

%preun server
%systemd_preun telnet.socket

%postun server
%systemd_postun_with_restart telnet.socket

%files
%doc README
%defattr(-,root,root,-)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*

%files server
%{_unitdir}/*
%{_sbindir}/in.telnetd
%{_mandir}/man5/issue.net.5*
%{_mandir}/man8/in.telnetd.8*
%{_mandir}/man8/telnetd.8*

%changelog
* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 0.17-81
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.17-80
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Mar 27 2020 Michal Ruprich <michalruprich@gmail.com> - 1:0.17-79
- Resolves: #1814478 - Arbitrary remote code execution in utility.c via short writes or urgent data

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-78
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 10 2018 Michal Ruprich <mruprich@redhat.com> - 1:0.17-75
- Adding -i option for disabling reverse DNS lookup

* Mon Jul 23 2018 Michal Ruprich <mruprich@redhat.com> - 1:0.17-74
- Resolves: #1606506 - telnet: FTBFS in Fedora rawhide
- Resolves: #1505954 - telnet failing to parse .telnetrc due to strncpy used on overlaping buffers

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-73
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Michal Ruprich <mruprich@redhat.com> - 1:0.17-69
- Resolves: #1445259 - telnet won't build with latest gcc
- added note about address resolution in manpage

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-68
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Michal Ruprich <mruprich@redhat.com> - 1:0.17-67
- Resolves: #1415706 - telnet dumps core with certain combination of parameters

* Sat Oct 01 2016 Richard W.M. Jones <rjones@redhat.com> - 1:0.17-66
- BR perl
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Luboš Uhliarik <luhliari@redhat.com> - 1:0.17-64
- Related: #1069809 - fixed wrong paths in patch

* Thu Oct 29 2015 Luboš Uhliarik <luhliari@redhat.com> - 1:0.17-63
- Related: #1069809 - changed patch name + some minor changes in patch

* Wed Sep 30 2015 Luboš Uhliarik <luhliari@redhat.com> - 1:0.17-62
- Resolves: #1069809 - No option to specify IPv6 or IPv4 explicitly must be used

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Michal Sekletar <msekleta@redhat.com> - 1:0.17-57
- enable hardened build
- fix dates in changelog
- add systemd to BuildRequires

* Mon May 06 2013 Michal Sekletar <msekleta@redhat.com> - 1:0.17-56
- telnet-server will use systemd socket based activation instead of xinetd

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Adam Tkac <atkac redhat com> 1:0.17-53
- update /var/run/utmp even on some corner cases

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Adam Tkac <atkac redhat com> 1:0.17-51
- add "-debug6" option to telnetd (#rh674942)
- telnet wasn't interruptable (^C) when started with specious -b argument (#704604)

* Tue Jun 28 2011 Adam Tkac <atkac redhat com> 1:0.17-50
- telnetd: store "from" address in sockaddr_storage (#678324)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Karsten Hopp <karsten@redhat.com> 1:0.17-48
- update telnet-0.17-sa-01-49.patch to make it apply with fuzz=0

* Tue Mar 09 2010 Adam Tkac <atkac redhat com> 1:0.17-47
- add URL and README

* Fri Nov 27 2009 Adam Tkac <atkac redhat com> 1:0.17-46
- changes related package review (#226484)
- remove unused patches
  - telnet-0.17-linemode.patch
  - telnet-0.17-env-5x.patch

* Wed Sep 02 2009 Adam Tkac <atkac redhat com> 1:0.17-45
- add new option -N to disable DNS lookups (#490242)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.17-42
- Autorebuild for GCC 4.3

* Tue Sep 25 2007 Adam Tkac <atkac redhat com> 1:0.17-41
- rebased "nodns" patch with patch from Bryn M. Reeves

* Thu Sep 20 2007 Adam Tkac <atkac redhat com> 1:0.17-40
- improved patch to #274991

* Wed Aug 22 2007 Harald Hoyer <harald@redhat.com> - 1:0.17-39
- added patch to prevent a rare loop in the client

* Fri Apr 13 2007 Adam Tkac <atkac redhat com> - 1:0.17-38.fc7
- added -c option which disables reverse dns checking (#223448)
- added smp_mflags to make
- start using dist macro

* Fri Jul 14 2006 Harald Hoyer <harald@redhat.com> - 1:0.17-37
- added netkit-telnet-0.17-ipv6.diff from Marek Grác, 
  which adds IPv6 support to telnetd

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:0.17-36.1
- rebuild

* Mon May 08 2006 Harald Hoyer <harald@redhat.com> - 1:0.17-36
- patch to remove gethostbyname() (bug #190296)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.17-35.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.17-35.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Harald Hoyer <harald@redhat.com> - 1:0.17-35
- fixed CAN-2005-468 and CAN-2005-469

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Fri Jan 21 2005 Harald Hoyer <harald@redhat.com> - 1:0.17-33
- added patch telnetd-0.17-pty_read.patch, which fixes 145636

* Thu Jan 13 2005 Jason Vas Dias <jvdias@redhat.com> - 1:0.17-31
- bug 143929 / 145004 : fix race condition in telnetd on wtmp lock 
- when cleanup() is entered from main process and in signal
- handler 

* Mon Jun 28 2004 Harald Hoyer <harald@redhat.com> - 1:0.17-30
- fixed 126858: Too long /proc/X/cmdline: bad ps output when 
                piped to less/more

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Harald Hoyer <harald@redhat.com> - 1:0.17-27
- added PIE compile flags

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Harald Hoyer <harald@redhat.de> 1:0.17-26
- cleanup of spec file
- 8bit binary patch #91023

* Wed Jan 29 2003 Harald Hoyer <harald@redhat.de> 0.17-25
- rebuilt 

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Harald Hoyer <harald@redhat.de> 0.17-24
- changed description
- removed unused .desktop files

* Tue Jul 23 2002 Harald Hoyer <harald@redhat.de> 0.17-23
- removed prestripping

* Tue Jul  9 2002 Harald Hoyer <harald@redhat.de>
- removed x86 -O gcc-2.96 hack (#59514)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun  6 2002 Tim Powers <timp@redhat.com>
- bump release number and rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Sep 06 2001 Harald Hoyer <harald@redhat.de> 0.17-20
- hopefully fixed #52817, #52224

* Thu Aug 16 2001 Bill Nottingham <notting@redhat.com>
- bump version for 7.2

* Wed Aug 15 2001 Bill Nottingham <notting@redhat.com>
- fix versioning

* Tue Jul 31 2001 Harald Hoyer <harald@redhat.de>
- fixed security issues (#50335)
- patched the patches to fit the 5x version
- one world -> one spec file for all versions ;)

* Sat Jul 21 2001 Tim Powers <timp@redhat.com>
- no applnk file, it's clutrtering the menus

* Wed Jul 18 2001 Bill Nottingham <notting@redhat.com>
- apply the patch, duh (and fix it while we're here)

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- make /etc/issue.net parsing match the various gettys

* Mon Jun 18 2001 Harald Hoyer <harald@redhat.de>
- merged Jakubs and Pekka's patches 

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Fri Mar  9 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.17
- apply latest changes from CVS to telnet client, enable IPv6
- BuildPreReq ncurses-devel

* Mon Jan 22 2001 Helge Deller <hdeller@redhat.com>
- added swedish & german translation to .desktop-file (#15332)

* Sat Dec 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- mark the xinetd config file as config(noreplace)

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make sure the server is turned off by default

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add description & default to xinetd file

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17-pre20000412.

* Tue May 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- moved the xinet entry to the server

* Mon May 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add an entry to /etc/xinetd.d

* Tue May 16 2000 Jeff Johnson <jbj@redhat.com>
- permit telnet queries only for exported variables.

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.17

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- fix description

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig gone

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Sun Oct 10 1999 Matt Wilson <msw@redhat.com>
- corrected the Terminal setting of the .desktop (needs to be 'true' not '1')

* Sat Sep 25 1999 Preston Brown <pbrown@redhat.com>
- red hat .desktop entry

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- rebuild for 6.1.

* Wed Aug 18 1999 Bill Nottingham <notting@redhat.com>
- don't trust random TERM variables in telnetd (#4560)

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- fix (#3098).

* Thu May 27 1999 Antti Andreimann <Antti.Andreimann@mail.ee>
- fixed the problem with escape character (it could not be disabled)
- changed the spec file to use %%setup macro for unpacking telnet-client

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- use glibc utmp routines.

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- fix the fix (wrong way memcpy).

* Wed Apr  7 1999 Jeff Johnson <jbj@redhat.com>
- fix "telnet localhost" bus error on sparc64 (alpha?).

* Tue Apr  6 1999 Jeff Johnson <jbj@redhat.com>
- use OpenBSD telnet client (and fix minor core dump with .telnetrc #247)

* Thu Mar 25 1999 Erik Troan <ewt@redhat.com>
- use openpty in telnetd

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 24 1998 Cristian Gafton <gafton@redhat.com>
- compile C++ code using egcs

* Tue Apr 14 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
