Name:		perl-Test-Distribution
Version:	2.00
Release:	34%{?dist}
Summary:	Perform tests on all modules of a distribution
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Test-Distribution
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Distribution-%{version}.tar.gz#/perl-Test-Distribution-%{version}.tar.gz
Patch0:		Test-Distribution-2.00-utf8.patch
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Module::Build)
# Module
BuildRequires:	perl(ExtUtils::Manifest)
BuildRequires:	perl(File::Find::Rule) >= 0.03
BuildRequires:	perl(Module::CoreList) >= 1.93
BuildRequires:	perl(Module::Signature)
BuildRequires:	perl(Pod::Coverage) >= 0.17
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 0.95
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
# (no additional dependencies)
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# these are considered "optional"; autoreq doesn't pick them up
Requires:	perl(File::Find::Rule) >= 0.03
Requires:	perl(Module::CoreList) >= 1.93
Requires:	perl(Module::Signature)
Requires:	perl(Pod::Coverage) >= 0.17
Requires:	perl(Test::Pod) >= 0.95
Requires:	perl(Test::Pod::Coverage)

%description
When using this module in a test script, it goes through all the modules in
your distribution, checks their POD, checks that they compile OK and checks
that they all define a $VERSION.

%prep
%setup -q -n Test-Distribution-%{version}

# Fix character encoding of documentation
%patch0

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%doc Changes.pod README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Distribution.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.00-34
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 2.00-32
- Spec tidy-up
  - Use author-independent source URL
  - Classify builds by usage
  - Drop redundant buildroot cleaning in %%install section
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-30
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-27
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-24
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-22
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-19
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-18
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 2.00-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.00-12
- Perl 5.16 rebuild

* Sat Mar 10 2012 Paul Howarth <paul@city-fan.org> - 2.00-11
- BR:perl(ExtUtils::Manifest) and perl(Test::More)
- Drop workarounds for no-longer-shipped signature test
- Drop BR: perl(Module::Signature)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.00-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.00-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.00-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.00-5
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> - 2.00-2
- Changes -> Changes.pod in doc

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> - 2.00-1
- Update to 2.00

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-5
- Rebuild for new perl

* Sat Mar 10 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.26-4
- Don't mess with debuginfo, just disable it
- Appease Module::Signature/gpg

* Thu Mar 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.26-3
- Cause rm to not fail on non-existance of debug*list in %%check

* Wed Dec 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.26-2
- Bump

* Wed Dec 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.26-1
- Specfile autogenerated by cpanspec 1.69.1
