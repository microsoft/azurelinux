Summary:        The GNU shar utilities for packaging and unpackaging shell archives
Name:           sharutils
Version:        4.15.2
Release:        21%{?dist}
# The main code:                GPLv3+
# intl/dngettext.c:             LGPLv2+
# lib (gnulib):                 GPLv3+
# lib/md5.c:                    GPLv3+ and Public Domain
# libopts/file.c:               LGPLv3+ or BSD
# libopts/genshell.h:           LGPLv2+
# libopts/m4/libopts.m4:        GPLv3+
# doc/sharutils.texi:           GFDL
# src/uuencode.c:               GPLv3+ and BSD
## Not in the binary package
# ar-lib:                       GPLv2+
# config.rpath:                 FSFULLR
# INSTALL:                      FSFAPP
# install-sh:                   MIT
License:        GPLv3+ AND (GPLv3+ AND BSD) AND (LGPLv3+ OR BSD) AND LGPLv2+ AND Public Domain AND GFDL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.gnu.org/software/%{name}/
Source:         https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
# Pass compilation with -Werror=format-security, bug #1037323
Patch0:         %{name}-4.14.2-Pass-compilation-with-Werror-format-security.patch
# Fix CVE-2018-1000097 (a heap buffer overflow in find_archive()),
# bug #1548019,
# <http://lists.gnu.org/archive/html/bug-gnu-utils/2018-02/msg00004.html>
Patch1:         CVE-2018-1000097.patch
# Adapt bundled gnulib to glibc-2.28
Patch2:         %{name}-4.15.2-fflush-adjust-to-glibc-2.28-libio.h-removal.patch
# Fix building with GCC 10,
# <https://lists.gnu.org/archive/html/bug-gnu-utils/2020-01/msg00001.html>
Patch3:         %{name}-4.15.2-Fix-building-with-GCC-10.patch
# Fix building with GCC 10,
# <https://lists.gnu.org/archive/html/bug-gnu-utils/2020-01/msg00001.html>
Patch4:         %{name}-4.15.2-Do-not-include-lib-md5.c-into-src-shar.c.patch

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext
# glibc-common for iconv
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  sed

%if %{with_check}
BuildRequires:  diffutils
%endif

Provides:       bundled(gnulib)
# See libopts/autoopts/options.h for OPTIONS_DOTTED_VERSION
Provides:       bundled(libopts) = 41.1

%description
The sharutils package contains the GNU shar utilities, a set of tools for
encoding and decoding packages of files (in binary or text format) in
a special plain text format called shell archives (shar).  This format can be
sent through e-mail (which can be problematic for regular binary files).  The
shar utility supports a wide range of capabilities (compressing, uuencoding,
splitting long files for multi-part mailings, providing check-sums), which
make it very flexible at creating shar files.  After the files have been sent,
the unshar tool scans mail messages looking for shar files.  Unshar
automatically strips off mail headers and introductory text and then unpacks
the shar files.

%prep
%setup -q
%patch0 -p1 -b .format
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# convert TODO, THANKS to UTF-8
for i in TODO THANKS; do
  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
  mv $i{.utf8,}
