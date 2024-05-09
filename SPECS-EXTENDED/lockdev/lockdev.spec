Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Where lock files are stored
%global _lockdir /run/lock/lockdev

%global checkout 20111007git
%global co_date  2011-10-07

#https://lists.fedoraproject.org/pipermail/devel/2011-August/155358.html
%global _hardened_build 1

Summary: A library for locking devices
Name: lockdev
Version: 1.0.4
Release: 3%{?dist}
License: LGPLv2.1
URL: https://github.com/definesat/lockdev

# This is a nightly snapshot downloaded via
# https://github.com/definesat/lockdev
Source0: %{_distro_sources_url}/lockdev-%{version}.%{checkout}.tar.gz

Patch1: lockdev-euidaccess.patch
Patch2: 0001-major-and-minor-functions-moved-to-sysmacros.h.patch

Requires(pre): shadow-utils
Requires(post): glibc
Requires(postun): glibc
Requires: systemd

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: perl-interpreter
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: systemd

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%package devel
Summary: The header files for the lockdev library
Requires: lockdev = %{version}-%{release}

%description devel
The lockdev library provides a reliable way to put an exclusive lock
on devices using both FSSTND and SVr4 methods. The lockdev-devel
package contains the development headers.


%prep
%setup -q -n lockdev-scm-%{co_date}

# Replace access() calls with euidaccess() (600636#c33)
%patch 1 -p1 -b .access
%patch 2 -p1

%build
# Generate version information from git release tag
./scripts/git-version > VERSION

# To satisfy automake
touch ChangeLog

# Bootstrap autotools
autoreconf --verbose --force --install

CFLAGS="%{optflags} -D_PATH_LOCK=\\\"%{_lockdir}\\\"" \
%configure --disable-static --enable-helper --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

# %%ghosted, but needs to be in buildroot
# on reboot re-created by %%{_prefix}/lib/tmpfiles.d/legacy.conf
mkdir -p %{buildroot}%{_lockdir}

# install /usr/lib/tmpfiles.d/lockdev.conf (#1324184)
mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/lockdev.conf <<EOF
# See tmpfiles.d(5) for details

d %{_lockdir} 0775 root lock -
EOF

%pre
getent group lock >/dev/null 2>&1 || groupadd -g 54 -r -f lock >/dev/null 2>&1 || :

%post
if [ $1 -eq 1 ] ; then
# for the time until first reboot
%tmpfiles_create lockdev.conf
fi

