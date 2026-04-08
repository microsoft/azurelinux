# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Is this a stable/testing release:
#%%global rcversion RC1
Name:       pcre
Version:    8.45
Release:    %{?rcversion:0.}1%{?rcversion:.%rcversion}%{?dist}.9
%global myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
## Source package only:
# INSTALL:                  FSFAP
# install-sh:               MIT and Public Domain
# ltmain.sh:                (GPLv2+ or BSD) and (GPLv3+ or MIT)
# missing:                  GPLv2+ or BSD
# compile:                  GPLv2+ or BSD
# config.sub:               GPLv3+ or BSD
# m4/ax_pthread.m4:         GPLv3+ with exception
# m4/libtool.m4:            GPLv2+ or BSD
# m4/ltversion.m4:          FSFULLR
# m4/pcre_visibility.m4:    FSFULLR
# m4/lt~obsolete.m4:        FSFULLR
# m4/ltsugar.m4:            FSFULLR
# m4/ltoptions.m4:          FSFULLR
# aclocal.m4:               (GPLv2+ or BSD) and FSFULLR 
# Makefile.in:              FSFULLR
# configure:                FSFUL
# test-driver:              GPLv2+ with exception
# testdata:                 Public Domain (see LICENSE file)
## Binary packages:
# other files:              BSD
License:    BSD-3-Clause
URL:        https://www.pcre.org/
Source0:    https://ftp.pcre.org/pub/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
Source1:    https://ftp.pcre.org/pub/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2.sig
Source2:    https://ftp.pcre.org/pub/pcre/Public-Key
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1:     pcre-8.32-refused_spelling_terminated.patch
# Fix recursion stack estimator, upstream bug #2173, refused by upstream
Patch2:     pcre-8.41-fix_stack_estimator.patch
# Link applications to PCRE-specific symbols when using POSIX API, bug #1667614,
# upstream bug 1830, partially borrowed from PCRE2, proposed to upstream,
# This amends ABI, application built with this patch cannot run with
# previous libpcreposix builds.
Patch3:     pcre-8.42-Declare-POSIX-regex-function-names-as-macros-to-PCRE.patch
# Fix reading an uninitialized memory when populating a name table,
# upstream bug #2661, proposed to the upstream
Patch4:     pcre-8.44-Inicialize-name-table-memory-region.patch
# Implement CET, bug #1909554, proposed to the upstream
# <https://lists.exim.org/lurker/message/20201220.222016.d8cd6d61.en.html>
Patch5:     pcre-8.44-JIT-compiler-update-for-Intel-CET.patch
Patch6:     pcre-8.44-Pass-mshstk-to-the-compiler-when-Intel-CET-is-enable.patch

# IMPORTANT
# This package has been deprecated since Fedora 38
# The reason behind this is that upstream stopped supporting this package
# and recommended to port to the new pcre2 version
# FESCo approval is located here: https://pagure.io/fesco/issue/2862
# Change proposal is located here: https://fedoraproject.org/wiki/PcreDeprecation
Provides:  deprecated()

BuildRequires:  readline-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
# glibc-common for iconv
BuildRequires:  glibc-common
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
# perl not used because config.h.generic is pregenerated
# Tests:
BuildRequires:  bash
BuildRequires:  diffutils
BuildRequires:  grep

%description
PCRE, Perl-compatible regular expression, library has its own native API, but
a set of wrapper functions that are based on the POSIX API are also supplied
in the libpcreposix library. Note that this just provides a POSIX calling
interface to PCRE: the regular expressions themselves still follow Perl syntax
and semantics. This package provides support for strings in 8-bit and UTF-8
encodings. Detailed change log is provided by %{name}-doc package.

%package utf16
Summary:    UTF-16 variant of PCRE
Conflicts:  %{name}%{?_isa} < 8.38-12

# For details, see above
Provides:  deprecated()

%description utf16
This is Perl-compatible regular expression library working on UTF-16 strings.
Detailed change log is provided by %{name}-doc package.

%package utf32
Summary:    UTF-32 variant of PCRE
Conflicts:  %{name}%{?_isa} < 8.38-12

# For details, see above
Provides:  deprecated()

