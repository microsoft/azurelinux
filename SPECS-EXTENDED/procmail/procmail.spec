Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# hardened build if not overridden
%{!?_hardened_build:%global _hardened_build 1}

%if %{?_hardened_build}%{!?_hardened_build:0}
%global hardened_flags -pie -Wl,-z,relro,-z,now
%endif

Summary: Mail processing program
Name: procmail
Version: 3.22
Release: 53%{?dist}
License: GPLv2+ or Artistic
# Source: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
# The original source doesn't seem to be available anymore, using mirror
Source: ftp://ftp.ucsb.edu/pub/mirrors/procmail/procmail-%{version}.tar.gz
# Source2: https://www.linux.org.uk/~telsa/BitsAndPieces/procmailrc
# The Telsa config file doesn't seem to be available anymore, using local copy
Source2: procmailrc
URL: https://www.procmail.org
Patch0: procmail-3.22-rhconfig.patch
Patch1: procmail-3.15.1-man.patch
Patch2: procmail_3.22-8.debian.patch
Patch4: procmail-3.22-truncate.patch
Patch5: procmail-3.22-ipv6.patch
Patch6: procmail-3.22-getline.patch
Patch7: procmail-3.22-CVE-2014-3618.patch
Patch8: procmail-3.22-crash-fix.patch
Patch9: procmail-3.22-CVE-2017-16844.patch
Patch10: procmail-3.22-coverity-scan-fixes.patch
BuildRequires: gcc

%description
Procmail can be used to create mail-servers, mailing lists, sort your
incoming mail into separate folders/files (real convenient when subscribing
to one or more mailing lists or for prioritising your mail), preprocess
your mail, start any programs upon mail arrival (e.g. to generate different
chimes on your workstation for different types of mail) or selectively
forward certain incoming mail automatically to someone.

%prep
%setup -q
%patch 0 -p1 -b .rhconfig
%patch 1 -p1
%patch 2 -p1
%patch 4 -p1 -b .truncate
%patch 5 -p1 -b .ipv6
%patch 6 -p1 -b .getline
%patch 7 -p1 -b .CVE-2014-3618
%patch 8 -p1 -b .crash-fix
%patch 9 -p1 -b .CVE-2017-16844
%patch 10 -p1 -b .coverity-scan-fixes

find examples -type f | xargs chmod 644

%build
make RPM_OPT_FLAGS="$(getconf LFS_CFLAGS)" autoconf.h
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?hardened_flags} -Wno-comments $(getconf LFS_CFLAGS)"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5}

make \
    BASENAME=${RPM_BUILD_ROOT}%{_prefix} MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
    install

cp debian/mailstat.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
cp -p %{SOURCE2} telsas_procmailrc


%files
%doc Artistic COPYING FAQ FEATURES HISTORY README KNOWN_BUGS examples telsas_procmailrc debian/QuickStart debian/README.Maildir

%{_bindir}/formail
%attr(2755,root,mail) %{_bindir}/lockfile
%{_bindir}/mailstat
%attr(0755,root,mail) %{_bindir}/procmail

%{_mandir}/man[15]/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.22-53
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec  6 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-49
- Fixed issues found by Coverity Scan

* Fri Jul 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-48
- Fixed FTBFS by adding gcc requirement
  Resolves: rhbz#1606850

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-45
- Renamed loadbuf-fix patch to CVE-2017-16844, because it got CVE number

* Tue Oct 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-44
- Fixed possible buffer overflow in loadbuf function
  Resolves: rhbz#1500071

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-41
- Fixed some more conditional jumps that depended on uninitialized values

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-37
- Fixed more buffer overflows and memory corruptions (by crash-fix patch)

* Thu Sep  4 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-36
- Fixed buffer overflow in formail
  Resolves: CVE-2014-3618

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-32
- Updated sources URLs

* Tue Sep  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-31
- Hardened build with PIE and full RELRO
  Resolves: rhbz#853186

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-29
- Rebuilt without NO_NFS_ATIME_HACK
  Resolves: rhbz#666383

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.22-27
- Defuzzification of ipv6 patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Miroslav Lichvar <mlichvar@redhat.com> 3.22-24
- rename getline to avoid conflict with glibc (#505977)
- add -Wno-comments to CFLAGS
- remove package name from summary

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 04 2008 Miroslav Lichvar <mlichvar@redhat.com> 3.22-22
- fix building on sh (CHIKAMA Masaki) (#447658)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.22-21
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 3.22-20
- update license tag

* Tue Mar 27 2007 Miroslav Lichvar <mlichvar@redhat.com> 3.22-19
- fix description (#234098)
- spec cleanup

* Fri Oct 27 2006 Miroslav Lichvar <mlichvar@redhat.com> 3.22-18
- add IPv6 support to comsat notification (#198403)
- package man page for mailstat
- change mail spool directory to /var/spool/mail

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.22-17.1
- rebuild

* Thu Mar 30 2006 Peter Vrabec <pvrabec@redhat.com> 3.22-17
- fix truncation of mailbox when running into a disk quota or a
  full partition. Patch from Solar Designer.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.22-16.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.22-16.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com> 3.22-16
- rebuilt

* Mon Nov  8 2004 Martin Stransky <stransky@redhat.com> 3.22-15
- add largefiles patch to support 64-bit file I/O

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan  6 2004 Jens Petersen <petersen@redhat.com> - 3.22-12
- apply procmail_3.22-8.debian.patch from Debian (fixes #79691)

* Mon Sep 22 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -ldl and -lnsl

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Jens Petersen <petersen@redhat.com>
- convert changelog to utf8

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.22-8
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.22-5
- Updated Telss's procmailrc file (#61872)

* Thu Mar 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.22-4
- Add Telsa Gwynne's procmailrc as a doc file - it's
  excellently commented, and is a great example

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.22-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Sep 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.22-1
- 3.22

* Sat Jun 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.21

* Fri Jun 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.20
- Enable LMTP

* Thu Apr 12 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Change to "License: GPL or artistic" from "Copyright: distributable"
- Fix man page (#35825)
- 3.15.1
- redo config patch

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- lose setuid/setgid (root,mail) bits (#23257).

* Fri Aug 11 2000 Jeff Johnson <jbj@redhat.com>
- add space in delivery rules with '!' (#15947).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.14.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- fix doc perms.

* Wed Apr 21 1999 Cristian Gafton <gafton@redhat.com>
- turn on GROUP_PER_USER
- add some docs to the package

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- version 3.13

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- fixed Group line

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
