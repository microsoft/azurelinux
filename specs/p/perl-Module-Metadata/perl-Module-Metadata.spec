# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Module-Metadata
Version:	1.000038
Release: 521%{?dist}
Summary:	Gather package and POD information from perl module files
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Module-Metadata
Source0:	https://cpan.metacpan.org/modules/by-module/Module/Module-Metadata-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(version) >= 0.87
BuildRequires:	perl(warnings)
# Regular test suite
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(vars)
# Optional test requirements
BuildRequires:	perl(CPAN::Meta) >= 2.120900
# Dependencies
Requires:	perl(Encode)
Requires:	perl(Fcntl)

%description
This module provides a standard way to gather metadata about a .pm file
without executing unsafe code.

%prep
%setup -q -n Module-Metadata-%{version}

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
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Metadata.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.000038-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.000038-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.000038-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.000038-2
- Perl 5.38 rebuild

* Fri Apr 28 2023 Paul Howarth <paul@city-fan.org> - 1.000038-1
- Update to 1.000038
  - Detects "class" syntax
- Use SPDX-format license tag

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.000037-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.000037-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.000037-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.000037-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep  9 2019 Paul Howarth <paul@city-fan.org> - 1.000037-1
- Update to 1.000037
  - Add decode_pod option for automatic =encoding handling

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.000036-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.000036-438
- Increase release to favour standalone package

* Fri Apr 19 2019 Paul Howarth <paul@city-fan.org> - 1.000036-1
- Update to 1.000036
  - Properly clean up temp dirs after testing

