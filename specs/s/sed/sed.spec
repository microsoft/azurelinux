# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- coding: utf-8 -*-

Summary: A GNU stream text editor
Name: sed
Version: 4.9
Release: 5%{?dist}
License: GPL-3.0-or-later
URL: http://sed.sourceforge.net/
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.xz
Source1: http://sed.sourceforge.net/sedfaq.txt
Patch0: sed-b-flag.patch
Patch1: sed-c-flag.patch
Patch2: sed-covscan-annotations.patch
BuildRequires: make
BuildRequires: glibc-devel, libselinux-devel, libacl-devel, automake, autoconf, gcc
BuildRequires: perl-Getopt-Long
BuildRequires: perl(FileHandle)

# for tests.  More tests require a ja_JP locale, but glibc-langpack-ja gives:
#   invalid-mb-seq-UMR.sh: skipped test: locale 'ja_JP' is buggy
#   mb-charclass-non-utf8.sh: skipped test: ja_JP shift-jis locale not found
BuildRequires: glibc-langpack-el, glibc-langpack-en
BuildRequires: glibc-langpack-ru

%ifarch %{valgrind_arches}
BuildRequires: valgrind
%endif

Provides: /bin/sed

#copylib
Provides: bundled(gnulib)

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%autosetup -p1

%build
%configure --without-included-regex
%make_build
install -m 644 -p %{SOURCE1} sedfaq.txt
gzip -9 sedfaq.txt

%check
echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}
%make_install
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %{name}

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING 
%doc BUGS NEWS THANKS README AUTHORS sedfaq.txt.gz
%{_bindir}/sed
%{_infodir}/sed.info*
%{_mandir}/man1/sed.1*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 David Abdurachmanov <davidlt@rivosinc.com> - 4.9-2
- Properly check valgrind arches (riscv64 is not ported)

* Tue Jan 30 2024 Paolo Bonzini <pbonzini@redhat.com> - 4.9-1
- Rebase to 4.9
- Update downstream patches
- Resolves: rhbz#2140486
- Remove change to gnulib tests, they pass anyway
- Install valgrind and langpacks to increase test coverage

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 4.8-13
- migrate to SPDX license format

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Jakub Martisko <jamartis@redhat.com> - 4.8-9
- Add annotations to disable false positives in the covscan
- Related: rhbz#1938867

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 Jakub Martisko <jamartis@redhat.com> - 4.8-6
- Minor spec cleanup

* Mon Aug 03 2020 Jakub Martisko <jamartis@redhat.com> - 4.8-5
- Use make macros

* Mon Aug 03 2020 Jakub Martisko <jamartis@redhat.com> - 4.8-4
- Replace some hardcoded constants in the gnulib-testsuite
  ... that caused build failures on arm7

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 11 2020 Jakub Martisko <jamartis@redhat.com> - 4.8-1
- Rebase to 4.8
- Refresh the downstream patch and split it into two

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 03 2018 Jakub Martisko <jamartis@redhat.com> - 4.5-1
- Rebase to 4.5
- Drop patches from 4.4-4 and 4.4-7

* Thu Mar 08 2018 Jakub Martisko <jamartis@redhat.com> - 4.4-7
- Fix build failure with glibc-2.28

* Thu Mar 08 2018 Jakub Martisko <jamartis@redhat.com> - 4.4-6
- Add gcc to BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018  Jakub Martisko <jamartis@redhat.com> - 4.4-4
- When editing file inplace, the SELinux context should
  be based on the link instead of the target file itself.
  --follow-symlinks option remains unchanged
- Resolves: #1401442

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 09 2017  Jakub Martisko <jamartis@redhat.com> - 4.4-1
- new version 4.4
- removed COPYING.DOC license which is no longer in upstream
- Resolves: #1410093

* Wed Jan 04 2017  Jakub Martisko <jamartis@redhat.com> - 4.3-1
- new version 4.3
- Resolves: #1410093

* Tue Feb 09 2016 Petr Stodulka <pstodulk@redhat.com> - 4.2.2-15
- provides /bin/sed

* Tue Feb 09 2016 Petr Stodulka <pstodulk@redhat.com> - 4.2.2-14
- remove meaningless redefinition of _bindir - it's standard macro now;
  sed will be store in /usr/bin/sed
  Resovles: #1305835

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Petr Stodulka <pstodulk@redhat.com> - 4.2.2-12
- use global instead of define in spec file
- added new build dependency on perl-Getopt-Long

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.2.2-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 4.2.2-8
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Jan Pacner <jpacner@redhat.com> - 4.2.2-6
- Resolves: #1061367 (Dropping -b option breaks cross-platform compat.)
- Related: #948598 (Man page scan results for sed)
- introduce -c argument, add help for -b --binary arguments,
  cleanup arguments & help)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Fridolin Pokorny <fpokorny@redhat.com> - 4.2.2-4
