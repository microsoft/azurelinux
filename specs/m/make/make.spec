# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- coding: utf-8 -*-
# This decides the SRPM name.  Set to "make" for a rolling release
# (like Fedora) or "make-latest" for a long term release that needs
# optional versioned updates.
Name: make
Epoch: 1
Version: 4.4.1
Release: 12%{?dist}
License: GPL-3.0-or-later AND LGPL-2.1-or-later AND GFDL-1.3-or-later AND FSFULLR
URL: https://www.gnu.org/software/make/
Source: https://ftp.gnu.org/gnu/make/make-%{version}.tar.gz

%if "%{name}" != "make"
# Set this to the sub-package base name, for "make-latest"
%global make %(echo make%{version} | tr -d .)
%if 0%{?rhel} > 0
%global _prefix /opt/rh/%{make}
%else
# We intentionally do not define a case for Fedora, as it should not
# need this functionality, and letting it error avoids accidents.
%{error:"Each downstream must specify its own /opt namespace"}
%endif
Summary: Meta package to include latest version of make
%else
%global make %{name}
Summary: A GNU tool which simplifies the build process for users
Provides:   make-latest = %{version}-%{release}
Provides:   %(echo make%{version} | tr -d .) = %{version}-%{release}
%endif

# This gives the user the option of saying --with guile, but defaults to WITHOUT
%bcond_with guile

Patch0: make-4.3-getcwd.patch

# Assume we don't have clock_gettime in configure, so that
# make is not linked against -lpthread (and thus does not
# limit stack to 2MB).
Patch1: make-4.0-noclock_gettime.patch

# BZs #142691, #17374
Patch2: make-4.3-j8k.patch

# autoreconf
BuildRequires: make
BuildRequires: autoconf, automake, gettext-devel
BuildRequires: procps
BuildRequires: perl
%if %{with guile}
BuildRequires: pkgconfig(guile-3.0)
%endif
BuildRequires: gcc

%if "%{name}" != "make"
# We're still on the make-latest package
Requires: %{make}
%description -n make-latest
The latest GNU Make, with a version-specific install
%files -n make-latest

%package -n %{make}
Summary: A GNU tool which simplifies the build process for users
%endif

%description -n %{make}
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%package -n %{make}-devel
Summary: Header file for externally visible definitions

%description -n %{make}-devel
The %{make}-devel package contains gnumake.h.

%prep
%autosetup -n make-%{version} -p1

rm -f tests/scripts/features/parallelism.orig

%build
autoreconf -vfi

%configure \
%if %{with guile}
    --with-guile
%else
    --without-guile
%endif

%make_build

%install
%make_install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%if "%{name}" != "make"
install -d -m 755 ${RPM_BUILD_ROOT}/etc/scl/prefixes
dirname %{_prefix} > %{make}.prefix
install -p -m 644 %{make}.prefix ${RPM_BUILD_ROOT}/etc/scl/prefixes/%{make}

echo "export PATH=%{_prefix}/bin:\$PATH" > enable.scl
install -p -m 755 enable.scl ${RPM_BUILD_ROOT}/%{_prefix}/enable
%endif

%find_lang make

%check
echo ============TESTING===============
/usr/bin/env LANG=C make check && true
echo ============END TESTING===========

%files -n %{make} -f make.lang
%license COPYING
%doc NEWS README AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_includedir}/gnumake.h
%if "%{name}" != "make"
/etc/scl/prefixes/%{make}
%{_prefix}/enable
%endif

%files -n %{make}-devel
%{_includedir}/gnumake.h

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 2 2024 DJ Delorie <dj@redhat.com> - 1:4.4.1-9
- Ensure that we can upgrade from make-latest to make

* Mon Jul 22 2024 Florian Weimer <fweimer@redhat.com> - 1:4.4.1-8
- Disable guile support by default

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 01 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:4.4.1-4
- Use guile-3.0

* Thu Jul 20 2023 DJ Delorie <dj@redhat.com> - 1:4.4.1-3
- Migrate License field to SPDX identifiers for
  https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 31 2023 DJ Delorie <dj@redhat.com> - 1:4.4.1-1
- Rebase to make 4.4

* Mon Jan 30 2023 DJ Delorie <dj@redhat.com> - 1:4.4-3
- Handle SIGPIPE as a fatal signal

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 1 2022 DJ Delorie <dj@redhat.com> - 1:4.4-1
- Rebase to make 4.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 DJ Delorie <dj@redhat.com> - 1:4.3-10
- Add SCL compatibility to LTS builds.

* Wed Jun 29 2022 DJ Delorie <dj@redhat.com> - 1:4.3-9
- Enable long-term supported builds.

