Name:		perl-Test-EOL
Version:	2.00
Release:	12%{?dist}
Summary:	Check the correct line endings in your project
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Test-EOL
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-EOL-%{version}.tar.gz#/perl-Test-EOL-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Optional Tests
%if "%{?rhel}" != "6"
BuildRequires:	perl(CPAN::Meta) >= 2.120900
%endif
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module scans your project/distribution for any perl files (scripts,
modules, etc.) with Windows line endings. It can also check for trailing
whitespace.

%prep
%setup -q -n Test-EOL-%{version}

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
%license LICENCE
%else
%doc LICENCE
%endif
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::EOL.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.00-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Paul Howarth <paul@city-fan.org> - 2.00-10
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-8
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-2
- Perl 5.26 rebuild

* Thu May  4 2017 Paul Howarth <paul@city-fan.org> - 2.00-1
- Update to 2.00
  - Update documentation for starting point change in version 1.5
  - Check *.pod files as well as *.pm, *.pl and *.t (CPAN RT#82032)
  - Repository has moved to GitHub
- This release by ETHER → update source URL
- Simplify find command using -delete
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 31 2015 Paul Howarth <paul@city-fan.org> - 1.6-1
- Update to 1.6
  - Add 'no_test' import option to allow more composability
- This release by FREW → update source URL
- Use %%license where possible
- Classify buildreqs by usage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-7
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 1.5-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep  9 2012 Paul Howarth <paul@city-fan.org> - 1.5-1
- Update to 1.5
  - Properly fix Win32 (CPAN RT#76037)
  - Change default to searching for trailing whitespace from the current
    directory downwards (as tests are run from the top of a dist normally),
    rather than one directory above the test file, as then we don't work as
    expected if tests are in t/author or similar
- BR: perl(Pod::Coverage::TrustPod) even when bootstrapping

* Tue Aug  7 2012 Paul Howarth <paul@city-fan.org> - 1.3-6
- Reinstate EPEL-5 compatibility
- Drop redundant patch for building with ExtUtils::MakeMaker < 6.30

* Tue Aug  7 2012 Jitka Plesnikova <jplesnik@redhat.com>
- Update BR and clean up spec for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.3-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.3-2
- Perl 5.16 rebuild

* Sun Jun 17 2012 Paul Howarth <paul@city-fan.org> - 1.3-1
- Update to 1.3
  - Fix to ignore inc/ directory used by Module::Install
- Drop hack to remove tabs from bundled Module::Install
- Bump version requirement for perl(Test::NoTabs) to 1.2 to avoid failing
  release tests due to tabs in bundled Module::Install

* Fri Jun 15 2012 Paul Howarth <paul@city-fan.org> - 1.2-1
- Update to 1.2
  - Fix bad regex matching directories containing 'svn', not just '.svn'
    directories (CPAN RT#75968)
- BR: perl(Cwd)
- Drop non-dual-lived buildreqs perl(File::Find) and perl(FindBin)
- This release by BOBTFISH -> update source URL
- Remove tabs from bundled Module::Install that break release tests
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.1-2
- Perl 5.16 rebuild

* Mon Jan 16 2012 Paul Howarth <paul@city-fan.org> - 1.1-1
- Update to 1.1
  - Fix test fails on < 5.8 perls
  - Fix t/13-latin1.t failures on Win32 and under TB1.5
- Add buildreqs for required core modules, which might be dual-lived

* Thu Jan  5 2012 Paul Howarth <paul@city-fan.org> - 1.0-1
- Update to 1.0
  - Fix misleading test failure diagnostics when only issue is trailing
    whitespace
  - No longer blindly assume utf8 on input files (CPAN RT#59877)
  - Properly document testing options
- This release by RIBASUSHI -> update source URL
- Drop upstreamed patch for CPAN RT#59877
- Update patch for building with old ExtUtils::MakeMaker versions

* Thu Jun 30 2011 Paul Howarth <paul@city-fan.org> - 0.9-5
- Restore EPEL-4 compatibility
- perl(Pod::Coverage::TrustPod) is available everywhere now
- %%{?perl_default_filter} isn't needed for this tiny package
- Nobody else likes macros for commands

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9-4
- Perl mass rebuild
- Add macro perl_bootstrap

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Paul Howarth <paul@city-fan.org> - 0.9-2
- Don't assume tested files are UTF-8 encoded (CPAN RT#59877)

* Wed Jun 16 2010 Paul Howarth <paul@city-fan.org> - 0.9-1
- Update to 0.9 (fix warnings on very old perls - CPAN RT#58442)
- Use DESTDIR instead of PERL_INSTALL_ROOT
- Add %%{?perl_default_filter}

* Wed Jun 16 2010 Paul Howarth <paul@city-fan.org> - 0.8-1
- Initial RPM version