%description utf32
This is Perl-compatible regular expression library working on UTF-32 strings.
Detailed change log is provided by %{name}-doc package.

%package cpp
Summary:    C++ bindings for PCRE
Requires:   %{name}%{?_isa} = %{version}-%{release}

# For details, see above
Provides:  deprecated()

%description cpp
This is C++ bindings for the Perl-compatible regular expression library.
Detailed change log is provided by %{name}-doc package.

%package doc
Summary:    Change log for %{name}
BuildArch:  noarch

# For details, see above
Provides:  deprecated()

%description doc
These are large documentation files about PCRE.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-cpp%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf16%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf32%{?_isa} = %{version}-%{release}

# For details, see above
Provides:  deprecated()

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel%{_isa} = %{version}-%{release}

# For details, see above
Provides:  deprecated()

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
Requires:   %{name}%{_isa} = %{version}-%{release}

# For details, see above
Provides:  deprecated()

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -n %{name}-%{myversion}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p2
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
# Because of the multilib patch
libtoolize --copy --force
autoreconf -vif
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit \
%else
    --enable-jit \
%endif
    --enable-pcretest-libreadline \
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcre8 \
    --enable-pcre16 \
    --enable-pcre32 \
    --disable-silent-rules
%{make_build}

%install
%{make_install}
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%check
%ifarch s390 s390x ppc
# larger stack is needed on s390, ppc
ulimit -s 10240
%endif
make %{?_smp_mflags} check VERBOSE=yes

%files
%{_libdir}/libpcre.so.1
%{_libdir}/libpcre.so.1.*
%{_libdir}/libpcreposix.so.0
%{_libdir}/libpcreposix.so.0.*
%license COPYING LICENCE
%doc AUTHORS NEWS

%files utf16
%{_libdir}/libpcre16.so.0
%{_libdir}/libpcre16.so.0.*
%license COPYING LICENCE
%doc AUTHORS NEWS

%files utf32
%{_libdir}/libpcre32.so.0
%{_libdir}/libpcre32.so.0.*
%license COPYING LICENCE
%doc AUTHORS NEWS

%files cpp
%{_libdir}/libpcrecpp.so.0
%{_libdir}/libpcrecpp.so.0.*

%files doc
%doc ChangeLog

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre-config.*
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc README HACKING pcredemo.c

