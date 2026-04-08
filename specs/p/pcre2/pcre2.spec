# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Add readline edditing in pcre2test tool
%bcond_without pcre2_enables_readline

# Disable SELinux-frindly JIT allocator because it seems not to be fork-safe,
# https://bugs.exim.org/show_bug.cgi?id=1749#c45
%bcond_with pcre2_enables_sealloc

# This is stable release:
#%%global rcversion RC1
Name:       pcre2
Version:    10.47
Release:    %{?rcversion:0.}1%{?rcversion:.%rcversion}%{?dist}
%global     myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
# the library:                          BSD with exceptions
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text with exceptions and
#                                       Public Domain declaration
#                                       for testdata
#Bundled
# src/sljit:                            BSD
#Not distributed in any binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# cmake/COPYING-CMAKE-SCRIPTS:          BSD
# compile:                              GPLv2+ with exception
# config.guess:                         GPLv3+ with exception
# config.sub:                           GPLv3+ with exception
# configure:                            FSFUL and GPLv2+ with exception
# depcomp:                              GPLv2+ with exception
# INSTALL:                              FSFAP
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and (MIT or GPLv3+)
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFUL and FSFULLR and
#                                       GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# Makefile.in:                          FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:    BSD-3-Clause AND FSFULLR AND X11 AND GPL-2.0-or-later AND FSFAP AND FSFUL AND GPL-3.0-or-later
URL:        https://www.pcre.org/
Source0:    https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{version}/pcre2-%{myversion}.tar.bz2
Source1:    https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{version}/pcre2-%{myversion}.tar.bz2.sig
# This New-Public-Key was retrieved using
# gpg --keyserver keyserver.ubuntu.com --recv-keys A95536204A3BB489715231282A98E77EB6F24CA8
# gpg --export --armor A95536204A3BB489715231282A98E77EB6F24CA8 > New-Public-Key
# The GPG key changed with the new upstream maintainer
# More in https://github.com/PCRE2Project/pcre2/blob/master/SECURITY.md
Source2:    https://ftp.pcre.org/pub/pcre/New-Public-Key
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre2-10.10-Fix-multilib.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
%if %{with pcre2_enables_readline}
BuildRequires:  readline-devel
%endif
BuildRequires:  sed
Requires:       %{name}-syntax = %{version}-%{release}
Provides:       bundled(sljit)

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%package utf16
Summary:    UTF-16 variant of PCRE2
Provides:   bundled(sljit)
Requires:   %{name}-syntax = %{version}-%{release}
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf16
This is PCRE2 library working on UTF-16 strings.

%package utf32
Summary:    UTF-32 variant of PCRE2
Provides:   bundled(sljit)
Requires:   %{name}-syntax = %{version}-%{release}
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf32
This is PCRE2 library working on UTF-32 strings.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf16%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf32%{?_isa} = %{version}-%{release}

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel%{_isa} = %{version}-%{release}
Provides:   bundled(sljit)

%description static
Library for static linking for %{name}.

%package syntax
Summary:    Documentation for PCRE2 regular expressions
BuildArch:  noarch
Conflicts:  %{name}-devel < 10.34-8

%description syntax
This is a set of manual pages that document a syntax of the regular
expressions implemented by the PCRE2 library.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test:   BSD
License:    BSD-3-Clause
Requires:   %{name}%{_isa} = %{version}-%{release}
Requires:   %{name}-utf32 = %{version}-%{release}
Requires:   %{name}-utf16 = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}-%{myversion} -p1
# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 sparc64 sparcv9
    --disable-jit \
    --disable-pcre2grep-jit \
%else
    --enable-jit \
    --enable-pcre2grep-jit \
%endif
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
%if %{with pcre2_enables_sealloc}
    --enable-jit-sealloc \
%else
    --disable-jit-sealloc \
%endif
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-callout-fork \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
%if %{with pcre2_enables_readline}
    --enable-pcre2test-libreadline \
