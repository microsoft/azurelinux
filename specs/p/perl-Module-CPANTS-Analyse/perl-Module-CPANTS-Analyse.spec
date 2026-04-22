# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Module-CPANTS-Analyse
Version:        1.02
Release: 7%{?dist}
Summary:        Generate Kwalitee ratings for a distribution
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-CPANTS-Analyse
Source0:        https://cpan.metacpan.org/modules/by-module/Module/Module-CPANTS-Analyse-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.58
BuildRequires:  perl(ExtUtils::MakeMaker::CPANfile) >= 0.08
# Module Runtime
BuildRequires:  perl(Archive::Any::Lite) >= 0.06
BuildRequires:  perl(Archive::Tar) >= 1.76
BuildRequires:  perl(Array::Diff) >= 0.04
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Accessor) >= 0.19
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(CPAN::Meta::Converter)
BuildRequires:  perl(CPAN::Meta::Validator) >= 2.133380
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.008
BuildRequires:  perl(Data::Binary)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Find::Object) >= 0.2.1
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Module::CPANfile)
BuildRequires:  perl(Perl::PrereqScanner::NotQuiteLite) >= 0.9901
BuildRequires:  perl(Module::Find)
BuildRequires:  perl(Parse::Distname)
BuildRequires:  perl(Software::License) >= 0.103012
BuildRequires:  perl(Software::LicenseUtils)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Balanced)
BuildRequires:  perl(version) >= 0.73
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies
Requires:       perl(Archive::Any::Lite) >= 0.06
Requires:       perl(Archive::Tar) >= 1.76
Requires:       perl(Array::Diff) >= 0.04
Requires:       perl(Class::Accessor) >= 0.19
Requires:       perl(CPAN::Meta::Validator) >= 2.133380
Requires:       perl(CPAN::Meta::YAML) >= 0.008
Requires:       perl(Exporter)
Requires:       perl(File::Find::Object) >= 0.2.1
Requires:       perl(JSON::PP)
Requires:       perl(Module::CPANfile)
Requires:       perl(Software::License) >= 0.103012
Requires:       perl(version) >= 0.73

# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Archive::Any::Lite\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Array::Diff\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Class::Accessor\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::Validator\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\)$
%global __requires_exclude %__requires_exclude|^perl\\(File::Find::Object\\)$
%global __requires_exclude %__requires_exclude|^perl\\(version\\)$

%description
CPANTS is an acronym for CPAN Testing Service. The goals of the CPANTS project
are to provide some sort of quality measure (called "Kwalitee") and lots of
metadata for all distributions on CPAN.

