# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Data-Section-Simple
Version:	0.07
Release: 34%{?dist}
Summary:	Read data from __DATA__
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Data-Section-Simple
Source0:	https://cpan.metacpan.org/modules/by-module/Data/Data-Section-Simple-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(warnings)
# Module
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires:	perl(Test::Pod) >= 1.41
%endif
# Dependencies
# (none)

%description
Data::Section::Simple is a simple module to extract data from the __DATA__
section of the file.

%prep
%setup -q -n Data-Section-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if 0%{?fedora} || 0%{?rhel} > 6
make test RELEASE_TESTING=1
%else
make test
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::Section::Simple.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-25
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-22
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-19
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 0.07-17
- Spec tidy-up
  - Use author-independent URLs
  - Specify all build dependencies
  - Drop support for building with Test::More < 0.88
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Fix permissions verbosely
  - Use %%license where possible

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Revert the change in 0.06
- Update patch for building with Test::More < 0.88

* Sat Apr 12 2014 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Fix race condition in a forked environment
    (https://github.com/miyagawa/Data-Section-Simple/pull/4)
- Update patch for building with Test::More < 0.88
- Don't run the release tests for EPEL-5 or EPEL-6 builds

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.05-2
- Perl 5.18 rebuild

* Tue Jun 11 2013 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Use MakeMaker
- Revert to ExtUtils::MakeMaker flow
- Drop Test::Pod version requirement for EPEL build compatibility

* Mon May 20 2013 Paul Howarth <paul@city-fan.org> - 0.04-2
- Use Module::Build::Tiny's new --create_packlist option

* Fri Mar 29 2013 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - Do not throw exceptions when there's no template
    (https://github.com/miyagawa/Data-Section-Simple/pull/2)
- URL moved to github
- Source0 moved to MetaCPAN
- Package upstream's new LICENSE file
- Switch to Module::Build::Tiny flow
- Update patch for building with Test::More < 0.88
- Drop %%defattr, redundant since rpm 4.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.03-3
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Fedora 17 mass rebuild

* Mon Sep 19 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Noted the use of utf8 pragma
  - Doc typo fixes (Util)

* Thu Aug  4 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
