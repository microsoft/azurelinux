# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%bcond_without perl_JSON_PP_enables_optional_test

Name:		perl-JSON-PP
Epoch:		1
Version:	4.16
Release: 523%{?dist}
Summary:	JSON::XS compatible pure-Perl module
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/JSON-PP
Source0:	https://cpan.metacpan.org/modules/by-module/JSON/JSON-PP-%{version}.tar.gz
Patch0:		https://patch-diff.githubusercontent.com/raw/makamaka/JSON-PP/pull/93.patch
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(lib)
# Module Runtime
BuildRequires:	perl(bytes)
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Math::BigFloat)
BuildRequires:	perl(Math::BigInt)
BuildRequires:	perl(overload)
BuildRequires:	perl(Scalar::Util) >= 1.08
BuildRequires:	perl(strict)
BuildRequires:	perl(utf8)
BuildRequires:	perl(warnings)
# Script Runtime
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Getopt::Long)
# Test Suite
BuildRequires:	perl(charnames)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Tie::Array)
BuildRequires:	perl(Tie::Hash)
BuildRequires:	perl(vars)
# Optional Tests
%if %{with perl_JSON_PP_enables_optional_test}
# Note: t/rt_122270_old_xs_boolean.t is testing for compatibility with old
# versions of JSON:XS and Types::Serialiser that we no longer use, so we
# don't include those modules as optional test dependencies
%if !%{defined perl_bootstrap}
# Disable non-core dependencies when bootstrapping a core module
BuildRequires:	perl(Tie::IxHash)
%endif
%endif
# Dependencies
Requires:	perl(Data::Dumper)
Requires:	perl(Encode)
Requires:	perl(Math::BigFloat)
Requires:	perl(Math::BigInt)
Requires:	perl(Scalar::Util) >= 1.08
Requires:	perl(utf8)
Conflicts:	perl-JSON < 2.50

%description
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.

JSON::PP is a pure-Perl module and is compatible with JSON::XS.

%prep
%setup -q -n JSON-PP-%{version}

# Silence Getopt::Long warning (fix already committed upstream)
# https://bugzilla.redhat.com/show_bug.cgi?id=2417867
# https://src.fedoraproject.org/rpms/perl-JSON-PP/pull-request/1
# https://github.com/makamaka/JSON-PP/issues/88
# https://github.com/makamaka/JSON-PP/pull/93
%patch -P0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{_bindir}/json_pp
%{perl_vendorlib}/JSON/
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON::PP.3*
%{_mandir}/man3/JSON::PP::Boolean.3*

