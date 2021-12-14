# Run optional tests
%if ! (0%{?rhel})
%bcond_without perl_IPC_System_Simple_enables_optional_test
%else
%bcond_with perl_IPC_System_Simple_enables_optional_test
%endif

Name:		perl-IPC-System-Simple
Version:	1.30
Release:	2%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	Run commands simply, with detailed diagnostics
URL:		https://metacpan.org/release/IPC-System-Simple
Source0:	https://cpan.metacpan.org/modules/by-module/IPC/IPC-System-Simple-%{version}.tar.gz#/perl-IPC-System-Simple-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(re)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::More)
%if %{with perl_IPC_System_Simple_enables_optional_test}
# Optional Tests
BuildRequires:	perl(BSD::Resource)
BuildRequires:	perl(Test::NoWarnings)
%endif
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Calling Perl's in-built 'system()' function is easy; determining if it
was successful is _hard_. Let's face it, '$?' isn't the nicest variable
in the world to play with, and even if you _do_ check it, producing a
well-formatted error string takes a lot of work. 'IPC::System::Simple'
takes the hard work out of calling external commands. In fact, if you
want to be really lazy, you can just write:

    use IPC::System::Simple qw(system);

and all of your "system" commands will either succeed (run to completion and
return a zero exit value), or die with rich diagnostic messages.

%prep
%setup -q -n IPC-System-Simple-%{version}

# Avoid doc-file dependencies
chmod -c -x examples/*.pl

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
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/IPC/
%{_mandir}/man3/IPC::System::Simple.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.30-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 24 2020 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - On MSWin32, make Win32::Process a prerequisite

* Sun Mar 22 2020 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - Improved handling of shell commands on Windows, which should get us closer
    to resolving Win32-related issues; there should be no change of
    functionality on Unix-like platforms
  - Better workaround for bug in perl-5.8.9 (GH#129)
  - Add t/args.t
  - Modify t/win32.t
  - Added Travis and AppVeyor configuration files
  - Eliminated use of Dist::Zilla for build, using older, but more reliable and
    better understood (by maintainer) ExtUtils::MakeMaker-based configuration
  - Move author testing to xt/ directory

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - BUILD: Update FAIL_POSIX warning message (GH#28)
  - TEST: t/07_taint.t: Use executable name as source of taintedness (GH#21)
  - OTHER: Typographic corrections (CPAN RT#60211, CPAN RT#86403)
  - Add Travis configuration

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-23
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-22
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-19
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-18
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Petr Pisar <ppisar@redhat.com> - 1.25-16
- Fix random test failures with Test-Simple 1.302065

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-14
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-13
- Perl 5.26 rebuild

* Mon Apr 10 2017 Paul Howarth <paul@city-fan.org> - 1.25-12
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
- Introduce build-condition for optional tests
- Use %%license where possible
- Simplify find command using -delete
- Classify buildreqs by usage

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-10
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-6
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-5
- Perl 5.22 rebuild

* Tue Apr 21 2015 Petr Pisar <ppisar@redhat.com> - 1.25-4
- Break build-cycle: perl-IPC-System-Simple → perl-Test-Perl-Critic
  → perl-Perl-Critic → perl-PPI → perl-IO-All → perl-File-MimeInfo
  → perl-File-BaseDir → perl-IPC-System-Simple


* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 20 2013 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - No longer ship unrequired file Debian_CPANTS.txt (GH #7)

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24
  - No longer mark BSD::Resource as required (GH #6)
  - Skip core-dump tests on OS X; they're not as straightforward as the test
    script would like (GH #5)

* Wed Oct  9 2013 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23
  - Silence "Statement unlikely to be reached" warning
  - Repository information fix, and typo fixes
  - Converted to using dzil
- Specify all dependencies
- Don't need to remove empty directories from the buildroot
- Restore EL-5 compatibility

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.21-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 1.21-4
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.21-3
- Run author tests too for completeness
- Add buildreqs needed for author tests
- Add buildreqs for core perl modules, which may be dual-lived
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.21-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> - 1.21-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-4
- Mass rebuild with perl-5.12.0

* Mon Dec 07 2009 Stepan Kasal <skasal@redhat.com> - 1.18-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.18-1
- Submission

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.18-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