* Thu Apr 18 2019 Paul Howarth <paul@city-fan.org> - 1.000035-1
- Update to 1.000035
  - Fix how relative paths are absolutized, so they work properly on MSWin32
    (GH#24)
  - Quieten noisy tests (GH#31)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.000033-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.000033-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.000033-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.000033-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.000033-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.000033-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.000033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jul 25 2016 Paul Howarth <paul@city-fan.org> - 1.000033-1
- Update to 1.000033
  - Use a more strict matching heuristic when attempting to infer the "primary"
    module name in a parsed .pm file
  - Only report "main" as the module name if code was seen outside another
    namespace, fixing bad results for pod files (CPAN RT#107525)
  - Fix file operation in tests for VMS
- BR: perl-generators
- Simplify find command using -delete

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.000031-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.000031-1
- 1.000031 bump; Used trial version to compete with Perl 5.24
  - Refactor and expand test cases
  - Fix a $VERSION extraction issue on perl 5.6.2 (CPAN RT#105978, PR#17)
  - Fix the detection of package Foo when $Foo::VERSION is set (CPAN RT#85961)
  - Fix missing "use" statement in refactored test helper (only affected older
    perls, due to other module interactions)
  - Temporary directories cleaned up during tests
  - More accurately mark tests as TODO, so as to have a quieter and less
    confusing test run without passing TODO tests
  - Be less noisy on failure when building as part of perl core (see
    Perl RT#126685)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.000027-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000027-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.000027-2
- Perl 5.22 rebuild

* Sat Apr 11 2015 Paul Howarth <paul@city-fan.org> - 1.000027-1
- Update to 1.000027
  - Work around issues with an unconfigured Log::Contextual
  - Allow tests to pass in a perl with no taint support

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 1.000026-1
- Update to 1.000026
  - Patched tests to be less noisy in blead builds (CPAN RT#101491)

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 1.000025-1
- Update to 1.000025
  - Evaluate version assignment in a clean environment, to fix assignment in a
    block (CPAN RT#101095)
- Use %%license

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.000024-2
- Perl 5.20 rebuild

* Tue Jun 10 2014 Paul Howarth <paul@city-fan.org> - 1.000024-1
- Update to 1.000024
  - Support installations on older perls with an ExtUtils::MakeMaker earlier
    than 6.63_03
- Don't bother trying to run the release tests
- Package new documentation files from upstream: CONTRIBUTING LICENSE README.md

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Paul Howarth <paul@city-fan.org> - 1.000022-1
- Update to 1.000022
  - New is_indexable() object method (CPAN RT#84357)
  - Eliminated dependency on IO::File (and by virtue, XS)
  - Removed cruft in test infrastructure left behind from separation from
    Module::Build
  - Repository moved to https://github.com/Perl-Toolchain-Gang/Module-Metadata
  - .pm file is now wholly ascii, for nicer fatpacking (CPAN RT#95086)
  - Some code micro-optimizations
    (https://github.com/Perl-Toolchain-Gang/Module-Metadata/pull/4)
  - Fixed all out of date prereq declarations
  - Work around change in comparison behaviour in Test::More 0.95_01 by being
    more explicit with our tests - now explicitly checking the string form of
    the extracted version, rather than the entire version object
  - Ensure the extracted version is returned as a version object in all cases
    (CPAN RT#87782)
- Drop redundant Group: tag

* Sun Oct  6 2013 Paul Howarth <paul@city-fan.org> - 1.000019-1
- Update to 1.000019
  - Warnings now disabled inside during the evaluation of generated version sub
    (CPAN RT#89282)
- BR: perl(Config), perl(File::Basename) and perl(IO::File) for the test suite

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000018-1
- Update to 1.000018
  - Re-release of de-tainting fix without unstated non-core test dependencies
- Drop BR: perl(Test::Fatal)

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000017-1
- Update to 1.000017
  - De-taint version, if needed (CPAN RT#88576)
- BR: perl(Test::Fatal)

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.000016-1
- Update to 1.000016
  - Re-release to fix prereqs and other metadata
- This release by ETHER -> update source URL
- Specify all dependencies

* Wed Aug 21 2013 Paul Howarth <paul@city-fan.org> - 1.000015-1
- Update to 1.000015
  - Change wording about safety/security to satisfy CVE-2013-1437

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.000014-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.000014-2
- Perl 5.18 rebuild

* Thu May  9 2013 Paul Howarth <paul@city-fan.org> - 1.000014-1
- Update to 1.000014
  - Fix reliance on recent Test::Builder
  - Make tests perl 5.6 compatible
- This release by BOBTFISH -> update source URL

* Sun May  5 2013 Paul Howarth <paul@city-fan.org> - 1.000012-1
- Update to 1.000012
  - Improved package detection heuristics
  - Fix ->contains_pod (CPAN RT#84932)
  - Fix detection of pod after __END__ (CPAN RT#79656)
- This release by ETHER -> update source URL
- Package new upstream README file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 1.000011-1
- Update to 1.000011
  - Fix various warning messages
- This release by APEIRON -> update source URL

* Mon Jul 30 2012 Paul Howarth <paul@city-fan.org> - 1.000010-1
- Update to 1.000010
  - Performance improvement: the creation of a Module::Metadata object
    for a typical module file has been sped up by about 40%%
  - Fix t/metadata.t failure under Cygwin
  - Portability fix-ups for new_from_module() and test failures on VMS
- This release by VPIT -> update source URL
- Drop buildreqs for Perl core modules that aren't dual-lived
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-2
- Skip optional POD tests on bootstrap

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 1.000009-1
- Update to 1.000009
  - Adds 'provides' method to generate a CPAN META provides data structure
    correctly; use of package_versions_from_directory is discouraged
  - Fatal errors now use 'croak' instead of 'die'; Carp added as
    prerequisite
- Improve %%description
- Include all buildreqs explicitly required and classify them by Build,
  Module, Regular test suite, and Release tests
- Run main test suite and release tests separately
- Drop explicit versioned runtime dependency on perl(version) as no supported
  release now requires it

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.000007-2
- Fedora 17 mass rebuild

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 1.000007-1
- Update to 1.000007
  - Apply VMS fixes backported from blead

* Sun Sep  4 2011 Paul Howarth <paul@city-fan.org> - 1.000006-1
- Update to 1.000006
  - Support PACKAGE BLOCK syntax

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.000005-1
- Update to 1.000005
  - Localize $package::VERSION during version discovery
  - Fix references to Module::Build::ModuleInfo (CPAN RT#66133)
  - Added 'new_from_handle()' method (CPAN RT#68875)
  - Improved documentation (SYNOPSIS, broke out class/object method, and
    other minor edits)
- Install to vendor directories rather than perl directories

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 1.000004-5
- Bump and rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.000004-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-2
- Tweaks from package review (#672779)
  - Explicitly duplicate %%summary in %%description as upstream provides
    nothing particularly useful
  - Drop redundant BuildRoot tag
  - Add BuildRequires for possibly dual-lived perl modules:
    Cwd Data::Dumper Exporter File::Path File::Spec File::Temp IO::File
- Explicitly require perl(version) >= 0.87 for builds on OS releases older
  than Fedora 15 where the versioned dependency isn't picked up automatically

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-1
- Update to 1.000004
  - Fix broken metadata.t when @INC has relative paths

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.000003-2
- Sanitize for Fedora submission
- Drop support for releases prior to F-15 due to needing perl(version) >= 0.87

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.000003-1
- Initial RPM version