%files
%license COPYING
%doc AUTHORS
%ghost %dir %attr(0775,root,lock) %{_lockdir}
%attr(2711,root,lock)  %{_sbindir}/lockdev
%{_tmpfilesdir}/lockdev.conf
%{_libdir}/*.so.*
%{_mandir}/man8/*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/lockdev.pc
%{_mandir}/man3/*
%{_includedir}/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-3
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-2
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.33.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Kalev Lember <klember@redhat.com> - 1.0.4-0.32.20111007git
- Fix the build with latest rpmbuild (#1736075)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.31.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-0.30.20111007git
- Remove obsolete scriptlets

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.29.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Sebastian Kisela <skisela@redhat.com> - 1.0.4-0.28.
- Explicitly include <sys/sysmacros.h> due to glibc-headers changes.
Definition of major and minor macros is no longer transitively included
through <sys/types.h>, hence make it explicit.
Ref:
https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=NEWS;hb=HEAD

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.27.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.26.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.25.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.24.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.23.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 06 2016 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.22.20111007git
- /run/lock/lockdev no longer created by systemd (#1324184)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-0.21.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.20.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.19.20111007git
- change _lockdir from /var/lock/lockdev to /run/lock/lockdev

* Thu Sep 18 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.18.20111007git
- better euidaccess.patch from Paolo Bonzini (#600636#c33)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.17.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.16.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.0.4-0.15.20111007git
- BuildRequire systemd for %%tmpfiles_create.

* Thu Dec 05 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.14.20111007git
- Define _GNU_SOURCE in lockdev.c

* Thu Nov 28 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.13.20111007git
- revert previous change and use %%tmpfiles_create in %%post

* Wed Nov 27 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.12.20111007git
- do not %%ghost /var/lock/lockdev (https://fedorahosted.org/fesco/ticket/525)

* Mon Aug 26 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.11.20111007git
- Remove the %%post scriptlet completely (#983772)

* Mon Aug 26 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.10.20111007git
- Silence possible %%post scriptlet errors (#983772)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.9.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.8.20111007git
- %%{_lockdir} is %%ghost-ed (#983772)

* Mon Jun 03 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.7.20111007git
- Replace access() calls with euidaccess(), build with -D_GNU_SOURCE (600636#c9)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.6.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.5.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-0.4.20111007git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.3.20111007git
- Define _hardened_build

* Wed Oct 19 2011 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.2.20111007git
- Fixed URL
- Removed unused patches

* Fri Oct 07 2011 Jiri Popelka <jpopelka@redhat.com> - 1.0.4-0.1.20111007git
- pre 1.0.4 nightly snapshot

* Mon Apr 04 2011 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-10
- Revert previous change (#681898)
- /etc/tmpfiles.d/lockdev.conf moved into systemd upstream (#692714)

* Thu Mar 03 2011 Jan Görig <jgorig@redhat.com> - 1.0.3-9
- Change /var/lock/lockdev permissions to 1777 (#681898)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-7
- Fixed some rpmlint warnings

* Thu Nov 25 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-6
- Added /etc/tmpfiles.d/lockdev.conf to enable lock directory on tmpfs (#656614)
- Don't ship static library at all

* Mon Apr 19 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-5
- Changed directory for lock files from /var/lock to /var/lock/lockdev (#581884)

* Thu Jan 21 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-4
- Created -static subpackage to ship static library separately
- Updated lockdev.8 manpage

* Thu Dec 10 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-3
- Correct rh.patch

* Thu Dec 10 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-2
- Correct rh.patch

* Mon Dec 07 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.3-1
- 1.0.3.  No longer need 1.0.0-signal, 1.0.1-subdir, 1.0.1-fcntl, 1.0.1-32bit patches.
- Renumbered patches and sources.

* Thu Dec 03 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.1-20
- Fixed pre section (https://fedoraproject.org/wiki/Packaging/UsersAndGroups)
- Added back Buildroot to silence rpmlint's false positive

* Tue Dec 01 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.1-19
- Added license text to package

* Fri Oct 02 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.1-18
- Fixed mixed-use-of-spaces-and-tabs

* Fri Oct 02 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.1-17
- Removed PreReq tag

* Fri Sep 25 2009 Jiri Popelka <jpopelka@redhat.com> - 1.0.1-16
- Manual page for /usr/sbin/lockdev

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct  6 2008 Karel Zak <kzak@redhat.com> - 1.0.1-13
- refresh patches (due --fuzz=0)
- fix compiler warnings

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-12.1
- Autorebuild for GCC 4.3

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.1-11.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Apr 12 2007 Karel Zak <kzak@redhat.com> - 1.0.1-11
- fix rpmlint issues
- change lockdev permissions from 2755 to 2711

* Wed Jul 19 2006 Karel Zak <kzak@redhat.com> - 1.0.1-10
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-9.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-9.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-9.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Karel Zak <kzak@redhat.com> 1.0.1-9
- fix #165189 - The naming of the lock file by the lockdev command is abnormal.

* Thu Sep  1 2005 Karel Zak <kzak@redhat.com> 1.0.1-8
- fix #163276 - baudboy.h should include fcntl.h

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 1.0.1-6
- rebuilt

* Wed Feb 23 2005 Karel Zak <kzak@redhat.com> 1.0.1-5
- lockdev errs on /dev/input/ttyACM0 (3-component pathname) (#126082, #98160, #74454)

* Fri Oct 22 2004 Adrian Havill <havill@redhat.com> 1.0.1-4
- don't unlock files if pid still exists (#128104)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep  9 2003 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-1.3
- rebuild

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-1.2
- rebuild

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 1.0.1-1.1
- bump n-v-r for 3.0E

* Fri Aug 15 2003 Adrian Havill <havill@redhat.com> 1.0.1-1
- bumped version
- make the dev rewrite work with ttys in the /dev/input subdir, not just
  the base level dir (#98160)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared lib

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Jeff Johnson <jbj@redhat.com>
- don't segfault if device arg is missing.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun  5 2002 Jeff Johnson <jbj@redhat.com> 1.0.0-19
- fix: don't ignore signals, use default behavior instead (#63468).

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.0-16
- include liblockdev.so so that programs can link to a shared liblockdev
- fix shared library version numbers

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 29 2001 Trond Eivind Glomsrod <teg@redhat.com> 1.0.0-16
- Rebuilt

* Fri Oct 26 2001 Trond Eivind Glomsrod <teg@redhat.com> 1.0.0-15
- Add copyright/license info to baudboy.h (#54321)

* Tue Sep  4 2001 Jeff Johnson <jbj@redhat.com>
- swap egid and gid for lockdev's access(2) device check (#52029).

* Tue Aug 28 2001 Jeff Johnson <jbj@redhat.com>
- typo in include file (#52704).
- map specific errno's into status for return from helper.

* Tue Aug 14 2001 Jeff Johnson <jbj@redhat.com>
- set exit status correctly.

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- check that we can open the device r/w before locking
- fix calling lockdev without any arguments
- fix waitpid() call in baudboy.h
- use umask(002), not umask(0)

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- add lock group here, own /var/lock as well

* Sun Aug  5 2001 Jeff Johnson <jbj@redhat.com>
- include setgid helper binary and baudboy.h.

* Mon Jun 18 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Make the -devel depend on the main package

* Sun Aug 06 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- add %%defattr for -devel

* Sat Jun 10 2000 Trond Eivind Glomsrod <teg@redhat.com>
- use %%{_mandir}

* Thu May 04 2000 Trond Eivind Glomsrod <teg@redhat.com>
- first build
