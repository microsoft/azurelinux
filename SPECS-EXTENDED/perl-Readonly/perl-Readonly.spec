Name:		perl-Readonly
Version:	2.05
Release:	12%{?dist}
Summary:	Facility for creating read-only scalars, arrays, hashes
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Readonly
Source0:	https://cpan.metacpan.org/authors/id/S/SA/SANKO/Readonly-%{version}.tar.gz#/perl-Readonly-%{version}.tar.gz
Patch0:		Readonly-2.05-interpreter.patch
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(Module::Build::Tiny) >= 0.035
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Storable)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(warnings)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Storable)

%description
Readonly provides a facility for creating non-modifiable scalars,
arrays, and hashes. Any attempt to modify a Readonly variable throws
an exception.

Readonly:
* Creates scalars, arrays (not lists), and hashes
* Creates variables that look and work like native perl variables
* Creates global or lexical variables
* Works at run-time or compile-time
* Works with deep or shallow data structures
* Prevents reassignment of Readonly variables

%prep
%setup -q -n Readonly-%{version}

# Fix script interpreter for test suite since we're packaging it
%patch0

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes README.md eg/benchmark.pl t/
%{perl_vendorlib}/Readonly.pm
%{_mandir}/man3/Readonly.3*

%changelog
* Fri Oct 30 2020 Joe Schmitt <joschmit@microsoft.com> - 2.05-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Always set a BR on perl-generators.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Paul Howarth <paul@city-fan.org> - 2.05-1
- Update to 2.05
  - Fix deref when using the stupid and utterly unnecessary Readonly::Clone
- BR: perl-generators where available
- Bump Test::More version requirement to 0.88 due to use of done_testing
- Update interpreter patch

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-2
- Perl 5.24 rebuild

* Sat May  7 2016 Paul Howarth <paul@city-fan.org> - 2.04-1
- Update to 2.04
  - Create mutable clones of readonly structures with Readonly::Clone (GH#13)
  - Minor typo fix (GH#21)
  - Rewording some documentation
  - No longer require an explicit version of perl in META.json or cpanfile
  - Quiet compile time warnings about function prototypes and vars being used
    only once
- Update interpreter patch

* Thu Feb 25 2016 Paul Howarth <paul@city-fan.org> - 2.01-1
- Update to 2.01
  - Disallow initialization of Readonly variables by assignment, allowed by
    Perl prototype changes in v5.16; assignment initialization of scalars sets
    scalar variables to undef and lists and hashes initialized by assignment
    are not read only
- Use %%license
- Upstream switched to Module::Build::Tiny flow
- Update interpreter patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-3
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-2
- Perl 5.20 rebuild

* Thu Jul  3 2014 Paul Howarth <paul@city-fan.org> - 2.00-1
- Update to 2.00
  - Deprecation of Readonly::XS as a requirement for fast, readonly scalars is
    complete
- Upstream dropped TODO file

* Mon Jun 30 2014 Paul Howarth <paul@city-fan.org> - 1.610-1
- Update to 1.61
  - Fix array and hash tie() while in XS mode (exposed by Params::Validate
    tests)
  - Fix implicit undef value regression
    (https://github.com/sanko/readonly/issues/8)
  - Normal constants (strings, numbers) do not appear to be read-only to
    Internals::SvREADONLY($) but perl itself doesn't miss a beat when you
    attempt to assign a value to them; fixing test regression in
    t/general/reassign.t
  - Minor documentation fixes (spell check, etc.)
    (https://github.com/sanko/readonly/issues/7)
- Update shellbang patch

* Thu Jun 26 2014 Paul Howarth <paul@city-fan.org> - 1.500.0-1
- Update to v1.500.0
  - Re-release with new version number

* Wed Jun 25 2014 Paul Howarth <paul@city-fan.org> - 1.5.0-1
- Update to v1.5.0
  - Readonly::XS is no longer needed
  - Typo fix (CPAN RT#86350)
  - Array and Hash scalar references were not made deeply readonly
    (CPAN RT#37864)
  - Upstream magic related bugs were reported to p5p and fixed in perl itself
    so we can resolve the following local issues:
    - CPAN RT#24216 ('looks_like_number' doesn't handle Readonly properly)
    - CPAN RT#29487 (magical variable bug in perl 5.8.5)
    - CPAN RT#36653 (Readonly scalar as class name sometimes undefined)
    - CPAN RT#57382 (tie-related bug in perl's core)
    - CPAN RT#70167 (unaccessed read-only variables are undef in select calls)
  - Reported Perl RT#120122 (tie + smartmatch bug) upstream to p5p; will
    eventually resolve local (CPAN RT#59256)
  - Use readonly support exposed in Internals on perl ≥ 5.8.0
  - Checking Readonly::XS::Okay is no longer suggested... never should have
    been
- Update shellbang patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Paul Howarth <paul@city-fan.org> - 1.04-1
- Update to 1.04
  - Module now maintained by Sanko Robinson; please see TODO for a possible set
    of changes to this module that may affect code written for old, pre-perl
    5.14.0 platforms!
  - Don't install benchmark.pl (CPAN RT#16167)
- This release by SANKO -> update source URL
- Switch to Module::Build flow
- Update shellbang patch
- Modernize spec since EPEL < 7 will never have buildreq CPAN::Meta
- Drop obsoletes/provides for old -tests subpackage

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.03-23
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.03-21
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.03-19
- Perl 5.16 rebuild

* Thu Mar  1 2012 Paul Howarth <paul@city-fan.org> - 1.03-18
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- No need to remove empty directories from buildroot
- Add buildreqs for Perl core modules that might be dual-lived
- Fix script interpreter for test suite since we're packaging it
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands
- Make %%files list more explicit
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-16
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-14
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-13
- Mass rebuild with perl-5.12.0

* Sun Feb 21 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-12
- Add perl_default_filter, etc
- Minor spec updates

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.03-11
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-8
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-7
- Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-6.2
- Add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-6.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Wed Oct 04 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-6
- Add explict requires on perl(Readonly::XS); perl(Readonly::XS) is available
  for all architectures Fedora supports, so there's no good reason to not
  require it
- Spec file rework

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-5
- Bump for mass rebuild

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-4
- Remove requires on perl-Readonly-XS

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-3
- Fix license and BuildRequires, use %%{?_smp_mflags} with make

* Sat Nov 12 2005 Michael A. Peters <mpeters@mac.com> - 1.03-2
- Separate out perl-Readonly-XS into its own package
- Package benchmark.pl as a doc

* Mon Nov 7 2005 Michael A. Peters <mpeters@mac.com> - 1.03-1
- Initial spec file
