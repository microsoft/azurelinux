# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if ! (0%{?rhel})
%{bcond_without perl_Try_Tiny_enables_optional_test}
%else
%{bcond_with perl_Try_Tiny_enables_optional_test}
%endif

Name:		perl-Try-Tiny
Summary:	Minimal try/catch with proper localization of $@
Version:	0.32
Release: 4%{?dist}
License:	MIT
URL:		https://metacpan.org/release/Try-Tiny
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Util)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More) >= 0.96
# Optional Tests
%if %{with perl_Try_Tiny_enables_optional_test}
BuildRequires:	perl(Capture::Tiny) >= 0.12
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Check) >= 0.011
BuildRequires:	perl(CPAN::Meta::Requirements)
%endif
# Dependencies
Requires:	perl(Sub::Util)

# Do not provide private modules from tests packaged as a documentation
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}/

%description
This module provides bare bones try/catch statements that are designed to
minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch, which provides a nice syntax and avoids adding
another call stack layer, and supports calling return from the try block to
return from the parent subroutine. These extra features come at a cost of a
few dependencies, namely Devel::Declare and Scope::Upper that are occasionally
problematic, and the additional catch filtering uses Moose type constraints,
which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

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
%license LICENCE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/Try/
%{_mandir}/man3/Try::Tiny.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 17 2024 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Skip given, when tests on perls ≥ 5.41.3, which removed these constructs

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 24 2021 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Plug Syntax::Keyword::Try and Feature::Compat::Try in the docs

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Expand "when" test skippage to more perl versions

* Tue Dec 19 2017 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29
  - Skip tests of "when" and "given/when" usage for perl 5.27.7 *only*
    (see CPAN RT#123908)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  9 2017 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - Enabled some tests of finally blocks that were disabled on 5.6, now that
    that functionality works (since 0.13) (GH#4)

* Tue Aug 16 2016 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - "finally" blocks are now run for all methods of leaving the try block
     (including via exit, goto) (CPAN RT#112099)
  - Switch from finalizers using an array to a hash, to resolve segfaults when
    creating a pseudofork on MSWin before perl 5.20
    (karenetheridge/Sub-Name/#3)
  - Repository moved to the github p5sagit organization (the primary is on
    shadowcat, mirrored to github)
- BR: perl-generators
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix syntax of example code (PR#22)
  - 'perl' removed from prerequisite recommendations, to avoid tripping up CPAN
    clients
  - Sub::Util is used preferentially to Sub::Name in most cases (PR#27)
- This release by ETHER → update source URL
- Modernize spec
- Don't run the extra tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-5
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 0.22-4
- Correct dependencies

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Add optional test deps as recommended prereqs
    (https://github.com/doy/try-tiny/pull/18)
- Update patch for building with Test::More < 0.88

* Tue Apr 15 2014 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Also skip the test if Capture::Tiny is too old
    (https://github.com/doy/try-tiny/issues/17)

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Documentation updates
- Update patch for building with Test::More < 0.88

* Thu Jan 23 2014 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - Fix an obscure issue with loading modules during global destruction
    (https://github.com/doy/try-tiny/pull/11)
  - Documentation updates (https://github.com/doy/try-tiny/pull/12)
- Add patch to support building with Test::More < 0.88 again

* Sat Aug 17 2013 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Fix tests for pre-Test-More-0.88 (https://github.com/doy/try-tiny/pull/10)
- Drop upstreamed patch for building with Test::More < 0.88

* Sat Aug 17 2013 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Work around Perl RT#119311, which was causing incorrect error messages in
    some cases during global destruction
    (https://github.com/doy/try-tiny/pull/9)
- Add patch to support building with Test::More < 0.88

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.18 rebuild

* Wed Jul 10 2013 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Remove accidental Sub::Name test dependency

* Tue Jul  9 2013 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Optionally use Sub::Name to name the try/catch/finally blocks, if available
- BR:/R: perl(Sub::Name)
- Drop obsoletes/provides for old -tests subpackage

* Sat Jul  6 2013 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Also throw an exception for catch/finally in scalar context (CPAN RT#81070)

* Fri Jul  5 2013 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Fix tests failing on 5.6.x due to differing DESTROY semantics
  - Excise superfluous local($@) call - 7%% speedup
  - Fix broken URLs (CPAN RT#55659)
  - Proper exception on erroneous usage of bare catch/finally (CPAN RT#81070)
  - Proper exception on erroneous use of multiple catch{} blocks
  - Clarify exception occuring on unterminated try block (CPAN RT#75712)
  - Fix the prototypes shown in docs to match code (CPAN RT#79590)
  - Warn loudly on exceptions in finally() blocks
  - dzilify
- Ship upstream LICENSE and README files
- Classify buildreqs by usage
- Add buildreqs for extra tests and explicitly run them

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Documentation fixes

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Add BR/R perl(Exporter)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.11-5
- Perl 5.16 rebuild

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 0.11-4
- BR: perl(Carp)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop redundant %%{?perl_default_filter}
- Enhance %%description
- Reinstate EPEL-5 compatibility:
  - Define buildroot
  - Clean buildroot in %%install and %%clean
- Use tabs

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> - 0.11-3
- Drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 0.11-1
- Update to latest upstream version

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> - 0.09-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Allow multiple finally blocks
  - Pass the error, if any, to finally blocks when called
  - Documentation fixes and clarifications
- This release by RJBS -> update source URL

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-2
- Mass rebuild with perl-5.12.0

* Tue Mar 02 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- Updating to latest GA CPAN version (0.04)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-2
- Rebuild against perl 5.10.1

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Submission

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
