Vendor:         Microsoft Corporation
Distribution:   Mariner
# Class::Load::XS is an optional extra
%if 0%{?rhel:1}
%bcond_with Class_Load_XS
%else
%bcond_without Class_Load_XS
%endif

Name:		perl-Class-Load
Version:	0.25
Release:	11%{?dist}
Summary:	A working (require "Class::Name") and more
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Class-Load
Source0:	https://cpan.metacpan.org/modules/by-module/Class/Class-Load-%{version}.tar.gz#/perl-Class-Load-%{version}.tar.gz
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Data::OptList) >= 0.110
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Module::Implementation) >= 0.04
BuildRequires:	perl(Module::Runtime) >= 0.012
BuildRequires:	perl(Package::Stash) >= 0.14
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Try::Tiny)
# ===================================================================
# Regular test suite requirements
# ===================================================================
# Class::Load::XS → Class::Load
%if 0%{!?perl_bootstrap:1} && %{with Class_Load_XS}
BuildRequires:	perl(Class::Load::XS)
%endif
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Needs)
BuildRequires:	perl(Test::Without::Module)
BuildRequires:	perl(version)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Also requires core module perl(Exporter) via a "use base" construct

%description
require EXPR only accepts Class/Name.pm style module names, not Class::Name.
How frustrating! For that, we provide load_class 'Class::Name'.

It's often useful to test whether a module can be loaded, instead of throwing
an error when it's not available. For that, we provide
try_load_class 'Class::Name'.

Finally, sometimes we need to know whether a particular class has been loaded.
Asking %%INC is an option, but that will miss inner packages and any class for
which the filename does not correspond to the package name. For that, we
provide is_class_loaded 'Class::Name'.

%prep
%setup -q -n Class-Load-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::Load.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.25-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 13 2019 Paul Howarth <paul@city-fan.org> - 0.25-9
- Build without Class::Load::XS for EPEL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-7
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.28 rebuild

