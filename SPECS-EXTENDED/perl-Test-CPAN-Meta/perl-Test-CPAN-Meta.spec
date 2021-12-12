# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Test_CPAN_Meta_enables_optional_test
%else
%bcond_with perl_Test_CPAN_Meta_enables_optional_test
%endif

Name:           perl-Test-CPAN-Meta
Version:        0.25
Release:        21%{?dist}
Summary:        Validation of the META.yml file in a CPAN distribution
License:        Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-CPAN-Meta
Source0:        https://cpan.metacpan.org/authors/id/B/BA/BARBIE/Test-CPAN-Meta-%{version}.tar.gz#/perl-Test-CPAN-Meta-%{version}.tar.gz
Patch0:         Test-CPAN-Meta-0.25-utf8.patch
BuildArch:      noarch
# Module Build
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Parse::CPAN::Meta) >= 0.02
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More) >= 0.62
# Optional Tests
%if %{with perl_Test_CPAN_Meta_enables_optional_test} && !%{defined perl_bootstrap}
# Break build-cycle: perl-Test-CPAN-Meta → perl-Test-CPAN-Meta-JSON
# → perl-Test-CPAN-Meta
BuildRequires:  perl(Test::CPAN::Meta::JSON)
%endif
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 0.08
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module was written to ensure that a META.yml file, provided with a
standard distribution uploaded to CPAN, meets the specifications that are
slowly being introduced to module uploads, via the use of package makers
and installers such as ExtUtils::MakeMaker, Module::Build and
Module::Install.

%prep
%setup -q -n Test-CPAN-Meta-%{version}

# Re-code documentation as UTF-8
%patch0

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test AUTOMATED_TESTING=1

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CPAN::Meta.3*
%{_mandir}/man3/Test::CPAN::Meta::Version.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.25-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-18
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-17
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-14
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-13
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-10
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.22 rebuild

* Wed May  6 2015 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - POD fix for usage example
  - Removed Test::CPAN::Meta from the recommends list, as CPAN.pm tries to
    install it first (CPAN RT#104023)
- Update UTF8 patch

* Wed Feb 04 2015 Petr Pisar <ppisar@redhat.com> - 0.24-2
- Break build-cycle: perl-Test-CPAN-Meta → perl-Test-CPAN-Meta-JSON →
  perl-Test-CPAN-Meta

* Tue Jan 13 2015 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Extended META test suite
  - Added META.json and tests
  - Documentation updates
- Classify buildreqs by usage
- Use a patch rather than scripted iconv to fix character encoding
- Modernize spec

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.23-2
- Perl 5.18 rebuild

* Mon Apr  8 2013 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Updated INSTALL instructions
  - Added minimum perl version (5.006)
  - Reworked Makefile.PL for clarity
  - Implemented Perl::Critic suggestions
  - Added meta_yaml_ok test and example
  - Several Version.pm updates, including new() parameter name change:
    'yaml' is now 'data'
  - Changes file dates changed to meet W3CDTF standards
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.21-2
- Perl 5.16 rebuild

* Fri Apr 27 2012 Petr Pisar <ppisar@redhat.com> - 0.21-1
- 0.21 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.17-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Fix RT#46473: license url with fragment part
  - Fix RT#47393: "optional_features" as map rather than list
  - Renamed word() to keyword()
  - Added identifier() validation
  - Changed optional_features key from a keyword to an identifier type
  - Clarified spec defined and user defined keys
  - Fixed qr// delimiters due to issues with the NOT SIGN symbol

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 01 2008 Steven Pritchard <steve@kspei.com> 0.12-1
- Update to 0.12.
- BR Test::Builder and Test::Builder::Tester.

* Wed Jun 04 2008 Steven Pritchard <steve@kspei.com> 0.11-1
- Update to 0.11.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.10-1
- Specfile autogenerated by cpanspec 1.75.
- Enable author tests.
- Add examples to docs.
- BR Test::More.
- Convert LICENSE to UTF-8.
- Drop bogus Requires.
