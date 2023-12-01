%bcond_with tex_docs

Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:    A GNU program for formatting C code
Name:       indent
Version:    2.2.12
Release:    6%{?dist}
# COPYING:                      GPLv3 text
# doc/indent.info:              Verbatim (generated from doc/indent.texi)
#   <http://lists.gnu.org/archive/html/bug-indent/2018-09/msg00008.html>
# doc/indent.texi:              Verbatim (or GPL?)
# src/code_io.c:                BSD
# src/globs.c:                  GPLv3+
# src/indent.c:                 BSD
# src/utils.h:                  GPLv3+
## Not in any binary package
# aclocal.m4:                   GPLv3+ with exception
# config/config.guess:          GPLv2+ with exception
# config/config.rpath:          FSFULLR
# config/install-sh:            MIT
# doc/Makefile.in:              FSFULLR
# INSTALL:                      FSFAP
# m4/longlong.m4:               FSFULLR
# man/texinfo2man.c:            BSD with advertising
# regression/standard/globs.c:  BSD with advertising
# regression/standard/sys.h:    FSFUL (or so)
## Unused
# config/texinfo.tex:           GPLv3+ with exception
# intl/plural.c:                LGPLv2+ with exception
# intl/vasnprintf.c:            LGPLv2+
License:    GPLv3+ and BSD and Verbatim
URL:        http://www.gnu.org/software/%{name}/
Source:     http://ftpmirror.gnu.org/%{name}/%{name}-%{version}.tar.xz
# Correct documentation, proposed to upstream
# <http://lists.gnu.org/archive/html/bug-indent/2018-09/threads.html>
Patch1:     indent-2.2.12-doc-Fix-dont-cuddle-else-short-option-and-index-remo.patch
# Add AX_CC_FOR_BUILD m4 macro definition, copied from
# <http://git.savannah.gnu.org/gitweb/?p=autoconf-archive.git;a=blob_plain;f=m4/ax_cc_for_build.m4>,
# license is "GPLv3+ with exception", proposed to upstream
# <http://lists.gnu.org/archive/html/bug-indent/2018-09/threads.html>
Patch2:     indent-2.2.12-Add-m4-ax_cc_for_build.m4-for-CC_FOR_BUILD.patch
# Recognize binary integer literals, bug #1655319, submitted to the upstream
# <http://lists.gnu.org/archive/html/bug-indent/2018-12/msg00000.html>
Patch3:     indent-2.2.12-Recognize-binary-integer-literals.patch
# Update config.sub to support aarch64, bug #925588
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext-devel
# gperf to update pre-generated code to fix compiler warnings
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  texinfo
%if %{with tex_docs}
BuildRequires:  texi2html
%endif

%description
Indent is a GNU program for beautifying C code, so that it is easier to
read.  Indent can also convert from one C writing style to a different
one.  Indent understands correct C syntax and tries to handle incorrect
C syntax.

Install the indent package if you are developing applications in C and
you want a program to format your code.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Regenerate sources
rm src/gperf.c src/gperf-cc.c
# Update config.sub to support aarch64, bug #925588
autoreconf -i -f

%build
# Enable 64-bit stat(2)
%configure CFLAGS='%optflags -D_FILE_OFFSET_BITS=64'
%{make_build}

%install
%{make_install}
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir $RPM_BUILD_ROOT/%{_bindir}/texinfo2man \
    $RPM_BUILD_ROOT/usr/doc/indent/indent.html

%find_lang %name

%check
make check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README.md ChangeLog*
%{_bindir}/indent
%{_mandir}/man1/indent.*
%{_infodir}/indent.info*