* Mon Jun 11 2018 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Merged required and recommended Data::OptList version prerequisite, to work
    around CPAN.pm bug (CPAN RT#123447)
- Switch upstream from search.cpan.org to metacpan.org

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-2
- Perl 5.26 rebuild

* Tue Apr 11 2017 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix test to handle altered Test::Without::Module exception message (GH#2)

* Fri Apr  7 2017 Paul Howarth <paul@city-fan.org> - 0.23-6
- Fix FTBFS with Test::Without::Module ≥ 0.19
  (https://github.com/moose/Class-Load/pull/2)
- Drop redundant Group: tag
- Simplify find command using -delete

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Remove use of namespace::clean
- Switch to ExtUtils::MakeMaker flow

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-4
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Sep 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-2
- Perl 5.20 rebuild

* Thu Sep  4 2014 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Document some of the caveats to using this module, and refer to
    Module::Runtime as an alternative
- Use %%license where possible

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Repository moved to the github moose organization
- This release by ETHER -> update source URL
- Switch to Module::Build::Tiny flow
- Package upstream CONTRIBUTING and README.md files
- Add manpage for Class::Load::PP to %%files list
- Don't attempt to run author/release tests as Module::Build::Tiny does not
  provide a convenient way of doing that

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.20-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Same as the most recent 0.19, but with a new version (CPAN RT#78389)

* Sun Jul 15 2012 Paul Howarth <paul@city-fan.org> - 0.19-7
- New upstream re-release of 0.19 by DROLSKY
  - The load_class() subroutine now returns the class name on success
    (CPAN RT#76931)
  - Exceptions and errors from Class::Load no longer contain references to line
    numbers in Class::Load or Module::Runtime; this applies to exceptions
    thrown by load_class, load_first_existing_class, and load_optional_class,
    as well as the error returned by try_load_class
  - Exceptions are now croaked properly so they appear to come from the calling
    code, not from an internal subroutine; this makes the exceptions look more
    like the ones thrown by Perl's require (CPAN RT#68663)
- This release by DROLSKY -> update source URL
- BR: perl(Scalar::Util) for the module
- BR: perl(lib) for the test suite
- Drop buildreqs perl(strict) and perl(warnings) - not dual-lived

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.19-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 26 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-5
- Conditionalize Pod::Coverage::Moose

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.19-4
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.19-3
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-2
- Conditionalize aspell-en dependency

* Tue Apr  3 2012 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19 (no functional changes)
- This release by DOY -> update source URL
- BR: perl(Exporter)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18:
  - Require Package::Stash ≥ 0.14 (CPAN RT#75095)

* Sun Feb 12 2012 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17:
  - Require Module::Runtime 0.012, which has a number of useful bug fixes
  - A bug in Class::Load caused test failures when Module::Runtime 0.012 was
    used with Perl 5.8.x (CPAN RT#74897)

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15:
  - Small test changes to accomodate latest version of Module::Implementation
- BR: at least version 0.04 of perl(Module::Implementation)

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14:
  - Use Module::Implementation to handle loading the XS or PP versions of the
    code; using this module fixes a few bugs
  - Under taint mode, setting an implementation in the
    CLASS_LOAD_IMPLEMENTATION env var caused a taint error
  - An invalid value in the CLASS_LOAD_IMPLEMENTATION env var is now detected
    and reported immediately; no attempt is made to load an invalid
    implementation
- BR: perl(Module::Implementation)
- BR: perl(base), perl(Carp), perl(strict) and perl(warnings) for completeness
- Drop version requirement for perl(Package::Stash), no longer present upstream
- Drop explicit runtime dependencies, no longer needed
- Don't BR: perl(Class::Load::XS) or perl(Pod::Coverage::Moose) if we're
  bootstrapping
- Don't run the release tests when bootstrapping as the Pod coverage test will
  fail in the absence of Pod::Coverage::Moose

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.13-2
- Fedora 17 mass rebuild

* Thu Dec 22 2011 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13:
  - Fix some bugs with our use of Try::Tiny, which could cause warnings on some
    systems where Class::Load::XS wasn't installed (CPAN RT#72345)
- BR: perl(Test::Without::Module)

* Tue Oct 25 2011 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Require Module::Runtime ≥ 0.011, which fixes problems with Catalyst under
    Perl 5.8 and 5.10
- Add versioned runtime dependencies for Module::Runtime and Package::Stash

* Wed Oct  5 2011 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11:
  - Don't accept package names that start with a digit
  - Rewrite some of the guts to use Module::Runtime rather than reimplementing
    its functionality
- BR: perl(Module::Runtime) ≥ 0.009
- Drop all support for older distributions as required module
  Module::Runtime ≥ 0.009 will not be available prior to F-16

* Tue Sep  6 2011 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10:
  - Fix is_class_loaded to ignore $ISA (but still look for @ISA) when trying to
    determine whether a class is loaded
  - Lots of internals cleanup
- BR: perl(Package::Stash) ≥ 0.32 and perl(Try::Tiny)
- Update patches to apply cleanly

* Tue Aug 16 2011 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08:
  - The previous version was missing a prereq declaration for Data::OptList
    (CPAN RT#70285)
- This release by DROLSKY -> update source URL
- Package new documentation: LICENSE and README
- Add build requirements for new release tests and run them:
  - perl(Pod::Coverage::Moose)
  - perl(Test::CPAN::Changes)
  - perl(Test::EOL)
  - perl(Test::NoTabs)
  - perl(Test::Pod)
  - perl(Test::Pod::Coverage)
  - perl(Test::Requires)
  - perl(Test::Spelling) and aspell-en
- Add patch for building with ExtUtils::MakeMaker < 6.30
- Add patch for building with Test::More < 0.88
- Add patch for building without Test::Requires
- Add patch for fixing spell checker word list
- Don't try to run the POD Coverage test if we don't have Pod::Coverage::Moose

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Paul Howarth <paul@city-fan.org> - 0.06-3
- Drop explicit dependency on core module perl(Exporter) (#656408)

* Tue Nov 23 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Sanitize spec for Fedora submission

* Mon Nov 22 2010 Paul Howarth <paul@city-fan.org> - 0.06-1
- Initial RPM version
