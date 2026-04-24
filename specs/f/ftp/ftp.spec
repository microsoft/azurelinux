# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: The standard UNIX FTP (File Transfer Protocol) client
Name: ftp
Version: 0.17
Release: 100%{?dist}
License: BSD-4-Clause-UC
# The Upstream of ftp is no longer active.
# The source file for ftp is no longer available anywhere
# else than in Fedora repos.
Source0: netkit-ftp-%{version}.tar.gz
Patch1: netkit-ftp-0.17-pre20000412.pasv-security.patch
Patch2: netkit-ftp-0.17-acct.patch
Patch3: netkit-ftp.usagi-ipv6.patch
Patch4: netkit-ftp-0.17-segv.patch
Patch5: netkit-ftp-0.17-volatile.patch
Patch6: netkit-ftp-0.17-runique_mget.patch
Patch7: netkit-ftp-locale.patch
Patch8: netkit-ftp-0.17-printf.patch
Patch9: netkit-ftp-0.17-longint.patch
Patch10: netkit-ftp-0.17-vsftp165083.patch
Patch11: netkit-ftp-0.17-C-Frame121.patch
Patch12: netkit-ftp-0.17-data.patch
Patch13: netkit-ftp-0.17-multihome.patch
Patch14: netkit-ftp-0.17-longnames.patch
Patch15: netkit-ftp-0.17-multiipv6.patch
Patch16: netkit-ftp-0.17-nodebug.patch
Patch17: netkit-ftp-0.17-stamp.patch
Patch18: netkit-ftp-0.17-sigseg.patch
Patch19: netkit-ftp-0.17-size.patch
Patch20: netkit-ftp-0.17-fdleak.patch
Patch21: netkit-ftp-0.17-fprintf.patch
Patch22: netkit-ftp-0.17-bitrate.patch
Patch23: netkit-ftp-0.17-arg_max.patch
Patch24: netkit-ftp-0.17-case.patch
Patch25: netkit-ftp-0.17-chkmalloc.patch
Patch26: netkit-ftp-0.17-man.patch
Patch27: netkit-ftp-0.17-acct_ovl.patch
Patch28: netkit-ftp-0.17-remove-nested-include.patch
Patch29: netkit-ftp-0.17-linelen.patch
Patch30: netkit-ftp-0.17-active-mode-option.patch
Patch31: netkit-ftp-0.17-commands-leaks.patch
Patch32: netkit-ftp-0.17-lsn-timeout.patch
Patch33: netkit-ftp-0.17-getlogin.patch
Patch34: netkit-ftp-0.17-token.patch
Patch35: netkit-ftp-0.17-linelen-segfault.patch
Patch36: netkit-ftp-0.17-out-of-memory.patch
Patch37: netkit-ftp-0.17-gcc15.patch

BuildRequires: glibc-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: perl-interpreter
BuildRequires: gcc
BuildRequires: make
BuildRequires: git-core

%description
The ftp package provides the standard UNIX command-line FTP (File
Transfer Protocol) client.  FTP is a widely used protocol for
transferring files over the Internet and for archiving files.

If your system is on a network, you should install ftp in order to do
file transfers.

%prep
%autosetup -n netkit-ftp-%{version} -S git