done

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
chmod 644 AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_infodir}/*info*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.15.2-21
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Oct 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.15.2-20
- Fix typo in CVE-2018-1000097 patch filename to ensure detection by CVE tooling

* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.15.2-19
- Using HTTPS for source URL.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.15.2-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Petr Pisar <ppisar@redhat.com> - 4.15.2-16
- Fix building with GCC 10

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Petr Pisar <ppisar@redhat.com> - 4.15.2-13
- License corrected to "GPLv3+ and (GPLv3+ and BSD) and (LGPLv3+ or BSD) and
  LGPLv2+ and Public Domain and GFDL"

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Petr Pisar <ppisar@redhat.com> - 4.15.2-11
- Remove install-info from scriptlets

* Tue Apr 10 2018 Petr Pisar <ppisar@redhat.com> - 4.15.2-10
- Adapt bundled gnulib to glibc-2.28

* Thu Feb 22 2018 Petr Pisar <ppisar@redhat.com> - 4.15.2-9
- Fix CVE-2018-1000097 (a heap buffer overflow in find_archive())
  (bug #1548019)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 09 2016 Petr Pisar <ppisar@redhat.com> - 4.15.2-4
- Build-require gcc instead of glibc-headers (bug #1230494)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Petr Pisar <ppisar@redhat.com> - 4.15.2-1
- 4.15.2 bump
- Specify all dependencies

* Mon May 04 2015 Petr Pisar <ppisar@redhat.com> - 4.15.1-1
- 4.15.1 bump

* Mon Feb 09 2015 Petr Pisar <ppisar@redhat.com> - 4.15-1
- 4.15 bump

* Mon Dec 15 2014 Petr Pisar <ppisar@redhat.com> - 4.14.2-1
- 4.14.2 bump
- License changed from (GPLv3+ and LGPLv3+ and (LGPLv3+ or BSD) and LGPLv2+
  and Public Domain and GFDL) to (GPLv3+ and (LGPLv3+ or BSD) and LGPLv2+
  and Public Domain and GFDL)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 Petr Pisar <ppisar@redhat.com> - 4.14-2
- Pass compilation with -Werror=format-security (bug #1037323)

* Mon Oct 21 2013 Petr Pisar <ppisar@redhat.com> - 4.14-1
- 4.14 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Petr Pisar <ppisar@redhat.com> - 4.13.5-2
- Correct license declaration (LGPLv3+ and (LGPLv3+ or BSD) and GFDL added)

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 4.13.5-1
- 4.13.5 bump

* Wed Apr 03 2013 Petr Pisar <ppisar@redhat.com> - 4.13.4-1
- 4.13.4 bump

* Fri Feb 08 2013 Petr Pisar <ppisar@redhat.com> - 4.13.3-3
- Collect message catalogs in install phase (bug #908967)

* Wed Jan 23 2013 Petr Pisar <ppisar@redhat.com> - 4.13.3-2
- Fix decoding from positional argument while overriding output file
  (bug #901895)
- Fix decoding to standard output when output file is - or /dev/stdout
  (bug #901895)

* Mon Jan 07 2013 Petr Pisar <ppisar@redhat.com> - 4.13.3-1
- 4.13.3 bump

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 4.13.1-2
- Fix MD5 checksum generation on big-endian machines

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 4.13.1-1
- 4.13.1 bump

* Thu Aug 02 2012 Petr Pisar <ppisar@redhat.com> - 4.11.1-5
- Fix building with glibc-2.16.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 4.11.1-3
- Export bundled(gnulib) (bug #821789)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 06 2011 Petr Pisar <ppisar@redhat.com> - 4.11.1-1
- 4.11.1 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Petr Pisar <ppisar@redhat.com> - 4.11-1
- 4.11 bump
- Do not install header files injected by gnulib-tool
- Remove BuildRoot stuff

* Mon Aug 30 2010 Petr Pisar <ppisar@redhat.com> - 4.10-1
- 4.10 bump (bug #628304)

* Thu Jun  3 2010 Petr Pisar <ppisar@redhat.com> - 4.9-1
- version bump to 4.9 (bug #569059, bug #583187)

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 4.7-6
- fix the License tag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.7-3
- Requires(pre) should be Requires(post).

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7-2
- forgot the new source

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7-1
- update to 4.7
- fix license tag
- package cleanups

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.6.3-2
- Autorebuild for GCC 4.3

* Tue Apr 10 2007 Than Ngo <than@redhat.com> - 4.6.3-1
- 4.6.3

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 4.6.1-2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.6.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.6.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 4.6.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 03 2005 Than Ngo <than@redhat.com> 4.6-2
- fix wrong permission #171889

* Wed Oct 26 2005 Than Ngo <than@redhat.com> 4.6-1
- update to 4.6

* Mon Apr 11 2005 Than Ngo <than@redhat.com> 4.2.1-27
- apply debian patch to fix insecure temporary file creation
  in unshar #154049, CAN-2005-0990

* Thu Mar 31 2005 Than Ngo <than@redhat.com> 4.2.1-26
- apply patch to fix multiple buffer overflows #152571

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 4.2.1-25
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 4.2.1-24
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 4.2.1-23
- rebuilt

* Fri Oct 01 2004 Than Ngo <than@redhat.com> 4.2.1-22
- fix buffer overflow in shar, (from Ulf Harnhammer)

* Thu Jun 24 2004 Than Ngo <than@redhat.com> 4.2.1-21
- add builrequires on gettext, bug #126599

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Than Ngo <than@redhat.com> 4.2.1-19
- add suse patch, which fixes buffer overflow in handling of -o option, #123230

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 16 2003 Than Ngo <than@redhat.com> 4.2.1-17
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 4.2.1-13
- rebuild on all arches

* Mon Jun 24 2002 Than Ngo <than@redhat.com> 4.2.1-12
- fixed #66892

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Apr 14 2002 Than Ngo <than@redhat.com> 4.2.1-9
- added fix for Unsecure outputfile handling in uudecode (#63303)
- Copyright -> License

* Fri May 11 2001 Than Ngo <than@redhat.com>
- use find_lang macro
- use mktemp

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- fix typo (Bug# 12447)

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment

* Thu Jun 08 2000 Than Ngo <than@redhat.de>
- add %%defattr(-,root,root) (Bug# 11990)
- use rpm macros

* Sun May 21 2000 Ngo Than <than@redhat.de>
- rebuild to put man pages and info files in right place

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Tue Dec 21 1999 Preston Brown <pbrown@redhat.com>
- sharutils 4.2.1 for Y2K (2 digit date) fix.
- ja message catalog move (#7878)

* Tue Sep  7 1999 Jeff Johnson <jbj@redhat.com>
- handle spaces in uuencoded file names (David Fox <dsfox@cogsci.ucsd.edu>).

* Wed Jul 28 1999 Cristian Gafton <gafton@redhat.com>
- use the /usr/share/locale for the localedir instead of /usr/lib/locale
  (#2998)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- ALRIGHT!  Woo-hoo!  Erik already did the install-info stuff!
- added BuildRoot
- spec file cleanups

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
