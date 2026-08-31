# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Test-Perl-Critic
Summary:	Use Perl::Critic in test programs
Version:	1.04
Release:	25%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Perl-Critic
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Perl-Critic-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Module::Build) >= 0.40
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(English)
BuildRequires:	perl(Perl::Critic) >= 1.105
BuildRequires:	perl(Perl::Critic::Utils) >= 1.105
BuildRequires:	perl(Perl::Critic::Violation) >= 1.105
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder) >= 0.88
BuildRequires:	perl(warnings)
# Optional Runtime
BuildRequires:	perl(MCE::Grep) >= 1.827
# Test Suite
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(MCE::Grep) >= 1.827
Requires:	perl(Perl::Critic) >= 1.105
Requires:	perl(Perl::Critic::Utils) >= 1.105
Requires:	perl(Perl::Critic::Violation) >= 1.105
Requires:	perl(Test::Builder) >= 0.88

# Avoid doc-file dependencies from tests
%{?perl_default_filter}

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Perl::Critic\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Perl::Critic::Utils\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Perl::Critic::Violation\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Builder\\)$

%description
Test::Perl::Critic wraps the Perl::Critic engine in a convenient
subroutine suitable for test programs written using the Test::More
framework. This makes it easy to integrate coding-standards enforcement
into the build process. For ultimate convenience (at the expense of some
flexibility), see the criticism pragma.

%prep
%setup -q -n Test-Perl-Critic-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%license LICENSE
%doc Changes README t/ xt/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Perl::Critic.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.04-19
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-16
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 31 2021 Paul Howarth <paul@city-fan.org> - 1.04-14
- Use %%license unconditionally

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 30 2019 Paul Howarth <paul@city-fan.org> - 1.04-7
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-2
- Perl 5.28 rebuild

* Tue Mar 27 2018 Paul Howarth <paul@city-fan.org> - 1.04-1
- Update to 1.04
  - Sped up critic_ok() by 4x by not recreating a Perl::Critic object over and
    over (GH#10)
  - Now requires Test::Builder~0.88 or later to support the done_testing()
    method (GH#2)
  - Now requires MCE 1.827 to deal with problems running under taint mode (GH#6)
- This release by PETDANCE → update source URL
- Drop BuildRoot: and Group: tags

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Wed Feb  4 2015 Paul Howarth <paul@city-fan.org> - 1.03-1
- Update to 1.03
  - all_critic_ok() will now run tests in parallel over multiple cores. So if
    you have 8 cores, your Perl::Critic tests could run 8x faster. However,
    the actual performance depends on the size and shape of your code base and
    your Perl::Critic configuration.
  - If you're using the critic_ok() function directly (perhaps because you want
    more control over which files are tested) then you won't see any
    performance boost. I recommend gathering your list of files first, and then
    passing the list to all_critic_ok().
  - The deprecated function all_code_files() has now been removed from
    Test::Perl::Critic. Use Perl::Critic::Utils::all_perl_files() instead.
- Classify buildreqs by usage
- Drop obsoletes/provides for old -tests package
- Use %%license where possible

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.02-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.02-8
- Perl 5.16 rebuild

* Wed Mar 21 2012 Paul Howarth <paul@city-fan.org> - 1.02-7
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Drop redundant BR: perl(ExtUtils::MakeMaker)
- Drop redundant unversioned explicit requires
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands
- Run the author tests in %%check
- BR: perl(Test::Pod) and perl(Test::Pod::Coverage)
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.02-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.02-1
- Update by Fedora::App::MaintainerTools 0.006
- Updating to latest GA CPAN version (1.02)
- Added a new br on perl(Carp) (version 0)
- Added a new br on perl(English) (version 0)
- Altered br on perl(Module::Build) (0 => 0.35)
- Altered br on perl(Perl::Critic) (0.21 => 1.105)
- Added a new br on perl(Perl::Critic::Utils) (version 1.105)
- Added a new br on perl(Perl::Critic::Violation) (version 1.105)
- Added a new br on perl(Test::Builder) (version 0)
- Added a new br on perl(Test::More) (version 0)
- Force-adding ExtUtils::MakeMaker as a BR
- Dropped old BR on perl(Test::Pod)
- Dropped old BR on perl(Test::Pod::Coverage)
- Added a new req on perl(Carp) (version 0)
- Added a new req on perl(English) (version 0)
- Added a new req on perl(Perl::Critic) (version 1.105)
- Added a new req on perl(Perl::Critic::Utils) (version 1.105)
- Added a new req on perl(Perl::Critic::Violation) (version 1.105)
- Added a new req on perl(Test::Builder) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.01-8
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-5
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-4
- Disable tests, take out patch, doesn't fix test failures

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-3
- Patch for test failure

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-2
- Rebuild for new perl

* Sat Jan 27 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01

* Sun Nov 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-1
- Update to 0.08

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.07-1
- First build
