# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Test-Requires
Summary:	Checks to see if a given module can be loaded
Version:	0.11
Release: 18%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Requires
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Requires-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:	perl(base)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Test::More) >= 0.47
# Runtime

%description
Test::Requires checks to see if the module can be loaded.

If this fails, rather than failing tests this skips all tests.

%prep
%setup -q -n Test-Requires-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
# note the "skipped" warnings indicate success :)
make test

%files
%license LICENSE
%doc Changes README.md t/ xt/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Requires.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.11-11
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-8
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-2
- Perl 5.32 rebuild

* Thu May 14 2020 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Re-packaging
- Drop running of extra tests at package build time to avoid need for
  bootstrapping
- Use %%{make_build} and %%{make_install}

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-17
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-16
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Paul Howarth <paul@city-fan.org> - 0.10-14
- Simplify find command using -delete
- Drop redundant buildroot cleaning in %%install section
- Drop redundant explicit %%clean section

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-12
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-8
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 0.10-5
- Adapt RPM version detection to SRPM build root without perl

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Support 5.6 again

* Tue Jul 21 2015 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Requires 5.8.1
- Use %%license where possible

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-4
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.20 rebuild

* Wed Jul 16 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Switch to ExtUtils::MakeMaker

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Petr Pisar <ppisar@redhat.com> - 0.07-5
- Specify all dependencies (bug #1066077)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Perl 5.18 rebuild

* Mon Jul  1 2013 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - If the RELEASE_TESTING environment variable is true, then instead of
    skipping tests, Test::Requires bails out
  - Document that use Test::Requires "5.010" works
- Switch to Module::Build flow
- Classify buildreqs by usage
- Package upstream's new LICENSE and README.md files
- Drop obsoletes/provides of perl-Test-Requires-tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.06-9
- BR: perl(base), perl(Cwd), perl(Data::Dumper)
- RHEL builds don't use Test::Spelling so they don't need dictionaries either

* Wed Aug 15 2012 Marcela Maslanova <mmaslano@redhat.com> - 0.06-8
- Conditionalize test packages

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.06-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.06-5
- Perl 5.16 rebuild

* Thu Mar 22 2012 Paul Howarth <paul@city-fan.org> - 0.06-4
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't need explicit runtime dependency on perl(Test::Builder::Module) if we
  have rpm ≥ 4.9 as it can auto-detect it
- BR: at least version 0.61 of perl(Test::More) as per upstream
- Drop unnecessary version requirement for perl(ExtUtils::MakeMaker)
- Drop redundant %%{?perl_default_filter}
- BR: aspell-en rather than hunspell-en on old distributions where
  Test::Spelling uses aspell instead of hunspell
- Don't BR: perl(Test::Perl::Critic) when bootstrapping
- Don't use macros for commands
- Don't need to remove empty directories from buildroot
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 0.06-3
- BR: hunspell-en rather than aspell-en (#731272)

* Thu Nov 18 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Run release tests as well as standard test suite in %%check
- Drop no-longer-needed buildreq perl(Filter::Util::Call)
- New buildreqs perl(Test::Perl::Critic), perl(Test::Pod), perl(Test::Spelling)

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> - 0.06-1
- Update to latest upstream version

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-2
- Mass rebuild with perl-5.12.0

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Specfile by Fedora::App::MaintainerTools 0.006


