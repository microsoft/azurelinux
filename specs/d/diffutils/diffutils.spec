# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: GNU collection of diff utilities
Name: diffutils
Version: 3.12
Release: 3%{?dist}
URL: https://www.gnu.org/software/diffutils/diffutils.html
Source: https://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz
# upstream fixes
# cross compile build of 3.12 diffutils fails
Patch: diffutils-3.12-cross-compiler-build-fail.patch
# sdiff: continue → break
Patch: diffutils-3.12-sdiff-continue-break.patch
# sdiff: pacify gcc -flto -Wmaybe-uninitialized
Patch: 0001-sdiff-pacify-gcc-flto-Wmaybe-uninitialized.patch
# sdiff: port back to C17
Patch: 0001-sdiff-port-back-to-C17.patch
License: GPL-3.0-or-later
Provides: bundled(gnulib)
BuildRequires: gcc
BuildRequires: help2man
BuildRequires: autoconf, automake, texinfo
BuildRequires: make

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

%prep
%autosetup -p1

# Run autoreconf for aarch64 support (bug #925256).
autoreconf

%build
%configure
make PR_PROGRAM=%{_bindir}/pr

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%find_lang %{name}

%check
# Disable update-copyright gnulib test (bug #1239428).
>gnulib-tests/test-update-copyright.sh
make check

%files -f %{name}.lang
%doc NEWS README
%license COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/diffutils.info*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 05 2025 Than Ngo <than@redhat.com> - 3.12-2
- Upstream patches
  * cross compile build of 3.12 diffutils fails
  * sdiff: continue → break
  * sdiff: pacify gcc -flto -Wmaybe-uninitialized
  * sdiff: port back to C17

* Fri Apr 11 2025 Than Ngo <than@redhat.com> - 3.12-1
- Fixed rhbz#2358545, Update to 3.12

* Thu Mar 27 2025 Than Ngo <than@redhat.com> - 3.11-3
- diff does not show a unified diff when one of the file is empty

* Thu Mar 27 2025 Than Ngo <than@redhat.com> - 3.11-2
- Backported upstream patch, Fixed allocation typo leading to crash

* Thu Mar 27 2025 Than Ngo <than@redhat.com> - 3.11-1
- Fixed rhbz#2343469, Update to 3.11

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 30 2024 Than Ngo <than@redhat.com> - 3.10-8
- refresh patch for 'cmp -s'

* Tue Jul 23 2024 Than Ngo <than@redhat.com> - 3.10-7
- fix a regression, 'cmp -s' returns 1 even if files are identical

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Than Ngo <than@redhat.com> - 3.10-2
- Fix output of "diff -l -y" for non-ASCII input files

* Thu Jun 29 2023 Than Ngo <than@redhat.com> - 3.10-1
- Fix bz#2208831, update to 3.10
- Fix bz#2196671, diff -D no longer fails to output #ifndef lines introduced in 3.9

* Tue Mar 28 2023 Than Ngo <than@redhat.com> - 3.9-4
- Fix deprecated patch rpm marco

