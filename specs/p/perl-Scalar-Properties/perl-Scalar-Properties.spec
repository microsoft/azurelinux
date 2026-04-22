# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform author and release tests
%if 0%{?rhel} >= 10
%bcond_with perl_Scalar_Properties_enables_extra_test
%else
%bcond_without perl_Scalar_Properties_enables_extra_test
%endif

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

# Similarly for .package_note* files (#2062685)
%undefine _package_note_file

Name:           perl-Scalar-Properties
Version:        1.100860
Release: 41%{?dist}
Summary:        Run-time properties on scalar variables
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Scalar-Properties
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MARCEL/Scalar-Properties-%{version}.tar.gz
Patch0:         Scalar-Properties-1.100860-English-is-for-author-tests.patch
Patch3:         Scalar-Properties-1.100860-skip-MYMETA.yml.patch
BuildArch:      noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.11
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# ===================================================================
# Test requirements
# ===================================================================
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Scalar_Properties_enables_extra_test}
# ===================================================================
# Author test requirements
# (skipped as the Critic test fails in version 1.100860)
# ===================================================================
BuildRequires:  perl(English)
BuildConflicts: perl(Test::Perl::Critic)
# ===================================================================
# Release test requirements
# (Spelling check can't find "versa" in version 1.100860)
# ===================================================================
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildConflicts: perl(Pod::Wordlist::hanekomu)
BuildRequires:  perl(Test::CheckChanges)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::DistManifest)
BuildRequires:  perl(Test::HasVersion)
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Synopsis)
%endif
# ===================================================================
# Runtime dependencies
# ===================================================================
# (none)

%description
Scalar::Properties attempts to make Perl more object-oriented by taking an idea
from Ruby: Everything you manipulate is an object, and the results of those
manipulations are objects themselves.

%prep
%setup -q -n Scalar-Properties-%{version}

# Delist English from run-time dependencies, otherise t/000-report-versions.t
# may fail if build without extra tests, CPAN RT#134158
%patch -P 0 -p1

# MANIFEST.SKIP should include MYMETA.yml; otherwise, t/release-dist-manifest.t
# may fail due to it appearing unexpectedly
%patch -P 3 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if %{with perl_Scalar_Properties_enables_extra_test}
make test AUTHOR_TESTING=1 RELEASE_TESTING=1
%else
make test
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Scalar/
%{_mandir}/man3/Scalar::Properties.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-32
- Perl 5.36 rebuild

* Thu Mar 10 2022 Paul Howarth <paul@city-fan.org> - 1.100860-31
- Work around package note files breaking t/release-dist-manifest.t (#2062685)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Paul Howarth <paul@city-fan.org> - 1.100860-29
- Re-enable extra tests for RHEL 9
- Use %%license unconditionally

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-27
- Perl 5.34 rebuild

* Wed Jan 27 2021 Petr Pisar <ppisar@redhat.com> - 1.100860-26
- Delist English from run-time dependencies (CPAN RT#134158)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Petr Pisar <ppisar@redhat.com> - 1.100860-24
- Disable extra tests since RHEL 9

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-22
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Paul Howarth <paul@city-fan.org> - 1.100860-20
- Spec tidy-up
  - Specify all dependencies
  - Simplify find command using -delete
  - Fix permissions verbosely
  - Use %%license where possible

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-15
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.100860-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-7
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 1.100860-4
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.100860-1
- Update to 1.100860
  - Converted the distribution to Dist::Zilla-style
- Run the author/release tests too, adding buildreqs as necessary
- Package LICENSE file
- Clean up for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.13-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-8
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-3
- fix source url

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1.1
- BR: Test::More

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1
- 0.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Apr 09 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.12-1
- First build.
