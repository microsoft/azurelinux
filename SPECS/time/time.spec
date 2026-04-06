# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:    A GNU utility for monitoring a program's use of system resources
Name:       time
Version:    1.9
Release:    27%{?dist}
# src/time.c:               GPL-3.0-or-later
# COPYING:                  GPL-3.0 text
# doc/time.texi:            GFDL-1.3-no-invariants-or-later
# doc/fdl.texi:             GFDL-1.3 text
# doc/time.info:            GFDL-1.3-no-invariants-or-later
# lib/stdnoreturn.in.h:     GPL-3.0-or-later
# lib/strerror-override.c:  GPL-3.0-or-later
# lib/error.h:              GPL-3.0-or-later
## Not in a binary package
# tests/init.sh:            GPL-3.0-or-later
# INSTALL:                  FSFAP
# configure:                FSFUL
# build-aux/config.guess:   GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
# build-aux/install-sh:     X11 AND LicenseRef-Fedora-Public-Domain
# build-aux/config.rpath:   FSFULLR
# build-aux/test-driver:    GPL-2.0-or-later WITH Autoconf-exception-generic
# build-aux/update-copyright:   GPL-3.0-or-later
# build-aux/useless-if-before-free: GPL-3.0-or-later
# build-aux/vc-list-files:  GPL-3.0-or-later
# build-aux/missing:        GPL-2.0-or-later WITH Autoconf-exception-generic
# build-aux/compile:        GPL-2.0-or-later WITH Autoconf-exception-generic
# build-aux/config.sub:     GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
# build-aux/gitlog-to-changelog:    GPL-3.0-or-later
# build-aux/git-version-gen:        GPL-3.0-or-later
# build-aux/texinfo.tex:    GPL-3.0-or-later WITH Texinfo-exception AND GPL-1.0-or-later
# build-aux/depcomp:        GPL-2.0-or-later WITH Autoconf-exception-generic
# build-aux/mdate-sh:       GPL-2.0-or-later WITH Autoconf-exception-generic
# GNUmakefile:              GPL-3.0-or-later
# m4/asm-underscore.m4:     FSFULLR
# m4/gnulib-cache.m4:       GPL-3.0-or-later WITH Autoconf-exception-generic
#                           (Waiting on an approval
#                           <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/473?)
# m4/host-cpu-c-abi.m4:     FSFULLR
# m4/longlong.m4:           FSFULLR
# m4/ssize_t.m4:            FSFULLR
# m4/stdnoreturn.m4:        FSFULLR
# maint.mk:                 GPL-3.0-or-later
# tests/time-posix-quiet.sh:    GPL-3.0-or-later
License:    GPL-3.0-or-later AND GFDL-1.3-no-invariants-or-later
SourceLicense: %{license} AND GPL-3.0-or-later WITH Autoconf-exception-generic AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GPL-3.0-or-later WITH Texinfo-exception AND GPL-2.0-or-later WITH Autoconf-exception-generic AND GPL-1.0-or-later AND X11 AND FSFAP AND FSFUL AND FSFULLR AND LicenseRef-Fedora-Public-Domain
Url:        https://www.gnu.org/software/%{name}/
Source0:    https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:    https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
# Obtained from a key server
Source2:    gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
# Fix measuring time when a clock experiences a jump, bug #1004416,
# <http://lists.gnu.org/archive/html/bug-gnu-utils/2013-09/msg00003.html>
Patch0:     time-1.8-Prefer-clock_gettime-CLOCK_MONOTONIC.patch
# Fix info directory entry
Patch1:     time-1.9-Improve-info-directory-index-entry-description.patch
# Clarify RSS size as kibibytes in a documentation, proposed to an upstream,
# <https://lists.gnu.org/archive/html/bug-time/2020-07/msg00000.html>
Patch2:     time-1.9-Use-kibibytes-instead-of-kilobytes-in-a-documentatio.patch
# Do not leak a file descriptor of the --output argument to a command,
# proposed to an upstream,
# <https://lists.gnu.org/archive/html/bug-time/2020-11/msg00001.html>
Patch3:     time-1.9-Close-outfp-before-exec.patch
# The time-max-rss.sh test randomly fails( mallocating 5 MB more does not have
# to increase RSS in 5 MB). In addition there is regression in ppc64le kernel
# (bug #2212765) which always fails.
Patch4:     time-1.9-drop-flawed-rss-test.patch
# Fix formatting a trailing backslash, proposed to the upstream,
# <https://lists.gnu.org/archive/html/bug-time/2024-01/msg00000.html>
Patch5:     time-1.9-Fix-formatting-a-trailing-backslash-and-a-percent-si.patch
# Fixes compiler error that occured after the switch to GCC15
# <https://lists.gnu.org/archive/html/bug-time/2025-01/msg00000.html>
Patch6:     time-1.9-Fix-compiling-with-GCC15.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  texinfo

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running, and displays
the results.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
# Set time stamp stored in an info page to the latest patch
touch -d "$(sed -n -e '/^Date: /{s/^[^:]*: //;p}' %{PATCH2})" doc/time.texi
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
# Correct version VERSION flag for doc/time.texi
# <https://lists.gnu.org/archive/html/bug-time/2021-01/msg00000.html>
printf '%{version}\n' > .tarball-version
autoreconf -fi