%prep
%setup -q -n Module-CPANTS-Analyse-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc AUTHORS Changes README.md TODO
%dir %{perl_vendorlib}/Module/
%dir %{perl_vendorlib}/Module/CPANTS/
%{perl_vendorlib}/Module/CPANTS/Analyse.pm
%{perl_vendorlib}/Module/CPANTS/Kwalitee.pm
%dir %{perl_vendorlib}/Module/CPANTS/Kwalitee/
%{perl_vendorlib}/Module/CPANTS/Kwalitee/*.pm
%{_mandir}/man3/Module::CPANTS::Analyse.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::BrokenInstaller.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::CpantsErrors.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Distname.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Distros.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Files.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::FindModules.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::License.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Manifest.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::MetaYML.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::NeedsCompiler.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Pod.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Prereq.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Repackageable.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Signature.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Uses.3*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Version.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Paul Howarth <paul@city-fan.org> - 1.02-1
- Update to 1.02
  - Treat use v5.36 as use_warnings (GH#49)
  - Skip some of the manifest test if symlink is not available (GH#50)
  - Improve prereq sorting
  - Improve pod detection
  - Improve script detection
  - Use Parse::Distname to get a little more information from a distribution
    name
  - Dedupe possible licences
  - Add Object::Pad as use strict equivalent (GH#42)
  - Fix has_license_in_source_file for distributions that contain only a
    script under bin or scripts (GH#37)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Paul Howarth <paul@city-fan.org> - 1.01-1
- Update to 1.01
  - Fixed not to set an error message when extracted nicely
  - Fixed to restore mtime of MANIFEST.SKIP if it is modified by
    #include_default
  - Improved primary module detection
  - Fixed to catch CPAN::Meta::YAML's warnings (of duplicate keys)
  - Improved test_prereqs_match to handle t::lib::Util, and ignore files that
    contain but don't end with .t
  - Fixed to store multiple licenses in META files

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-2
- Perl 5.30 rebuild

* Mon Feb  4 2019 Paul Howarth <paul@city-fan.org> - 1.00-1
- Update to 1.00
  - Module::CPANTS::Kwalitee::Uses now uses a different prereq scanner
    (Perl::PrereqScanner::NotQuiteLite)
  - Added new kwalitee metrics:
    no_maniskip_error, no_missing_files_in_provides, no_files_to_be_skipped
  - Delayed plugin loading
- Upstream no longer ships the extra tests, so don't try to run them

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Paul Howarth <paul@city-fan.org> - 0.99-1
- Update to 0.99
  - Module::CPANTS::Kwalitee now uses Module::Find to find Kwalitee modules
    (instead of Module::Pluggable, which unconditionally spits a deprecation
    warning); you usually don't need to care but if you have your custom
    Kwalitee plugin loader (such as Module::CPANTS::SiteKwalitee), you need to
    change it - sorry for the inconvenience
  - Allow dash and dot in script name in the NAME section for
    non-pm, non-pod files
  - Added has_meta_json metric (CPAN RT#107885)
  - Accept a few more README extensions
  - Accept two more Moose modules as strict equivalents
  - Various micro optimization for performance
  - Dropped a few dependencies
  - Various documentation updates
  - Not to check use_strict/use_warnings for Perl 6 modules in a Perl 5
    distribution
  - Worked around a File::Find::Object issue
  - Fixed dynamic_config handling
  - Improved LICENSE file detection (CPAN RT#114247)
  - Skip everything in MANIFEST.SKIP while testing symlinks (GH#33)
- Simplify find command using -delete
- Add file xt/kwalitee/mas_meta_json.t missing from dist, needed for
  xt/kwalitee.t (GH#38)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.96-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.96-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.96-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.96-2
- Perl 5.22 rebuild

* Mon Nov 24 2014 Paul Howarth <paul@city-fan.org> - 0.96-1
- Update to 0.96
  - Added an import option to load extra Kwalitee plugins
  - has_readme now accepts README.pod as well (CPAN RT#100512)
  - Improved no_abstract_stub_in_pod to detect "The great new" as a boilerplate
  - Switched to File::Find::Object

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 0.95-2
- BR:/R: perl(Software::License::CC_BY_SA_3_0)

* Mon Sep 29 2014 Paul Howarth <paul@city-fan.org> - 0.95-1
- Update to 0.95
  - Added the following metrics:
    - has_abstract_in_pod
    - has_known_license_in_source_file
    - meta_json_conforms_to_known_spec
    - meta_json_is_parsable
    - meta_yml_has_repository_resource
    - no_abstract_stub_in_pod
  - Removed metayml_conforms_spec_current metric
  - Renamed metayml_ metrics to meta_yml_
  - Removed cpants_lint.pl in favor of App::CPANTS::Lint
  - Supported x_cpants custom META field to tell analyzer to ignore some of
    the metrics (only) when calculating a kwalitee score
  - Refactored several Kwalitee files, and internal stash layout has changed
    rather significantly; you might need to modify your tools if they happen
    to depend on the stash directly
  - Refactored tests
  - Fixed CPAN RT#94468 - use_strict metric doesn't like .pod files that
    contain no perl
  - Fixed CPAN RT#99141 - use_strict metric does not recognize "use v5.14"
    syntax
  - Fixed abstract encoding issues
  - Fixed not to ignore directory symlinks
  - Fixed CPAN RT#97858 - wrong no_symlinks test in files not in MANIFEST (for
    a local distribution; CPANTS site doesn't ignore symlinks not listed in
    MANIFEST)
  - Fixed CPAN RT#97601 - Test::Kwalitee incorrectly reports non-use of strict
    in Inline::CPP
  - Accept COPYING as a license file
  - Take included module (under inc/) into consideration while analyzing
    prereq_matches_use
  - Changed most of the META.yml metrics to pass if META.yml doesn't exist
  - Switched to Test::FailWarnings to make CPAN testers happier
- Classify buildreqs by usage
- Modernize spec

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.92-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 22 2013 Paul Howarth <paul@city-fan.org> - 0.92-1
- Update to 0.92 release
  - Fixed a case when more than one license section came in a row
  - Stopped checking auto_features

* Thu Sep  5 2013 Paul Howarth <paul@city-fan.org> - 0.91-1
- Update to 0.91 release
  - Add metrics no_dot_underscore_files, portable_filenames
  - Remove metrics distributed_by_debian, latest_version_distributed_by_debian,
    has_no_bugs_reported_in_debian, has_no_patches_in_debian, no_cpants_errors,
    uses_test_nowarnings, has_test_pod, has_test_pod_coverage, has_examples
  - Removed a few non-portable metrics for Test::Kwalitee
  - Numerous fixes for a smoother operation of www-cpants
  - Fixed CPAN RT#87535: incorrect version specification in 0.90_01
  - Fixed CPAN RT#87534: test failure in 0.90_01
  - Fixed CPAN RT#87561: t/11_hash_random.t fails due to undeclared test
    dependency
  - Fixed CPAN RT#69233: doesn't detect 'use' ≥ 5.012 as 'use strict'
  - Fixed CPAN RT#83336: fails to detect strict via 'use MooseX::Types'
  - Fixed CPAN RT#83851: 'use v5.16' and greater not deemed "strict"
  - Fixed CPAN RT#86504: fix sort order of Kwalitee generators
  - Fixed CPAN RT#87155: more Module::Install tests needed (1.04 is broken)
  - Fixed CPAN RT#87597: proper_libs is a dubious test
  - Fixed CPAN RT#87598: can't use an undefined value as an ARRAY reference at
    .../FindModules.pm line 115
  - Fixed CPAN RT#87988: fix use of $Test::Kwalitee::VERSION
  - Fixed CPAN RT#88216: extracts_nicely metric fails for -TRIAL releases
  - Fixed CPAN RT#88365: YAML/JSON tests are not failing when improperly
    encoded characters are seen
  - Moose::Exporter also provides strict and warnings
- Don't run the author test (Perl::Critic) as it would fail anyway
- Module no longer checks signatures, so drop all related hacks
- No longer need to fix line endings

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.89-3
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug  2 2013 Paul Howarth <paul@city-fan.org> - 0.89-1
- Update to 0.89 release
  - Additional tests
- This release by ISHIGAKI -> update source URL
- BR: perl(Data::Dump) for the test suite

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.87-2
- Perl 5.18 rebuild

* Mon Feb 25 2013 Paul Howarth <paul@city-fan.org> - 0.87-1
- Update to 0.87 release
  - Fix test failures due to Test::CPAN::Meta::YAML::Version interface change
    (CPAN RT#80225)
  - Fix failure in 10_analyse.t due to hash randomization (CPAN RT#82939)
  - Module::CPANTS::Kwalitee::Manifest was broken for MANIFESTs containing
    files with spaces (CPAN RT#44796)
- Bump version requirements for Module::ExtractUse and
  Test::CPAN::Meta::YAML::Version as per upstream

* Fri Feb 22 2013 Daniel P. Berrange <berrange@redhat.com> - 0.86-6
- Fix test suite for newer metayml spec (rhbz #914299)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.86-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.86-2
- Perl 5.16 rebuild

* Mon May 28 2012 Paul Howarth <paul@city-fan.org> - 0.86-1
- Update to 0.86 release
  - Add several strict and warnings equivalents and make it easy to add more
  - Fix when Moose is used and strict is not used
  - Add info about MIN_PERL_VERSION
  - Better remedy for metayml_declares_perl_version
  - metayml_declares_perl_version moved from experimental to extra
  - Some pod improvements
  - Fix CPAN RT#65903 - no more Test::YAML::Meta::Version on CPAN
  - Replace YAML::Syck with YAML::Any
  - no_symlinks checks only files in MANIFEST, use "maniread" in
    ExtUtils::Manifest
  - Add more equivalents for use_strict and use_warnings tests
  - Implement valid_signature metric
- This release by DAXIM -> update source URL
- Drop patch for Test::CPAN::Meta::YAML::Version, no longer needed
- Bump module version requirements:
  - perl(Archive::Tar) => 1.48
  - perl(Software::License) => 0.003
  - perl(Test::Warn) => 0.11
  - perl(Text::CSV_XS) => 0.45
- Switch to ExtUtils::MakeMaker flow so we don't need Module::Build ≥ 0.40
- BR: perl(Cwd), perl(ExtUtils::Manifest), perl(File::chdir),
  perl(Module::Signature), perl(Set::Scalar) and perl(Test::Pod::Coverage)
- BR: perl(YAML::Any) rather than perl(YAML::Syck)
- Drop perl(Test::CPAN::Meta::YAML::Version) version requirement

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.85-11
- Fix line endings of cpants_lint.pl script and documentation
- Run the author tests too
- BR: perl(Perl::Critic) except when bootstrapping
- BR: perl(Test::CPAN::Meta::YAML::Version) rather than
  perl(Test::CPAN::Meta::YAML)
- Don't BR: perl(Test::Pod::Coverage) due to presence of naked subroutines
- Sort buildreqs for readability
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.85-9
- Patch to use Test::CPAN::Meta::YAML instead of Test::YAML::Meta

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.85-9
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.85-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.85-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.85-5
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.85-4
- Fix source URL

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.85-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.85-1
- Update to 0.85 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-2
- Added more new & missing BRs

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-1
- Update to 0.82 release

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.75-3
- rebuild for new perl

* Wed Dec 26 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-2.fc9
- Added Test::Deep, Test::Pod, Test::Pod::Coverage build requires

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-1.fc9
- Specfile autogenerated by cpanspec 1.73.
