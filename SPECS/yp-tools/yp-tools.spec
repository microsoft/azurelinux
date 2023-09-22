%global __filter_GLIBC_PRIVATE 1
Summary:        NIS (or YP) client programs
Name:           yp-tools
Version:        4.2.3
Release:        15%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/thkukuk/yp-tools
Source:         https://github.com/thkukuk/yp-tools/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1:         yp-tools-2.12-hash.patch
Patch2:         yp-tools-2.12-crypt.patch
Patch3:         yp-tools-2.12-adjunct.patch
Patch4:         yp-tools-4.2.2-strict-prototypes.patch
Patch5:         yp-tools-4.2.3-yppasswd.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libnsl2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libtool
BuildRequires:  make
Requires:       glibc
Requires:       ypbind >= 2.4-2

%description
The Network Information Service (NIS) is a system which provides
network information (login names, passwords, home directories, groupinformation) to all of the machines on a network.  NIS can enable
information) to all of the machines on a network.  NIS can enable
users to login on any machine on the network, as long as the machine
has the NIS client programs running and the user's password is
recorded in the NIS passwd database.  NIS was formerly known as Sun
Yellow Pages (YP).

This package's NIS implementation is based on FreeBSD's YP and is a
special port for glibc 2.x and libc versions 5.4.21 and later.  This
package only provides the NIS client programs.  In order to use the
clients, you'll need to already have an NIS server running on your
network. An NIS server is provided in the ypserv package.

Install the yp-tools package if you need NIS client programs for machines
on your network.  You will also need to install the ypbind package on
every machine running NIS client programs.  If you need an NIS server,
you'll need to install the ypserv package on one machine on the network.

%package devel
Summary:        NIS (or YP) client programs
Requires:       yp-tools

%description devel
Install yp-tools-devel package for developing applications that use yp-tools

%prep
%setup -q
%patch1 -p1 -b .hash
%patch2 -p1 -b .crypt
%patch3 -p1 -b .adjunct
%patch4 -p1 -b .strict-prototypes
%patch5 -p1


autoreconf -i -f -v

%build

export CFLAGS="$CFLAGS %{optflags} -Wno-cast-function-type"

%configure --disable-domainname

%make_build