%files static
%{_libdir}/*.a
%license COPYING LICENCE

%files tools
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.*
%{_mandir}/man1/pcretest.*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.45-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 28 2021 Wolfgang Stöggl <c72578@yahoo.de> - 8.45-1
- Rebase to 8.45

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.44-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.44-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Petr Pisar <ppisar@redhat.com> - 8.44-3
- Implement CET (bug #1909554)

* Mon Oct 19 2020 Petr Pisar <ppisar@redhat.com> - 8.44-2
- Fix reading an uninitialized memory when populating a name table
  (upstream bug #2661)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.44-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 14 2020 Petr Pisar <ppisar@redhat.com> - 8.44-1
- 8.44 bump

* Wed Feb 12 2020 Petr Pisar <ppisar@redhat.com> - 8.43-3
- Make erroroffset initializion in a POSIX wrapper thread-safe
  (upstream bug #2447)
- Fix an integer overflow when parsing numbers after "(?C" (upstream bug #2463)
- Fix shifting integer bits and a NULL pointer dereferce in pcretest tool
  (upstream bug #2380)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.43-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.43-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Petr Pisar <ppisar@redhat.com> - 8.43-2
- Add (*LF) to a list of start-of-pattern options in the C++ wrapper
  (upstream bug #2400)

* Mon Feb 25 2019 Petr Pisar <ppisar@redhat.com> - 8.43-1
- 8.43 bump

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.43-0.1.RC1.2
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.43-0.1.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Petr Pisar <ppisar@redhat.com> - 8.43-0.1.RC1
- 8.43-RC1 bump

* Wed Jan 23 2019 Petr Pisar <ppisar@redhat.com> - 8.42-7
- Link applications to PCRE-specific symbols when using POSIX API (bug #1667614)

* Thu Jan 03 2019 Petr Pisar <ppisar@redhat.com> - 8.42-6
- Fix OpenPOWER 64-bit ELFv2 ABI detection in JIT compiler (upstream bug #2353)
- Fix an undefined behavior in aarch64 JIT compiler (upstream bug #2355)

* Thu Nov 01 2018 Petr Pisar <ppisar@redhat.com> - 8.42-5
- Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
  a greater than 1 fixed quantifier
- Fix matching a zero-repeated subroutine call at a start of a pattern
  (upstream bug #2332)

* Mon Sep 03 2018 Petr Pisar <ppisar@redhat.com> - 8.42-4
- Fix anchoring in conditionals with only one branch (upstream bug #2307)

* Mon Aug 20 2018 Petr Pisar <ppisar@redhat.com> - 8.42-3
- Fix autopossessifying a repeated negative class with no characters less than
  256 that is followed by a positive class with only characters less than 256
  (upstream bug #2300)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.42-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Petr Pisar <ppisar@redhat.com> - 8.42-2
- Fix handling UTF and start-of-pattern options in C++ wrapper
  (upstream bug #2283)
- Fix an error message and locale handling in pcregrep tool

* Tue Mar 20 2018 Petr Pisar <ppisar@redhat.com> - 8.42-1
- 8.42 bump

* Mon Feb 26 2018 Petr Pisar <ppisar@redhat.com> - 8.42-0.2.RC1
- Fix compiler warnings in pcregrep

* Fri Feb 23 2018 Petr Pisar <ppisar@redhat.com> - 8.42-0.1.RC1
- 8.42-RC1 bump

* Tue Feb 20 2018 Petr Pisar <ppisar@redhat.com> - 8.41-6
- Fix returning unset groups in POSIX interface if REG_STARTEND has a non-zero
  starting offset (upstream bug #2244)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.41-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.41-5.1
- Switch to %%ldconfig_scriptlets

* Tue Jan 30 2018 Petr Pisar <ppisar@redhat.com> - 8.41-5
- Fix out-of-bounds read for partial matching of /./ against an empty string
  when the newline type is CRLF (upstream bug #2226)

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 8.41-4
- Allow pcregrep match counter to handle values larger than 2147483647
  (upstream bug #2208)
- Fix incorrect first matching character when a backreference with zero minimum
  repeat starts a pattern (upstream bug #2209)

* Thu Nov 02 2017 Petr Pisar <ppisar@redhat.com> - 8.41-3
- Accept files names longer than 128 bytes in recursive mode of pcregrep
  (upstream bug #2177)

* Mon Oct 09 2017 Petr Pisar <ppisar@redhat.com> - 8.41-2
- Fix recursion stack estimator (upstream bug #2173)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.41-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.41-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Petr Pisar <ppisar@redhat.com> - 8.41-1
- 8.41 bump

* Wed Jun 14 2017 Petr Pisar <ppisar@redhat.com> - 8.41-0.1.RC1
- 8.41 RC1 bump

* Fri Apr 21 2017 Petr Pisar <ppisar@redhat.com> - 8.40-7
- Fix a buffer overflow in pcretest tool when copying a string in UTF-32 mode
- Fix CVE-2017-7186 in JIT mode (a crash when finding a Unicode property for
  a character with a code point greater than 0x10ffff in UTF-32 library while
  UTF mode is disabled) (bug #1434504)

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 8.40-6
- Fix DFA match for a possessively repeated character class (upstream bug #2086)

* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 8.40-5
- Fix a crash in pcretest when \O directive was supplied with too big number
  (upstream bug #2044)
- Document pcretest input cannot contain binary zeroes (upstream bug #2045)
- Fix CVE-2017-7244 (a crash when finding a Unicode property for a character
  with a code point greater than 0x10ffff in UTF-32 library while UTF mode is
  disabled) (upstream bug #2052)

* Thu Feb 23 2017 Petr Pisar <ppisar@redhat.com> - 8.40-4
- Fix a crash in pcretest when printing non-ASCII characters
  (upstream bug #2043)

* Tue Feb 21 2017 Petr Pisar <ppisar@redhat.com> - 8.40-3
- Fix parsing comments between quantifiers (upstream bug #2019)

* Tue Feb 14 2017 Petr Pisar <ppisar@redhat.com> - 8.40-2
- Fix pcregrep multi-line matching --only-matching option (upstream bug #1848)
- Fix CVE-2017-6004 (a crash in JIT compilation) (upstream bug #2035)
- Fix a potenial buffer overflow in formatting a pcregrep error message
  (upstream bug #2037)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.40-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 8.40-1.1
- Rebuild for readline 7.x

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 8.40-1
- 8.40 bump

* Mon Dec 12 2016 Petr Pisar <ppisar@redhat.com> - 8.40-0.1.RC1
- 8.40-RC1 bump

* Mon Oct 24 2016 Petr Pisar <ppisar@redhat.com> - 8.39-6
- Document assert capture limitation (upstream bug #1887)

* Wed Oct 19 2016 Petr Pisar <ppisar@redhat.com> - 8.39-5
- Fix internal option documentation in pcrepattern(3) (upstream bug #1875)
- Fix optimization bugs for patterns starting with lookaheads
  (upstream bug #1882)

* Fri Oct 14 2016 Petr Pisar <ppisar@redhat.com> - 8.39-4
- Fix displaying position in pcretest callout with an escape sequence greater
  than \x{ff}
- Fix pcrepattern(3) documentation
- Fix miscopmilation of conditionals when a group name start with "R"
  (upstream bug #1873)

* Tue Aug 30 2016 Petr Pisar <ppisar@redhat.com> - 8.39-3
- Fix register overwite in JIT when SSE2 acceleration is enabled
- Fix matching characters above 255 when a negative character type was used
  without enabled UCP in a positive class (upstream bug #1866)

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 8.39-2
- Fix repeated pcregrep output if -o with -M options were used and the match
  extended over a line boundary (upstream bug #1848)

* Tue Jun 14 2016 Petr Pisar <ppisar@redhat.com> - 8.39-1
- 8.39 bump

* Tue May 24 2016 Petr Pisar <ppisar@redhat.com> - 8.39-0.1.RC1
- 8.39-RC1 bump

* Thu Apr 07 2016 Petr Pisar <ppisar@redhat.com> - 8.38-14
- Separate pcre-cpp subpackage for C++ bindings, thanks to Yaakov Selkowitz
  (bug #1324580)
- Correct pcre-devel dependencies
- Remove rich dependency from pcre-doc

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 8.38-13
- Remove useless dependencies between UTF variants

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 8.38-12
- Move UTF-16 and UTF-32 libraries into pcre-ut16 and pcre-32 subpackages

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 8.38-11
- Ship ChangeLog in pcre-doc package

* Sat Mar  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 8.38-10
- Don't ship ChangeLog, details covered in NEWS
- Ship README in devel as it covers API and build, not general info

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 8.38-9
- Fix a non-diagnosis of missing assection after (?(?C) that could corrupt
  process stack (upstream bug #1780)
- Fix a typo in pcre_study()

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 8.38-8
- Fix CVE-2016-1283 (a heap buffer overflow in handling of nested duplicate
  named groups with a nested back reference) (bug #1295386)
- Fix a heap buffer overflow in pcretest causing infinite loop when matching
  globally with an ovector less than 2 (bug #1312786)

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> - 8.38-7
- Fix pcretest for expressions with a callout inside a look-behind assertion
  (upstream bug #1783)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (upstream bug #1791)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.38-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 08 2015 Petr Pisar <ppisar@redhat.com> - 8.38-6
- Fix a crash in pcre_get_substring_list() if the use of \K caused the start
  of the match to be earlier than the end (upstream bug #1744)

* Mon Dec 07 2015 Petr Pisar <ppisar@redhat.com> - 8.38-5
- Fix possible crash in pcre_copy_named_substring() if a named substring has
  number greater than the space in the ovector (upstream bug #1741)
- Fix a buffer overflow when compiling an expression with named groups with
  a group that reset capture numbers (upstream bug #1742)

* Fri Dec 04 2015 Petr Pisar <ppisar@redhat.com> - 8.38-4
- Fix compiling expressions with global extended modifier that is disabled by
  local no-extended option at the start of the expression just after
  a whitespace

* Tue Dec 01 2015 Petr Pisar <ppisar@redhat.com> - 8.38-3
- Fix compiling expressions with negated classes in UCP mode
  (upstream bug #1732)
- Fix compiling expressions with an isolated \E between an item and its
  qualifier with auto-callouts (upstream bug #1724)
- Fix crash in regexec() if REG_STARTEND option is set and pmatch argument is
  NULL (upstream bug #1727)
- Fix a stack overflow when formatting a 32-bit integer in pcregrep tool
  (upstream bug #1728)
- Fix compiling expressions with an empty \Q\E sequence between an item and
  its qualifier with auto-callouts (upstream bug #1735)

* Fri Nov 27 2015 Petr Pisar <ppisar@redhat.com> - 8.38-2
- Fix compiling comments with auto-callouts

* Tue Nov 24 2015 Petr Pisar <ppisar@redhat.com> - 8.38-1
- 8.38 bump

* Wed Nov 18 2015 Petr Pisar <ppisar@redhat.com> - 8.38-0.2.RC1
- Fix crash when compiling an expression with long (*MARK) or (*THEN) names
- Fix compiling a POSIX character class followed by a single ASCII character
  in a class item while UCP mode is active (upstream bug #1717)
- Fix mismatching characters in the range 128-255 against [:punct:] in UCP
  mode (upstream bug #1718)

* Thu Oct 29 2015 Petr Pisar <ppisar@redhat.com> - 8.38-0.1.RC1
- 8.38-RC1 bump

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 8.37-5
- Fix compiling classes with a negative escape and a property escape
  (upstream bug #1697)

* Tue Aug 25 2015 Petr Pisar <ppisar@redhat.com> - 8.37-4
- Fix CVE-2015-8381 (a heap overflow when compiling certain expression with
  named references) (bug #1256452)

* Thu Aug 06 2015 Petr Pisar <ppisar@redhat.com> - 8.37-3
- Fix a buffer overflow with duplicated named groups with a reference between
  their definition, with a group that reset capture numbers
- Fix a buffer overflow with a forward reference by name to a group whose
  number is the same as the current group
- Fix CVE-2015-8385 (a buffer overflow with duplicated named groups and an
  occurrence of "(?|") (bug #1250946)

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> - 8.37-2
- Fix CVE-2015-3210 (heap overflow when compiling an expression with named
  recursive back reference and the name is duplicated) (bug #1236659)
- Fix CVE-2015-5073 (heap overflow when compiling an expression with an
  forward reference within backward asserion with excessive closing
  paranthesis) (bug #1237224)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.37-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Petr Pisar <ppisar@redhat.com> - 8.37-1
- 8.37 bump

* Thu Apr 23 2015 Petr Pisar <ppisar@redhat.com> - 8.37-0.2.RC1
- Fix static linking (bug #1214494)
- Package pcredemo.c as a documentation for pcre-devel
- Fix JIT on AArch64

* Wed Apr 22 2015 Petr Pisar <ppisar@redhat.com> - 8.37-0.1.RC1
- 8.37 RC1 bump

* Thu Apr 09 2015 Petr Pisar <ppisar@redhat.com> - 8.36-5
- Fix computing size for pattern with a negated special calss in on-UCP mode
  (bug #1210383)
- Fix compilation of a pattern with mutual recursion nested inside other group
  (bug #1210393)
- Fix compilation of a parenthesized comment (bug #1210410)
- Fix compliation of mutual recursion inside a lookbehind assertion
  (bug #1210417)
- Fix pcregrep loop when \K is used in a lookbehind assertion (bug #1210423)
- Fix pcretest loop when \K is used in a lookbehind assertion (bug #1210423)
- Fix backtracking for \C\X* in UTF-8 mode (bug #1210576)

* Thu Mar 26 2015 Petr Pisar <ppisar@redhat.com> - 8.36-4
- Fix computing size of JIT read-only data (bug #1206131)

* Thu Feb 19 2015 David Tardon <dtardon@redhat.com> - 8.36-3.1
- rebuild for C++ stdlib API changes in gcc5

* Thu Nov 20 2014 Petr Pisar <ppisar@redhat.com> - 8.36-3
- Fix CVE-2014-8964 (unused memory usage on zero-repeat assertion condition)
  (bug #1165626)

* Fri Nov 07 2014 Petr Pisar <ppisar@redhat.com> - 8.36-2
- Reset non-matched groups within capturing group up to forced match
  (bug #1161587)

* Tue Oct 07 2014 Petr Pisar <ppisar@redhat.com> - 8.36-1
- 8.36 bump

* Tue Sep 16 2014 Petr Pisar <ppisar@redhat.com> - 8.36-0.1.RC1
- 8.36 RC1 bump
- Enable JIT on aarch64

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Petr Pisar <ppisar@redhat.com> - 8.35-6
- Fix compile-time loop for recursive reference within a group with an
  indefinite repeat (bug #1128577)

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> - 8.35-5
- fix license handling

* Mon Jul 14 2014 Petr Pisar <ppisar@redhat.com> - 8.35-4
- Fix empty-matching possessive zero-repeat groups in interpreted mode
  (bug #1119241)
- Fix memory leaks in pcregrep (bug #1119257)
- Fix compiler crash for zero-repeated groups with a recursive back reference
  (bug #1119272)

* Thu Jun 19 2014 Petr Pisar <ppisar@redhat.com> - 8.35-3
- Fix bad starting data when char with more than one other case follows
  circumflex in multiline UTF mode (bug #1110620)
- Fix not including VT in starting characters for \s if pcre_study() is used
  (bug #1111045)
- Fix character class with a literal quotation (bug #1111054)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Petr Pisar <ppisar@redhat.com> - 8.35-2
- Do no rely on wrapping signed integer while parsing {min,max} expression
  (bug #1086630)

* Wed Apr 09 2014 Petr Pisar <ppisar@redhat.com> - 8.35-1
- 8.35 bump
- Run tests in parallel

* Fri Mar 14 2014 Petr Pisar <ppisar@redhat.com> - 8.35-0.1.RC1
- 8.35-RC1 bump

* Tue Mar 11 2014 Petr Pisar <ppisar@redhat.com> - 8.34-4
- Fix max/min quantifiers in ungreedy mode (bug #1074500)

* Tue Jan 21 2014 Dan Horák <dan[at]danny.cz> - 8.34-3
- enlarge stack for tests on s390x

* Thu Jan 09 2014 Petr Pisar <ppisar@redhat.com> - 8.34-2
- Fix jitted range check (bug #1048097)

* Mon Dec 16 2013 Petr Pisar <ppisar@redhat.com> - 8.34-1
- 8.34 bump

* Wed Oct 16 2013 Petr Pisar <ppisar@redhat.com> - 8.33-3
- Disable strict-aliasing on PPC64 (bug #881232)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.33-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Petr Pisar <ppisar@redhat.com> - 8.33-2
- Disable unsupported JIT on aarch64 (bug #969693)

* Thu May 30 2013 Petr Pisar <ppisar@redhat.com> - 8.33-1
- 8.33 bump

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.3.RC1
- Fix passing too small output vector to pcre_dfa_exec (bug #963284)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.2.RC1
- Fix bad handling of empty lines in pcregrep tool (bug #961789)
- Fix possible pcretest crash with a data line longer than 65536 bytes

* Thu May 02 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.1.RC1
- 8.33-RC1 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 8.32-4
- Fix forward search in JIT when link size is 3 or greater
- Fix buffer over-read in UTF-16 and UTF-32 modes with JIT

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 8.32-3
- Adjust autoreconf to fix FTBFS on F-19

* Mon Jan 07 2013 Petr Pisar <ppisar@redhat.com> - 8.32-2
- Make inter-subpackage dependencies architecture specific (bug #892187)

* Fri Nov 30 2012 Petr Pisar <ppisar@redhat.com> - 8.32-1
- 8.32 bump

* Thu Nov 29 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.2.RC1
- Inter-depend sub-packages to prevent from mixing different versions

* Tue Nov 13 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.1.RC1
- 8.32-RC1 bump

* Mon Sep 03 2012 Petr Pisar <ppisar@redhat.com> - 8.31-2
- Set re_nsub in regcomp() properly (bug #853990)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.31-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Petr Pisar <ppisar@redhat.com> - 8.31-1
- 8.31 bump

* Tue Jun 05 2012 Petr Pisar <ppisar@redhat.com> - 8.31-0.1.RC1
- 8.31-RC1 bump

* Sat May 12 2012 Tom Callaway <spot@fedoraproject.org> - 8.30-7
- disable jit for sparcv9 and sparc64

* Fri May 11 2012 Petr Pisar <ppisar@redhat.com> - 8.30-6
- Fix spelling in manual pages (bug #820978)

* Mon Apr 23 2012 Petr Pisar <ppisar@redhat.com> - 8.30-5
- Possessify high ASCII (bug #815217)
- Fix ovector overflow (bug #815214)

* Fri Apr 20 2012 Petr Pisar <ppisar@redhat.com> - 8.30-4
- Possesify \s*\R (bug #813237)

* Thu Apr 05 2012 Petr Pisar <ppisar@redhat.com> - 8.30-3
- Fix look-behind assertion in UTF-8 JIT mode (bug #810314)

* Tue Feb 28 2012 Petr Pisar <ppisar@redhat.com> - 8.30-2
- Remove old libpcre.so.0 from distribution
- Move library to /usr

* Thu Feb 09 2012 Petr Pisar <ppisar@redhat.com> - 8.30-1
- 8.30 bump
- Add old libpcre.so.0 to preserve compatibility temporarily

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 8.30-0.1.RC1
- 8.30 Relase candidate 1 with UTF-16 support and *API change*
- Enable UTF-16 variant of PCRE library
- The pcre_info() function has been removed from pcre library.
- Loading compiled pattern does not fix endianity anymore. Instead an errror
  is returned and the application can use pcre_pattern_to_host_byte_order() to
  convert the pattern.
- Surrogates (0xD800---0xDFFF) are forbidden in UTF-8 mode now.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.21-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Petr Pisar <ppisar@redhat.com> - 8.21-2
- Fix unmatched subpattern to not become wildcard (bug #769597)
- Fix NULL pointer derefernce in pcre_free_study() (upstream bug #1186)

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 8.21-1
- 8.21 bump

* Thu Dec 08 2011 Karsten Hopp <karsten@redhat.com> 8.21-0.2.RC1
- ppc needs a larger stack similar to s390

* Tue Dec 06 2011 Petr Pisar <ppisar@redhat.com> - 8.21-0.1.RC1
- 8.21-RC1 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 8.20-7
- Fix case-less match if cases differ in encoding length (bug #756675)

* Fri Nov 25 2011 Petr Pisar <ppisar@redhat.com> - 8.20-6
- Fix cache-flush in JIT on PPC

* Tue Nov 22 2011 Petr Pisar <ppisar@redhat.com> - 8.20-5
- Fix repeated forward reference (bug #755969)

* Wed Nov 16 2011 Petr Pisar <ppisar@redhat.com> - 8.20-4
- Fix other look-behind regressions

* Tue Nov 15 2011 Petr Pisar <ppisar@redhat.com> - 8.20-3
- Fix look-behind regression in 8.20

* Tue Nov 15 2011 Dan Horák <dan[at]danny.cz> - 8.20-2
- fix build on s390(x) - disable jit and use larger stack for tests

* Fri Oct 21 2011 Petr Pisar <ppisar@redhat.com> - 8.20-1
- 8.20 bump

* Tue Oct 11 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC3
- 8.20-RC3 bump

* Fri Sep 23 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC2
- 8.20-RC2 bump

* Mon Sep 12 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC1
- 8.20-RC1 bump with JIT

* Tue Sep 06 2011 Petr Pisar <ppisar@redhat.com> - 8.13-4
- Fix infinite matching PRUNE (bug #735720)

* Mon Aug 22 2011 Petr Pisar <ppisar@redhat.com> - 8.13-3
- Fix parsing named class in expression (bug #732368)

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-2
- Separate utilities from libraries
- Move pcre-config(1) manual to pcre-devel sub-package
- Remove explicit defattr from spec code
- Compile pcretest with readline support

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-1
- 8.13 bump: Bug-fix version, Unicode tables updated to 6.0.0, new pcregrep
  option --buffer-size to adjust to long lines, new feature is passing of
  *MARK information to callouts.
- Should fix crash back-tracking over unicode sequence (bug #691319)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-4
- Fix caseless reference matching in UTF-8 mode when the upper/lower case
  characters have different lengths (bug #702623)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-3
- Fix typos in manual pages (bugs #675476, #675477)
- Clean spec file up

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Petr Pisar <ppisar@redhat.com> - 8.12-1
- 8.12 bump
- Remove accepted pcre-8.11-Fix-typo-in-pcreprecompile-3.patch

* Mon Dec 13 2010 Petr Pisar <ppisar@redhat.com> - 8.11-1
- 8.11 bump
- See ChangeLog for changes. Namely changes have been made to the way
  PCRE_PARTIAL_HARD affects the matching of $, \z, \Z, \b, and \B.
- Fix typo in pcreprecompile(3) manual
- Document why shared library is not under /usr

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 8.10-1
- 8.10 bump (bug #612635)
- Add LICENCE to static subpackage because COPYING refers to it
- Remove useless rpath by using new libtool (simple sed does not work anymore
  because tests need to link against just-compiled library in %%check phase)

* Thu Jul 08 2010 Petr Pisar <ppisar@redhat.com> - 7.8-4
- Add COPYING to static subpackage
- Remove useless rpath

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> - 7.8-1
- Update to 7.8, drop upstreamed patches
- Fix destination of documentation (#427763)
- Use buildroot macro consistently
- Separate the static library, as per current Guidelines
- Satisfy rpmlint

* Fri Jul  4 2008 Tomas Hoger <thoger@redhat.com> - 7.3-4
- Apply Tavis Ormandy's patch for CVE-2008-2371.

* Tue Feb 12 2008 Tomas Hoger <thoger@redhat.com> - 7.3-3
- Backport patch from upstream pcre 7.6 to address buffer overflow
  caused by "a character class containing a very large number of
  characters with codepoints greater than 255 (in UTF-8 mode)"
  CVE-2008-0674, #431660
- Try re-enabling make check again.

* Fri Nov 16 2007 Stepan Kasal <skasal@redhat.com> - 7.3-2
- Remove obsolete ``reqs''
- add dist tag
- update BuildRoot

* Mon Sep 17 2007 Than Ngo <than@redhat.com> - 7.3-1
- bz292501, update to 7.3

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 7.0-1
- 7.0

* Mon Nov 27 2006 Than Ngo <than@redhat.com> - 6.7-1
- update to 6.7
- fix #217303, enable-unicode-properties
- sane stack limit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Tue May 09 2006 Than Ngo <than@redhat.com> 6.6-1
- update to 6.6
- fix multilib problem

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Than Ngo <than@redhat.com> 6.3-1
- update to 6.3

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 5.0-4
- rebuild

* Fri Feb 11 2005 Joe Orton <jorton@redhat.com> 5.0-3
- don't print $libdir in 'pcre-config --libs' output

* Thu Nov 18 2004 Joe Orton <jorton@redhat.com> 5.0-2
- include LICENCE, AUTHORS in docdir
- run make check
- move %%configure to %%build

* Thu Nov 18 2004 Than Ngo <than@redhat.com> 5.0-1
- update to 5.0
- change License: BSD
- fix header location #64248

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 4.5-2
- add the correct pcre license, #118781

* Fri Mar 12 2004 Than Ngo <than@redhat.com> 4.5-1
- update to 4.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 4.4-1
- 4.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Than Ngo <than@redhat.com> 4.2-1
- update to 4.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 3.9-9
- build with utf8, bug #81504

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 3.9-8
- Really remove .la files

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 3.9-7
- remove .la

* Thu Oct 10 2002 Than Ngo <than@redhat.com> 3.9-7
- Typo bug

* Wed Oct  9 2002 Than Ngo <than@redhat.com> 3.9-6
- Added missing so symlink

* Thu Sep 19 2002 Than Ngo <than@redhat.com> 3.9-5.1
- Fixed to build s390/s390x/x86_64

* Thu Jun 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-5
- Fix #65009

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-2
- rebuild

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-1
- Update to 3.9

* Wed Nov 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.7-1
- Update to 3.7

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.4-2
- Move libpcre to /lib, grep uses it these days (#41104)

* Wed Apr 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Move this to a separate package, used to be in kdesupport, but it's
  generally useful...
