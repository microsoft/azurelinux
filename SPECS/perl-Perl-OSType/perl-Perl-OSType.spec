# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional tests
%bcond_without perl_Perl_OSType_enables_optional_test

Name:		perl-Perl-OSType
Version:	1.010
Release:	521%{?dist}
Summary:	Map Perl operating system names to generic types
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Perl-OSType
Source0:	https://cpan.metacpan.org/modules/by-module/Perl/Perl-OSType-%{version}.tar.gz
Patch2:		Perl-OSType-1.010-stopwords.patch
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(constant)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More) >= 0.88
# Optional tests, not run for this dual-lived module when bootstrapping
# Also not run for EPEL builds due to package unavailability
%if !%{defined perl_bootstrap} && 0%{?fedora} && %{with perl_Perl_OSType_enables_optional_test}
BuildRequires:	glibc-langpack-en
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Pod::Wordlist)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling), hunspell-en
BuildRequires:	perl(Test::Version)
%endif
# Dependencies
# (none)

%description
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.

This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').

%prep
%setup -q -n Perl-OSType-%{version}

# More stopwords for the spell checker
%patch -P 2

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if !%{defined perl_bootstrap} && 0%{?fedora} && %{with perl_Perl_OSType_enables_optional_test}
LANG=en_US make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING.mkdn README
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::OSType.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-420
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov  7 2018 Paul Howarth <paul@city-fan.org> - 1.010-419
- Explicitly BR: glibc-langpack-en

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.010-393
- Perl 5.26 rebuild

* Wed Apr  5 2017 Paul Howarth <paul@city-fan.org> - 1.010-4
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - Drop workaround for building with Test::More < 0.88
  - Spell checker is always hunspell now
- Introduce build-condition for optional tests

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 1.010-2
- Use distribution instead of perl version to control build-time dependencies

* Wed Jun 22 2016 Paul Howarth <paul@city-fan.org> - 1.010-1
- Update to 1.010
  - Added 'msys' as a Unix-type OS
- BR: perl-generators where available
- Simplify find command using -delete
- Update patches as needed

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Paul Howarth <paul@city-fan.org> - 1.009-1
- Update to 1.009
  - Added 'sco' as a Unix-type OS
- Update patches as needed

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-2
- Perl 5.22 rebuild

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 1.008-1
- Update to 1.008
  - Added 'minix' as a Unix-type OS
- Use %%license where possible
- Update patch for building on old distributions

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Paul Howarth <paul@city-fan.org> - 1.007-1
- Update to 1.007
  - Added 'android' as a Unix-type OS
- Update stopwords patch

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 1.006-1
- Update to 1.006
  - Compile test could hang on Windows
  - Dropped configure_requires for ExtUtils::MakeMaker to 6.17

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.005-1
- Update to 1.005
  - Ensured no non-core test dependencies
  - Various non-functional changes to files and metadata included with
    the distribution
- Add patch with additional stopwords for the spell checker
- Reinstate EPEL support as we no longer require Capture::Tiny

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.004-1
- Update to 1.004
  - 'bitrig' is a Unix
- Specify all dependencies
- Drop EPEL-5/EPEL-6 support as they don't have Capture::Tiny
- Always use aspell for the spell check as Pod::Wordlist::hanekomu explicitly
  sets the speller to aspell

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.003-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.003-3
- Perl 5.18 rebuild

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 1.003-2
- Disable optional tests on RHEL 7 too

* Thu Mar 21 2013 Paul Howarth <paul@city-fan.org> - 1.003-1
- Update to 1.003
  - Fixed detection of VOS; $^O reports 'vos', not 'VOS'
  - Additional release tests
- BR: perl(File::Spec::Functions), perl(List::Util),
  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire),
  perl(Pod::Wordlist::hanekomu), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic), perl(Test::Spelling) and perl(Test::Version)
- Identify purpose of each build requirement
- Update patches for building on old distributions
- Don't run extra tests for EPEL-5/6 builds

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-242
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 1.002-241
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't delete the extra tests when bootstrapping, but don't run them either

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.002-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.002-11
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.002-10
- Skip author tests on bootstrap

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.002-9
- Fedora 17 mass rebuild

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 1.002-8
- BR: perl(Pod::Coverage::TrustPod) unconditionally now that it's available in
  EPEL-4

* Tue Aug 16 2011 Marcela Maslanova <mmaslano@redhat.com> - 1.002-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.002-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-3
- BR: perl(constant), perl(Exporter), perl(File::Temp) in case they are
  dual-lived at some point (#672801)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.002-1
- Initial RPM version
