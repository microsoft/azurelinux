%if ! (0%{?rhel})
# Run extra test
%bcond_without perl_Module_Implementation_enables_extra_test
# Run optional test
%bcond_without perl_Module_Implementation_enables_optional_test
%else
%bcond_with perl_Module_Implementation_enables_extra_test
%bcond_with perl_Module_Implementation_enables_optional_test
%endif

Name:		perl-Module-Implementation
Version:	0.09
Release:	24%{?dist}
Summary:	Loads one of several alternate underlying implementations for a module
License:	Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/pod/Module::Implementation
Source0:	https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Module-Implementation-%{version}.tar.gz#/perl-Module-Implementation-%{version}.tar.gz
BuildArch:	noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Carp)
BuildRequires:	perl(Module::Runtime) >= 0.012
BuildRequires:	perl(Try::Tiny)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# ===================================================================
# Test suite requirements
# ===================================================================
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Fatal) >= 0.006
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::Requires)
%if %{with perl_Module_Implementation_enables_optional_test}
# ===================================================================
# Optional test requirements
# ===================================================================
BuildRequires:	perl(CPAN::Meta) >= 2.120900
%if ! %{defined perl_bootstrap}
# Build cycle: Test::CleanNamespaces → Package::Stash → Module::Implementation
BuildRequires:	perl(Test::CleanNamespaces)
%endif
BuildRequires:	perl(Test::Taint)
%endif
%if %{with perl_Module_Implementation_enables_extra_test}
# ===================================================================
# Author/Release test requirements
# ===================================================================
# Release tests include circular dependencies, so don't do them when bootstrapping:
%if ! %{defined perl_bootstrap}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Changes) >= 0.19
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
# Can't use EPEL packages as BR: for RHEL package
%if ! 0%{?rhel}
BuildRequires:	aspell-en
BuildRequires:	perl(Pod::Wordlist)
BuildRequires:	perl(Test::Pod::LinkCheck)
BuildRequires:	perl(Test::Pod::No404s)
BuildRequires:	perl(Test::Spelling) >= 0.12
%endif
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

%description
This module abstracts out the process of choosing one of several underlying
implementations for a module. This can be used to provide XS and pure Perl
implementations of a module, or it could be used to load an implementation
for a given OS or any other case of needing to provide multiple
implementations.

This module is only useful when you know all the implementations ahead of
time. If you want to load arbitrary implementations then you probably want
something like a plugin system, not this module.

%prep
%setup -q -n Module-Implementation-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
%if %{defined perl_bootstrap}
make test
%else
%if %{with perl_Module_Implementation_enables_extra_test}
# Don't run the author tests for EL builds (see above)
%if ! 0%{?rhel}
make test AUTHOR_TESTING=1 RELEASE_TESTING=1
%else
make test RELEASE_TESTING=1
%endif
%else
make test
%endif
%endif

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Implementation.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.09-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-21
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-20
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-17
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-16
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-13
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Petr Pisar <ppisar@redhat.com> - 0.09-10
- Break build cycle when bootstrapping (Test::CleanNamespaces →
  Package::Stash → Module::Implementation)

* Tue Sep  6 2016 Paul Howarth <paul@city-fan.org> - 0.09-9
- BR: perl(Test::CleanNamespaces)
- Simplify find command using -delete

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-4
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Implemented and then reverted a change to use Sub::Name (CPAN RT#98097)
- Modernize spec
- Hack out references to currently-unavailable Test::CleanNamespaces

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-6
- Perl 5.20 rebuild

* Tue Aug 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-5
- Do not run release and author tests on bootstrap

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Perl 5.18 rebuild

* Mon Jul 15 2013 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Require Test::Fatal ≥ 0.006 to avoid test failures (CPAN RT#76809)
- Explicitly run author tests, except for EL builds
- Add buildreqs for new tests
- Apply old Test::More patch if we have Test::More < 0.96

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.06-4
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.06-3
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from buildroot
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-2
- Conditionalize aspell-en dependency

* Sun Feb 12 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Require Module::Runtime 0.012, which has a number of useful bug fixes

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Make Test::Taint an optional dependency; it requires XS, and requiring a
    compiler for Module::Implementation defeats its purpose (CPAN RT#74817)
- BR: perl(Test::Requires)
- Update patch for building with old Test::More versions

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - This module no longer installs an _implementation() subroutine in callers;
    instead, you can call Module::Implementation::implementation_for($package)
    to get the implementation used for a given package
- Update patch for building with old Test::More versions

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.03-3
- Incorporate feedback from package review (#788258)
  - Correct License tag, which should be Artistic 2.0
  - BR: perl(lib) for test suite
  - Explicitly require perl(Carp), not automatically detected

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Sanitize for Fedora submission

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