* Tue Feb 21 2023 Than Ngo <than@redhat.com> - 3.9-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Tim Waugh <twaugh@redhat.com> - 3.9-1
- 3.9 (bug #2161117).

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug  2 2021 Tim Waugh <twaugh@redhat.com> - 3.8-1
- 3.8.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 12 2021 Tim Waugh <twaugh@redhat.com> - 3.7-9
- Handle SIGSTKSZ no longer being a constant (bug #1943016).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 2020 Tim Waugh <twaugh@redhat.com> - 3.7-7
- Fix from gnulib upstream, commit 175e0bc (bug #1863423).

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Than Ngo <than@redhat.com> - 3.7-1
- 3.7

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Tim Waugh <twaugh@redhat.com> - 3.6-1
- 3.6 (bug #1453019).

* Tue Feb 21 2017 Than Ngo <than@redhat.com> - 3.5-3
- backport to fix  FTBFs with GCC 7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Tim Waugh <twaugh@redhat.com> - 3.5-1
- 3.5 (bug #1365325).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul  6 2015 Tim Waugh <twaugh@redhat.com> - 3.3-12
- Disable update-copyright gnulib test (bug #1239428).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.3-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 3.3-8
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Tim Waugh <twaugh@redhat.com> 3.3-6
- Fix --help output and man page (bug #1079076).

* Wed Dec  4 2013 Tim Waugh <twaugh@redhat.com> 3.3-5
- Applied upstream gnulib patch to avoid -Wformat-security warning
  (bug #1037038).

* Wed Oct 23 2013 Tim Waugh <twaugh@redhat.com> 3.3-4
- Fixed multibyte handling logic for diff -Z (bug #1012075).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Tim Waugh <twaugh@redhat.com> 3.3-2
- Run autoreconf for aarch64 support (bug #925256).

* Tue Mar 26 2013 Tim Waugh <twaugh@redhat.com> 3.3-1
- 3.3 (bug #927560).

* Fri Feb 22 2013 Tim Waugh <twaugh@redhat.com> 3.2-13
- Fixed i18n handling of 'diff -E' (bug #914666).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Tim Waugh <twaugh@redhat.com> 3.2-11
- Ported i18n patch and reinstated it (bug #870460).

* Wed Sep 19 2012 Tim Waugh <twaugh@redhat.com> 3.2-10
- Fixed license as current source says GPLv3+.

* Mon Jul 23 2012 Tim Waugh <twaugh@redhat.com> 3.2-9
- Fixed build failure.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21  2012 Tim Waugh <twaugh@redhat.com> 3.2-7
- Provides bundled(gnulib) (bug #821751).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec  8 2011 Tim Waugh <twaugh@redhat.com> 3.2-5
- Fix bug #747969 again.

* Tue Nov 29 2011 Tim Waugh <twaugh@redhat.com> 3.2-4
- Real fix for bug #747969: the diffutils info file changed name in
  3.1.  Updated the scriptlets to install/remove the correct filename
  from the info directory.

* Fri Nov 25 2011 Tim Waugh <twaugh@redhat.com> 3.2-3
- Fixed up reference to info page in man pages (bug #747969).

* Fri Nov 25 2011 Tim Waugh <twaugh@redhat.com> 3.2-2
- Applied upstream gnulib fix for float test on ppc, as well as
  correction for LDBL_MANT_DIG definition (bug #733536).

* Fri Sep  2 2011 Tim Waugh <twaugh@redhat.com> 3.2-1
- 3.2.

* Thu Aug 11 2011 Tim Waugh <twaugh@redhat.com> 3.1-1
- 3.1.

* Wed Apr 13 2011 Tim Waugh <twaugh@redhat.com> 3.0-1
- 3.0 (bug #566482).
- The i18n patch is dropped for the time being.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 25 2010 Tim Waugh <twaugh@redhat.com> 2.8.1-29
- For 'cmp -s', compare file sizes only if both non-zero (bug #563618).

* Wed Apr 21 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-28
- Build requires help2man (bug #577325).  Fixes empty diff man page.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-27
- Added comments for all patches.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-26
- Use upstream man pages.
- Ship COPYING file.

* Tue Aug 11 2009 Tim Waugh <twaugh@redhat.com> 2.8.1-25
- Only try to install the info file if it exists so that package
  installation does not fail with --excludedocs (bug #515919).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.1-22
- Fixed 'sdiff -E' (bug #484892).

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 2.8.1-21
- Rebuild for GCC 4.3.

* Wed Jan  2 2008 Tim Waugh <twaugh@redhat.com> 2.8.1-20
- Converted spec file to UTF-8 (bug #225696).
- Fixed summary (bug #225696).
- Fixed PreReq (bug #225696).
- Removed Prefix (bug #225696).
- Fixed build root (bug #225696).
- Avoid %%makeinstall (bug #225696).
- Fixed license tag (bug #225696).

* Tue Nov  6 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-19
- Rebuilt.

* Tue Nov  6 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-18
- Fixed multibyte speed improvement patch (bug #363831).

* Tue Aug 14 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-17
- Multibyte speed improvement (bug #252117).

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-16
- Make scriptlet unconditionally succeed (bug #223683).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Apr  6 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-15
- Fixed sdiff exit code handling (bug #152967).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-14
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-13
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan  8 2004 Tim Waugh <twaugh@redhat.com> 2.8.1-10
- Fix mistaken use of '|' instead of '||'.

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 2.8.1-9
- Rebuilt.

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 2.8.1-8
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-5
- i18n patch.

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-4
- Ship translations.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-1
- 2.8.1.
- No longer need immunix-owl-tmp patch.

* Wed Feb 27 2002 Tim Waugh <twaugh@redhat.com> 2.7.2-5
- Rebuild in new environment.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Nov 02 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-3
- Make sure %%post scriplet doesn't fail if --excludedocs is used.

* Fri Jun 01 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-2
- Install diff.1, since it's no longer in man-pages.

* Fri Mar 30 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-1
- 2.7.2.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix %%changelog entries (escape them)
- update source location
- remove manual stripping
- add URL

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- add %%defattr
- use rpm macros

* Wed May 31 2000 Ngo Than <than@redhat.de>
- put man pages and info files in correct place
- cleanup specfile

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Mon Apr 19 1999 Jeff Johnson <jbj@redhat.com>
- man pages not in %%files.
- but avoid conflict for diff.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- add man pages (#831).
- add %%configure and Prefix.

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul 14 1998 Bill Kawakami <billk@home.com>
- included the four man pages stolen from Slackware

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun May 03 1998 Cristian Gafton <gafton@redhat.com>
- fixed spec file to reference/use the $RPM_BUILD_ROOT always
    
* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed where it looks for 'pr' (/usr/bin, rather than /bin)

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
