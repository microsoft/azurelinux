# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Path-Class
Version:	0.37
Release:	30%{?dist}
Summary:	Cross-platform path specification manipulation
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Path-Class
Source0:	https://cpan.metacpan.org/authors/id/K/KW/KWILLIAMS/Path-Class-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 7.32
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec) >= 3.26
BuildRequires:	perl(File::stat)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Dir)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(overload)
BuildRequires:	perl(parent)
BuildRequires:	perl(Perl::OSType)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(warnings)
# Dependencies
Requires:	perl(File::Copy)
Requires:	perl(Perl::OSType)

%description
Path::Class is a module for manipulation of file and directory specifications
(strings describing their locations, like '/home/ken/foo.txt' or
'C:\Windows\Foo.txt') in a cross-platform manner. It supports pretty much every
platform Perl runs on, including Unix, Windows, Mac, VMS, Epoc, Cygwin, OS/2,
and NetWare.

%prep
%setup -q -n Path-Class-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Path/
%{_mandir}/man3/Path::Class.3*
%{_mandir}/man3/Path::Class::Dir.3*
%{_mandir}/man3/Path::Class::Entity.3*
%{_mandir}/man3/Path::Class::File.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-22
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-19
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-16
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 28 2019 Paul Howarth <paul@city-fan.org> - 0.37-14
- Switch to ExtUtils::MakeMaker flow
- Don't try to run author tests during package build
- Modernize spec using %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-12
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 15 2016 Paul Howarth <paul@city-fan.org> - 0.37-1
- Update to 0.37:
  - Doc update for contains/subsumes
  - Fix "contains" when $self is a relative path (GH#43)
  - Handle case where $other evaluates false
  - Add additional test cases for contains and subsumes
  - Test with Perl 5.24
- BR: perl-generators

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-2
- Perl 5.24 rebuild

* Wed Feb 17 2016 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36:
  - Use croak instead of die; use eval syntax instead of universal::isa (as
    perlcritic wishes)
  - Load File::Copy and Perl::OSType only when used (copy_to, move_to)
  - Always use canonpath on arguments to splitdir
  - Fix 'Operation "eq": no method found' error (CPAN RT#77259)
  - Add some fixes and tests for contains() with updir stuff (GH#43)
  - Fix Carp::Croak to Carp::croak
  - Fixed and improved Travis testing configuration
  - Fix Pod typos
  - Check all print calls in spew and explicitly call (and check) close

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-2
- Perl 5.22 rebuild

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35:
  - Fixed a t/03-filesystem.t test error on Windows
- Classify buildreqs by usage

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34:
  - Add a new spew_lines() method
  - Don't convert file into directory in subsumes()
  - Updated POD for copy_to and move_to methods
  - Stringify destination for copy_to method
  - Stringify destination for move_to method
  - Add Continuous Integration with Travis CI
  - Change bugtracker to github's
- Use %%license where possible

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Petr Pisar <ppisar@redhat.com> - 0.33-2
- Break build-cycle: perl-Path-Class → perl-Test-Perl-Critic →
  perl-Perl-Critic → perl-Pod-Spell → perl-File-ShareDir-ProjectDistDir →
  perl-Path-Class

* Thu Dec 12 2013 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33:
  - New copy_to() and move_to() methods
  - As advised in the utime() docs, pass undef as the time for touch()
  - Do a better job cleaning up temp files in the tests
  - Optimization: use parent.pm instead of base.pm
  - Changed the docs to show that file() and dir() are exported by default
  - Fixed spelling error in POD
- Update buildreqs as needed
- Drop patch for building with old Module::Build versions

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.32-2
- Perl 5.18 rebuild

* Tue Mar 19 2013 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32:
  - Updated dependency on File::Spec to 3.26 (CPAN RT#83143)
  - Fixed bug with leading empty string in dir() - became unintentional
    UNC path on Cygwin
  - Fixed "Unterminated C<...> sequence" in Pod

* Thu Mar  7 2013 Paul Howarth <paul@city-fan.org> - 0.31-2
- Bump perl(File::Spec) version requirement to 3.26 (CPAN RT#83143)
- Drop EL-5 support since it doesn't have File::Spec ≥ 3.26

* Tue Feb  5 2013 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31:
  - Optimization: stringify variables passed to canonpath
  - Optimization: Use internal guts when constructing Dirs from Dirs, instead
    of concatenating and splitting them again with File::Spec
  - Fix grammar error in docs
  - Implement a 'split' parameter for the slurp() method
  - In docs, replace unicode MINUS SIGN with ascii HYPHEN-MINUS
- BR: perl(Scalar::Util)

* Tue Dec 18 2012 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29:
  - Add components() method, which returns directory names (and filename, if
    this is a File object) as a list
  - Fix a test failure on non-Unix platforms; the 07-recurseprune.t test was
    written in a Unix-specific way

* Mon Dec 17 2012 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28:
  - Fix test failures when run as root - they were relying on permissions
    failures, but permissions never fail as root
  - Add links in docs to the other modules we rely on and talk about in the
    docs, which makes for easier viewing through search.cpan.org / MetaCPAN
  - Fixed some misleading variable names in docs (CPAN RT#81795)

* Mon Dec 10 2012 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27:
  - Added pruning support in dir->recurse(); if recurse callback returns
    $item->PRUNE, no children of this item will be analyzed
  - Documented 'basename' method for directories
  - Added traverse_if() function, which allows one to filter children before
    processing them
  - Added tempdir() function
- Package upstream LICENSE file

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.26-2
- Perl 5.16 rebuild

* Fri Jun 15 2012 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26:
  - resolve() now includes the name of the non-existent file in the error
    message
  - New shortcut opena(), to open a file for appending
  - New spew() method that does the inverse of the slurp() method
  - Fixed a typo in a class name in the docs for Path::Class::Entity
- Drop %%defattr, redundant since rpm 4.4
- Drop conditional for EPEL-4 support (EL-4 now EOL-ed)

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25:
  - resolve() now croak()s instead of die()s on non-existent file
  - Added a traverse() method for directories, based on the fmap_cont() method
    of Forest::Tree::Pure; it's an alternative to ->recurse, which allows for
    more control over how the recursion happens
  - Fixed a grammar error in the docs
  - Added a tempfile() method for Dir objects, which provides an interface to
    File::Temp (CPAN RT#60485)
  - Fixed a non-helpful fatal error message when calling resolve() on a path
    that doesn't exist; now dies with the proper "No such file or directory"
    message and exit status
- BR: perl(Test::Perl::Critic) and run author tests where possible
- Add patch to support building with Module::Build < 0.3601

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.23-4
- Spec clean-up:
  - Add buildreqs for Perl core modules that might be dual-lived
  - Tidy %%description
  - Make %%files list more explicit
  - Don't use macros for commands
  - Use search.cpan.org source URL
  - BR: at least version 0.87 of File::Spec

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild

* Thu Apr 14 2011 Ian Burrell <ianburrell@gmail.com> - 0.23-1
- Update to 0.23

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-2
- Mass rebuild with perl-5.12.0

* Mon Feb 22 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.18-1
- Update to 0.18 (for latest DBIx::Class)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.16-6
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-3
- Rebuild for new perl

* Thu Aug 16 2007 Ian Burrell <ianburrell@gmail.com> - 0.16-2
- Fix BuildRequires

* Mon Jan 29 2007 Ian Burrell <ianburrell@gmail.com> - 0.16-1
- Specfile autogenerated by cpanspec 1.69.1
