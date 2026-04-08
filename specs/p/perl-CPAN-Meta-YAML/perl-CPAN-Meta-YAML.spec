# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if 0%{!?perl_bootstrap:1}
%if ! (0%{?rhel})
%bcond_without perl_CPAN_Meta_YAML_enables_extra_test
%else
%bcond_with perl_CPAN_Meta_YAML_enables_extra_test
%endif
%else
# Don't run extra tests when bootstrapping as many of those
# tests' dependencies build-require this package
%global _without_perl_CPAN_Meta_YAML_enables_extra_test 1
%global _with_perl_CPAN_Meta_YAML_enables_extra_test 0
%endif

Name:		perl-CPAN-Meta-YAML
Version:	0.020
Release:	521%{?dist}
Summary:	Read and write a subset of YAML for CPAN Meta files
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/CPAN-Meta-YAML
Source0:	https://www.cpan.org/modules/by-module/CPAN/CPAN-Meta-YAML-%{version}.tar.gz
BuildArch:	noarch
# Build:
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime:
BuildRequires:	perl(B)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Tests:
BuildRequires:	perl(base)
# CPAN::Meta requires CPAN::Meta::YAML
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
%endif
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(IO::Dir)
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(lib)
BuildRequires:	perl(open)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(utf8)
BuildRequires:	perl(vars)
%if %{with perl_CPAN_Meta_YAML_enables_extra_test}
# Extra Tests:
BuildRequires:	perl(blib)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Version)
%endif
# Dependencies
Requires:	perl(Carp)
Requires:	perl(Fcntl)

%description
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.

%prep
%setup -q -n CPAN-Meta-YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 UNINST=0
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_CPAN_Meta_YAML_enables_extra_test}
make test TEST_FILES="xt/*/*.t"
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::YAML.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-519
- Increase release to favour standalone package

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.20
  - Generated from ETHER/YAML-Tiny-1.76.tar.gz

* Mon Dec 16 2024 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.19
  - Generated from ETHER/YAML-Tiny-1.75.tar.gz
- Use author-independent source URL
- Use %%{make_build} and %%{make_install}

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-488
- Increase release to favour standalone package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-477
- Increase release to favour standalone package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-416
- Increase release to favour standalone package

* Thu Mar 15 2018 Paul Howarth <paul@city-fan.org> - 0.018-397
- Simplify find command using -delete
- Drop legacy Group: tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-367
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Generated from ETHER/YAML-Tiny-1.69.tar.gz

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-2
- Perl 5.22 rebuild

* Tue May 19 2015 Paul Howarth <paul@city-fan.org> - 0.016-1
- Update to 0.016
  - Generated from ETHER/YAML-Tiny-1.67.tar.gz

* Tue Mar 17 2015 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Generated from ETHER/YAML-Tiny-1.66.tar.gz
- Use %%license

* Fri Jan 09 2015 Petr Pisar <ppisar@redhat.com> - 0.012-313
- Require undetected dependencies explicitly

* Fri Dec 12 2014 Petr Pisar <ppisar@redhat.com> - 0.012-312
- Remove unused build-time dependency on YAML

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-310
- Increase release to favour standalone package

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012:
  - Generated from ETHER/YAML-Tiny-1.61.tar.gz

* Fri Feb 14 2014 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011:
  - Generated from ETHER/YAML-Tiny-1.60.tar.gz
- Give up trying to support EPEL (test suite now requires Test::More 0.99)

* Mon Sep 23 2013 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010:
  - Generated from ETHER/YAML-Tiny-1.55.tar.gz
  - Makefile.PL will use UNINST=1 on old perls that might have an old version
    incorrectly installed into the core library path
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
- Drop redundant BRs: perl(Pod::Wordlist::hanekomu), perl(Test::Requires),
  perl(Test::Spelling) and aspell-en
- Add new test dependencies perl(IO::Handle) and perl(IPC::Open3)
- Build with UNINST=0 to avoid build failures as we can't remove the system
  version of the package when building an rpm for a new version
- Update patch for building with old Test::More, and add new patch to support
  building with Test::More < 0.94
- Don't run the extra tests in EPEL as we don't have Test::Version there

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.008-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.008-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-13
- Update dependencies

* Thu Oct 11 2012 Paul Howarth <paul@city-fan.org> - 0.008-12
- Never BR: perl(Test::Version) for EL builds as perl(version) is too old
  prior to EL-7 and this package is included in RHEL ≥ 7 but Test::Version
  is only in EPEL

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 0.008-11
- Restrict Test::Version optional test on RHEL to version 6 only

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.008-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.008-8
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.008-7
- Run the extra tests in a separate test run, and only when not bootstrapping
- Don't BR: perl(Test::Spelling) with RHEL ≥ 7 as we don't have the other
  dependencies needed do the spell check test

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-6
- Conditionalize dependency on aspell

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.008-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 0.008-4
- Disable author tests on bootstrap

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-3
- Data::Dumper is not really needed, dependencies must be fixed in YAML

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-2
- Don't BR: Pod::Wordlist::hanekomu for RHEL-7+ builds; RHEL package cannot
  have buildreq from EPEL
- Add missing Data::Dumper dependency

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008:
  - Generated from ADAMK/YAML-Tiny-1.51.tar.gz
  - Updated from YAML-Tiny to fix compatibility with older Scalar::Util
- Drop upstreamed patch for old Scalar::Util versions
- Don't need to remove empty directories from the buildroot

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007:
  - Documentation fix to replace missing abstract

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006:
  - Set back configure_requires prerequisite for ExtUtils::MakeMaker
    from 6.30 to 6.17
- BR: perl(Test::Requires)
- BR: perl(Test::Spelling), perl(Pod::Wordlist::hanekomu) and aspell-en to
  enable the spell checker test
- Drop patch for building with old ExtUtils::MakeMaker versions, no longer
  needed
- Drop support for soon-to-be-EOL RHEL-4:
  - Drop %%defattr, redundant since rpm 4.4
- Update patch for building with Test::More < 0.88

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.005-2
- Fedora 17 mass rebuild

* Tue Dec 13 2011 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005:
  - Fix documentation to clarify that users are responsible for UTF-8
    encoding/decoding

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004:
  - Generated from ADAMK/YAML-Tiny-1.50.tar.gz
- BR: perl(Test::Version) for additional test coverage
- Update patch for building with ExtUtils::MakeMaker < 6.30
- Add patch to support building with Test::More < 0.88
- Add patch to fix operation with Scalar::Util < 1.18

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> - 0.003-3
- Trim %%description (#672807)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 0.003-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
