# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Test-CPAN-Meta-JSON
Version:	0.16
Release:	31%{?dist}
Summary:	Validate a META.json file within a CPAN distribution
License:	Artistic-2.0
URL:		https://metacpan.org/release/Test-CPAN-Meta-YAML
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-CPAN-Meta-JSON-%{version}.tar.gz
Patch0:		Test-CPAN-Meta-JSON-0.16-utf8.patch
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(IO::File)
BuildRequires:	perl(JSON) >= 2.15
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
# Optional Tests
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 0.08
# Dependencies
# (none)

%description
This module was written to ensure that a META.json file, provided with a
standard distribution uploaded to CPAN, meets the specifications that are
slowly being introduced to module uploads, via the use of ExtUtils::MakeMaker,
Module::Build and Module::Install.

See CPAN::Meta for further details of the CPAN Meta Specification.

%prep
%setup -q -n Test-CPAN-Meta-JSON-%{version}

# Recode LICENSE as UTF-8
%patch -P 0

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test AUTOMATED_TESTING=1

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CPAN::Meta::JSON.3*
%{_mandir}/man3/Test::CPAN::Meta::JSON::Version.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-23
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-20
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-17
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Paul Howarth <paul@city-fan.org> - 0.16-15
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-2
- Perl 5.22 rebuild

* Wed Jan 14 2015 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Fixed license fields in META.json to be lists
  - Extended META test suite
  - Added '2.0' as an alias to '2' version spec.
  - License MUST be a list of strings
- Classify buildreqs by usage
- Update UTF8 patch
- Use %%license where possible

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Changes file dates changed to meet W3CDTF standards

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.14-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Added minimum perl version (5.006)
  - Reworked Makefile.PL for clarity
  - Implemented Perl::Critic suggestions
  - Added meta_json_ok test and example
  - Several Version.pm updates
- Update UTF8 patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.13-2
- Perl 5.16 rebuild

* Fri Apr 20 2012 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Further spelling fix
  - Removed DSLIP info

* Tue Apr 17 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - CPAN RT#76609: Spelling fix

* Sun Apr 15 2012 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - CPAN RT#74317: imported url validation from CPAN::Meta
  - CPAN RT#66692: updated license type
  - Updates to examples
- BR: perl(Test::CPAN::Meta) rather than perl(Test::CPAN::Meta::YAML)
- Don't need to remove empty directories from buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Paul Howarth <paul@city-fan.org> - 0.10-2
- Sanitize for Fedora/EPEL submission

* Wed Aug 10 2011 Paul Howarth <paul@city-fan.org> - 0.10-1
- Initial RPM version