* Fri Apr 8 2022 DJ Delorie <dj@redhat.com> - 1:4.3-8
- Rewrite filter/filter-out to avoid large stack usage. BZ #2010506
- Require perl core modules for testsuite

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 19 2021 DJ Delorie <dj@redhat.com> - 1:4.3-5
- Allow users to build with or without guile support as desired.
- Allow derivative downstreams to default to disabling guile support.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 DJ Delorie <dj@redhat.com> - 1:4.3-3
- Disable inheritance of jobserver FDs for recursive make. BZ #1827850

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 11 2020 DJ Delorie <dj@redhat.com> - 1:4.3-1
- Rebase to make-4.3. Remove obsolete patches.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 DJ Delorie <dj@redhat.com> - 1:4.2.1-15
- Use a non-blocking read with pselect to avoid hangs. BZ #1556839

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:4.2.1-13
- Run autoreconf

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:4.2.1-12
- Switch to latest guile version

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Patsy Griffin Franklin <pfrankli@redhat.com> 1:4.2.1-9
- Fix build failure caused by automake versioning differences related
  to the glob changes.
- Fix testing failure due to Perl changes related to expanding paths.

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.2.1-8
- BR: gcc, rebuild (guile)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:4.2.1-6
- Fix wrong assumptions of glibc's glob internals

* Thu Feb 01 2018 Richard W.M. Jones <rjones@redhat.com> - 1:4.2.1-5
- Add upstream patch to fix incorrect use of glibc 2.27 glob internals.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 4.2.1-2
- Add missing %%license macro

* Sun Sep 25 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-1
- Rebase to make-4.2.1. Remove obsolete patches. BZ #1338558

* Sun Sep 25 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1-6
- Make test suite requires Perl to run.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Patsy Franklin <pfrankli@redhat.com> 1:4.1-4
- Handle NULL returns from ttyname() Upstream Bug 43434.
  Resolves: #1277968

* Thu Oct 29 2015 Patsy Franklin <pfrankli@redhat.com> 1:4.1-3
- Enable Guile support.

* Thu Oct 29 2015 Patsy Franklin <pfrankli@redhat.com> 1:4.1-2
- Include patches dropped in last update as they fix reported bugs and
  update the spec file to include more info on the patches.

* Sat Oct 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 1:4.1-1
- Update to latest version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:4.0-4.1
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Sep 03 2014 Kyle McMartin <kyle@fedoraproject.org> - 1:4.0-3.1
- Pass the test-suite unconditionally until I fix the tests to cope with
  deterministic ar archives (which result in expected rebuilds not occuring)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Patsy Franklin <pfrankli@redhat.com> 1:4.0-1
- Rebase to make-4.0
  - Created make-devel sub-package to handle new dependency on gnumake.h.

* Thu Aug 22 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-19
- make now restores rlimit to its original values before launching
  subprocess via $(shell) (make-3.82-func_shell-rlimit.patch)
- Determinize one test (make-3.82-tests-SECONDARY.patch)

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-18
- Backport upstream patch that adds wildcard expansion to pattern
  rules. (make-3.82-stem_glob.patch)

* Wed Jun 19 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-17
- Add another fix for upstream bug 30612

* Thu Apr  4 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-16
- Update config.sub and config.guess to support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-14
- Drop patch5, which hasn't been applied for years

* Mon Sep 10 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-13
- Add fix for upstream bug 30653
- Resolves: #835424

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-11
- Add a patch for avoiding glob if possible by Michael Meeks

* Mon Mar 12 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-10
- Apply the following patches, proposed upstream by Norbert Thiebaud:
  - A patch for warning on call of undefined function
  - A patch for tracing calls to "eval" and "call"

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  3 2011 Petr Machata <pmachata@redhat.com> - 1:3.82-8
- Add a patch for preserving -j across Makefile rebuild
- Resolves: #698702

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-7
- Rebuilt for glibc bug#747377

