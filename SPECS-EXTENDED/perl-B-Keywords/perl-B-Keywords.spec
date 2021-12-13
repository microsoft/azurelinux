# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_B_Keywords_enables_extra_test
%else
%bcond_with perl_B_Keywords_enables_extra_test
%endif

Name:           perl-B-Keywords
Version:        1.21
Release:        4%{?dist}
Summary:        Lists of reserved barewords and symbol names
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/B-Keywords
Source0:        https://cpan.metacpan.org/modules/by-module/B/B-Keywords-%{version}.tar.gz#/perl-B-Keywords-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl-devel
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional Tests
BuildRequires:  perl(Test::Pod) >= 1.0
# Maintainer Tests
%if 0%{!?perl_bootstrap:1} && %{with perl_B_Keywords_enables_extra_test}
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Perl::MinimumVersion) >= 1.20
BuildRequires:  perl(Test::CPAN::Meta) >= 0.12
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::MinimumVersion) >= 0.008
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Text::CSV_XS)
BuildRequires:  perl(warnings)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
B::Keywords supplies several arrays of exportable keywords: @Scalars, @Arrays,
@Hashes, @Filehandles, @Symbols, @Functions, @Barewords, @TieIOMethods,
@UNIVERSALMethods and @ExporterSymbols.

The @Symbols array includes the contents of each of @Scalars, @Arrays, @Hashes,
@Functions and @Filehandles.

Similarly, @Barewords adds a few non-function keywords and operators to the
@Functions array.

%prep
%setup -q -n B-Keywords-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if 0%{!?perl_bootstrap:1} && %{with perl_B_Keywords_enables_extra_test}
make test IS_MAINTAINER=1 AUTHOR_TESTING=1
%else
make test
%endif

%files
%license LICENSE
%doc Changes
%{perl_vendorlib}/B/
%{_mandir}/man3/B::Keywords.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.21-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Paul Howarth <paul@city-fan.org> - 1.21-2
- Text::CSV_XS is wanted by t/z_kwalitee.t

* Wed Dec 18 2019 Robin Lee <cheeselee@fedoraproject.org> - 1.21-1
- Release 1.21 (RHBZ#1784567)
  - isa was added with 5.31.7
  - improved t/z_kwalitee.t

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-2
- Perl 5.30 rebuild

* Fri Feb 15 2019 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20
  - extern was added with 5.29.0c

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Paul Howarth <paul@city-fan.org> - 1.19-1
- Update to 1.19
  - our was added with 5.005_61

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - Added 5.27.8 changes: no whereis/-so

* Sun Dec 31 2017 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Added 5.27.7 changes (CPAN RT#123948)
  - Added cperl class keywords
  - Added keywords per version back to 5.004
- Drop legacy Group: tag
- Simplify find command using -delete

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-7
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Fixed $OUTPUT_AUTOFLUSH (CPAN RT#108572)
  - Made $* $MULTILINE_MATCHING version specific, deprecated with 5.8.1,
    removed with 5.10
- Explicitly require perl-devel, for CORE/keywords.h

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-2
- Perl 5.22 rebuild

* Sun Feb 22 2015 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Removed err from Barewords (CPAN RT#102259)
- Run the maintainer tests if we're not bootstrapping
- Expand %%description
- Use %%license

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.13-2
- Perl 5.18 rebuild

* Sat Apr  6 2013 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Removed diag before each big t/11keywords.t loop
  - Added lots of suggested keywords from CPAN RT#62382
  - Moved exp from @Barewords to @Functions
  - Added $^CHILD_ERROR_NATIVE $^GLOBAL_PHASE $^LAST_FH $^MATCH $^PREMATCH
    $^POSTMATCH $^UTF8CACHE $^WIN32_SLOPPY_STAT to @Scalars
  - Added English names for %%!, @F (perlrun) and @ARG for @_
  - Added %%+ %%- and $LAST_SUBMATCH_RESULT
- BR: perl(Test::Pod)
- Don't need to remove empty directories from the buildroot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug  1 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-4
- Add BR: perl(File::Spec), perl(lib), perl(Test), perl(Exporter)
- Clean up for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.12-2
- Perl 5.16 rebuild

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Add new keyword fc (Unicode casefolding) for 5.16
  - Added diag before each big t/11keywords.t loop
- This release by RURBAN -> update source URL
- Don't use macros for commands

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Add new keywords for 5.16: __SUB__ and evalbytes
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep  5 2010 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10 (fix typo in SYNOPSIS)
- This release by FLORA -> update source URL

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.09-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.09-2
- BR Test -> Test::More

* Sat Mar 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.09-1
- update to 1.09

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat May 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.08-2
- update buildrequires

* Sat Mar 15 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.08-1
- update to 1.08

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-4
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-3
- Rebuild for perl 5.10 (again), disable tests for first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-2
- rebuild normally, second pass

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-1.1
- rebuild for new perl
- disable Test-Pod-Coverage, tests for first pass

* Thu Feb 15 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sat Jan 20 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- First build.