%install
make DESTDIR=%{buildroot} INSTALL_PROGRAM=install install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog NEWS etc/nsswitch.conf
%doc THANKS
%{_bindir}/*

%{_mandir}/*/*
%{_sbindir}/*
%{_var}/yp/nicknames

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.2.3-15
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Aug 24 2022 Zhichun Wan <zhichunwan@microsoft.com> - 4.2.3-14
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 4.2.3-11
- Rebuild(libnsl2)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Filip Januš <fjanus@redhat.com> - 4.2.3-6
- Add yppasswd patch
- Bug https://bugzilla.redhat.com/show_bug.cgi?id=1671452
- Pull request https://github.com/thkukuk/yp-tools/pull/7

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.2.3-3
- Rebuilt for libcrypt.so.2 (#1666033)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Petr Kubat <pkubat@redhat.com> - 4.2.3-1
- Update to version 4.2.3

* Thu Mar 15 2018 Matej Mužila <mmuzila@redhat.com> - 4.2.2-7
- Disable cast-function-type warning

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.2.2-5
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Matej Mužila <mmuzila@redhat.com> - 4.2.2-2
- Require ypbind >= 3:2.4-2

* Fri May 19 2017 Matej Mužila <mmuzila@redhat.com> - 4.2.2-1
- Update to version 4.2.2 supporting IPv6

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Petr Kubat <pkubat@redhat.com> - 2.14-7
- Modified passwd.adjunct patch by Gilbert E. Detillieux (#1297955)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 06 2013 Honza Horak <hhorak@redhat.com> - 2.14-1
- New upstream version 2.14

* Mon Mar 25 2013 Honza Horak <hhorak@redhat.com> - 2.12-13
- Fix build for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 24 2012 Honza Horak <hhorak@redhat.com> - 2.12-12
- Minor spec file fixes

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Honza Horak <hhorak@redhat.com> - 2.12-10
- Minor spec file fixes

* Mon Apr 23 2012 Honza Horak <hhorak@redhat.com> - 2.12-9
- Do not check old passwords using passwd.adjunct feature
- Patch from Paul Wouters to handle crypt() returning NULL
  Resolves: #814803

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Honza Horak <hhorak@redhat.com> - 2.12-7
- Added YP_PASSWD_HASH environment variable to set default
  algorithm for hashing a new password
  Resolves: #699666

* Wed May 04 2011 Honza Horak <hhorak@redhat.com> - 2.12-6
- Applied -gethost patch to check return value
  (rhbz#698619)

* Fri Mar 18 2011 Honza Horak <hhorak@redhat.com> - 2.12-5
- Applied -typo patch to fix a grammar mistake
  (rhbz#668743)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Karel Klic <kklic@redhat.com> - 2.12-3
- Reverted previous change

* Tue Nov 23 2010 Karel Klic <kklic@redhat.com> - 2.12-2
- Added patch that removes ypclnt.c from being compiled into
  ypmatch (rhbz#546149)

* Fri Nov 19 2010 Karel Klic <kklic@redhat.com> - 2.12-1
- New upstream version

* Fri Nov 19 2010 Karel Klic <kklic@redhat.com> - 2.11-2
- Added patch to fix yppasswd utility when used with shadow
  passwords (rhbz#653921)
- Removed %%clean section

* Tue Apr 20 2010 Karel Klic <kklic@redhat.com> - 2.11-1
- New upstream release
- MD5, SHA-2 passwords patch merged by upstream
- Removed BuildRoot tag

* Thu Apr 15 2010 Karel Klic <kklic@redhat.com> - 2.10-3
- Added a new patch -passwords, which merges -md5 and -sha-2 patches
  together, and adds proper MD5/SHA support to verifypassword()
  #514061

* Mon Mar 01 2010 Karel Klic <kklic@redhat.com> - 2.10-2
- /var/yp is owned by the filesystem package (#569383)

* Thu Dec 10 2009 Karel Klic <kklic@redhat.com> - 2.10-1
- Updated to new version
- Removed unnecessary obsoletes

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.9-8
- Convert specfile to UTF-8.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.9-6
- Add SHA-2 password hashes support
  Resolves: #487607

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.9-4
- Fix license tag.

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.9-3
- Fix Buildroot

* Tue Jul 31 2007 Steve Dickson <steved@redhat.com> 2.9-1
- Changed install process to create an useful debuginfo package (bz 249961) 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9-0.1
- rebuild

* Mon Feb 13 2006 Chris Feist <cfeist@redhat.com> - 2.9-0
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8-8.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jun 18 2004 Alan Cox <alan@redhat.com>
- Fix buffer overflow (non security) thanks to D Binderman

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 23 2003 Steve Dickson <SteveD@RedHat.com>
- Update to 2.7 from upstream
- Updated yppasswd md5 patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Wed Aug 28 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-3
- properly terminate an alloca'ed string in yppasswd which would lead to
  improper rejection of the request if the user's pw_passwd was visible

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Alexander Larsson <alexl@redhat.com>
- Update to 2.7 from upstream
- Updated yppasswd md5 patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 2.6-4
- Updated passwd patch with Nalins comments

* Fri Mar 22 2002 Alex Larsson <alexl@redhat.com> 2.6-3
- Add patch that handles MD5 passwords and HPU/X password aging.
- This should hopefully fix #19045 and #22667

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- own /var/yp

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Feb 26 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify

* Wed Sep 27 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add another security patch

* Sun Aug 20 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- allow passwords up to 128 characters

* Tue Aug 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- change License from GNU to GPL
- fix handling of defaults in ypchfn (#13830)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir}

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- version 2.4

* Tue Oct 26 1999 Bill Nottingham <notting@redhat.com>
- get rid of bogus messages.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- patched /var/yp/nicknames so that hosts resolves to hosts.byname,
- not hosts.byaddr (bug # 2389)

* Sun May 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.3.

* Fri Apr 16 1999 Cristian Gafton <gafton@redhat.com>
- version 2.2
- make it obsolete older yp-clients package

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2/1
- version 2.1
- require ypbind

* Fri Jun 12 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 2.0

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Apr 13 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.4.1

* Thu Dec 04 1997 Cristian Gafton <gafton@redhat.com>
- put yppasswd again in the package, 'cause it is the right thing to do
  (sorry djb!)
- obsoletes old, unmaintained yppasswd package

* Sat Nov 01 1997 Donnie Barnes <djb@redhat.com>
- removed yppasswd from this package.

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- pulled from contrib into distribution (got fresh sources).  Thanks
  to Thorsten Kukuk <kukuk@vt.uni-paderborn.de> for the original.
- used fresh sources
