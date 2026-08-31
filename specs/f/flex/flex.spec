# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: A tool for generating scanners (text pattern recognizers)
Name: flex
Version: 2.6.4
Release: 20%{?dist}

# An SPDX license string check done against flex-2.6.4 using fossology
# found strings corresponding to the licenses noted below across the flex
# source tree.
License: BSD-3-Clause-flex AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GPL-3.0-or-later WITH Bison-exception-2.2 AND GPL-3.0-or-later WITH Texinfo-exception AND FSFAP AND FSFUL AND FSFULLR AND FSFULLRWD AND GPL-2.0-or-later AND X11

URL: https://github.com/westes/flex
Source: https://github.com/westes/flex/releases/download/v%{version}/flex-%{version}.tar.gz

Patch0: flex-rh1389575.patch

Requires: m4
BuildRequires: gettext gettext-devel bison m4 help2man gcc gcc-c++ automake libtool
BuildRequires: make

Obsoletes: flex-doc < 2.6.4-8
Provides: flex-doc = %{version}-%{release}

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

# We keep the libraries in separate sub-package to allow for multilib
# installations of flex.

%define somajor 2

%package -n libfl%{somajor}
Summary: Libraries for the flex scanner generator

%description -n libfl%{somajor}
flex is a tool for generating scanners.

This package contains the shared library with default implementations of
`main' and `yywrap' functions that binaries using flex can choose to link
against instead of implementing on their own.

%package -n libfl-devel
Summary: Development files for the flex scanner generator
Requires: libfl%{somajor} = %{version}-%{release}

%description -n libfl-devel
flex is a tool for generating scanners.

This package contains files required to build programs that use flex
libraries.

%package -n libfl-static
Summary: Static libraries for the flex scanner generator
# We renamed flex-static to flex-devel in version 2.5.35-15:
Obsoletes: flex-static < 2.5.35-15
Provides: flex-static = %{version}-%{release}
# We renamed flex-devel to libfl-static in version 2.6.4-6.  This clarifies
# the nature of the package and brings us in line with naming used by SUSE
# and Debian:
Obsoletes: flex-devel < 2.6.4-6
Provides: flex-devel = %{version}-%{release}

%description -n libfl-static

flex is a tool for generating scanners.

This package contains the static library with default implementations of
`main' and `yywrap' functions that binaries using flex can choose to
statically link against instead of implementing their own.

%prep
%autosetup -p1

%build
autoreconf -i
%configure --docdir=%{_pkgdocdir} CFLAGS="-fPIC $RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_pkgdocdir}/{README.cvs,TODO,AUTHORS,COPYING,ONEWS}
# Exclude libtool archives (.la) as per Fedora packaging guidelines
find %{buildroot} -name '*.la' -delete

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_libdir}/libl.a
)

%find_lang flex

%check
echo ============TESTING===============
make check
echo ============END TESTING===========