%build
%configure
%{make_build}

%install
%{make_install}
# Remove info index, it's updated by file triggers
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%check
%{make_build} check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/time
%{_infodir}/time.info*
# time(1) manual page lives in man-pages package, bug #1612294.

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 30 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.9-26
- Fix compiling with GCC 15

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Petr Pisar <ppisar@redhat.com> - 1.9-23
- Fix formatting a trailing backslash

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Stephen Gallagher <sgallagh@redhat.com> - 1.9-21
- Tests: drop time-max-rss.sh test (bug #2212765)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Petr Pisar <ppisar@redhat.com> - 1.9-15
- Retrieve a time stamp of the info page from a patch date header

* Wed Jan 13 2021 Petr Pisar <ppisar@redhat.com> - 1.9-14
- Correct version in an info page
- Set time stamp stored in an info page to the latest patch

* Wed Jan 13 2021 Petr Pisar <ppisar@redhat.com> - 1.9-13
- Update URL and Source addresses (thanks to Robert Scheck)
- Verify an upstream archive signature

* Mon Nov 16 2020 Petr Pisar <ppisar@redhat.com> - 1.9-12
- Fix a regression in closing a file descriptor if no --output was given
  (bug #1898138)

* Wed Nov 11 2020 Petr Pisar <ppisar@redhat.com> - 1.9-11
- Do not leak a file descriptor of the --output argument to a command

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Petr Pisar <ppisar@redhat.com> - 1.9-9
- Clarify RSS size as kibibytes in a documentation

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Petr Pisar <ppisar@redhat.com> - 1.9-5
- Remove time(1) manual page because it's provided by man-pages (bug #1612294)

* Mon Aug 06 2018 Petr Pisar <ppisar@redhat.com> - 1.9-4
- Add time(1) manual page (bug #1612294)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Petr Pisar <ppisar@redhat.com> - 1.9-2
- Remove install-info from scriptlets

* Tue Mar 13 2018 Petr Pisar <ppisar@redhat.com> - 1.9-1
- 1.9 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Petr Pisar <ppisar@redhat.com> - 1.8-2
- Use upstream patch for POSIX mode
- Silence compiler warnings

* Wed Nov 08 2017 Petr Pisar <ppisar@redhat.com> - 1.8-1
- 1.8 bump
- License changed from GPLv2+ to (GPLv3+ and GFDL)
- Disable printing command failure in POSIX mode

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Petr Pisar <ppisar@redhat.com> - 1.7-52
- Package COPYING file as a license text (bug #1418528)

* Wed Jan 11 2017 Petr Pisar <ppisar@redhat.com> - 1.7-51
- Search clock_gettime() also in rt library (bug #1004416)

* Wed Jan 11 2017 Petr Pisar <ppisar@redhat.com> - 1.7-50
- Fix measuring time when a clock experiences a jump (bug #1004416)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.7-47
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 06 2012 Petr Pisar <ppisar@redhat.com> - 1.7-42
- Package AUTHORS and ChangeLog

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Petr Pisar <ppisar@redhat.com> - 1.7-39
- Fix maximal RSS report (bug #702826)
- Clean spec file
- Recompute CPU usage at finer level (bug #527276)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Roman Rakus <rrakus@redhat.com> - 1.7-37
- Don't print errors in post and preun sections (#515936)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.7-34
- Fix Patch:/%%patch0 mismatch.
  Resolves: #463067

* Tue Mar  4 2008 Roman Rakus <rrakus@redhat.cz> - 1.7-33
- Added patch from JW (redhat@zacglen.com), less nonverbose output

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.7-32
- Autorebuild for GCC 4.3

* Tue Jan 08 2008 Florian La Roche <laroche@redhat.com> - 1.7-31
- update url/license tags

* Tue Aug 21 2007 Florian La Roche <laroche@redhat.com> - 1.7-30
- rebuild

* Tue Feb 27 2007 Karsten Hopp <karsten@redhat.com> 1.7-29
- remove trailing dot from summary
- replace tabs with spaces
- replace PreReq with Requires(post)/Requires(preun)
- include license file in %%doc
- add smp flags
- use make install DESTDIR=

* Mon Jan 22 2007 Florian La Roche <laroche@redhat.com>
- add dist tag
- fix rhbz#223720

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.7-27
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 1.7-26
- update source URL
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip apps, do not compress info page

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Feb 25 2002 Elliot Lee <sopwith@redhat.com>
- Remove HAVE_WAIT3 hack, tried to replace it with a requirement for an 
autoconf with the fixed test, didn't work, put in another less-bad hack 
instead.

* Wed Dec 05 2001 Tom Tromey <tromey@redhat.com>
- Bump release, force HAVE_WAIT3 to be defined at build time

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jan 31 2001 Preston Brown <pbrown@redhat.com>
- prereq install-info (#24715)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- using / as the file manifesto has weird results.

* Sun Jun  4 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- buildrooted and defattr'd

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 27 1997 Cristian Gafton <gafton@redhat.com>
- fixed info handling

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- updated the spec file; added info file handling

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