%changelog
* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.2.12-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Conditionally build tex-based documentation

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Petr Pisar <ppisar@redhat.com> - 2.2.12-3
- Correct invoking tests at build time
- Recognize binary integer literals (bug #1655319)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Petr Pisar <ppisar@redhat.com> - 2.2.12-1
- 2.2.12 bump
- License corrected to from "GPLv3+" to "GPLv3+ and BSD and Verbatim"

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Petr Pisar <ppisar@redhat.com> - 2.2.11-25
- Remove install-info from scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 09 2015 Petr Pisar <ppisar@redhat.com> - 2.2.11-19
- Fix -nbdfa and -nbdfe typo in the manual

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Petr Pisar <ppisar@redhat.com> - 2.2.11-17
- Correct a typo about enabling control comment in manual page

* Wed Mar 18 2015 Petr Pisar <ppisar@redhat.com> - 2.2.11-16
- Support hexadecimal floats
- Adapt to changes in texi2html-5.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Petr Pisar <ppisar@redhat.com> - 2.2.11-13
- Move upstream URL to Free Software Foundation

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Petr Pisar <ppisar@redhat.com> - 2.2.11-11
- Update config.sub to support aarch64 (bug #925588)

* Thu Mar 07 2013 Petr Pisar <ppisar@redhat.com> - 2.2.11-10
- Fix copying overlapping comments when using -fca option

* Tue Feb 19 2013 Petr Pisar <ppisar@redhat.com> - 2.2.11-9
- Fix compiler warnings
- Enable 64-bit stat (bug #912635)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Petr Pisar <ppisar@redhat.com> - 2.2.11-6
- Return non-zero exit code on tests failure

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Petr Pisar <ppisar@redhat.com> - 2.2.11-4
- Fix decimal float constant suffixes (bug #733051)
- Remove uneeded spec code

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010 Petr Pisar <ppisar@redhat.com> - 2.2.11-2
- Clean spec file from commented code

* Tue Jul 20 2010 Petr Pisar <ppisar@redhat.com> - 2.2.11-1
- 2.2.11 bump (#485022)
- Remove useless patches: indent-2.2.9-cdw.patch, indent-2.2.9-explicits.patch
- Reenable parallel build
- Distribute upstream changelogs

* Tue Aug 11 2009 Roman Rakus <rrakus@redhat.com> - 2.2.10-5
- Don't print errors in post and preun sections (#515935)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.10-2
- Cleared man patch to comply with fuzz=0
  Resolves: #465015

* Wed Mar 12 2008 Petr Machata <pmachata@redhat.com> - 2.2.10-1
- Rebase to 2.2.10
  - Dropped three patches
  - Fix Source and URL
  - Clean up spec

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.9-19
- Autorebuild for GCC 4.3

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-18
- Fix licensing tag.

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-17
- Tidy up the specfile per rpmlint comments
- Use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-15
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223703

* Mon Jul 17 2006 Karsten Hopp <karsten@redhat.de> 2.2.9-14
- add buildrequires makeinfo

* Sun Jul 16 2006 Petr Machata <pmachata@redhat.com> - 2.2.9-13
- Add some missing options to manpage/infopage (#199037)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.3.1
- rebuild

* Tue Jun  6 2006 Petr Machata <pmachata@redhat.com> - 2.2.9-12.3
- BuildRequires gettext

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Petr Machata <pmachata@redhat.com> 2.2.9-12
- Adding Wei-Lun Chao's zh_TW UTF-8 messages (#134044)

* Wed Feb 01 2006 Petr Machata <pmachata@redhat.com> 2.2.9-11
- Setting LC_ALL instead of LC_MESSAGES in order to fix output of
  KOI8-R characters.  (#134044)

* Fri Jan 27 2006 Petr Machata <pmachata@redhat.com> 2.2.9-10
- Changed the placement of closing `while' of `do {} while' command
  under a -cdw option.  It's now cuddled up to the brace. (#67781)
- Changed the indentation of cuddled `else': the brace is lined up
  under opening brace.  Let's see if people like it.  It looks less
  strange than before, but still it looks strange.

* Wed Jan 18 2006 Petr Machata <pmachata@redhat.com> 2.2.9-9
- Silenting some warnings, voidifying some functions that were
  implicitly int but didn't actually return anything. (#114376)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.2.9-8
- add %%check

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.2.9-7
- rebuilt with GCC4
- fixed source URL

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 03 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add a bugfix (copied from debian)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.9

* Wed Nov 27 2002 Elliot Lee <sopwith@redhat.com> 2.2.8-4
- Don't use wildcard on bindir

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.8

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.7-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.7
- use find_lang for translations
- do not gzip man-page

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Nov 19 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.6

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%configure, %%makeinstall, %%{_infodir}, %%{_mandir} 
  and %%{_tmppath}
- don't use %%{_prefix}

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL
- remove manual stripping


* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed

* Thu Jan 20 2000 Bill Nottingham <notting@redhat.com>
- 2.2.5

* Mon Jul 26 1999 Bill Nottingham <notting@redhat.com>
- 2.2.0

* Fri Jul 16 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1.1

* Sun May 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.0.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- use install-info

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
