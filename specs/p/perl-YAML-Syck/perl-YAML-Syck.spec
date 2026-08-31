# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! 0%{?rhel}
%bcond_without perl_YAML_Syck_enables_optional_test
%else
%bcond_with perl_YAML_Syck_enables_optional_test
%endif

Name:           perl-YAML-Syck
Version:        1.47
Release:        1%{?dist}
Summary:        Fast, lightweight YAML loader and dumper
# gram.*: GPL-2.0-or-later
# *:      MIT
# Note that libsyck COPYING file describes itself as BSD but it's actually MIT
License:        GPL-2.0-or-later AND MIT
URL:            https://metacpan.org/release/YAML-Syck
Source0:        https://cpan.metacpan.org/modules/by-module/YAML/YAML-Syck-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::Mksymlists)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
# Module Runtime
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(parent)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Optional Tests
%if %{with perl_YAML_Syck_enables_optional_test}
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Devel::Leak)
BuildRequires:  perl(JSON)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Symbol)
%endif
# Dependencies
# (none)

# Avoid provides for private perl objects
%{?perl_default_filter}

%description
This module provides a Perl interface to the libsyck data serialization
library. It exports the Dump and Load functions for converting Perl data
structures to YAML strings, and the other way around.

%prep
%setup -q -n YAML-Syck-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 \
  OPTIMIZE="%{optflags} -DI_STDLIB=1 -DI_STRING=1"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license COPYING
%doc Changes COMPATIBILITY README.md
%{perl_vendorarch}/auto/YAML/
%{perl_vendorarch}/YAML/
%{perl_vendorarch}/JSON/
%{_mandir}/man3/JSON::Syck.3*
%{_mandir}/man3/YAML::Syck.3*

