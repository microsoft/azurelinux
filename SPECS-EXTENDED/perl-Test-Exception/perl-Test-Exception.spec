Name:           perl-Test-Exception
Version:        0.43
Release:        14%{?dist}
Summary:        Library of test functions for exception based Perl code
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-Exception
Source0:        https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Test-Exception-%{version}.tar.gz#/perl-Test-Exception-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Uplevel) >= 0.18
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

# Avoid bogus perl(DB) provide
%{?perl_default_filter}

%description
This module provides a few convenience methods for testing exception
based code. It is built with Test::Builder and plays happily with
Test::More and friends.

%prep
%setup -q -n Test-Exception-%{version}

# Remove unnecessary exec permissions
chmod -c -x Changes

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Exception.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.43-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-11
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  1 2016 Paul Howarth <paul@city-fan.org> - 0.43-1
- Update to 0.43
  - Remove Test2/Test-Stream special cases; they are not needed

* Tue Dec 22 2015 Paul Howarth <paul@city-fan.org> - 0.41-1
- Update to 0.41
  - Updated for Test2
- This release by EXODIST → update source URL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Tom Callaway <spot@fedoraproject.org> - 0.40-1
- update to 0.40

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-2
- Perl 5.22 rebuild

* Sun Mar  1 2015 Paul Howarth <paul@city-fan.org> - 0.38-1
- Update to 0.38
  - Distribution is now managed by ExtUtils::MakeMaker (CPAN RT#102054)
  - Fixed repository link in metadata
- This release by ETHER → update source URL

* Fri Jan  9 2015 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Fix bug when Test::More has been downgraded

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Fix a bug when Test::Builder isn't new (better version)
- Switch to ExtUtils::MakeMaker flow
- Classify buildreqs by usage

* Sat Sep 20 2014 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Fixed test broken by changes in Test::Builder and friends
- This release by EXODIST → update source URL
- Modernize spec

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.32-2
- Perl 5.18 rebuild

* Mon Apr 29 2013 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Fixed tests that broke due to diagnostic changes in Test::More 0.99
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Remove bogus exec permission on Changes file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-8
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.31-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.31-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Dec 10 2010 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-2
- Mass rebuild with perl-5.12.0

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- auto-update to 0.29 (by cpan-spec-update 0.01)
- altered br on perl(Module::Build) (0 => 0.35)
- altered br on perl(Test::Builder) (0 => 0.7)
- altered br on perl(Test::Builder::Tester) (0 => 1.07)
- added a new br on perl(Test::Harness) (version 2.03)
- added a new br on perl(Test::More) (version 0.7)
- added a new br on perl(Test::Simple) (version 0.7)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.27-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.27-2
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 0.27-1
- Update to 0.27.

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.26-2
- rebuild for new perl

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.26-1
- Update to 0.26.
- Update License tag.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.
- Drop executable bits.

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-3
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-2
- Rebuild for FC5 (perl 5.8.8).

* Tue Jun  7 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-4
- Add dist tag.

* Sat Apr 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.20-3
- Avoid .packlist creation with Module::Build >= 0.2609.
- Trust that %%{perl_vendorlib} is defined.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.20-2
- Rebuilt

* Fri Nov  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-0.fdr.1
- First build.