%files -f flex.lang
%dir %{_pkgdocdir}
%license COPYING
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README.md
%{_bindir}/*
%{_mandir}/man1/*
%{_includedir}/FlexLexer.h
%{_infodir}/flex.info*

%files -n libfl%{somajor}
%{_libdir}/libfl.so.%{somajor}*

%files -n libfl-devel
%{_includedir}/FlexLexer.h
%{_libdir}/libfl.so

%files -n libfl-static
%dir %{_pkgdocdir}
%license COPYING
%{_libdir}/*.a

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 23 2024 Arjun Shankar <arjun@redhat.com> - 2.6.4-17
- Provide flex-doc via the main flex package

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Arjun Shankar <arjun@redhat.com> - 2.6.4-14
- Analyse flex sources for license information
- Migrate License field to SPDX identifiers for
  https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2
  (#2222083)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 06 2021 Arjun Shankar <arjun@redhat.com> - 2.6.4-8
- Remove and obsolete the flex-doc subpackage; documention is provided in the
  main package itself
- Specify versions in "Provides:" lines for flex-static and flex-devel

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 21 2020 Arjun Shankar <arjun@redhat.com> - 2.6.4-6
- Re-work flex subpackages and provide shared libraries (#1327851):
- Remove and obsolete the flex-devel subpackage containing static libraries
- Provide shared libraries in a new subpackage named libfl2
- Provide development files in a new subpackage named libfl-devel
- Provide static libraries in a new subpackage named libfl-static

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 03 2018 Arjun Shankar <arjun@redhat.com> - 2.6.4-1
- Rebase to 2.6.4
- Fix build failure due to missing include and `reallocarray' prototype
- Add gettext-devel, automake and libtool to build dependencies, and
  execute `autoreconf -i' to regenerate files after patching configure.ac

* Mon Jul 23 2018 Arjun Shankar <arjun@redhat.com> - 2.6.1-10
- Add gcc-c++ as a build-time requirement

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Arjun Shankar <arjun@redhat.com> - 2.6.1-8
- Remove g++ signed/unsigned comparison warning in generated scanner

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.6.1-7
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.6.1-3
- Add missing %%license macro

* Sun Sep 25 2016 Patsy Franklin <pfrankli@redhat.com> - 2.6.1-2
- Fix several type comparison issues including BZ #1373601

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.6.1-1
- Rebase to 2.6.1 (#1318074,#1364943)
- update URL (github), drop unused patches (#1238860)

* Wed Jul 27 2016 Patsy Franklin <pfrankli@redhat.com> - 2.6.0-2
  Fix wrong type on num_to_read.  BZ #1360744

* Thu Mar 10 2016 Patsy Franklin <pfrankli@redhat.com> - 2.6.0-1
- Rebase to 2.6.0
- Pick up an additional patch requested in BZ #1281976

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Patsy Franklin <pfrankli@redhat.com> - 2.5.39-3
- Remove obsolete patches from git repository.  (BZ #1238860)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Patsy Franklin <pfrankli@redhat.com> - 2.5.39-1
- Rebase to 2.5.39

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.37-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.5.37-7
- Make docdir unversioned where appropriate (#993754)
- Install docs to one common package doc dir, drop separate one for -doc
- Include COPYING in -devel
- Fix bogus dates in %%changelog

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Patsy Franklin <pfrankli@redhat.com> - 2.5.37-5
- Add a patch to remove obsolete bison constructs YYLEX_PARAM and 
  YYPARSE_PARAM. Use %%lex-param, %%parse-param, or %%param.

* Tue Sep  3 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-4
- Add a patch for "comparison between signed and unsigned" warnings
  that GCC produces when compiling flex-generated scanners
  (flex-2.5.37-types.patch)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-2
- Update config.sub and config.guess to support aarch64

* Wed Mar 20 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-1
- Rebase to 2.5.37

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Petr Machata <pmachata@redhat.com> - 2.5.36-2
- Bump for rebuild

* Tue Jul 31 2012 Petr Machata <pmachata@redhat.com> - 2.5.36-1
- Rebase to 2.5.36
  - Drop flex-2.5.35-sign.patch, flex-2.5.35-hardening.patch,
    flex-2.5.35-gcc44.patch, flex-2.5.35-missing-prototypes.patch
  - Add flex-2.5.36-bison-2.6.1.patch
  - Add a subpackage doc
- Resolves #842073

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Petr Machata <pmachata@redhat.com> - 2.5.35-15
- Rename flex-static to flex-devel so that it gets to repositories of
  minor multi-lib arch (i386 on x86_64 etc.)
- Resolves: #674301

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-12
- Drop the dependency of core package on flex-static.
- Resolves: #624549

* Wed Jul 14 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-11
- Forgot that the changes in flex.skl won't propagate to skel.c
- Resolves: #612465

* Tue Jul 13 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-10
- Declare yyget_column and yyset_column in reentrant mode.
- Resolves: #612465

* Wed Jan 20 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-9
- Move libraries into a sub-package of their own.

* Tue Jan 12 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-8
- Add source URL

* Mon Aug 24 2009 Petr Machata <pmachata@redhat.com> - 2.5.35-7
- Fix installation with --excludedocs
- Resolves: #515928

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.5.35-5
- Resolves: #496548.

* Mon Apr 20 2009 Petr Machata <pmachata@redhat.com> - 2.5.35-4
- Get rid of warning caused by ignoring return value of fwrite() in
  ECHO macro.  Debian patch.
- Resolves: #484961

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 12 2008 Petr Machata <pmachata@redhat.com> - 2.5.35-2
- Resolves: #445950

* Wed Feb 27 2008 Petr Machata <pmachata@redhat.com> - 2.5.35-1
- Rebase to 2.5.35. Drop two patches.
- Resolves: #434961
- Resolves: #435047

* Mon Feb 25 2008 Petr Machata <pmachata@redhat.com> - 2.5.34-1
- Rebase to 2.5.34. Drop five patches.
- Resolves: #434676

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-17
- Generate prototypes for accessor functions.  Upstream patch.
- Related: #432203

* Mon Feb  4 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-16
- Fix comparison between signed and unsigned in generated scanner.
  Patch by Roland McGrath.
- Resolves: #431151

* Tue Jan 15 2008 Stepan Kasal <skasal@redhat.com> - 2.5.33-15
- Do not run autogen.sh, it undoes the effect of includedir patch.
- Adapt test-linedir-r.patch so that it fixes Makefile.in and works
  even though autogen.sh is not run.

* Thu Jan 10 2008 Stepan Kasal <skasal@redhat.com> - 2.5.33-14
- Insert the "-fPIC" on configure command-line.
- Drop the -fPIC patch.

* Tue Jan  8 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-13
- Patch with -fPIC only after the autogen.sh is run.

* Thu Jan  3 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-12
- Run autogen.sh before the rest of the build.
- Add BR autoconf automake gettext-devel.

* Thu Aug 30 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-11
- Add BR gawk
- Fix use of awk in one of the tests

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.5.33-10
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-9
- Remove wrong use of @includedir@ in Makefile.in.
- Spec cleanups.
- Related: #225758

* Fri Jun 22 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-8
- Don't emit yy-prefixed variables in C++ mode.  Thanks Srinivas Aji.
- Related: #242742
- Related: #244259

* Fri May 11 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-7
- Allow joining short options into one commandline argument.
- Resolves: #239695

* Fri Mar 30 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-5
- Make yy-prefixed variables available to scanner even with -P.

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-4
- Use %%find_lang to package locale files.

* Wed Jan 31 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-3
- Compile with -fPIC.

* Tue Jan 30 2007 Petr Machata <pmachata@redaht.com> - 2.5.33-2
- Add Requires:m4.

* Fri Jan 19 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-1
- Rebase to 2.5.33

* Tue Jul 18 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-41
- Reverting posix patch.  Imposing posix because of warning is too
  much of a restriction.

* Sun Jul 16 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-40
- using dist tag

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-39
- fileno is defined in posix standard, so adding #define _POSIX_SOURCE
  to compile without warnings (#195687)
- dropping 183098 test, since the original bug was already resolved

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-38.1
- rebuild

* Fri Mar 10 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-38
- Caught the real cause of #183098.  It failed because the parser
  built with `flex -f' *sometimes* made it into the final package, and
  -f assumes seven-bit tables.  Solution has two steps.  Move `make
  bigcheck' to `%%check' part, where it belongs anyway, so that flexes
  built during `make bigcheck' don't overwrite original build.  And
  change makefile so that `make bigcheck' will *always* execute *all*
  check commands.

* Wed Mar  8 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-37.4
- adding test for #183098 into build process

* Thu Mar  2 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-37.3
- rebuilt, no changes inside. In hunt for #183098

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-37.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-37.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-37
- adding `make bigcheck' into build process.  Refreshing initscan.c to
  make this possible.

* Wed Jan 18 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-36
- Applying Jonathan S. Shapiro's bugfix-fixing patch. More std:: fixes
  and better way to silent warnings under gcc.

* Fri Jan 13 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-35
- Adding `std::' prefixes, got rid of `using namespace std'. (#115354)
- Dummy use of `yy_flex_realloc' to silent warnings. (#30943)
- Adding URL of flex home page to spec (#142675)

* Sun Dec 18 2005 Jason Vas Dias<jvdias@redhat.com>
- rebuild with 'flex-pic.patch' to enable -pie links
  on x86_64 (patch from Jesse Keating) .

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.5.4a-34
- rebuilt with GCC 4
- add %%check script

* Tue Aug 24 2004 Warren Togami <wtogami@redhat.com> 2.5.4a-33
- #116407 BR byacc

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 2.5.4a-28
- don't include -debuginfo files in package.

* Mon Nov  4 2002 Than Ngo <than@redhat.com> 2.5.4a-27
- YY_NO_INPUT patch from Jean Marie

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Than Ngo <than@redhat.com> 2.5.4a-25
- don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  2 2002 Than Ngo <than@redhat.com> 2.5.4a-23
- More ISO C++ 98 fixes (#59670)

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 2.5.4a-22
- rebuild in new enviroment

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.4a-21
- More ISO C++ 98 fixes (#59670)

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.4a-20
- Fix ISO C++ 98 compliance (#59670)

* Wed Jan 23 2002 Than Ngo <than@redhat.com> 2.5.4a-19
- fixed #58643

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov  6 2001 Than Ngo <than@redhat.com> 2.5.4a-17
- fixed for working with gcc 3 (bug #55778)

* Sat Oct 13 2001 Than Ngo <than@redhat.com> 2.5.4a-16
- fix wrong License (bug #54574)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sat Sep 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix generation of broken code (conflicting isatty() prototype w/ glibc 2.2)
  This broke, among other things, the kdelibs 2.0 build
- Fix source URL

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging (64bit systems need to use libdir).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff.

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- add a libl.a link to libfl.a

* Wed Aug 25 1999 Jeff Johnson <jbj@redhat.com>
- avoid uninitialized variable warning (Erez Zadok).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.5.4 to 2.5.4a

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 2.5.4
