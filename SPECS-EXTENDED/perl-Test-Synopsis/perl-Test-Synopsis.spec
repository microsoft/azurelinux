Vendor:         Microsoft Corporation
Distribution:   Mariner
# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Test-Synopsis
Version:	0.16
Release:	7%{?dist}
Summary:	Test your SYNOPSIS code
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Test-Synopsis
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Synopsis-%{version}.tar.gz#/perl-Test-Synopsis-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(ExtUtils::Manifest)
BuildRequires:	perl(parent)
BuildRequires:	perl(Pod::Simple) >= 3.09
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::Builder) >= 0.34
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(blib)
# Extra Tests; can't run these when bootstrapping or in EL since many
# of these packages won't be available
%if 0%{!?perl_bootstrap:1} && 0%{!?rhel:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Pod::Wordlist) >= 1.06
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Kwalitee) >= 1.21
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Mojibake)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling) >= 0.23, hunspell-en
BuildRequires:	perl(Test::Version)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Test::Builder::Module)

%description
Test::Synopsis is an (author) test module to find .pm or .pod files under your
lib directory and then make sure the example snippet code in your SYNOPSIS
section passes the perl compile check.

Note that this module only checks the perl syntax (by wrapping the code with
sub) and doesn't actually run the code.

%prep
%setup -q -n Test-Synopsis-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if 0%{!?perl_bootstrap:1} && 0%{!?rhel:1}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README README.md
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Synopsis.3*

%changelog
* Mon Apr 25 2022 Muhammad Falak <mwani@microsoft.com> - 0.16-7
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-2
- Perl 5.30 rebuild

* Tue May 28 2019 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Fix test failures when version 0.23 of Test::Spelling is in use (GH#21)

* Fri May 24 2019 Paul Howarth <paul@city-fan.org> - 0.15-14
- Simpler fix for FTBFS with Test::Spelling 0.23 (#1713565)

* Fri May 24 2019 Petr Pisar <ppisar@redhat.com> - 0.15-13
- Correct a spelling test (bug #1713565)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-10
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-9
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-6
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.24 rebuild

* Thu Mar  3 2016 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Require Pod::Simple ≥ 3.09, as needed feature missing from older versions

* Wed Feb 17 2016 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Complete rewrite by dolmen
  - The undocumented PRIVATE subroutine extract_synopsis has been renamed; any
    code using it will break

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan  5 2016 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Fix #12 (conflict with multiple chunks)

* Mon Dec 28 2015 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Add META.json
- Re-enable use of Test::Vars with Perl 5.22

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.22 re-rebuild of bootstrapped packages
- Disable using of Test::Vars with Perl 5.22

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-2
- Perl 5.22 rebuild

* Thu Oct  9 2014 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Added #10 to CAVEATS (redefined warnings)
  - Fixed #11 (failing tests on newer perls)
- Use %%license where possible

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb  7 2014 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Fixed prereqs to allow earlier versions of Test-Simple (Issue #9)
  - Removed POD errors from test .pm's to increase Kwalitee
  - Reverted the change of renaming extract_synopsis() to _extract_synopsis(),
    as it appears some distros have used undocumented extract_synopsis() in
    their user tests, and the change is causing their distros to fail
  - Added contributors into META file through dzil plugin

* Wed Feb  5 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Implemented proper handling of __DATA__ tokens
  - Removed unwanted warnings issued during tests
  - Upped required Test-Simple distro version (fixes Issue #9)
  - Minor pod fixes

* Wed Feb  5 2014 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Converted to dzil for automation of everything and auto-generation of all
    the author/release tests and extra files
  - Fixed CPAN RT#84863: Should ignore descriptions, and other text that is not
    code
  - Fixed CPAN RT#76856: Sandbox breaks when combining synopses that use Moose
    and Moose::Role
  - Fixed CPAN RT#69438: Heredocs fail to terminate because of the leading
    space for verbatim blocks
  - Fixed CPAN RT#54731: Suggest =for conditionalized synopsis check
  - Fixed CPAN RT#53192: Missing Copyright information for Test::Synopsis
  - Fixed CPAN RT#52684: Pod directive to skip Test::Synopsis
  - Fixed CPAN RT#51534: End =for at blank line
  - Fixed CPAN RT#51535: Show failing code on error
- This release by ZOFFIX -> update source URL
- Package upstream's LICENSE and README.md files
- Classify buildreqs by usage

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-19
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.06-17
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-15
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.06-13
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.06-12
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.06-11
- Separate bootstrap and RHEL conditionals
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from buildroot
- BR: perl(base)

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-10
- Conditionalize aspell-en & friends

* Wed Jan 25 2012 Paul Howarth <paul@city-fan.org> - 0.06-9
- Can run spelling test unconditionally now
- BR: perl(ExtUtils::Manifest)
- Don't BR: perl(Test::Perl::Critic) if we're bootstrapping
- Use %%{_fixperms} macro rather than our own chmod incantation
- Run developer tests in a separate test run
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 15 2010 Paul Howarth <paul@city-fan.org> - 0.06-4
- Whittle down for Fedora submission

* Mon May 17 2010 Paul Howarth <paul@city-fan.org> - 0.06-3
- Fix dist tag for RHEL-6 Beta

* Tue Feb  2 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Add buildreq perl(Test::Perl::Critic) if we have Perl 5.8.8 or later

* Fri Nov 27 2009 Paul Howarth <paul@city-fan.org> - 0.06-1
- Initial RPM version