* Thu May 12 2011 Lubomir Rintel <lkundrak@v3.sk> - 1:3.82-6
- Fix free-after-use with nested assignments (#703104)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-4
- Fix a discrepancy between behavior of find_next_token and
  pre-allocation of token memory in func_sort.
- Resolves: #643359

* Wed Sep 29 2010 jkeating - 1:3.82-3
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-2
- Add upstream fixes for upstream bugs 30612 and 30723
- Resolves: #631552

* Wed Aug 11 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-1
- Upstream 3.82:
  - Drop rlimit, fdleak, strcpy-overlap, recursion-test, double-free
    patches, make supports this functionality now
  - Disable the memory patch for the time being
  - Port remaining patches
  - Add weird-shell patch, upstream bug 30748
- Resolves: #618998

* Wed Aug 11 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-21
- Add BR procps
- Resolves: #616813

* Thu Jul  1 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-20
- Add a patch by Steve Kemp @debian that might fix the double free
  problem.
- Related: #609806

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-19
- Fix testsuite on F13
- Resolves: #600004

* Tue Aug 11 2009 Petr Machata <pmachata@redhat.com> - 1:3.81-18
- Fix installation with --excludedocs
- Resolves: #515917

* Fri Jul 31 2009 Petr Machata <pmachata@redhat.com> - 1:3.81-17
- Replace the use of strcpy on overlapping areas with memmove
- Resolves: #514721

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.81-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.81-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-14
- Fix patches to apply cleanly with fuzz=0

* Tue Sep 16 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-13
- Mark opened files as cloexec to prevent their leaking through fork
- Resolves: #462090

* Tue Mar 25 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-12
- Fix the rlimit patch.  The success flag is kept in memory shared
  with parent process after vfork, and so cannot be reset.
- Related: #214033

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.81-11
- Autorebuild for GCC 4.3

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-10
- Fix parallel builds with reexec.
- Related: #212111, #211290

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-8
- Cleaned up per merge review.
- Related: #226120

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-7
- Fix licensing tag.

* Fri Mar 16 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-6
- Always run testsuite with C locale.
- Resolves: #232607

* Thu Feb 22 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-5
- Fix newline handling for quoted SHELL.
- Resolves: #219409

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-4
- Tidy up the specfile per rpmlint comments
- Use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-3
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223709

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-2
- make now restores rlimit to its original values before launching
  subprocess (#214033)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.81-1.1
- rebuild

* Tue May 23 2006 Petr Machata <pmachata@redhat.com> - 1:3.81-1
- Upstream 3.81:
  - Contains several backwards incompatible changes.  See NEWS inside
    the source package to find out more.
- memory patch and error reporting patch were ported to this version.

* Wed Mar 15 2006 Petr Machata <pmachata@redhat.com> 1:3.80-11
- Applied (five years old) patch from Jonathan Kamens to allow make to
  handle several pattern-specific variables (#52962).

  The patch was changed so that it forces make to process pattern
  specific variables in the same order as they appear in file.
  (Upstream make behaves this way, too.)  This is change from old make
  behavior, which processed the variables in reverse order.  In case
  you used only x=a assignments, this had the effect of using the
  first pattern specific variable that matched.  For x+=a this just
  doesn't work, and it produces absolutely nonintuitive results.

- (It would be great if make's target-specific variables were handled
  the same way as pattern-specific ones, just without the pattern
  component.  However current handling is documented and considered a
  feature.)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 3.80-10
- H.J. Lu caught a typo in the patch and provided a new one. (#175376)

* Mon Jan 09 2006 Petr Machata <pmachata@redhat.com> 3.80-9
- Applied patch from H.J. Lu.  Somehow reduces make's enormous memory
  consumption. (#175376)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 22 2005 Jakub Jelinek <jakub@redhat.com> 3.80-8
- make sure errno for error reporting is not lost accross _() calls
- report EOF on read pipe differently from read returning < 0 reporting

* Mon Mar  7 2005 Jakub Jelinek <jakub@redhat.com> 3.80-7
- rebuilt with GCC 4

* Mon Dec 13 2004 Jakub Jelinek <jakub@redhat.com> 3.80-6
- refuse -jN where N is bigger than PIPE_BUF (#142691, #17374)

* Thu Oct  7 2004 Jakub Jelinek <jakub@redhat.com> 3.80-5
- add URL rpm tag (#134799)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add important bug-fixes from make home-page

* Sun Nov 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.80

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 29 2002 Tim Powers <timp@redhat.com>
- fix references to %%install in the changelog so that the package will build

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 3.79.1-15
- _smp_mflags
- Fix ppc build (sys_siglist issues in patch2)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Jakub Jelinek <jakub@redhat.com>
- Run make check during build

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build with current auto* tools

* Fri Jan 25 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt with gcc 3.1

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- langify
- Make sure it isn't setgid if built as root

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Aug  7 2000 Tim Waugh <twaugh@redhat.com>
- change info-dir entry so that 'info make' works (#15029).

* Tue Aug  1 2000 Jakub Jelinek <jakub@redhat.com>
- assume we don't have clock_gettime in configure, so that
  make is not linked against -lpthread (and thus does not
  limit stack to 2MB).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- add locale files (#14362).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 24 2000 Preston Brown <pbrown@redhat.com>
- 3.79.1 bugfix release

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun May  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build for some odd situations, such as
  - previously installed make != GNU make
  - /bin/sh != bash

* Mon Apr 17 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.79

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %%install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
