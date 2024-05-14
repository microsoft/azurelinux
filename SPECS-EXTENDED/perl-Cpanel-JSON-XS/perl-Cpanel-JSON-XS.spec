Summary:        JSON::XS for Cpanel, fast and correct serializing
Name:           perl-Cpanel-JSON-XS
Version:        4.27
Release:        2%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Cpanel-JSON-XS
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Cpanel-JSON-XS-%{version}.tar.gz
Patch0:         Cpanel-JSON-XS-4.20-signature.patch

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Script Runtime
BuildRequires:  perl(CBOR::XS)
BuildRequires:  perl(CPAN::Meta::YAML)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::LZF)
BuildRequires:  perl(Config)
BuildRequires:  perl(Convert::Bencode)
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(YAML)
BuildRequires:  perl(YAML::Syck)
BuildRequires:  perl(YAML::XS)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if 0%{?with_check}
BuildRequires:  perl(B)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Encode) >= 1.9081
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(charnames)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared) >= 1.21
BuildRequires:  perl(utf8)
# Optional Tests
# Cycle: perl-Cpanel-JSON-XS → perl-Test-LeakTrace → perl-Module-Install
# → perl-YAML-Tiny → perl-JSON-MaybeXS → perl-Cpanel-JSON-XS
# Cycle: perl-Cpanel-JSON-XS → perl-Perl-MinimumVersion → perl-PPI
# → perl-List-MoreUtils → perl-Test-LeakTrace → perl-Module-Install
# → perl-YAML-Tiny → perl-JSON-MaybeXS → perl-Cpanel-JSON-XS
# Cycle: perl-Cpanel-JSON-XS → perl-Test-MinimumVerion → perl-YAML-Tiny
# → perl-JSON-MaybeXS → perl-Cpanel-JSON-XS
# Cycle: perl-Cpanel-JSON-XS → perl-Test-Kwalitee → perl-Module-CPANTS-Analyse
# → perl-JSON-MaybeXS → perl-Cpanel-JSON-XS
%if !%{defined perl_bootstrap}
# Maintainer Tests (Test::Spelling intentionally omitted as associated test would fail due to various technical terms)
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(JSON) >= 2.09
BuildRequires:  perl(JSON::PP) >= 2.09
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Math::BigFloat) >= 1.16
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Mojo::JSON) >= 6.11
BuildRequires:  perl(Perl::MinimumVersion) >= 1.20
BuildRequires:  perl(Pod::Spell::CommonMistakes)
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::CPAN::Meta) >= 0.12
BuildRequires:  perl(Test::CheckChanges)
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::LeakTrace)
BuildRequires:  perl(Test::MinimumVersion) >= 0.008
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Text::CSV_XS)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(common::sense) >= 3.5
%endif
%endif

# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Scalar::Util)
Requires:       perl(overload)
Recommends:     perl(Math::BigFloat) >= 1.16
Recommends:     perl(Math::BigInt)
Suggests:       perl(Bencode)
Suggests:       perl(CBOR::XS)
Suggests:       perl(CPAN::Meta::YAML)
Suggests:       perl(Compress::LZF)
Suggests:       perl(Data::Dump)
Suggests:       perl(Data::Dumper)
Suggests:       perl(Sereal::Decoder)
Suggests:       perl(Sereal::Encoder)
Suggests:       perl(YAML)
Suggests:       perl(YAML::Syck)
Suggests:       perl(YAML::XS)
# Avoid unwanted provides and dependencies
%{?perl_default_filter}

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%prep
%setup -q -n Cpanel-JSON-XS-%{version}