%changelog
* Tue Dec 23 2025 Paul Howarth <paul@city-fan.org> - 1:4.16-522
- Silence Getopt::Long warning (rhbz#2417867, PR#1, GH#88, GH#93)
- Use %%{make_build} and %%{make_install}

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.16-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 Paul Howarth <paul@city-fan.org> - 1:4.16-1
- Update to 4.16
  - Drop support for perls < 5.8 (GH#84)

* Tue Dec 27 2022 Paul Howarth <paul@city-fan.org> - 1:4.15-1
- Update to 4.15
  - Fix core bool test to not ignore errors (GH#82)

* Mon Dec 26 2022 Paul Howarth <paul@city-fan.org> - 1:4.14-1
- Update to 4.14
  - Break up 099_binary.t into 16 pieces that can be tested in parallel (GH#80)

* Mon Oct 10 2022 Paul Howarth <paul@city-fan.org> - 1:4.12-1
- Update to 4.12
  - Call unimport overload first to silence warnings (GH#76)
- Use SPDX-format license tag

* Sun Jul 31 2022 Paul Howarth <paul@city-fan.org> - 1:4.11-1
- Update to 4.11
  - Restored core boolean support (GH#73, GH#74)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Paul Howarth <paul@city-fan.org> - 1:4.10-1
- Update to 4.10
  - Fix a regression of decode_error introduced at 4.08 (GH#75)
  - Convert all tests to use Test::More (GH#70)

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.09-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.09-2
- Perl 5.36 rebuild

* Sun May 22 2022 Paul Howarth <paul@city-fan.org> - 1:4.09-1
- Update to 4.09
  - Reverted core boolean support for now (GH#72)
  - Fix incr_parse() hanging on certain inputs (GH#67)
  - Silence warnings about non-characters on older perls (GH#68)

* Mon Apr 11 2022 Paul Howarth <paul@city-fan.org> - 1:4.08-1
- Update to 4.08
  - Remove unneeded utf8::upgrade and downgrade (GH#59)
  - Core boolean support (GH#62, GH#63)
  - EBCDIC support (GH#64)
  - Shorten a test name (GH#65)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 18 2021 Paul Howarth <paul@city-fan.org> - 1:4.07-1
- Update to 4.07
  - Fix incr_parse($unicode_str) bug (GH#56)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.06-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.06-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.06-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Paul Howarth <paul@city-fan.org> - 1:4.06-1
- Update to 4.06
  - Fix return values of boolean_values for compatibility

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  9 2020 Paul Howarth <paul@city-fan.org> - 1:4.05-1
- Update to 4.05
  - No code changes
  - Modify tests for Perl 7

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.04-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.04-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Paul Howarth <paul@city-fan.org> - 1:4.04-1
- Update to 4.04
  - Document indent_length option (GH#48)

* Wed Jun 19 2019 Paul Howarth <paul@city-fan.org> - 1:4.03-1
- Update to 4.03
  - (Encode::)decode json_pp input properly by default (GH#47)

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.02-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.02-438
- Increase release to favour standalone package

* Sat Feb 23 2019 Paul Howarth <paul@city-fan.org> - 1:4.02-1
- Update to 4.02
  - Fix a test that breaks if perl is compiled with -Dquadmath (CPAN RT#128589)

* Fri Feb 22 2019 Paul Howarth <paul@city-fan.org> - 1:4.01-1
- Update to 4.01
  - Allow to pass indent_length to json_pp (GH#46)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec  7 2018 Paul Howarth <paul@city-fan.org> - 1:4.00-1
- Update to 4.00
  - BACKWARD INCOMPATIBILITY: As JSON::XS 4.0 changed its policy and enabled
    allow_nonref by default, JSON::PP also enabled allow_nonref by default
  - Implement allow_tags that was introduced by JSON::XS 3.0
  - Add boolean_values that was introduced by JSON::XS 4.0
  - Allow literal tags in strings in relaxed mode, as JSON::XS 3.02 does
  - Allow PERL_JSON_PP_USE_B environmental variable to restore old number
    detection behavior for compatibility
  - Various documentation updates
- Drop provides filter, no longer needed

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.97.001-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.97.001-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.97.001-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.97.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Paul Howarth <paul@city-fan.org> - 1:2.97.001-1
- Update to 2.97001
  - Tweak internal number detector always to consider a flagged value as a
    string (GH#35)
  - Clarify json_pp options (CPAN RT#123766)

* Tue Nov 21 2017 Paul Howarth <paul@city-fan.org> - 1:2.97-1
- Update to 2.97000
  - Fix is_bool to use blessed() instead of ref()
  - Use 5 digit minor version number for a while to avoid confusion (GH#33)
- Stick to 2 digit minor version downstream as we already bumped epoch

* Mon Nov 20 2017 Paul Howarth <paul@city-fan.org> - 1:2.96-1
- Update to 2.96
  - json_pp now prints an encoded json string (CPAN RT#123653)
  - Fix is_bool to use ->isa("JSON::PP::Boolean"), instead of
    UNIVERSAL::isa("JSON::PP::Boolean") (GH#34)
  - Avoid use of newer Test::More features (CPAN RT#122421)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.94-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.94-2
- Perl 5.26 rebuild

* Mon May 29 2017 Paul Howarth <paul@city-fan.org> - 2.94000-1
- Update to 2.94
  - Fix a test to support perl 5.6

* Wed May 17 2017 Paul Howarth <paul@city-fan.org> - 2.93000-1
- Update to 2.93
  - Changed the number detection logic (experimental)
  - Correct 0 handling (GH#23)
  - Removed base.pm dependency (GH#5)
  - Fixed wrong character offset (CPAN RT#116998)
  - Address VAX issues (CPAN RT#118469)
  - Various documentation fixes
  - Remove . in @INC in json_pp (GH#25, CVE-2016-1238)
  - Removed $VAR1 from json_pp output (GH#11)
  - Fixed an issue to ignore trailing 0 (GH#29)
  - Added Scalar::Util dependency for Perl 5.8+ (CPAN RT#84347)
  - Fixed issues spotted by Nicolas Seriot's JSON Test Suite including
    experimental UTF-16/32 support and backward incompatible change of
    C style comment handling (now disabled by default) (GH#28)
  - Moved the guts of JSON::PP::Boolean into lib/JSON/PP/Boolean.pm and gave
    it a proper version
  - Refactored incremental parser to let it handle incomplete JSON text
    properly
  - Imported and tweaked tests from JSON.pm
  - Minor code clean up
  - Fixed not to fail tests under Perl 5.25.* (CPAN RT#119114)
  - Reworked documentation, based on the one for JSON::XS
  - Let json_pp utility show the version of JSON::PP
  - Fix loading order of B module (GH#31)
  - Fixed isa tests for bignum
- This release by ISHIGAKI → update source URL
- Use five-digit version number for rpm to maintain upgrade path
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27400-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.27400-4
- Avoid loading optional modules from default . (CVE-2016-1238)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.27400-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.27400-2
- Perl 5.24 rebuild

* Mon Apr 25 2016 Paul Howarth <paul@city-fan.org> - 2.27400-1
- Update to 2.27400
  - Applied and merged long term neglected patches and pull requests
  - Modified Makefile.PL to set UNINST=1 if needed on old perls
  - Decode decimals to Perl's internal NV type
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.27300-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27300-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.27300-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.27300-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.27300-3
- Perl 5.22 rebuild

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 2.27300-2
- Disable non-core dependencies when bootstraping a core module

* Wed Oct  8 2014 Paul Howarth <paul@city-fan.org> - 2.27300-1
- Update to 2.27300
  - Fixed a problem about substr in perl 5.8.6 and below
- Classify buildreqs by usage

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.27203-310
- Increase release to favour standalone package

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.27203-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 2.27203-1
- Update to 2.27203
  - Fixed return/or in _incr_parse (CPAN RT#86948)
- Specify all dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27202-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.27202-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.27202-2
- Perl 5.18 rebuild

* Wed Mar 13 2013 Paul Howarth <paul@city-fan.org> - 2.27202-1
- Update to 2.27202
  - Fix test failures due to hash iterator randomization in perl 5.17.6 onwards
    (CPAN RT#83421)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27200-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 2.27200-242
- Correct the URL
- Add a few missing buildtime dependencies
- Drop Getopt::Long dep; json_pp isn't tested

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 2.27200-241
- BR: perl(base), perl(constant) and perl(lib)
- Install to vendor directories
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27200-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-4
- Depend of Data::Dumper

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.27200-3
- Add buildreqs for perl core modules, which might be dual-lived

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.27200-2
- Perl mass rebuild

* Sun May 22 2011 Paul Howarth <paul@city-fan.org> - 2.27200-1
- Update to 2.27200
  - Fixed incr_parse decoding string more correctly (CPAN RT#68032)

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> - 2.27105-1
- Update to 2.27105
  - Removed t/900_pod.t from package because of author test
- Drop buildreq perl(Test::Pod), no longer needed

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> - 2.27104-3
- Conflict with perl-JSON < 2.50 (#672764)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 2.27104-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 2.27104-1
- Initial RPM version
