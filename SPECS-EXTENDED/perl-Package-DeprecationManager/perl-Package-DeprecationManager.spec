Name:		perl-Package-DeprecationManager
Version:	0.18
Release:	1%{?dist}
Summary:	Manage deprecation warnings for your distribution
License:	Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Package-DeprecationManager
Source0:	https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Package-DeprecationManager-%{version}.tar.gz#/perl-Package-DeprecationManager-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(List::Util) >= 1.33
BuildRequires:	perl(Package::Stash)
BuildRequires:	perl(Params::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Install)
BuildRequires:	perl(Sub::Name)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Warnings)
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module allows you to manage a set of deprecations for one or more modules.

When you import Package::DeprecationManager, you must provide a set of
-deprecations as a hash ref. The keys are "feature" names, and the values are
the version when that feature was deprecated.

%prep
%setup -q -n Package-DeprecationManager-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes CONTRIBUTING.md README.md
%{perl_vendorlib}/Package/
%{_mandir}/man3/Package::DeprecationManager.3*

%changelog
* Fri Dec 13 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.18-1
- Update to 0.18
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.17-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Remove use of namespace::autoclean
- BR: perl-generators
- Simplify find command using -delete
- Author and Release Tests moved to xt/ so don't bother trying to run them

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-2
- Perl 5.24 rebuild

* Tue Mar 22 2016 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - The subs installed into the caller are now named with Sub::Name; this makes
    these subs appear to be part of the caller, as opposed to an import, which
    is what we want, since each installed sub is constructed uniquely for a
    given package
- Update patches as needed

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Made this module co-operate with existing import() subs in packages that
    use this module, as long as you use this module last
- Drop support for old distributions due to non-optional test dependency of
  Test::Warnings

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-2
- Perl 5.22 rebuild

* Tue Apr 21 2015 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Use any() from List::Util 1.33+ instead of List::MoreUtils
- Add patch to use List::MoreUtils::any() on old distributions where we don't
  have List::Util 1.33+
- Add patch to support building without Test::Code::TidyAll
- Classify buildreqs by usage
- Update patches as needed
- Use %%license where possible
- Don't try to do the author or release tests for RHEL builds

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-11
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.13-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.13-5
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.13-4
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-3
- Conditionalize aspell-en

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 0.13-2
- Upstream has dropped Kwalitee test, so drop BR: perl(Test::Kwalitee)

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13:
  - Fix dist.ini to not add Test::Spelling as a requirement
- Drop %%defattr, redundant since rpm 4.4
- Test::Requires available on all supported distributions

* Mon Mar  5 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Fix tests to pass with Carp 1.25 (CPAN RT#75520)
- BR: perl(Test::Spelling), aspell-en
- Add patch to accept "deprecations" as a valid dictionary word
- Update patches to apply cleanly
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop EPEL-4 support:
  - Drop patch supporting build with ExtUtils::MakeMaker < 6.30

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.11-3
- Fedora 17 mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.11-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11:
  - Allow an empty hash for the -deprecations parameter
- BR: perl(ExtUtils::MakeMaker)
- BR: perl(Test::CPAN::Changes)
- BR: perl(Pod::Coverage::TrustPod) unconditionally
- Update patches for old ExtUtils::MakeMaker and Test::More compatibility

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Paul Howarth <paul@city-fan.org> - 0.10-2
- Update patches for old Test::More and no Test::Requires
- perl(Pod::Coverage::TrustPod) now available everywhere except EPEL-4

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> - 0.10-1
- Update to 0.10:
  - Test suite uses Test::Fatal instead of Test::Exception

* Mon Oct 18 2010 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09:
  - Added a compilation test

* Fri Oct 15 2010 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08:
  - The use of regular expressions in ignores didn't really work in 0.06
  - Added missing deps on List::MoreUtils and Test::Requires
  - Replaced Test::Warn with Test::Output in the tests
  - Made the tests actually test what they should be testing
- BR: Test::Output rather than Test::Warn
- Update patches

* Fri Oct 15 2010 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06:
  - Removed hard dep on Test::Warn for the benefit of Moose
  - Fixed what looked like a bug in -ignore handling
  - The -ignore parameter now accepts regexes as well as package names
- Update compatibility patches
- BR: List::MoreUtils
- BR: Test::Requires where possible, patch it out elsewhere

* Tue Jul 27 2010 Paul Howarth <paul@city-fan.org> - 0.04-2
- Clean up for Fedora submission

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 0.04-1
- Initial RPM version