# Fix shellbangs
perl -pi -e 's|^#!/opt/bin/perl|#!/usr/bin/perl|' eg/*

# Skip the signature check as we've tweaked some files
%patch 0

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
%if !%{defined perl_bootstrap}
make test xtest AUTHOR_TESTING=1
%else
make test
%endif

%files
%license COPYING
%doc Changes README eg/
%{_bindir}/cpanel_json_xs
%{perl_vendorarch}/auto/Cpanel/
%{perl_vendorarch}/Cpanel/
%{_mandir}/man1/cpanel_json_xs.1*
%{_mandir}/man3/Cpanel::JSON::XS.3*
%{_mandir}/man3/Cpanel::JSON::XS::Boolean.3*
%{_mandir}/man3/Cpanel::JSON::XS::Type.3*

%changelog
* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.27-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Oct 15 2021 Paul Howarth <paul@city-fan.org> - 4.27-1
- Update to 4.27
  - Only add -Werror=declaration-after-statement for 5.035004 and earlier
    (GH#186)
  - Fix 125_shared_boolean.t for threads (GH#184)
- Drop support for building for targets older than EL-7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.26-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.26-2
- Perl 5.34 rebuild

* Mon Apr 12 2021 Paul Howarth <paul@city-fan.org> - 4.26-1
- Update to 4.26
  - Fix compilation with C++ (GH#177)
- Use %%license unconditionally

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Paul Howarth <paul@city-fan.org> - 4.25-1
- Update to 4.25
  - Fix decode relaxed with comment at the end of the buffer (GH#174), a
    regression introduced with 3.0220, to fix n_number_then_00
  - Possible fix for a gcc-9 optimizer bug (GH#172)

* Fri Oct  2 2020 Paul Howarth <paul@city-fan.org> - 4.24-1
- Update to 4.24
  - Fix decode_json(scalar, 0), check 2nd arg for true-ness (GH#171)

* Sat Sep  5 2020 Paul Howarth <paul@city-fan.org> - 4.23-1
- Update to 4.23
  - Fix t/54_stringify needs JSON 2.09 for allow_unknown (GH#169)
  - Fix t/118_type.t for 5.6
  - Fix t/96_interop.t for missing JSON::XS
  - Possible fix for s390x with long double, untested (GH#83)

* Thu Aug 13 2020 Paul Howarth <paul@city-fan.org> - 4.21-1
- Update to 4.21
  - Fix not enough HEK memory allocation for the new canonical tied hashes
    feature (GH#168)
  - TODO broken JSON::PP::Boolean versions 2.9x - 4.0 with threads::shared in
    125_shared_boolean.t

* Wed Aug 12 2020 Paul Howarth <paul@city-fan.org> - 4.20-1
- Update to 4.20
  - New feature: sort tied hashes with canonical (GH#167)
  - Fix encode of threads::shared boolean (GH#166); this was broken with 4.00
  - Fix some stringify overload cases via convert_blessed (GH#105)
  - Fix a compat case with JSON::XS, when convert_blessed is set, but
    allow_blessed not (GH#105)
  - Improve blessed and stringify tests
  - Work on better inf/nan detection on AIX (GH#165)
  - Fix documentation for booleans and their types (GH#162)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.19-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.19-2
- Perl 5.32 rebuild

* Thu Feb  6 2020 Paul Howarth <paul@city-fan.org> - 4.19-1
- Update to 4.19
  - Fix typed decode memory leak (GH#160)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Paul Howarth <paul@city-fan.org> - 4.18-1
- Update to 4.18
  - Add new method ->type_all_string (GH#156); when type_all_string is set then
    the encode method produces stable deterministic string types in the
    resulting JSON - this can be an alternative to Cpanel::JSON::XS::Type when
    having deterministic output is required but string JSON types are enough
    for any output
  - Move SvGETMAGIC() from encode_av() and encode_hv() to encode_sv() (GH#156)
  - Add Math::BigInt and Math::BigFloat as recommended dependencies (GH#157)

* Tue Nov  5 2019 Paul Howarth <paul@city-fan.org> - 4.17-1
- Update to 4.17
  - Add Changes tests and fixups (GH#155)

* Mon Nov  4 2019 Paul Howarth <paul@city-fan.org> - 4.16-1
- Update to 4.16
  - Use Perl_strtod instead of self-made atof (via pow), to minimize
    differences from core string-to-float conversions (GH#154); this fixes
    float representation regressions (in the 1e-6 to 1e-16 range) since 5.22

* Tue Oct 22 2019 Paul Howarth <paul@city-fan.org> - 4.15-1
- Update to 4.15
  - Fix more tests for nvtype long double

* Tue Oct 15 2019 Paul Howarth <paul@city-fan.org> - 4.14-1
- Update to 4.14
  - Fix tests for nvtype long double (GH#153)
  - Fix PREREQ's, e.g. CentOS 7 has not Test::More anymore (GH#152)

* Mon Oct 14 2019 Paul Howarth <paul@city-fan.org> - 4.13-1
- Update to 4.13
  - For JSON_TYPE_INT and JSON_TYPE_FLOAT, allow to encode numeric values above
    2^64 in PV slot via Math::BigInt/Float (GH#145, GH#148, GH#149)
  - For JSON_TYPE_INT and JSON_TYPE_FLOAT encoder, allow to pass Math::BigInt
    and Math::BigFloat objects with allow_bignum (GH#147)
  - Fix encoding floating point values above 2^64 in PV slot to JSON_TYPE_INT
    (GH#148, GH#150)
  - Do not allow serializing objects when convert_blessed is not enabled
    (GH#146)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Paul Howarth <paul@city-fan.org> - 4.12-1
- Update to 4.12
  - Make encoder independent of Math::BigInt version (GH#140)
  - Rethrow error from eval_sv and eval_pv() (GH#138, GH#139), e.g. when
    Math::BigInt/BigFloat fails
  - Fix encoding Inf and NaN from PV and NV slots to JSON_TYPE_INT (GH#137)
  - Fix memory corruption in sv_to_ivuv() function (GH#136)
  - Add new method ->require_types (GH#135)
  - Fix typed json encoder conversion from scalar's PV and NV slot to
    JSON_TYPE_INT (GH#133, GH#134)
  - Fix inconsistency with warnings in typed json encoder (GH#131)
  - Fix Perl 5.8.0 support (GH#130)
  - Fixed minor pod typo (GH#129)
  - Document invalid recursive callbacks or overloads (GH#128)

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.11-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.11-2
- Perl 5.30 rebuild

* Wed Mar 27 2019 Paul Howarth <paul@city-fan.org> - 4.11-1
- Update to 4.11
  - Fix unicode strings with BOM corrupt ->utf8 state (GH#125); the BOM
    encoding affects only its very own decode call, not its object

* Mon Mar 18 2019 Paul Howarth <paul@city-fan.org> - 4.10-1
- Update to 4.10
  - Fix incr_text refcounts (GH#123)
  - Add incr_reset testcase (GH#123)
  - Fix encode_stringify string-overload refcnt problem (GH#124)
  - "Attempt to free unreferenced scalar" with convert_blessed and overload

* Fri Feb 15 2019 Paul Howarth <paul@city-fan.org> - 4.09-1
- Update to 4.09
  - Add separate allow_dupkeys property, in relaxed (GH#122)
  - Fixed allow_dupkeys for the XS slow path
  - Silence 2 -Wunused-value warnings
  - Fix ->unblessed_bool to produce modifiable perl structures (GH#121)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Paul Howarth <paul@city-fan.org> - 4.08-1
- Update to 4.08
  - Add unblessed_bool property (GH#118)

* Mon Nov  5 2018 Paul Howarth <paul@city-fan.org> - 4.07-1
- Update to 4.07
  - Silence Gconvert -Wunused-result

* Thu Aug 23 2018 Paul Howarth <paul@city-fan.org> - 4.06-1
- Update to 4.06
  - Fix overloaded eq/ne comparisons (GH#116, GH#117): detect strings, protect
    from endless recursion; false is now ne "True"; clarify eq/ne rules in the
    docs

* Mon Aug 20 2018 Paul Howarth <paul@city-fan.org> - 4.05-1
- Update to 4.05
  - Set decoded type (GH#115)
  - Add json_type_weaken (GH#114)
  - Fix tests for 5.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.04-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.04-2
- Perl 5.28 rebuild

* Sat Jun 23 2018 Paul Howarth <paul@city-fan.org> - 4.04-1
- Update to 4.04
  - Fix bignum NaN/inf handling (GH#78)
  - Move author tests to xt/ as suggested in GH#106, added a make xtest target
    (fixes a test fail with ASAN)

* Thu Jun 21 2018 Paul Howarth <paul@city-fan.org> - 4.03-1
- Update to 4.03
  - Add sereal cpanel_json_xs type (GH#110)
  - Fix bencode/bdecode methods in cpanel_json_xs (GH#111)
  - Overload ne operator for JSON::PP::Boolean (GH#107)
  - Add a missing semicolon to a documentation example (GH#104)
- Switch upstream from search.cpan.org to metacpan.org
- Add suggestions for Sereal::Decoder and Sereal::Encoder
- Switch suggestion of Convert::Bencode to Bencode
- Work around failing t/z_meta.t

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 4.02-2
- Rebuild with new redhat-rpm-config/perl build flags

* Tue Feb 27 2018 Paul Howarth <paul@city-fan.org> - 4.02-1
- Update to 4.02
  - Add encoder indent_length method, previously hard-coded to 3 (GH#103)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb  3 2018 Paul Howarth <paul@city-fan.org> - 4.01-1
- Update to 4.01
  - Fix locale crash with threaded perls < 5.22 and glibc (GH#101)

* Fri Feb  2 2018 Paul Howarth <paul@city-fan.org> - 4.00-1
- Update to 4.00
  - Simplify allow_singlequote check (coverity cid#165321)
  - Deprecate UTF-16 or UTF-32 BOM's: RFC 8259
  - Added Cpanel::JSON::XS::Type as 2nd optional encode argument (GH#94)
  - Removed calling get magic hooks twice in encode
  - Avoid setlocale race in threads with non-C locales, where the threads
    differ in the LC_NUMERIC locale (GH#99)
  - Fix uselocale() code
  - Probe for uselocale and xlocale.h with <5.22 threaded

* Tue Aug 29 2017 Paul Howarth <paul@city-fan.org> - 3.0239-1
- Update to 3.0239
  - Make printing of numbers on perls earlier than 5.22 locale-insensitive, to
    produce a dot as decimal separator (#96)
  - Fix compilation under Windows (#98)

* Mon Jul 31 2017 Paul Howarth <paul@city-fan.org> - 3.0237-1
- Update to 3.0237
  - Relax inf/nan tests as in t/op/infnan.t for windows: we cannot know if
    msvcrt.dll or the new ucrt.dll is used, so try a list of valid values

* Fri Jul 28 2017 Paul Howarth <paul@city-fan.org> - 3.0236-1
- Update to 3.0236
  - Fix and unify utf8 handling with 5.6.2, improve many utf8 tests (GH#88)
  - Add tests for boolean sv_yes and sv_no (GH#88)
  - Check for correct module in %%INC (GH#89)
  - Fix appveyor smoke with latest strawberry, use $Config{make} (GH#91)
  - Fix inf/nan for strawberry 5.26
  - Disallow duplicate keys by default; only allow them in relaxed mode (GH#75)
  - De-fragilize t/96_mojo.t false test to ""
  - Stringify true again as "1", not as "true" due to popular demand (GH#87)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0233-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.0233-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.0233-2
- Perl 5.26 rebuild

* Tue May  2 2017 Paul Howarth <paul@city-fan.org> - 3.0233-1
- Update to 3.0233
  - 5.6 test fixes, silence some cc warnings, add coverage and release targets,
    fix appveyor

* Mon May  1 2017 Paul Howarth <paul@city-fan.org> - 3.0232-1
- Update to 3.0232
  - Fix for MSVC 2015/14.0 and newer with changed nan/inf (GH#85)
  - Added appveyor CI
  - Silence 32bit debugging format warning
  - Stabilize decode_hv hook (Coverity)
  - Ignore sv_utf8_downgrade errors (Coverity)
- BR: perl-generators unconditionally

* Wed Mar 29 2017 Paul Howarth <paul@city-fan.org> - 3.0231-1
- Update to 3.0231
  - Fix need() overallocation (GH#84) and missing need() calls

* Sun Mar 12 2017 Paul Howarth <paul@city-fan.org> - 3.0230-1
- Update to 3.0230
  - Fix minor gcc compilation warnings
  - Add some core compat. warnings for gcc/clang compat. compilers

* Wed Mar  8 2017 Paul Howarth <paul@city-fan.org> - 3.0228-1
- Update to 3.0228
  - Fix decode_prefix offset when the string was re-allocated: rather return
    the offset, not the pointer to the old start (GH#82)

* Tue Feb 14 2017 Paul Howarth <paul@city-fan.org> - 3.0227-1
- Update to 3.0227
  - Fix CLONE and END, broken with 3.0226 (GH#80); these methods are usually
    called with arguments, which we ignore

* Sun Feb 12 2017 Paul Howarth <paul@city-fan.org> - 3.0226-1
- Update to 3.0226
  - Relax longdouble Gconvert test on ppc64le and aarch64-linux-ld, with
    apparent HW quadmath without USE_QUADMATH (older perls)
  - Fixed 2 uninit warnings in the XS

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0225-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Paul Howarth <paul@city-fan.org> - 3.0225-1
- Update to 3.0225
  - UTF8 decode security fixes for perl 5.6
  - Added extra detection code for overflows and non-continuations; this
    broke one 5.6 test with an overlong multi-byte character, which previously
    worked accidentally, i.e. decode "\ud801\udc02\x{10204}"
  - Added tests for ill-formed utf8 sequences from Encode

* Sun Nov 20 2016 Paul Howarth <paul@city-fan.org> - 3.0224-1
- Update to 3.0224
  - Fixes for g++-6, stricter -fpermissive and -Wc++11-compat

* Thu Nov 17 2016 Paul Howarth <paul@city-fan.org> - 3.0223-1
- Update to 3.0223
  - Fixed decode bignum with a string prefix (GH#76)

* Sun Oct 30 2016 Paul Howarth <paul@city-fan.org> - 3.0222-1
- Update to 3.0222
  - Fixed documentation of decode for unicode noncharacters
  - Added correct code to warn as in core
  - No replacement, ignore warnings when in relaxed mode
  - We used a wrong range too, but the wrong code from 3.0220 was never
    executed because of an coding error (GH#73, GH#74)
  - Fixed a perl 5.6 compilation regression from 3.0220
  - Improve decode_bom for multibyte encoding, but not yet enabled
  - Fix refcount error
  - Add 5.24 to travis tests
  - Enable decode_bom for multibyte encodings UTF16 and UTF32
  - Encode internally to UTF-8

* Fri Oct 28 2016 Paul Howarth <paul@city-fan.org> - 3.0220-1
- Update to 3.0220
  - Add comprehensive JSON decode spectests from
    https://seriot.ch/parsing_json.html (GH#72)
  - Decode with BOM (UTF-8, UTF-16, or UTF-32); for now only UTF-8, the others
    error
  - Fixed detection of final \0 as illegal non-whitespace garbage; fixes
    spectest 'n_number_then_00' (GH#72)
  - Changed decode of unicode noncharacters between U+FFFD and U+10FFFF to the
    recommended U+FFFD REPLACEMENT CHARACTER, when not in the binary or relaxed
    mode

* Wed Oct 26 2016 Paul Howarth <paul@city-fan.org> - 3.0219-1
- Update to 3.0219
  - Work around mingw 4.0 modfl() bug (Perl RT#125924)

* Thu Oct 13 2016 Paul Howarth <paul@city-fan.org> - 3.0218-1
- Update to 3.0218
  - Detect INF/NAN: ?/++/-?/--- on HP-UX (GH#56)
  - New stringify_infnan(3) infnan_mode; easy to detect platform-independent
    "inf", "-inf" or "nan" strings with double quotes, with qnan, snan or
    negative nan unified to "nan"
  - Use faster strEQc macros from cperl with constant strings
  - Prefer memEQ for systems without memcmp, to use bcmp there
  - Add more expect_false() to inf/nan branches
  - expect_false() macro fix for MSVC
  - Fix av and hv length types: protect from security sensitive overflows, add
    HVMAX_T and RITER_T
  - Add new "Hash key too large" error; perl5 silently truncates it, we prefer
    errors
  - Fix broken 5.8.1 SvPOK_only, i.e. assert_not_ROK
  - Fix and document wrong strEQc usage in new() (GH#70)
  - Fix t/gh70-asan.t for older perls < 5.14
  - Fix DPPP_dummy_PL_parser warnings

* Sat Jun 18 2016 Paul Howarth <paul@city-fan.org> - 3.0217-1
- Update to 3.0217
  - Improve test t/20_unknown.t for older JSON::PP

* Mon Jun 13 2016 Paul Howarth <paul@city-fan.org> - 3.0216-1
- Update to 3.0216
  - Fix wrong test 117 for 5.10.0

* Sun Jun 12 2016 Paul Howarth <paul@city-fan.org> - 3.0215-1
- Update to 3.0215
  - Fix wrong test 117
  - TODO the fragile mojo boolean interop test
  - Improve error message with class-based method calls, when forgetting ->new
    (GH#66)

* Fri Jun  3 2016 Paul Howarth <paul@city-fan.org> - 3.0214-1
- Update to 3.0214
  - Preserve numbers as numbers, enforce an added .0; also note that 42+"bar"
    will result > 5.10 in numbers, not integers, ⇒ 42.0
  - 5.6 compilation fixes
  - Add yaml-tiny formats to cpanel_json_xs
  - Remove author-only Pod::Usage dependency
  - Fix an off-by-one IV_MIN -> NV overflow in decode_json (GH#67)
  - Avoid encode_sv SEGV with -Dusequadmath (GH#62)
  - Fix quadmath NV stringification
- Simplify find commands using -empty and -delete
- BR: perl-generators where available

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.0213-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.0213-2
- Perl 5.24 rebuild

* Wed Mar  2 2016 Paul Howarth <paul@city-fan.org> - 3.0213-1
- Update to 3.0213
  - Silence JSON::PP::Boolean redefine warnings (GH#60)

* Sat Feb 27 2016 Paul Howarth <paul@city-fan.org> - 3.0212-1
- Update to 3.0212
  - Merge with JSON-XS-3.02:
    - docs: add some INTEROP, stricter nonref RFC 7159 and TAGGED VALUE
      SYNTAX AND STANDARD JSON EN/DECODERS paragraphs
    - Use 7159 nonref detection from JSON-XS: json_nonref()
    - Add some SAVESTACK_POS calls
    - Add -f cbor decode option (via CBOR::XS) to cpanel_json_xs
  - Fixed many spelling errors in the new docs
  - Fixed errors with threaded perls
  - Improved code quality in new merged code and fixed new warnings found with
    gcc-5
  - Add -f and -t yaml-xs and yaml-syck options to cpanel_json_xs
- Soften optional script dependencies to Suggests: if we have rpm ≥ 4.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Paul Howarth <paul@city-fan.org> - 3.0211-1
- Update to 3.0211
  - Relax Mojo interop test strictness ('' or 0 for false)
  - t/z_pod.t as author test
  - t/z_kwalitee.t accepts now RELEASE_TESTING
  - Fix mingw64 inf/nan with uselongdouble, strawberry 5.22.1 (GH#57)

* Thu Dec  3 2015 Paul Howarth <paul@city-fan.org> - 3.0210-1
- Update to 3.0210
  - Fix nasty regression bug with allow_singlequote or relaxed, hanging with
    single quotes in normal strings (GH#54)
  - Improve cpanel_json_xs: more input and output formats
  - Improved various spellings and add test
  - Much faster t/99_binary.t test

* Thu Dec  3 2015 Paul Howarth <paul@city-fan.org> - 3.0208-1
- Update to 3.0208
  - Fix regression decoding big strings (>16384) (GH#50)
  - Ignore allow_barekey if we detect quotes (GH#51)
  - Skip some unicode tests with 5.6
  - Fix regression for is_bool([]), with unblessed references (GH#53)

* Tue Dec  1 2015 Paul Howarth <paul@city-fan.org> - 3.0206-1
- Update to 3.0206
  - Add support for escape_slash from JSON::PP (GH#47)
  - Map sort_by to canonical from JSON::PP (GH#47); reverse sort or sort by
    custom keys not yet possible/silently ignored
  - Add support for allow_singlequote from JSON::PP (GH#47)
  - Add support for allow_barekey from JSON::PP (GH#47)
  - Add support for allow_bignum from JSON::PP (GH#47)
  - relaxed uses now also allow_singlequote and allow_barekey
  - Fixed t/20_unknown.t: SKIP when JSON is not available (GH#45)
  - Fixed t/55_modifiable.t: Broaden the is check of true <5.12 (GH#45)
  - Add t/zero-mojibake.t from JSON::PP testing all supported decoding options:
    none, utf8, ascii, latin1, binary

* Mon Nov 30 2015 Paul Howarth <paul@city-fan.org> - 3.0205-1
- Update to 3.0205
  - Add t/20_unknown.t tests from JSON::PP, extended
  - Fix convert_blessed, disallow invalid JSON (GH#46); convert_blessed always
    now returns a string, even for numbers
  - Fix encountered GLOB error message (still in JSON::XS, and JSON::PP took
    over the wrong message too)
  - Fixed regression of immediate raw values for null/true/false to be
    modifiable again (GH#45, broken with 3.0201-3.0204)

* Fri Nov 27 2015 Paul Howarth <paul@city-fan.org> - 3.0204-1
- Update to 3.0204
  - Fix is_bool with JSON::XS >3.0 interop (GH#44)
- Avoid running signature tests as we fix shellbangs in example code

* Thu Nov 26 2015 Paul Howarth <paul@city-fan.org> - 3.0203-1
- Update to 3.0203
  - Simplify handling of references, removing all the complicated work-around
    for reblessing; breaks overloaded values, but fixes serialising refs to
    read-only values (GH#21); schmorp thinks that overloading is broken with
    this patch, but reblessing and breaking read-only is worse
  - Stabilize Test::Kwalitee with missing XS dependencies
  - Suggests common::sense, not recommend (GH#36)
  - Boolean interop: use only JSON::PP::Boolean (GH#40)
    - Remove our own JSON::XS::Boolean, and solely use JSON::PP::Boolean and
      accept Mojo::JSON::_Bool (GH#37) and Types::Serialiser::Boolean, which is
      aliased to JSON::PP::Boolean
    - JSON::YAJL::Parser just produces an unbless IV (0|1)
    - Fix overload of our bools
    - Stringify true to "true", false to "0"
    - Accept is_bool as method call also
  - Implement native encode_sv of the internal sv_yes/sv_no values (GH#39) and
    map them to json true/false (YAML::XS compatible)
  - pod: add SECURITY CONSIDERATIONS; added a table of safe and unsafe
    serializers for comparison (only JSON and Data::MessagePack are safe by
    default)
  - New feature: convert_blessed for encode; stringify overloaded perl objects
    and with allow_blessed even without string overload (GH#37)
  - New optional decode_json() argument to set allow_nonref as in RFC 7159 and
    PHP; before 3.02, JSON::XS and Cpanel::JSON::XS always allowed nonref
    values for decode_json due to an internal bug
  - With canonical only skip hash keys sorting for actually tied hashes (GH#42)
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0115-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.0115-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.0115-2
- Perl 5.22 rebuild

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 3.0115-1
- Update to 3.0115
  - Fix stack corruption when encoding nested objects with FREEZE method
    (GH#35)

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 3.0114-1
- Update to 3.0114
  - Fix bad powl() with Freebsd 10 -Duselongdouble; rather use strtold
    (GH#34, CPAN RT#101265)

* Thu Dec 18 2014 Paul Howarth <paul@city-fan.org> - 3.0113-1
- Update to 3.0113
  - Relax the tests for negative NaN in t/117_number.t, as BSDs also cannot
    deal with it (GH#33)

* Mon Dec 15 2014 Paul Howarth <paul@city-fan.org> - 3.0112-1
- Update to 3.0112
  - Change encode of numbers with dual-strings (int and float); integers and
    numbers are now not mishandled anymore by dual-vars' temporary string
    representations
  - Add t/117_numbers.t from JSON::PP (GH#10)
  - Change stringification of false and true to 0 and 1, matching upstream
    JSON and JSON::XS (GH#29); this didn't affect string comparisons, just e.g.
    print decode_json("false")
  - Tolerate literal ASCII TABs in strings in relaxed mode (GH#22) (from
    JSON::XS)
  - Revise pod, merge updates from JSON::XS
  - Fix pod typo (PR#30)
  - Fixed detecting 1.#INF/1.#IND on Windows (GH#28)
  - Also detect now -inf and -nan (GH#28)
  - Fixed STRINGIFY_INFNAN return string, length off by one (GH#28)
  - Fixed a non-C99 declaration error in XS.xs, broken with older MSVC
  - Add {get_,}stringify_infnan methods and use it in the test, now run-time
    (GH#32); mode 0: null, 1: stringify, 2: inf/nan (invalid JSON) as before
  - Fix t/117_number tests for Solaris and MSWin32
  - Improve docs
- Add patch to make NaN encoding tests TODO (GH#33)

* Fri Nov 28 2014 Paul Howarth <paul@city-fan.org> - 3.0107-1
- Update to 3.0107
  - Fix fatal stack corruption with perl callbacks in list context (GH#27)

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 3.0106-1
- Update to 3.0106
  - More minor doc improvements (GH#26)

* Thu Nov  6 2014 Paul Howarth <paul@city-fan.org> - 3.0105-1
- Update to 3.0105
  - Minor doc improvements (GH#25)
  - Fix d_Gconvert test in t/11_pc_expo.t for 5.6
- Upstream no longer shipping SIGNATURE file
- Use %%license where possible

* Wed Oct 22 2014 Petr Pisar <ppisar@redhat.com> - 3.0104-5
- Break build cycles

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0104-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Paul Howarth <paul@city-fan.org> - 3.0104-1
- Update to 3.0104
  - Add t/z_leaktrace.t
  - Restore build on C89
  - Fix small cxt->sv_json leak on interp exit

* Tue Apr 22 2014 Paul Howarth <paul@city-fan.org> - 3.0103-1
- Update to 3.0103
  - Change booleans interop logic (again) for JSON-XS-3.01
    - Check now for Types::Serialiser::Boolean i.e. JSON::PP::Boolean refs
      (https://github.com/rurban/Cpanel-JSON-XS/issues/18) to avoid
      allow_blessed for JSON-XS-3.01 booleans
  - Fix boolean representation for JSON-XS-3.01/Types::Serialiser::Boolean
    interop (arrayref, not hashref)
  - Add t/52_object.t from JSON::XS
  - Backport encode_hv HE sort on stack < 64 or heap to avoid stack overflows
    from JSON-XS-3.01; do not use alloca
  - Backport allow_tags, decode_tag, FREEZE/THAW callbacks from JSON-XS-3.01
  - Added pod for OBJECT SERIALISATION (allow_tags, FREEZE/THAW)

* Thu Apr 17 2014 Paul Howarth <paul@city-fan.org> - 3.0102-1
- Update to 3.0102
  - Added PERL_NO_GET_CONTEXT for better performance on threaded Perls
  - MANIFEST: added t/96_interop.t
  - Document deprecated functions
  - Change booleans interop logic for JSON-XS-3.01
- Enable CLZF support via Compress::LZF

* Wed Apr 16 2014 Paul Howarth <paul@city-fan.org> - 3.0101-1
- Update to 3.0101
  - Added ithreads support: Cpanel::JSON::XS is now thread-safe
  - const'ed a translation table for memory savings
  - Fixed booleans for JSON 2.9 and JSON-XS-3.01 interop; JSON does not
    support JSON::XS booleans anymore, so I cannot think of any reason to
    still use JSON::XS

* Thu Apr 10 2014 Paul Howarth <paul@city-fan.org> - 2.3404-2
- Incorporate feedback from package review (#1085975)
  - Simplify %%summary
  - Temporarily drop Compress::LZF format support from cpanel_json_xs client
  - Add optional dependencies for module, tests and cpanel_json_xs client

* Wed Apr  9 2014 Paul Howarth <paul@city-fan.org> - 2.3404-1
- Initial RPM version