- Added libacl-devel to BuildRequires for ACL support rhbz#959432

* Fri May 03 2013 Fridolin Pokorny <fpokorny@redhat.com> - 4.2.2-3
- Fixed option handling rhbz#948598

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Martin Briza <mbriza@redhat.com> - 4.2.2-1
- New release
- Dropping included patches: sed-4.2.1-data-loss.patch sed-4.2.1-fix-0x26-on-RHS.patch sed-4.2.1-makecheck.patch
- Dropping unused patch sed-4.2.1-dummyparam.diff
- Regenerated sed-4.2.{1,2}-copy.patch
- Minor change to patching (creating backup files)

* Tue Jul 10 2012 Martin Briza <mbriza@redhat.com> - 4.2.1-10
- Fixed the readded -c option
  Resolves: #832855

* Wed Jun 13 2012 Martin Briza <mbriza@redhat.com> - 4.2.1-9
- Backported commit from upstream to fix treating "x26" as "&" character
- Added virtual provide for gnulib according to http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
  Resolves: #812067 #821776

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 4.2.1-7
- avoid silent data loss when an input line is 2^31 bytes or longer
  Resolves: #720438

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 17 2010 Jan Görig <jgorig@redhat.com> 4.2.1-5
- fixed make check on non UTF-8 locale - upstream patch rhbz#550731
- readded -c option (thanks Paolo Bonzini) rhbz#566455
- removed previous -c dummy patch
- changed license to GPLv3+

* Fri Oct 16 2009 Jiri Moskovcak <jmoskovc@redhat.com> 4.2.1-4
- added libselinux-devel to buildrequires rhbz#514182
- fixed problem with --excludedocs rhbz#515913

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.2.1-3
- Use bzipped upstream tarball.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009  Jiri Moskovcak <jmoskovc@redhat.com> - 4.2.1-1
- new version
- obsoletes previous patches
- added patch to maintain backwards compatibility for scripts using -c/--copy
- Resolves: #502934

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Jiri Moskovcak <jmoskovc@redhat.com> 4.1.5-11
- improved follow.patch (thanks to Arkadiusz Miskiewicz for initial patch)
- Resolves: #470912

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.5-10
- Autorebuild for GCC 4.3

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-9
- Fix licensing tag.
- Clean up per merge review comments.
- Resolves: #226404

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-8
- tidy up the specfile per rpmlint comments
- use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-7
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223716

* Fri Dec  8 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-6
- Split confused patches "copy+symlink" and "relsymlink" into discrete
  "copy" and "symlink".

* Mon Sep  4 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-5
- Fix handling of relative symlinks (#205122)

* Thu Aug  3 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-4
- remove superfluous multibyte processing in str_append for UTF-8
  encoding (thanks Paolo Bonzini, #177246)

* Mon Jul 17 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-3
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-2.2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.2
- typo in patch name

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2
- #185374:
  - Follow symlinks before rename (avoid symlink overwrite)
  - Add -c flag for copy instead of rename (avoid ownership change)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 4.1.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 4.1.4-1
- update to 4.1.4

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 4.1.2-5
- rebuilt with GCC 4

* Fri Oct  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-4
- fix up make check to run sed --version with LC_ALL=C
  in the environment (#129014)

* Sat Oct  2 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-3
- add sedfaq.txt to %%{_docdir} (#16202)

* Mon Aug 23 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.2

* Thu Jul  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.1-1
- update to 4.1.1

* Mon Jun 21 2004 Jakub Jelinek <jakub@redhat.com> 4.1-1
- update to 4.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Jakub Jelinek <jakub@redhat.com> 4.0.9-1
- update to 4.0.9
- BuildRequire recent glibc and glibc-devel (#123043)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 4.0.8-3
- if not -n, print current buffer after N command on the last line
  unless POSIXLY_CORRECT (#112952)
- adjust XFAIL_TESTS for the improved glibc regex implementation
  (#112642)

* Fri Nov 14 2003 Jakub Jelinek <jakub@redhat.com> 4.0.8-2
- enable --without-included-regex again
- use fastmap for regex searching

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.8
- simplify specfile
- disable --without-included-regex to pass the testsuite

* Thu Jun 26 2003 Jakub Jelinek <jakub@redhat.com> 4.0.7-3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.7
- use "--without-included-regex"
- do not gzip info pages in spec file, "TODO" is not present anymore

* Thu Jan 23 2003 Jakub Jelinek <jakub@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt to fix x86-64 miscompilation
- run make check in %%build

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com>
- Remove stale URLs from documentation (#62519)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 2000.11.28 patch
- Rebuild for 7.1 tree

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
