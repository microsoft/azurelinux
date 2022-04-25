Name:           perl-Test-Warn
Version:        0.36
Release:        9%{?dist}
Summary:        Perl extension to test methods for warnings
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-Warn
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BIGJ/Test-Warn-%{version}.tar.gz#/perl-Test-Warn-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Runtime
BuildRequires:  perl(Carp) >= 1.22
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Uplevel) >= 0.12
BuildRequires:  perl(Test::Builder) >= 0.13
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(constant)
BuildRequires:  perl(blib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Test::Builder) >= 0.13

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Test::Builder\\)$

%description
This module provides a few convenience methods for testing warning
based code.

%prep
%setup -q -n Test-Warn-%{version}

# Fix line endings
sed -i -e 's/\r$//' Changes

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
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Warn.3*

%changelog
* Mon Apr 25 2022 Muhammad Falak <mwani@microsoft.com> - 0.36-9
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.36-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-2
- Perl 5.28 rebuild

* Mon Jun 25 2018 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Added provide section to META.yml via changing Makefile.PL

* Wed Jun 13 2018 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Create META.json so that perl Makefile.PL stops complaining (GH#2)
  - Update META.yml (GH#3)
  - Add missing comma in Makefile.PL (GH#4)
  - Pod clean-up (GH#5)
  - README clean-up: assign copyright to current author (GH#6)

* Thu May 31 2018 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Added a note that XS warnings might not be caught (CPAN RT#42070, GH#1)
  - Removed TODO section
  - Updated Copyright section

* Tue May 29 2018 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Clean up some manpage language (Debian Bug #322351, CPAN RT#49519)
- Switch upstream from search.cpan.org to metacpan.org

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 24 2016 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Update Changes and distribution metadata

* Sun Dec 18 2016 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Improve support for warnings with trailing newlines
- This release by BIGJ → update source URL
- Classify buildreqs by usage
- Simplify find command using -delete
- Drop redundant Group: tag

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar  5 2014 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Important note in documentation how check for warning category is done; if
    you use Test::Warn with categories, you should check that it does what you
    expect
  - Category tree is now dynamic and does not use Tree::DAG_Node

* Tue Feb 18 2014 Petr Pisar <ppisar@redhat.com> - 0.24-8
- Specify all dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.24-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-4
- Convert end-of-lines in Changes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.24-2
- Perl 5.16 rebuild

* Sun Apr  1 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24 (compatibility with Carp 1.25) (#808856)
- BR: Perl core modules that might be dual-lived
- BR/R: at least version 1.02 of perl(Tree::DAG_Node)
- Drop redundant buildreq perl(Test::Exception)
- Don't need to remove empty directories from buildroot
- Drop explicit versioned runtime dependency on Test::Builder, satisfied in
  all distributions since the dawn of time (nearly)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Drop redundant %%{?perl_default_filter}
- Make %%files list more explicit
- Don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild
- remove unused BR Array::Compare

* Wed Mar  2 2011 Tom Callaway <spot@fedoraproject.org> - 0.23-1
- update to 0.23

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Tom Callaway <spot@fedoraproject.org> - 0.22-1
- update to 0.22

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.21-2
- rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- add perl default filter (pro forma)
- use _fixperms incantation
- auto-update to 0.21 (by cpan-spec-update 0.01)
- altered br on perl(Test::Builder::Tester) (0 => 1.02)
- altered req on perl(Test::Builder::Tester) (0 => 1.02)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (#477298)
- Buildreq ExtUtils::MakeMaker, File::Spec, Test::Builder,
  Test::Builder::Tester, and Test::More (from upstream Makefile.PL)
- Add runtime dependencies on Test::Builder and Test::Builder::Tester

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-3
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-2
- rebuild for new perl

* Sat May  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.10-1
- Update to 0.10.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.09-1
- Update to 0.09.
- New upstream maintainer.
- New BR: perl(Test::Pod).

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-4
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Jul  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-2
- Dist tag.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.08-0.fdr.1
- First build.