%changelog
* Tue Jul 14 2026 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  Security:
  - Fix four libsyck memory-safety CVEs reachable from the default
    YAML::Syck::Load() path on untrusted input with no special flags (GH#213)
    - CVE-2026-57075 (CWE-125): Out-of-bounds read in the base64 decoder
      caused by signed-char indexing of the decode table on !!binary input
    - CVE-2026-57076 (CWE-416): Use-after-free of an anchor key string shared
      between the node and the anchors table
    - CVE-2026-57077 (CWE-125): One-byte out-of-bounds read in the lexer
      newline scan during block-scalar parsing (incomplete-fix follow-on
      to CVE-2025-11683)
    - CVE-2026-13713 (CWE-416/CWE-415): Use-after-free / double-free of an
      anchor node on anchor redefinition, a remote-crash DoS from a 7-byte input
  - Harden syck_base64dec() to bounds-check each read so it cannot run past a
    non-NUL-terminated input buffer (defense-in-depth for callers passing raw
    buffers; GH#213)
  Bug Fixes:
  - Fix: Enforce $MaxDepth on Load to prevent C-stack exhaustion from deeply
    nested YAML/JSON input; YAML::Syck and JSON::Syck Load now default to 512,
    matching Dump (GH#204)
  - Fix: Emit YAML canonical forms (.nan, .inf, -.inf) for NaN/Inf values in
    Dump so they roundtrip with ImplicitTyping instead of reloading as plain
    strings (GH#201)
  Maintenance:
  - CI: add an AddressSanitizer job that builds the XS with
    -fsanitize=address and runs the suite plus the CVE trigger inputs to catch
    libsyck memory-safety defects; de-pin the libasan version so it tracks the
    runner's GCC (GH#213)

* Mon May 25 2026 Paul Howarth <paul@city-fan.org> - 1.46-1
- Update to 1.46
  Bug Fixes:
  - Preserve string nature of numeric-looking values in Dump; pure strings (POK
    only, no IOK/NOK) are now quoted to maintain roundtrip fidelity
    (GH#199, GH#200)
  - Accept trailing commas in flow sequences and mappings ([a, b,] and
    {a: 1,}), valid per YAML 1.0/1.1/1.2 spec (GH#195, GH#196)
  Maintenance:
  - CI: upgrade install-with-cpm to v2 for compatibility with Perl versions
    prior to 5.24 in perldocker containers (GH#197, GH#198)
  - Clean up MANIFEST.SKIP: add #!include_default, remove redundant entries,
    exclude .claude/ from distribution

* Mon Apr 27 2026 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  Bug Fixes:
  - Fix: Use syck_base64_free() to fix Windows "Free to wrong pool" crash in
    base64 encode/decode buffers; also plugs a memory leak (GH#189)
  - Fix: Clear type tag on blessed scalar alias early-return so the stale tag
    no longer leaks onto the next emitted item (GH#193, GH#194, rhbz#2459200)
  - Fix: Negative float#base60 values produce wrong results; strip sign before
    accumulating and avoid negative zero for portable stringification (GH#191)
  - Fix: Prevent memory leaks when Load/LoadJSON croak on parse errors (GH#192)
  Maintenance:
  - Test: Add coverage for SortKeys and JSON MaxDepth (GH#188)
  - Test: Add error handling coverage for LoadFile/DumpFile (GH#190)
  - Update README

* Fri Apr  3 2026 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  Bug Fixes:
  - Fix: Positive hex and octal values parsed as 0 with ImplicitTyping (GH#187)
  - Fix: Resolve uintptr_t redefinition error on Win64 MinGW (GH#186)

* Thu Apr  2 2026 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  Bug Fixes:
  - Fix: Prevent resource leaks on croak/early-return paths in Dump (GH#161)
  - Fix: Prevent output SV leaks on croak in Dump/DumpFile callers (GH#163)
  - Fix: Load() in list context returns empty list for empty/undef input; also
    applies to LoadBytes and LoadUTF8 (GH#164, GH#165)
  - Fix: DumpCode serializes prototype string instead of code body (GH#168)
  - Fix: Memory leak in !perl/scalar Load - newRV_inc should be newRV_noinc
    (GH#170)
  - Fix: Add pTHX_ to SAVEDESTRUCTOR_X callback for threaded Perl
    (GH#175, GH#176)
  - Fix: Add TODO guard for eval_pv leak on Perl < 5.14 (GH#179, GH#180)
  - Fix: Negative hex and octal values parsed as 0 with ImplicitTyping (GH#183)
  - Fix: Negative int#base60 values produce unsigned wraparound (GH#185)
  Improvements:
  - Modernize META_MERGE for CPANTS compliance (GH#162)
  - Fix hash table size handling and remove compile warnings in syck_st (GH#174)
  Maintenance:
  - Restore TODO guard for Dump code leak test on Perl < 5.26 (GH#167)
  - Resolve 2010 TODO in perl_json_postprocess with test coverage (GH#166)
  - CI: Upgrade actions to resolve Node.js 20 deprecation warnings (GH#177)

* Fri Mar 27 2026 Paul Howarth <paul@city-fan.org> - 1.42-1
- Update to 1.42
  Bug Fixes:
  - Fix: Replace strtok() with strpbrk() and fix sign-compare warnings in
    perl_syck.h (GH#145)
  - Fix: Terminate plain scalars at document boundaries --- and ... (GH#150)
  - Fix: Skip %%TAG and %%YAML directives in document header (GH#151)
  - Fix: Plug SV leak when eval_pv croaks on bad perl/code blocks (GH#153)
  - Fix: Allow non-specific tag '!' before block scalars (GH#27, GH#102)
  - Fix: Remove spurious %%type <nodeId> for indent_open in gram.y
    (GH#157, GH#158)
  - Fix: Use modern bison %%define api.prefix directive (GH#159, GH#160)
  Improvements:
  - Implement YAML merge key (<<) support (GH#149)
  Maintenance:
  - Remove dead Perl 5.6/5.8 version guards from test files (GH#146)
  - Add YAML 1.0 spec compliance audit and coverage tests (GH#148)
  - Add comprehensive round-trip tests for YAML 1.0 spec features (GH#152)
  - Remove unneeded TODO in t/json-basic.t (GH#154)
  - Add regex Dump/Load/round-trip tests to perl tag scheme (GH#155)
  - Do not require a .y file to build YAML::Syck; add brew support for bison
  - Don't ship docs/ directory in tarball

* Mon Mar 23 2026 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  Bug Fixes:
  - Fix float parsing on -Dusequadmath perls: use Perl's Atof() instead of
    strtod() so that floats like -3.14 are not corrupted by double-precision
    rounding artifacts (GH#140, GH#141)

* Sun Mar 22 2026 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  Bug Fixes:
  - Fix: escape solidus (/) as \/ in JSON::Syck::Dump for XSS safety
    (GH#125, GH#130)
  - Fix: anchor tracking for blessed scalar refs in Dump (GH#126, GH#131)
  - Fix: prevent buffer underflow in base60 (sexagesimal) parsing (GH#133)
  - Fix: guard against NULL type from strtok in tag parsing (GH#135)
  - Fix: correct copy-paste bug in syck_seq_assign() ASSERT macros (GH#137)
  - Fix t/yaml-implicit-typing.t failure with -Duselongdouble perls
    (GH#138, GH#139)
  Improvements:
  - Resolve TODO tests for empty/invalid YAML to match actual behaviour
    (GH#127, GH#129)
  Maintenance:
  - Remove dead Perl 5.6 TODOs and convert 5.8 TODO to SKIP (GH#129)
  - Add comprehensive implicit type resolution test suite (GH#137)
  - Update MANIFEST to include all unit tests
  - Clean up test names to remove unnecessary numbering

* Thu Mar 19 2026 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  Features:
  - Add LoadBytes, LoadUTF8, DumpBytes, DumpUTF8 functions (GH#51)
  Fixes:
  - Fix heap buffer overflow in the YAML emitter - CVE-2026-4177 (GH#67)
  - Fix DumpFile with tied filehandles (IO::String, IO::Scalar) (GH#22)
  - Fix _is_glob to recognize IO::Handle subclasses (GH#23)
  - Fix memory leak when dumping filehandles (CPAN RT#41199, GH#42)
  - Fix dumping of tied hashes (GH#31)
  - Fix dumping strings starting with '...' as unquoted plain scalars (GH#34)
  - Fix dumping strings with tabs and carriage returns as plain scalars (GH#59)
  - Fix double-dash YAML parsing (RT#34073, GH#35)
  - Fix extra newline after empty arrays/hashes in YAML output (GH#36)
  - Remove trailing whitespace from YAML output lines (GH#37, GH#38, GH#39)
  - Fix quoting of \r and \t in YAML output instead of emitting raw bytes
    (GH#40)
  - Fix growing !!perl/regexp objects in round-trips (GH#43)
  - Fix quoted '=' being transformed into 'str' (GH#45)
  - Fix backslash-space escape in double-quoted YAML strings (GH#61)
  - Fix flow sequence comma separator not recognized without trailing space
    (GH#60)
  - Fix wide character warning in DumpFile (GH#28)
  - Fix inline arrays without space after comma (GH#25)
  - Fix: quote strings matching YAML implicit types to prevent round-trip
    failures (GH#26)
  - Fix JSON::Syck::Dump to use JSON-valid \uXXXX escapes in output (GH#21)
  - Fix JSON::Syck::Load decoding of \/ and \uXXXX escape sequences (GH#30)
  - Fix: apply JSON postprocessing to JSON::Syck::DumpFile output (GH#104)
  - Fix: add tied-filehandle fallback to JSON::Syck::DumpFile (GH#98)
  - Fix: handle JSON escape sequences in SingleQuote mode Load (GH#99)
  - Fix: restore Perl 5.8 compatibility in test suite (GH#121)
  - Fix: correct copy-paste error in Makefile.PL clean target (GH#101)
  - Fix: correct $SortKeys POD default from false to true (GH#100)
  - Fix: correct POD documentation errors (GH#103)
  Maintenance:
  - Add C23-compatible function prototypes for GCC 15 compatibility (GH#112)
  - Silence macOS compiler warnings (GH#92)
  - Guard stdint.h include for portability (HP-UX 11.11) (GH#33)
  - Guard stdint.h include in syck_st.h for portability (GH#24)
  - Update ppport.h to 3.68
  - Add regression tests for magical variable dumping (GH#32)
  - CI: modernize GitHub Actions workflow (GH#123, GH#124)
  - CI: add disttest job to validate MANIFEST completeness
- Use %%{make_build} and %%{make_install}
- Drop workaround for C23 incompatibility

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Oct 11 2025 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - Address memory corruption leading to 'str' value being set on empty keys

* Fri Oct 10 2025 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35
  - Address parsing error related to string detection on read for empty strings

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-17
- Perl 5.42 rebuild

* Sat Jan 18 2025 Paul Howarth <paul@city-fan.org> - 1.34-16
- Build using -std=gnu17 since ancient code does not compile with -std=c23

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-13
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-9
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 27 2020 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - Fix memory corruption (GH#44, GH#48)
  - Fix for handling circular aliases (GH#52, GH#53)
  - Unconditionally include stdlib.h in syck.h (GH#56)
  - Switch changelog to a more parsable format
  - Update github CI to use a cpanfile
  - Update Devel::PPPort to 3.62
  - Stop depending on constants dropped from Perl 5.28 (GH#50)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-2
- Perl 5.32 rebuild

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32
  - Interface Change: Change default for LoadBlessed to false
  - Remove YAML::Syck tests that parse META.yml
  - Switch to github actions for testing
  - Remove 'use vars' from code in favor of 'our'

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31
  - Switch to ExtUtils::MakeMaker for builder
  - Switch official issue tracker and repo to github
  - MANIFEST warning is now fixed; also shipping additional tests because of
    this
- Make sure <stdlib.h> and <string.h> are included, quietens lots of warnings

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-2
- Perl 5.26 rebuild

* Thu Apr 20 2017 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - Fix handling carriage return after c-indicator (CPAN RT#41141)
  - Fix CHECK_UTF8 SEGV with empty len=0 strings (CPAN RT#61562)
  - Add missing function declarations
  - Tighten the TODO tests; no passing TODOs now, but still JSON
  - SingleQuote and \/ and \u roundtrips do fail
- Drop EL-5 support
  - Drop Group: and BuildRoot: tags
  - Drop buildroot cleaning in %%install
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-6
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1.29-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.22 rebuild

* Tue Dec 16 2014 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - Upstreamed fix for test failures on PPC and ARM (CPAN RT#83825)
  - Fix crash in syck_emit on platforms with long long pointers
- Use %%license

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 1.28-1
- 1.28 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.27-2
- Perl 5.18 rebuild

* Tue May 21 2013 Paul Howarth <paul@city-fan.org> 1.27-1
- Update to 1.27
  - Fix for hash randomization in yaml-alias.t on perl 5.18.0 (CPAN RT#84882,
    CPAN RT#84466)

* Mon Mar 11 2013 Paul Howarth <paul@city-fan.org> 1.25-1
- Update to 1.25
  - Bump version number and release to fix a MANIFEST mistake in 1.24

* Sun Mar 10 2013 Paul Howarth <paul@city-fan.org> 1.24-2
- Work around test failures on PPC and ARM (#919806, CPAN RT#83825)

* Thu Mar  7 2013 Paul Howarth <paul@city-fan.org> 1.24-1
- Update to 1.24
  - Implement $JSON::Syck::MaxDepth
  - Prevent failure when the same object is seen twice during Dump
  - Prevent YAML from being influenced by the previous change
  - MinGW64 compatibility (CPAN RT#78363)

* Wed Feb 27 2013 Paul Howarth <paul@city-fan.org> 1.23-1
- Update to 1.23
  - Synchronize JSON::Syck with YAML::Syck version number
  - Add DumpInto functions (YAML+Syck), which dump into a provided scalar
    instead of a newly-allocated one
  - Modify DumpFile functions to output directly to the specified
    file/filehandle instead of buffering all output in memory
  - Avoid modifying numbers into strings when emitting
  - Fix error message typo: s/existant/existent/g
  - Fix for non-printable character detection
  - Quote if non-printable characters are present
  - Make sure that LoadBlessed=0 blocks all blessing
  - Start listing primary repo as http://github.com/toddr/YAML-Syck
  - README refreshed via perldoc -t
- Require perl(XSLoader) at runtime
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-1
- 1.20 bump

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.17-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 1.17 -3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Steven Pritchard <steve@kspei.com> 1.17-1
- Update to 1.17.
- Update Source0 URL.
- BR JSON (for tests).

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-3
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-2
- fix license

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- auto-update to 1.07 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 09 2008 Steven Pritchard <steve@kspei.com> 1.05-1
- Update to 1.05.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.04-2
- rebuild for new perl (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 1.04-1
- Update to 1.04.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.01-3
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1.01-1
- Update to 1.01.

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.98-1
- Update to 0.98.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.97-1
- Update to 0.97.

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 0.96-1
- Update to 0.96.

* Fri Aug 03 2007 Steven Pritchard <steve@kspei.com> 0.95-1
- Update to 0.95.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 0.94-1
- Update to 0.94.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.91-1
- Update to 0.91.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 0.85-1
- Update to 0.85.

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-3
- add perl split BR's

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-2
- bump

* Thu Feb 01 2007 Steven Pritchard <steve@kspei.com> 0.82-1
- Specfile autogenerated by cpanspec 1.69.1.
- Remove explicit build dependency on perl.
- Include JSON module.
- BR Devel::Leak (for tests).