%build
sh configure --with-c-compiler=%{__cc} --enable-ipv6
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64,;
    s,^LDFLAGS=.*$,LDFLAGS=\$(RPM_LD_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

%{make_build}

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5

make INSTALLROOT=${RPM_BUILD_ROOT} install

%files
%{_bindir}/ftp
%{_bindir}/pftp
%{_mandir}/man1/ftp.*
%{_mandir}/man1/pftp.*
%{_mandir}/man5/netrc.*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-99
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Michal Ruprich <mruprich@redhat.com> - 0.17-98
- Fixing build with GCC15

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-97
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-96
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-95
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-94
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-93
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 16 2023 Michal Ruprich <mruprich@redhat.com> - 0.17-92
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-91
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-90
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-89
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 20 2021 Michal Ruprich <mruprich@redhat.com> - 0.17-87
- Fixes 'out of memory' error when stacksize is unlimited

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Michal Ruprich <mruprich@redhat.com> - 0.17-85
- Use make_build macro and remove hard-coded gcc
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-84
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-83
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.17-81
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Michal Ruprich <mruprich@redhat.com> - 0.17-79
- Resolves: #1624949 - netkit ftp client buffer overflow in makeargv()

* Mon Jul 23 2018 Michal Ruprich <mruprich@redhat.com> - 0.17-78
- Resolves: #1604015 - ftp: FTBFS in Fedora rawhide

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Michal Ruprich <mruprich@redhat.com> - 0.17-76
- use distribution LDFLAGS during build (#1548427) - fix by jsynacek
- fixed bogus dates in changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-74
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-73
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.17-71
- Rebuild for readline 7.x

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.17-68
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-66
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-63
- Fix buffer overflow in token parsing
- Resolves: #871296

* Tue Oct 30 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-62
- Fix linelen patch
- Resolves: #871290

* Wed Oct 03 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-61
- Fix: FTP client does not expand home directory correctly after sudo or su
- Resolves: #861113

* Tue Sep 25 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-60
- Plug leaks in "put", "send", "append"
- Add listening timeout

* Tue Aug 28 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-59
- Add active mode option

* Fri Aug 03 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-58
- Extend the input line buffer and the argument storage buffer
- Prettify spec some more and remove trailing space

* Fri Jul 20 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-57
- Remove nested include (fix compilation in rawhide)

* Thu Jul 19 2012 Jan Synáček <jsynacek@redhat.com> - 0.17-56
- Fixed Source0 and URL
- Make spec fedora-review-friendly

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Jiri Skala <jskala@redhat.com> - 0.17-54
- fixes #737016 - ftp: off-by-one in account command parsing

* Tue Mar 29 2011 Jiri Skala <jskala@redhat.com> - 0.17-53
- fixes #673850 - ftp(1) manpage fixes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Jiri Skala <jskala@redhat.com> - 0.17-49
- Resolves: #473491  unchecked malloc

* Wed Apr 23 2008 Martin Nagy <mnagy@redhat.com> - 0.17-48
- fix mget when using case
- Resolves: #442712

* Mon Apr 07 2008 Martin Nagy <mnagy@redhat.com> - 0.17-47
- Use sysconf to get ARG_MAX instead of a macro (#440782)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-46
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.17-45
- changed bitrate from 1e+03 KBytes/sec to 1000 kBytes/sec
- Resolves: rhbz#430457

* Thu Nov 15 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-44
- using fprintf instead of printf

* Mon Oct 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-43
- feature: for cmd size is switching to TYPE_I automatized
- bug: ftp leaks socket fds when it fails to open a file (#315241)
- rhbz#306191

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-42
- rebuilt (for mass rebuild)
- license tag checked

* Tue Aug 07 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-41
- #251074 add patch from Jan Kratochvil

* Thu Feb 15 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-40
- review again

* Wed Feb 14 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-39
- review again

* Wed Feb  7 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-38
- add gpl
- spec fix 
- rhbz#225774

* Tue Jan 30 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.17-35
- nodebug package

* Wed Sep 13 2006 Marcela Maslanova <mmaslano@redhat.com> - 0.17-33
- rebuilt

* Wed Aug 2 2006 Marcela Maslanova <mmaslano@redhat.com> - 0.17-32.1.2.4
- fix (#199145) patch for IPv6 multihome

* Tue Jul 25 2006 Marcela Maslanova <mmaslano@redhat.com> - 0.17-32.1.2.3
- fix (#196103) patch for long filenames

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 12 2006 Petr Raszyk <praszyk@redhat.com> - 0.17-32
- support for multi-homed clients
  See #171621, netkit-ftp-0.17-multihome.patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 2 2005 Petr Raszyk <praszyk@redhat.com> - 0.17-31
- ftp does not close socket descriptor (if the remote file
  does not exist).
  See #174599, netkit-ftp-0.17-data.patch

* Wed Oct 26 2005 Petr Raszyk <praszyk@redhat.com> - 0.17-30
- The patch netkit-ftp-0.17-C-Frame121.patch adds some
  comments/hints for C-Frame 121. It can be removed any time.

* Tue Aug 30 2005 Petr Raszyk <praszyk@redhat.com> - 0.17-29
- rebuild

* Tue Aug 30 2005 Petr Raszyk <praszyk@redhat.com> - 0.17-28
- This 'hack' will avoid a bug in ftp-server
  (  < vsftpd-2.0.1-5   ). See #165083 (server prints the 
  '150 FILE:...' line twice).
  This patch can be (later ?) removed. 

* Mon Aug 22 2005 Petr Raszyk <praszyk@redhat.com> - 0.17-27
- overflow using 'hash mode' (printing '#' but
  not reading data from network - #79367)

* Tue May 24 2005 Miloslav Trmac <mitr@redhat.com> - 0.17-26
- Fix passive mode with SELinux (#158234, patch by Nalin Dahyabhai)
- Fix format string mismatch

* Fri Mar 04 2005 Jiri Ryska <jryska@redhat.com>
- rebuilt

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 0.17-24
- Rebuilt for new readline.

* Wed Dec 15 2004 Tim Waugh <twaugh@redhat.com>
- Call setlocale() so that readline works correctly (bug #142265).

* Tue Dec  7 2004 Thomas Woerner <twoerner@redhat.com> 0.17-23
- fixed mget with runique (#79367)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Alan Cox <alan@redhat.com>
- Re-arranged some totally bogus old bezerkly code that could
  segfault ftp on connection loss. (BZ #122295)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com>
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.17-13
- Recompile with support for files > 2 GB

* Mon Jun 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.17-12
- Add some Build dependencies (#45007)

* Fri May 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.17-11
- Actually apply Patch #3

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.17-10
- Rebuild with new readline

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add IPv6 patch (RFE #35642)

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Sun Jan 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 0.17 final
- Fix up ACCT support in netrc (Bug #17353)

* Wed Aug 16 2000 Philipp Knirsch <pknirsch@redhat.com>
- Switched the default transfer protocol from PORT to PASV as proposed on
  bugzilla (#16134)
- Fixed a small compiler warning in ftp.c line 886

* Fri Jul 14 2000 Jeff Johnson <jbj@redhat.com>
- add netrc man page (#7443).
- fix possible buffer overflows in ftp client.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17-pre20000412.

* Wed Apr  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with current libreadline

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.17

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- the ftp client does not require inetd

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Mon Aug 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.15.
- enable readline support (#3796).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
