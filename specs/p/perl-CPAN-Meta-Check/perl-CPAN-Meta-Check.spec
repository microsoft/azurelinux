# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_CPAN_Meta_Check_enables_extra_test
%else
%bcond_with perl_CPAN_Meta_Check_enables_extra_test
%endif

Name:		perl-CPAN-Meta-Check
Summary:	Verify requirements in a CPAN::Meta object
Version:	0.018
Release:	6%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/CPAN-Meta-Check
Source0:	https://cpan.metacpan.org/modules/by-module/CPAN/CPAN-Meta-Check-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:	perl(base)
BuildRequires:	perl(CPAN::Meta::Prereqs) >= 2.132830
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Module::Metadata) >= 1.000023
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test
BuildRequires:	perl(blib)
BuildRequires:	perl(CPAN::Meta) >= 2.120920
BuildRequires:	perl(Env)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(lib)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::More) >= 0.88
%if %{with perl_CPAN_Meta_Check_enables_extra_test} && !%{defined perl_bootstrap}
# Break a build cycle: perl-Pod-Coverage-TrustPod → perl-Pod-Eventual
# → perl-Mixin-Linewise → perl-Sub-Exporter → perl-Params-Util
# → perl-Config-AutoConf → perl-File-Slurper → perl-Test-Warnings
# → perl-CPAN-Meta-Check
# Extra tests
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
%endif
# Dependencies
# (none)

%description
This module verifies if requirements described in a CPAN::Meta object are
present.

%prep
%setup -q -n CPAN-Meta-Check-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_CPAN_Meta_Check_enables_extra_test} && !%{defined perl_bootstrap}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::Check.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Fix version requirement for CPAN::Meta::Prereqs
  - Move issue tracker to GitHub

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan  3 2023 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Use Module::Metadata for more accurate testing

* Tue Jan  3 2023 Paul Howarth <paul@city-fan.org> - 0.015-1
- Update to 0.015
  - Drop Test::Deep prereq
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-21
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-20
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-17
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-16
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Paul Howarth <paul@city-fan.org> - 0.014-14
- Spec clean-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Use %%{make_build} and %%{make_install}
  - Fix permissions of installed files

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-12
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 26 2016 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Undef versions are now passed through to CPAN::Meta::Requirements for the
    check, rather than failing with "Missing version" errors

* Thu Jul 21 2016 Paul Howarth <paul@city-fan.org> - 0.013-1
- Update to 0.013
  - Make tests more resilient against dev versions of dependencies
- BR: perl-generators
- Drop legacy Group: tag
- Take advantage of features in recent EU::MM to simplify flow

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012
  - Drop dependency on Exporter 5.57

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.22 rebuild

* Mon Mar 23 2015 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - Declare the minimum version required for the "merged_requirements"
    interface
- Explicitly run the extra tests

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Bump Module::Metadata prereq for $VERSION parsing (CPAN RT#101095)
  - Consistently require same version of CPAN::Meta::Requirements
- Use %%license

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-3
- Perl 5.20 rebuild

* Tue Jul  1 2014 Paul Howarth <paul@city-fan.org> - 0.009-2
- Always run the release tests (#1114859)

* Mon Jun 23 2014 Paul Howarth <paul@city-fan.org> - 0.009-1
- Update to 0.009
  - Various POD fixes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 17 2013 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Switch to using merged_requirements
  - Test Env instead of Carp for version overshoot (CPAN RT#89591)
  - Document $incdirs in the right function

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.007-3
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Swap conflicts test, as underscore versions broke it (CPAN RT#87438)

* Sat Jul 27 2013 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Fixed bad dereference during conflicts checking

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.005-3
- Perl 5.18 rebuild

* Wed May  1 2013 Paul Howarth <paul@city-fan.org> - 0.005-2
- Sanitize for Fedora submission

* Sat Apr 27 2013 Paul Howarth <paul@city-fan.org> - 0.005-1
- Initial RPM version