%else
    --disable-pcre2test-libreadline \
%endif
    --enable-percent-zt \
    --disable-rebuild-chartables \
    --enable-shared \
    --disable-silent-rules \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
%{make_build}

%install
%{make_install}
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%check
make %{?_smp_mflags} check VERBOSE=yes

%files
%{_libdir}/libpcre2-8.so.0*
%{_libdir}/libpcre2-posix.so.3*

%files utf16
%{_libdir}/libpcre2-16.so.0*

%files utf32
%{_libdir}/libpcre2-32.so.0*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/pcre2_*
%{_mandir}/man3/pcre2api.*
%{_mandir}/man3/pcre2build.*
%{_mandir}/man3/pcre2callout.*
%{_mandir}/man3/pcre2convert.*
%{_mandir}/man3/pcre2demo.*
%{_mandir}/man3/pcre2jit.*
%{_mandir}/man3/pcre2posix.*
%{_mandir}/man3/pcre2sample.*
%{_mandir}/man3/pcre2serialize*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%files static
%{_libdir}/*.a
%license COPYING LICENCE.md

%files syntax
%license COPYING LICENCE.md
%doc AUTHORS.md ChangeLog NEWS
%{_mandir}/man3/pcre2.*
%{_mandir}/man3/pcre2compat.*
%{_mandir}/man3/pcre2limits.*
%{_mandir}/man3/pcre2matching.*
%{_mandir}/man3/pcre2partial.*
%{_mandir}/man3/pcre2pattern.*
%{_mandir}/man3/pcre2perform.*
%{_mandir}/man3/pcre2syntax.*
%{_mandir}/man3/pcre2unicode.*

%files tools
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%changelog
* Fri Nov 07 2025 Lukas Javorsky <ljavorsk@redhat.com> - 10.47-1
- Rebase to version 10.47
- Resolves: rhbz#2405255

* Mon Sep 01 2025 Lukas Javorsky <ljavorsk@redhat.com> - 10.46-1
- Rebase to version 10.46

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.45-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 05 2025 Lukas Javorsky <ljavorsk@redhat.com> - 10.45-1
- Rebase to version 10.45
- Upstream has changed it's owner and with that the GPG signatures

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.44-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.44-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Lukas Javorsky <ljavorsk@redhat.com> - 10.44-1
- Rebase to version 10.44

* Wed May 15 2024 Lukas Javorsky <ljavorsk@redhat.com> - 10.43-2.1
- Explicitly require uft subpackages in tools subpackage

* Fri Apr 12 2024 Adam Williamson <awilliam@redhat.com> - 10.43-2
- Backport PR #403 to fix crashes in multi-thread contexts

* Mon Feb 19 2024 Lukas Javorsky <ljavorsk@redhat.com> - 10.43-1
- Rebase to version 10.43

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.42-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.42-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 10 2023 Lukas Javorsky <ljavorsk@redhat.com> - 10.42-2
- Fix an issue with restoring originally unset entries in recursion
- Resolves: BZ#2248133

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.42-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.42-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Lukas Javorsky <ljavorsk@redhat.com> - 10.42-1
- Rebase to version 10.42
- RISC-V is JIT enabled according to the https://github.com/PCRE2Project/pcre2/issues/14

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.40-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Lukas Javorsky <ljavorsk@redhat.com> - 10.40-1
- Rebase to the 10.40
- Resolves multiple Out-of-bounds read errors

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.39-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 01 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.39-1
- Rebase to the 10.39

* Mon Oct 04 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.38-1
- Rebase to the 10.38
- Patch 1 upstreamed

* Tue Jul 27 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.37-4
- Fix invalid single character repetition in JIT
- Resolves: BZ#1985484

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.37-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.37-3
- Revert of copying the old posix library - After rebuilding all
- dependend packages we don't need to backport the old library

* Wed Jul 14 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.37-2
- Release bump

* Tue Jun 15 2021 Lukas Javorsky <ljavorsk@redhat.com> - 10.37-1
- Rebase to the 10.37
- libpcre2-posix.so.2* SONAME bump to libpcre2-posix.so.3*
- Enable JIT for s390x arch
- Patches upstreamed: Patch 1,2,3,4
- Resolves: rhbz#1970765, BZ#1965025

* Fri Feb 19 2021 Petr Pisar <ppisar@redhat.com> - 10.36-4
- Fix a mismatch if \K was involved in a recursion
- Restore single character repetition optimization in JIT (upstream bug #2698)

* Tue Feb 02 2021 Petr Pisar <ppisar@redhat.com> - 10.36-3
- Fix misparsing long numbers as a backreference and a number without
  a closing bracket as a quantifier (upstream bug #2690)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.36-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Petr Pisar <ppisar@redhat.com> - 10.36-2
- Fix a possible NULL pointer dereference in auto_possessify()
  (upstream bug #2686)

* Tue Dec 15 2020 Petr Pisar <ppisar@redhat.com> - 10.36-1
- 10.36 bump

* Mon Nov 09 2020 Petr Pisar <ppisar@redhat.com> - 10.36-0.1.RC1
- 10.36-RC1 bump

* Tue Oct 27 2020 Petr Pisar <ppisar@redhat.com> - 10.35-8
- Fix a partial matching for a word boundary in JIT mode (upstream bug #2663)

* Mon Sep 21 2020 Petr Pisar <ppisar@redhat.com> - 10.35-7
- Fix matching a character set when JIT is enabled and both Unicode script and
  Unicode class are present (upstream bug #2644)

* Wed Sep 16 2020 Petr Pisar <ppisar@redhat.com> - 10.35-6
- Fix escaping test data and only allow slash delimiter after perltest pragma
  (upstream bug #2641)
- Fix a mismatch when caselessly searching in an invalid UTF-8 text and a start
  optimization is enabled (upstream bug #2642)

* Mon Sep 14 2020 Petr Pisar <ppisar@redhat.com> - 10.35-5
- Fix escaping test data (upstream bug #2641)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.35-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Petr Pisar <ppisar@redhat.com> - 10.35-4
- Fix a buffer overread when parsing an unterminated VERSION condition with
  a single-digit minor number at the end of a regular expression
  (ClusterFuzz #23779)
- Fix an early fail optimization with character ranges and a buffer overread
  in JIT (upstream bug #2621)

* Tue Jun 02 2020 Petr Pisar <ppisar@redhat.com> - 10.35-3
- Fix an infinite loop when a single-byte newline is search in JIT if an
  invalid UTF-8 mode is enabled (upstream bug #2581)

* Wed May 27 2020 Petr Pisar <ppisar@redhat.com> - 10.35-2
- Enable shadow stack built-in functions if -fcf-protection compiler flag is
  used by patching a build script (upstream bug #2578)

* Mon May 11 2020 Petr Pisar <ppisar@redhat.com> - 10.35-1
- 10.35 bump

* Mon Apr 27 2020 Petr Pisar <ppisar@redhat.com> - 10.35-0.2.RC1
- Fix a compiler warning about -1 index

* Thu Apr 16 2020 Petr Pisar <ppisar@redhat.com> - 10.35-0.1.RC1
- 10.35-RC1 bump

* Mon Mar 23 2020 Petr Pisar <ppisar@redhat.com> - 10.34-9
- Fix a JIT compilation of the Unicode scripts in the extended character classes
  (upstream bug #2432)

* Mon Mar 16 2020 Petr Pisar <ppisar@redhat.com> - 10.34-8
- Fix computing an offest for the start of the UTF-16 error when a high
  surrogate is not followed by a valid low surrogate (upstream bug #2527)
- Fix compiling a lookbehind when preceded by a DEFINE group
  (upstream bug #2531)
- Make manual pages about pattern syntax available when the library is
  installed (bug #1808612)

* Thu Feb 20 2020 Petr Pisar <ppisar@redhat.com> - 10.34-7
- Fix a crash in JIT when an invalid UTF-8 character is encountered in
  match_invalid_utf mode (upstream bug #2529)

* Mon Feb 17 2020 Petr Pisar <ppisar@redhat.com> - 10.34-6
- Fix restoring a verb chain list when exiting a JIT-compiled recursive
  function

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.34-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Petr Pisar <ppisar@redhat.com> - 10.34-5
- Fix a memory leak when allocating a JIT stack fails
- Ensure a newline after the final line in a file is output by pcre2grep
  (upstream bug #2513)
- Fix processing (?(DEFINE)...) within look-behind assertions
- Prevent from a stack exhaustion when studying a pattern for nested groups by
  putting a limit of 1000 recursive calls

* Mon Jan 13 2020 Petr Pisar <ppisar@redhat.com> - 10.34-4
- Fix a crash in JITted code when a *THEN verb is used in a lookahead assertion
  (upstream bug #2510)

* Mon Dec 09 2019 Petr Pisar <ppisar@redhat.com> - 10.34-3
- Fix a crash in pcre2_jit_compile when passing a NULL code argument (upstream
  bug #2487)

* Thu Nov 28 2019 Petr Pisar <ppisar@redhat.com> - 10.34-2
- Fix JIT to respect NOTEMPTY options (upstream bug #2473)

* Fri Nov 22 2019 Petr Pisar <ppisar@redhat.com> - 10.34-1
- 10.34 bump

* Mon Nov 18 2019 Petr Pisar <ppisar@redhat.com> - 10.34-0.2.RC2
- Fix optimized caseless matching of non-ASCII characters in assertions
  (upstream bug #2466)

* Thu Nov 07 2019 Petr Pisar <ppisar@redhat.com> - 10.34-0.1.RC2
- 10.34-RC2 bump
- Fix an infinite loop in 64-bit ARM JIT with NEON instructions

* Wed Oct 30 2019 Petr Pisar <ppisar@redhat.com> - 10.34-0.1.RC1
- 10.34-RC1 bump

* Tue Oct 29 2019 Petr Pisar <ppisar@redhat.com> - 10.33-15
- Fix a use after free when freeing JIT memory (upstream bug #2453)
- Fix thread-safeness in regexec() (upstream bug #2447)

* Mon Sep 09 2019 Petr Pisar <ppisar@redhat.com> - 10.33-14
- Fix a crash in JIT match when a subject has a zero length and an invalid
  pointer (upstream bug #2440)

* Tue Aug 27 2019 Petr Pisar <ppisar@redhat.com> - 10.33-13
- Readd a fix for a mismatch with a lookbehind within a lookahead within
  a lookbehind and fix the regression in matching a lookbehind after
  a condition (bug #1743863)

* Mon Aug 26 2019 Petr Pisar <ppisar@redhat.com> - 10.33-12
- Revert a fix for a mismatch with a lookbehind within a lookahead within
  a lookbehind (bug #1743863)

* Mon Aug 12 2019 Petr Pisar <ppisar@redhat.com> - 10.33-11
- Fix reporting rightmost consulted characters

* Mon Aug 05 2019 Petr Pisar <ppisar@redhat.com> - 10.33-10
- Fix an incorrect computation of a group length when a branch exceeds 65535
  (upstream bug #2428)
- Use HTTPS protocol in URL metadata

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.33-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Petr Pisar <ppisar@redhat.com> - 10.33-9
- Fix a recursion in compiling an expression with a lookbehind within a
  lookahead (upstream bug #2412)

* Wed Jul 17 2019 Petr Pisar <ppisar@redhat.com> - 10.33-8
- Fix a mismatch with a lookbehind within a lookahead within a lookbehind
  (upstream bug #2412)

* Thu Jul 11 2019 Petr Pisar <ppisar@redhat.com> - 10.33-7
- Fix an integer overflow when checking a lookbehind length

* Wed Jul 03 2019 Petr Pisar <ppisar@redhat.com> - 10.33-6
- Fix a DFA to recognize a partial match if the end of a subject is encountered
  in a lookahead, an atomic group, or a recursion

* Thu Jun 20 2019 Petr Pisar <ppisar@redhat.com> - 10.33-5
- Do not ignore {1} quantifier when it is applied to a non-possessive group
  with more alternatives

* Mon Jun 17 2019 Petr Pisar <ppisar@redhat.com> - 10.33-4
- Fix a non-JIT match to return (*MARK) names from a successful conditional
  assertion
- Fix pcre2grep --only-matching output when number of capturing groups exceeds
  32 (upstream bug #2407)

* Mon May 13 2019 Petr Pisar <ppisar@redhat.com> - 10.33-3
- Correct a misspelling in a documentation
- Fix a crash when \X is used without UTF mode in a JIT (upstream bug #2399)

* Mon May 06 2019 Petr Pisar <ppisar@redhat.com> - 10.33-2
- Validate number of capturing parentheses

* Tue Apr 16 2019 Petr Pisar <ppisar@redhat.com> - 10.33-1
- 10.33 bump

* Tue Mar 26 2019 Petr Pisar <ppisar@redhat.com> - 10.33-0.4.RC1
- Do not use SSE2 instructions on x86 CPUs without SSE2 support
  (upstream bug #2385)

* Wed Mar 13 2019 Petr Pisar <ppisar@redhat.com> - 10.33-0.3.RC1
- Use upstream fix for a crash in pcre2_substitute() function if mcontext
  argument is NULL (bug #1686434)

* Mon Mar 11 2019 Petr Pisar <ppisar@redhat.com> - 10.33-0.2.RC1
- Fix a crash in pcre2_substitute() function if mcontext argument is NULL
  (bug #1686434)

* Tue Mar 05 2019 Petr Pisar <ppisar@redhat.com> - 10.33-0.1.RC1
- 10.33-RC1 bump

* Fri Feb 22 2019 Petr Pisar <ppisar@redhat.com> - 10.32-8
- Fix pcre2_pattern_info() documentation (upstream bug #2373)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.32-7.1
- Rebuild for readline 8.0

* Thu Jan 31 2019 Petr Pisar <ppisar@redhat.com> - 10.32-7
- Fix version conditions in DFA engine (upstream bug #2367)
- Use an upstream fix for POSIX names as macros (bug #1667614)

* Tue Jan 22 2019 Petr Pisar <ppisar@redhat.com> - 10.32-6
- Link applications to PCRE2-specific symbols when using POSIX API (bug #1667614)

* Thu Jan 03 2019 Petr Pisar <ppisar@redhat.com> - 10.32-5
- Fix anchoring a pattern preceded with (*MARK)
- Fix OpenPOWER 64-bit ELFv2 ABI detection in JIT compiler (upstream bug #2353)
- Fix an undefined behavior in aarch64 JIT compiler (upstream bug #2355)

* Thu Nov 01 2018 Petr Pisar <ppisar@redhat.com> - 10.32-4
- Fix matching a zero-repeated subroutine call at a start of a pattern
  (upstream bug #2332)
- Fix heap limit checking overflow in pcre2_dfa_match() (upstream bug #2334)

* Mon Sep 24 2018 Petr Pisar <ppisar@redhat.com> - 10.32-3
- Fix caseless matching an extended class in JIT mode (upstream bug #2321)

* Tue Sep 18 2018 Petr Pisar <ppisar@redhat.com> - 10.32-2
- Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
  a greater than 1 fixed quantifier (upstream bug #2320)

* Wed Sep 12 2018 Petr Pisar <ppisar@redhat.com> - 10.32-1
- 10.32 bump

* Mon Sep 03 2018 Petr Pisar <ppisar@redhat.com> - 10.32-0.3.RC1
- Accept \N{U+hhhh} only in UTF mode (upstream bug #2305)
- Fix anchoring in conditionals with only one branch (upstream bug #2307)

* Mon Aug 20 2018 Petr Pisar <ppisar@redhat.com> - 10.32-0.2.RC1
- Fix autopossessifying a repeated negative class with no characters less than
  256 that is followed by a positive class with only characters less than 256,
  (upstream bug #2300)

* Thu Aug 16 2018 Petr Pisar <ppisar@redhat.com> - 10.32-0.1.RC1
- 10.32-RC1 bump

* Thu Aug 16 2018 Petr Pisar <ppisar@redhat.com> - 10.31-9
- Recognize all Unicode space characters with /x option in a pattern
- Fix changing dynamic options

* Tue Jul 31 2018 Petr Pisar <ppisar@redhat.com> - 10.31-8
- Fix backtracking atomic groups when they are not separated by something with
  a backtracking point

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.31-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 10.31-7
- Fix checking that a lookbehind assertion has a fixed length if the
  lookbehind assertion is used inside a lookahead assertion
- Fix parsing VERSION conditions

* Mon Jul 02 2018 Petr Pisar <ppisar@redhat.com> - 10.31-6
- Fix global search/replace in pcre2test and pcre2_substitute() when the pattern
  matches an empty string, but never at the starting offset

* Mon Jun 25 2018 Petr Pisar <ppisar@redhat.com> - 10.31-5
- Fix bug when \K is used in a lookbehind in a substitute pattern

* Fri Mar 16 2018 Petr Pisar <ppisar@redhat.com> - 10.31-4
- Fix setting error offset zero for early errors in pcre2_pattern_convert()

* Mon Feb 26 2018 Petr Pisar <ppisar@redhat.com> - 10.31-3
- Add support to pcre2grep for binary zeros in -f files (upstream bug #2222)
- Fix compiler warnings in pcre2grep

* Tue Feb 20 2018 Petr Pisar <ppisar@redhat.com> - 10.31-2
- Fix returning unset groups in POSIX interface if REG_STARTEND has a non-zero
  starting offset (upstream bug #2244)
- Fix pcre2test -C to correctly show what \R matches
- Fix matching repeated character classes against an 8-bit string containting
  multi-code-unit characters

* Mon Feb 12 2018 Petr Pisar <ppisar@redhat.com> - 10.31-1
- 10.31 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.31-0.3.RC1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.31-0.3.RC1.1
- Switch to %%ldconfig_scriptlets

* Thu Feb 01 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.3.RC1
- Fix auto-possessification at the end of a capturing group that is called
  recursively (upstream bug #2232)

* Tue Jan 30 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.2.RC1
- Enlarge ovector array match data structure to be large enough in all cases
  (oss-fuzz #5415)

* Mon Jan 15 2018 Petr Pisar <ppisar@redhat.com> - 10.31-0.1.RC1
- 10.31-RC1 bump

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 10.30-5
- Fix handling \K in an assertion in pcre2grep tool and documentation
  (upstream bug #2211)
- Fix matching at a first code unit of a new line sequence if PCRE2_FIRSTLINE
  is enabled

* Fri Dec 22 2017 Petr Pisar <ppisar@redhat.com> - 10.30-4
- Fix pcre2_jit_match() to properly check the pattern was JIT-compiled
- Allow pcre2grep match counter to handle values larger than 2147483647,
  (upstream bug #2208)
- Fix incorrect first matching character when a backreference with zero minimum
  repeat starts a pattern (upstream bug #2209)

* Mon Nov 13 2017 Petr Pisar <ppisar@redhat.com> - 10.30-3
- Fix multi-line matching in pcre2grep tool (upstream bug #2187)

* Thu Nov 02 2017 Petr Pisar <ppisar@redhat.com> - 10.30-2
- Accept files names longer than 128 bytes in recursive mode of pcre2grep
  (upstream bug #2177)

* Tue Aug 15 2017 Petr Pisar <ppisar@redhat.com> - 10.30-1
- 10.30 bump

* Wed Aug 02 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.6.RC1
- Disable SELinux-friendly JIT allocator because it crashes after a fork
  (upstream bug #1749)

* Mon Jul 31 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.5.RC1
- Fix handling a hyphen at the end of a character class (upstream bug #2153)

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 10.30-0.4.RC1
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.3.RC1
- Fix applying local x modifier while global xx was in effect

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.30-0.2.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.2.RC1
- Fix a compiler warning in JIT code for ppc32

* Thu Jul 20 2017 Petr Pisar <ppisar@redhat.com> - 10.30-0.1.RC1
- 10.30-RC1 bump
- Heap-based matching implementation replaced stack-based one
- SELinux-friendly JIT enabled

* Fri Jun 16 2017 Petr Pisar <ppisar@redhat.com> - 10.23-8
- Fix DFA matching a lookbehind assertion that has a zero-length branch
  (PCRE2 oss-fuzz issue 1859)
- Fix returned offsets from regexec() when REG_STARTEND is used with starting offset
  greater than zero (upstream bug #2128)

* Tue May 09 2017 Petr Pisar <ppisar@redhat.com> - 10.23-7
- Fix a pcre2test crash on multiple push statements (upstream bug #2109)

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 10.23-6
- Fix CVE-2017-7186 in JIT mode (a crash when finding a Unicode property for
  a character with a code point greater than 0x10ffff in UTF-32 library while
  UTF mode is disabled) (bug #1434504)
- Fix an incorrect cast in UTF validation (upstream bug #2090)

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 10.23-5
- Fix DFA match for a possessively repeated character class (upstream bug #2086)
- Use a memory allocator from the pattern if no context is supplied to
  pcre2_match()

* Wed Mar 22 2017 Petr Pisar <ppisar@redhat.com> - 10.23-4
- Close serialization file in pcre2test after any error (upstream bug #2074)
- Fix a memory leak in pcre2_serialize_decode() when the input is invalid
  (upstream bug #2075)
- Fix a potential NULL dereference in pcre2_callout_enumerate() if called with
  a NULL pattern pointer when Unicode support is available (upstream bug #2076)
- Fix CVE-2017-8786 (32-bit error buffer size bug in pcre2test) (bug #1500717)

* Mon Mar 20 2017 Petr Pisar <ppisar@redhat.com> - 10.23-3
- Fix an internal error for a forward reference in a lookbehind with
  PCRE2_ANCHORED (oss-fuzz bug #865)
- Fix a pcre2test bug for global match with zero terminated subject
  (upstream bug #2063)

* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 10.23-2
- Handle memmory allocation failures in pcre2test tool
- Fix CVE-2017-7186 (a crash when finding a Unicode property for a character
  with a code point greater than 0x10ffff in UTF-32 library while UTF mode is
  disabled) (upstream bug #2052)

* Tue Feb 14 2017 Petr Pisar <ppisar@redhat.com> - 10.23-1
- 10.23 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.23-0.1.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Petr Pisar <ppisar@redhat.com> - 10.23-0.1.RC1
- 10.23-RC1 bump

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 10.22-10.1
- Rebuild for readline 7.x

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 10.22-10
- Fix an out-of-bound read in pcre2test tool within POSIX mode
  (upstream bug #2008)

* Tue Jan 03 2017 Petr Pisar <ppisar@redhat.com> - 10.22-9
- Fix compiling a class with UCP and without UTF

* Fri Dec 16 2016 Petr Pisar <ppisar@redhat.com> - 10.22-8
- Fix a crash when doing an extended substitution for \p, \P, or \X
  (upstream bug #1977)
- Fix a crash in substitution if starting offest was specified beyond the
  subject end (upstream bug #1992)

* Fri Dec 09 2016 Petr Pisar <ppisar@redhat.com> - 10.22-7
- Fix pcre2-config --libs-posix output (upstream bug #1924)
- Fix a memory leak and a typo in a documentation (upstream bug #1973)
- Fix a buffer overflow in partial match test for CRLF in an empty buffer
  (upstream bug #1975)
- Fix a crash in pcre2test when displaying a wide character with a set locate
  (upstream bug #1976)

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 10.22-6
- Fix faulty auto-anchoring patterns when .* is inside an assertion

* Mon Oct 24 2016 Petr Pisar <ppisar@redhat.com> - 10.22-5
- Document assert capture limitation (upstream bug #1887)
- Ignore offset modifier in pcre2test in POSIX mode (upstream bug #1898)

* Wed Oct 19 2016 Richard W.M. Jones <@redhat.com> - 10.22-4
- Disable the JIT on riscv64.

* Wed Oct 19 2016 Petr Pisar <ppisar@redhat.com> - 10.22-3
- Fix displaying a callout position in pcretest output with an escape sequence
  greater than \x{ff}
- Fix pcrepattern(3) documentation
- Fix miscopmilation of conditionals when a group name start with "R"
  (upstream bug #1873)
- Fix internal option documentation in pcre2pattern(3) (upstream bug #1875)
- Fix optimization bugs for patterns starting with lookaheads
  (upstream bug #1882)

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-2
- Fix matching characters above 255 when a negative character type was used
  without enabled UCP in a positive class (upstream bug #1866)

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-1
- 10.22 bump

* Thu Jun 30 2016 Petr Pisar <ppisar@redhat.com> - 10.22-0.1.RC1
- 10.22-RC1 bump
- libpcre2-posix library changed ABI
- Fix register overwite in JIT when SSE2 acceleration is enabled
- Correct pcre2unicode(3) documentation

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 10.21-6
- Fix repeated pcregrep output if -o with -M options were used and the match
  extended over a line boundary (upstream bug #1848)

* Fri Jun 03 2016 Petr Pisar <ppisar@redhat.com> - 10.21-5
- Fix a race in JIT locking condition
- Fix an ovector check in JIT test program
- Enable JIT in the pcre2grep tool

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 10.21-4
- Ship README in devel as it covers API and build, not general info
- Move UTF-16 and UTF-32 libraries into pcre-ut16 and pcre-32 subpackages

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 10.21-3
- Fix a typo in pcre2_study()

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> - 10.21-2
- Report unmatched closing parantheses properly
- Fix pcre2test for expressions with a callout inside a look-behind assertion
  (upstream bug #1783)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (upstream bug #1791)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.21-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 10.21-1
- 10.21 bump

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.2.RC1
- Adapt a test to French locale on RHEL

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.1.RC1
- 10.21-RC1 bump

* Mon Oct 26 2015 Petr Pisar <ppisar@redhat.com> - 10.20-3
- Fix compiling patterns with PCRE2_NO_AUTO_CAPTURE (upstream bug #1704)

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 10.20-2
- Fix compiling classes with a negative escape and a property escape
  (upstream bug #1697)
- Fix integer overflow for patterns whose minimum matching length is large
  (upstream bug #1699)

* Fri Jul 03 2015 Petr Pisar <ppisar@redhat.com> - 10.20-1
- 10.20 bump

* Fri Jun 19 2015 Petr Pisar <ppisar@redhat.com> - 10.20-0.1.RC1
- 10.20-RC1 bump
- Replace dependency on glibc-headers with gcc (bug #1230479)
- Preserve soname

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.10-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-3
- fixed Release field

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-2.1
- Backport fix for AArch64

* Tue May 05 2015 Petr Pisar <ppisar@redhat.com> - 10.10-2
- Package pcre2demo.c as a documentation for pcre2-devel

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 10.10-1
- PCRE2 library packaged

