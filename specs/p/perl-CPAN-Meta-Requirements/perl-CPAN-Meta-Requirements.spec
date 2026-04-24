# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional tests
%bcond_without perl_CPAN_Meta_Requirements_enables_optional_test

Name:           perl-CPAN-Meta-Requirements
Version:        2.143
Release: 14%{?dist}
Summary:        Set of version requirements for a CPAN dist
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/CPAN-Meta-Requirements
Source0:        https://cpan.metacpan.org/modules/by-module/CPAN/CPAN-Meta-Requirements-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(version) >= 0.88
BuildRequires:  perl(warnings)
# Test
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
# Extra Tests (not run when bootstrapping due to circular build dependencies)
%if !%{defined perl_bootstrap} && ! ( 0%{?rhel} ) && %{with perl_CPAN_Meta_Requirements_enables_optional_test}
%if 0%{?fedora} > 23 || 0%{?rhel} > 7
BuildRequires:  glibc-langpack-en
%endif
BuildRequires:  perl(blib)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:  perl(Perl::Critic::Policy::Miscellanea::RequireRcsKeywords)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Pod::Wordlist)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Spelling) >= 0.12, hunspell-en
BuildRequires:  perl(Test::Version) >= 1
%endif
# Dependencies
Requires:       perl(B)
Requires:       perl(version) >= 0.88

# Had a six-digit version in a previous life
%global six_digit_version %(LC_ALL=C; printf '%.6f' '%{version}')

# Provide the six-digit version of the module
%if "%{version}" != "%{six_digit_version}"
Provides:       perl(CPAN::Meta::Requirements) = %{six_digit_version}
%global __provides_exclude ^perl\\(CPAN::Meta::Requirements\\)
%endif

%description
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions. It
can be built up by adding more and more constraints, and it will reduce them
to the simplest representation.

Logically impossible constraints will be identified immediately by thrown
exceptions.

%prep
%setup -q -n CPAN-Meta-Requirements-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor UNINST=0
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test AUTHOR_TESTING=1
%if !%{defined perl_bootstrap} && ! ( 0%{?rhel} ) && %{with perl_CPAN_Meta_Requirements_enables_optional_test}
LANG=en_US make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING.mkdn README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::Requirements.3*
%{_mandir}/man3/CPAN::Meta::Requirements::Range.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-12
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-11
- Perl 5.42 rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-8
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-7
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.143-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-3
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.143-2
- Perl 5.38 rebuild

* Tue Jun 20 2023 Paul Howarth <paul@city-fan.org> - 2.143-1
- Update to 2.143 (rhbz#2216187)
  - Fix regression with implicit minimum value and multiple requirements (GH#38)
- Don't package perlcritic.rc

* Wed May 31 2023 Paul Howarth <paul@city-fan.org> - 2.142-2
- Fix regression with multiple version numbers
  (rhbz#2208279, GH#38)

* Tue May  9 2023 Paul Howarth <paul@city-fan.org> - 2.142-1
- Update to 2.142
  - confess() replaced with croak(): fewer stack traces
  - Broke the version range handling into the Range class
  - Note: this version now requires perl v5.10 rather than v5.6
- Use author-independent source URL

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-488
- Increase release to favour standalone package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-481
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-479
- Perl 5.34 re-rebuild of bootstrapped packages

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-477
- Increase release to favour standalone package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-393
- Perl 5.26 rebuild

* Thu Apr  6 2017 Paul Howarth <paul@city-fan.org> - 2.140-7
- Introduce build-condition for optional tests
- Simplify find command using -delete
- Switch to hunspell for spell check

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 2.140-5
- Do not use perl to compute Provides version

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.140-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.140-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Paul Howarth <paul@city-fan.org> - 2.140-1
- Update to 2.140
  - Added method for getting structured requirements
  - Skips impossible tests on Perls earlier than 5.8.0 (before v-string magic)
  - On Perls before 5.8.1, pad 1-part and 2-part literal v-strings to avoid old
    version.pm bugs with v-strings less than 3 characters
  - Protect internal _isa_version from non-refs that pass ->isa('version')
  - Much better error messages, explaining what conflicted and how
  - Repackage with fixed tests
  - Expanded dist.ini from author bundle to individual plugins

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.133-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.133-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.133-2
- Perl 5.22 rebuild

* Sun Feb 22 2015 Paul Howarth <paul@city-fan.org> - 2.133-1
- Update to 2.133
  - In fixing preservation of "0.00", some Module => 0 optimizations were lost;
    this restores those optimizations

* Fri Jan 23 2015 Paul Howarth <paul@city-fan.org> - 2.132-1
- Update to 2.132
  - Precision of version requirement "0.00" is preserved when merging
    requirements

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.131-1
- Update to 2.131
  - Merging Module => 0 into requirements is now optimized
  - Scalar::Utils removed as a prerequisite

* Thu Nov 20 2014 Paul Howarth <paul@city-fan.org> - 2.130-1
- Update to 2.130
  - from_string_hash can take optional constructor arguments
  - bad_version_hook callback gets module name as well as version string
  - undefined/empty versions given to from_string_hash or
    add_string_requirement now carp and are coerced to "0" instead of being
    fatal; this is more consistent with how the other requirement functions
    work
- Provide six-digit version in a more robust way

* Fri Nov 14 2014 Paul Howarth <paul@city-fan.org> - 2.129-1
- Update to 2.129
  - from_string_hash can now accept v-strings as hash values

* Thu Sep 18 2014 Petr Pisar <ppisar@redhat.com> - 2.128-1
- 2.128 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.126-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.126-2
- Perl 5.20 rebuild

* Thu Jul 31 2014 Paul Howarth <paul@city-fan.org> - 2.126-1
- Update to 2.126
  - Fixed compatibility with version.pm 0.77
  - Minor documentation fixes
  - Modernized distribution meta files
- Use %%license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Paul Howarth <paul@city-fan.org> - 2.125-1
- Update to 2.125
  - On Perls prior to v5.12, CPAN::Meta::Requirements will force UNINST=1 when
    necessary to remove stale copies from ExtUtils::MakeMaker
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
- README.PATCHING renamed to CONTRIBUTING
- Classify buildreqs by usage
- Add note about logically-impossible constraints to %%description

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.122-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.122-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.122-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.122-6
- Conditionalize Test::*

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.122-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.122-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com>
- Skip some tests on bootstrap

* Mon May 07 2012 Iain Arnell <iarnell@gmail.com> 2.122-1
- update to latest upstream version

* Tue Apr 03 2012 Iain Arnell <iarnell@gmail.com> 2.121-3
- provide perl(CPAN::Meta::Requirements) with six decimal places

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.121-2
- clean up spec following review
- run release/author tests too

* Sun Apr 01 2012 Iain Arnell <iarnell@gmail.com> 2.121-1
- Specfile autogenerated by cpanspec 1.79.
