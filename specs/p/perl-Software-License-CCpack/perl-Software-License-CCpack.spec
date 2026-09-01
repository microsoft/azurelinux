# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#TODO: BR: perl(Test::CheckManifest) ≥ 1.24 when available

# Run extra tests
%if ! (0%{?rhel})
%bcond_without perl_Software_License_CCpack_enables_extra_tests
%else
%bcond_with perl_Software_License_CCpack_enables_extra_tests
%endif

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

# Similarly, for package note feature
%undefine _package_note_file

Name:		perl-Software-License-CCpack
Version:	1.11
Release:	41%{?dist}
Summary:	Software::License pack for Creative Commons' licenses
License:	LGPL-3.0-only
URL:		https://metacpan.org/release/Software-License-CCpack
Source0:	https://cpan.metacpan.org/authors/id/B/BB/BBYRD/Software-License-CCpack-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Software::License)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::CheckDeps) >= 0.010
BuildRequires:	perl(Test::More) >= 0.96
# Extra Tests
%if 0%{!?perl_bootstrap:1} && %{with perl_Software_License_CCpack_enables_extra_tests}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Mojibake)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
%if 0%{?fedora} < 39 && 0%{?rhel} < 10
BuildRequires:	perl(Test::Vars)
%endif
%endif
# Dependencies
# (none)

%description
This "license pack" contains all of the licenses from Creative Commons, except
for CC0, which is already included in Software::License.

Note that I don't recommend using these licenses for your own CPAN modules
(most of the licenses aren't even compatible with CPAN). However, S:L modules
are useful for more than mere CPAN::Meta::license declaration, so these modules
exist for those other purposes.

%prep
%setup -q -n Software-License-CCpack-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if 0%{!?perl_bootstrap:1} && %{with perl_Software_License_CCpack_enables_extra_tests}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))" RELEASE_TESTING=1
%endif

%files
%license LICENSE
%doc README
%{perl_vendorlib}/Software/
%{_mandir}/man3/Software::License::CCpack.3*
%{_mandir}/man3/Software::License::CC_BY_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_4_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_4_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_ND_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_ND_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_ND_4_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_SA_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_SA_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_SA_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_NC_SA_4_0.3*
%{_mandir}/man3/Software::License::CC_BY_ND_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_ND_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_ND_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_ND_4_0.3*
%{_mandir}/man3/Software::License::CC_BY_ND_NC_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_SA_1_0.3*
%{_mandir}/man3/Software::License::CC_BY_SA_2_0.3*
%{_mandir}/man3/Software::License::CC_BY_SA_3_0.3*
%{_mandir}/man3/Software::License::CC_BY_SA_4_0.3*
%{_mandir}/man3/Software::License::CC_PDM_1_0.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Paul Howarth <paul@city-fan.org> - 1.11-38
- Drop test dependency Test::Vars from Fedora 39 onwards since Test::Vars is
  FTBFS with Perl 5.38

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-32
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-31
- Perl 5.36 rebuild

* Fri Mar 11 2022 Paul Howarth <paul@city-fan.org> - 1.11-30
- Work around FTBFS triggered by package note feature

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-27
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-26
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-23
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-22
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 1.11-21
- BR: perl(blib) for t/00-compile.t

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Paul Howarth <paul@city-fan.org> - 1.11-19
- Don't run extra tests for EPEL builds

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-17
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-16
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-13
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-12
- Perl 5.28 rebuild

* Fri Apr 13 2018 Paul Howarth <paul@city-fan.org> - 1.11-11
- Specify all build dependencies
- Simplify find command using -delete
- BR: perl(Test::Vars) unconditionally
- Don't run the extra tests whilst bootstrapping

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.22 rebuild

* Tue Jun 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Disable using of Test::Vars with Perl 5.22

* Mon Oct 20 2014 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Include all versions of licenses, including the new 4.0 ones
  - Downgrade the Perl version to 5.6
  - Fix links in POD
  - Minor clean-up of license files

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 1.01-3
- Skip the CHANGES file until such time as it has some content (#1148040)

* Tue Sep 30 2014 Paul Howarth <paul@city-fan.org> - 1.01-2
- Sanitize for Fedora submission

* Mon Sep 29 2014 Paul Howarth <paul@city-fan.org> - 1.01-1
- Initial RPM version
