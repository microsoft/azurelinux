# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A front end for testing other programs
Name: dejagnu
Version: 1.6.3
Release: 14%{?dist}
Epoch: 1
# Note: baseboards/riscv-sim.exp is GPL 2.0 or later
# GFDL-1.3-or-later: Everything in doc/
License: GPL-3.0-or-later AND GFDL-1.3-or-later
Source: ftp://ftp.gnu.org/gnu/dejagnu/dejagnu-%{version}.tar.gz
URL: http://www.gnu.org/software/dejagnu/
Requires: expect
BuildArch: noarch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: expect texinfo
BuildRequires: make

Patch0: rhbz460153.patch

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%patch -P0 -p1

%build
%configure -v

%check
echo ============TESTING===============
TMP=`mktemp`
export SCREENDIR=`mktemp -d`
# Skip selected tests.  Failed testcases reported upstream:
# https://lists.gnu.org/archive/html/dejagnu/2021-09/msg00001.html
(make check RUNTESTFLAGS="--ignore pr48155.exp stats.exp"; echo $?) >> $TMP
RESULT=`tail -n 1 $TMP`
cat $TMP
rm -f $TMP
rm -rf $SCREENDIR
echo ============END TESTING===========
exit $RESULT

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
chmod a-x $RPM_BUILD_ROOT/%{_datadir}/dejagnu/runtest.exp
make DESTDIR=$RPM_BUILD_ROOT install-man
install -D -m 644 doc/dejagnu.info $RPM_BUILD_ROOT/%{_infodir}/%{name}.info

%files
%doc COPYING NEWS README AUTHORS ChangeLog doc/dejagnu.texi
%{_bindir}/runtest
%{_bindir}/dejagnu
%{_datadir}/dejagnu
%{_includedir}/dejagnu.h
%{_mandir}/*/*
%{_infodir}/dejagnu*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb  7 2024 Siddhesh Poyarekar <siddhesh@redhat.com> - 1:1.6.3-10
- Add SPDX identifiers for licenses.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jan 24 2022 Martin Cermak <mcermak@redhat.com> - 1:1.6.3-4
- Re-fix #460153 using patch from upstream PR53427
  https://debbugs.gnu.org/cgi/bugreport.cgi?bug=53427

* Thu Jan 20 2022 Martin Cermak <mcermak@redhat.com> - 1:1.6.3-3
- Fix "perror should not errcnt across test files" (#460153)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Martin Cermak <mcermak@redhat.com> - 1:1.6.3-1
- Update upstream sources (#1791672)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Matej Mužila <mmuzila@redhat.com> - 1:1.6.1-4
- Fix tests
- Add BuildRequires: gcc-c++
- Resolves: #1603770

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Matej Mužila <mmuzila@redhat.com> - 1:1.6.1-1
- Update to 1.6.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 21 2016 Matej Mužila <mmuzila@redhat.com> - 1:1.6-1
- Rebase to new upstream version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Matej Muzila <mmuzila@redhat.com> 1:1.5.3-3
- Backport upstream patch making dejagnu not to kill wrong process due to
  PID-reuse races
- Resolves rhbz#1258142

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Matej Muzila <mmuzila@redhat.com> 1:1.5.3-1
- Update to 1.5.3

* Thu Feb 12 2015 Matej Muzila <mmuzila@redhat.com> 1:1.5.2-1
- Update to 1.5.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Honza Horak <hhorak@redhat.com> - 1:1.5.1-2
- add aarch64 support into config.guess and config.sub

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> - 1:1.5.1-1
- Update to 1.5.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Honza Horak <hhorak@redhat.com> 1:1.5-6
- Spec file cleanup
- Use dejagnu.texi from upstream source

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Honza Horak <hhorak@redhat.com> 1:1.5-4
- gfortran support added
  Resolves: #635651

* Thu Mar 15 2012 Honza Horak <hhorak@redhat.com> 1:1.5-3
- fixed search runtest.exp after usrmove
  Resolves: #788811

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Honza Horak <hhorak@redhat.com> 1:1.5-1
- Update to 1.5, license changed to GPLv3+

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 22 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4.4-17
- added utils speedup patch from jakub@redhat.com
- Resolves: #557564

* Fri Oct 16 2009 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4.4-16
- fixed installation with --excludedocs rhbz#515949

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1:1.4.4-13
- rewriten patch to work with fuzz=0

* Wed Aug 27 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1:1.4.4-12
- fixed runtest (patch from jan.kratochvil@redhat.com)
- Resolves: #460153

* Mon Nov 12 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-11
- Install info file.
- Resolves: #230652

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-10
- A few more cleanups after discussion with reviewer.
- Resolves: #225679

* Wed Oct  3 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-9
- Clean up spec per merge review comments.
- Fix testsuite.
- Resolves: #225679

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-8
- Fix licesing tag.

* Wed Mar  7 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-7
- Remove mention of dejagnu.info from manpage, per comments in
  doc/Makefile.
- Resolves: #230652

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-6
- Tidy up the specfile per rpmlint comments

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.4-5.1
- rebuild

* Thu Feb 2 2006 Petr Machata <pmachata@redhat.com> 1:1.4.4-5
- Applying H.J. Lu's race condition patch. (#166000)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-4
- rebuilt with GCC 4

* Mon Nov  8 2004 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-3
- add URL (#138280)

* Mon Sep 27 2004 Warren Togami <wtogami@redhat.com> 1:1.4.4-2
- remove INSTALL & redundant copies of overview

* Tue Aug  3 2004 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-1
- update to 1.4.4
- run make check during rpm build

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Karsten Hopp <karsten@redhat.de> 1:1.4.2-9
- more missing BuildRequires

* Tue Dec 17 2002 Karsten Hopp <karsten@redhat.de> 1:1.4.2-8
- Add jadetex Buildrequires

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 1:1.4.2-7
- include dejagnu.h
- move %%{_libexecdir}/config.guess into %%{_datadir}/dejagnu 
- include overview docs (bug #59095)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 1.4.2-4
- fix makefile style variable passing (#63984)

* Thu Feb 28 2002 Jakub Jelinek <jakub@redhat.com> 1.4.2-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 28 2001 Jakub Jelinek <jakub@redhat.com> 1.4.2-1
- update to 1.4.2, mainly so that it can be built with gcc3+

* Fri Sep  7 2001 Jakub Jelinek <jakub@redhat.com> 1.4.1-3
- make it noarch again

* Wed Aug 29 2001 Jakub Jelinek <jakub@redhat.com>
- fix a typo (#52404)

* Thu Jun 28 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Tue Feb 27 2001 Tim Powers <timp@redhat.com>
- minor modifications to the spec file. Built for Powertools.
- added Epoch

* Wed Feb 21 2001 Rob Savoye <rob@welcomehome.org>
- Fixed Requires line, and changed the URL to the new ftp site.

* Sun Oct 31 1999 Rob Savoye <rob@welcomehome.org>
- updated to the latest snapshot
- added doc files
- added the site.exp config file

* Mon Jul 12 1999 Tim Powers <timp@redhat.com>
- updated to 19990628
- updated patches as needed
- added %%defattr in files section

* Wed Mar 10 1999 Jeff Johnson <jbj@redhat.com>
- add alpha expect patch (#989)
- use %%configure

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- Update to 19981215.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-10-29.

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-05-28.

* Sun Feb  1 1998 Jeff Johnson <jbj@jbj.org>
- Create.
 
