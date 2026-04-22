# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Test-Class
Version:        0.52
Release: 14%{?dist}
Summary:        Easily create test classes in an xUnit/JUnit style
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Class
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Class-%{version}.tar.gz
Patch0:         perl-Test-Class-UTF8.patch
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Attribute::Handlers) >= 0.77
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(MRO::Compat) >= 0.11
BuildRequires:  perl(Storable) >= 2.04
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder) >= 0.78
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(IO::File) >= 1.09
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::Exception) >= 0.25
BuildRequires:  perl(Test::More) >= 1.001002
# Optional tests:
BuildRequires:  perl(Contextual::Return)
Requires:       perl(Attribute::Handlers) >= 0.77
Requires:       perl(MRO::Compat) >= 0.11
Requires:       perl(Storable) >= 2.04
Requires:       perl(Test::Builder) >= 0.78

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Attribute::Handlers|MRO::Compat|Storable|Test::Builder)\\)$

%description
Test::Class provides a simple way of creating classes and objects to test
your code in an xUnit style.

%prep
%setup -q -n Test-Class-%{version}

# Fix up broken permissions
find -type f -exec chmod -c -x {} \;

# Fix character encoding in documentation
%patch -P0

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
%{_mandir}/man3/Test::Class.3*
%{_mandir}/man3/Test::Class::Load.3*
%{_mandir}/man3/Test::Class::MethodInfo.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-2
- Perl 5.34 rebuild

* Wed Feb 17 2021 Paul Howarth <paul@city-fan.org> - 0.52-1
- Update to 0.52
  - Create fail_if_returned_late (GH#23)
  - Change bugtracker link to point GitHub issues instead of RT
  - Remove some old and broken links
  - Test fix (GH#32)
  - Fix reporting caller information (file+line) when number of tests does not
    match
  - Use better class names in t/runtests_return.t
  - Fix documentation to be more accurate regarding support and author activity
  - Ensure metadata is processed as v2
  - Remove unnecessary shebangs
  - chmod ugo-x

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-17
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep  7 2019 Paul Howarth <paul@city-fan.org> - 0.50-15
- Use author-independent source URL
- Specify all build dependencies
- Simplify find command using -delete
- Drop redundant buildroot cleaning in %%install section

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-2
- Perl 5.22 rebuild

* Sun Jun  7 2015 Paul Howarth <paul@city-fan.org> - 0.50-1
- Update to 0.50
  - Add links to Ovid's tutorial series on Test::Class (PR#19)
  - Add links to Test::Class::Most, Test::Class::Moose (PR#20)
  - List some distributions that use Test::Class in their test suite (PR#21)
  - Update documentation about running individual tests (PR#22)
  - Fix some tests to work with the new Test::Stream (PR#27)
  - Switch packaging to ExtUtils::MakeMaker

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-2
- Perl 5.22 rebuild

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 0.48-1
- Update to 0.48
  - Replace a few bare evals with more modern alternatives

* Mon Sep 29 2014 Paul Howarth <paul@city-fan.org> - 0.47-1
- 0.47 bump; test and documentation changes only
- Drop Module::Build version patch since we need a later Test::More than is in
  EL-7
- No need to clean the buildroot

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-2
- Perl 5.20 rebuild

* Mon Jul  7 2014 Paul Howarth <paul@city-fan.org> - 0.46-1
- 0.46 bump

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 0.45-1
- 0.45 bump

* Mon Jun 30 2014 Petr Šabata <contyk@redhat.com> - 0.43-1
- 0.43; META changes only

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May  8 2014 Paul Howarth <paul@city-fan.org> - 0.42-1
- Update to 0.42
  - Properly handle thrown exceptions that stringify to the empty string before
    or after chomping (https://github.com/adrianh/test-class/pull/11)
- This release by ETHER -> update source URL
- Drop workaround for CPAN RT#85106, no longer needed

* Tue Jan 21 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.41-1.1
- Make it build for el7

* Sat Nov 30 2013 Paul Howarth <paul@city-fan.org> - 0.41-1
- Update to 0.41
  - Require a newer Test::Builder if 0.99 is installed (CPAN RT#90699)

* Fri Nov 15 2013 Paul Howarth <paul@city-fan.org> - 0.40-1
- Update to 0.40
  - Test::Class failed on Test::Builder 0.99 (CPAN RT#89473)
- This release by RJBS -> update source URL
- Drop now-redundant test patch
- Use a patch to fix the documentation character encoding
- Drop %%defattr, redundant since rpm 4.4
- Make the %%files list more explicit
- No need to remove empty directories from the buildroot
- Don't use macros for commands
- Work around annoying noise from TAP::Parser::SourceHandler::Perl version 3.28
  (CPAN RT#85106)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
- Adjust to Test-Simple 0.98_04 (bug #992734)

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.39-2
- Perl 5.18 rebuild

* Thu Apr 18 2013 Petr Pisar <ppisar@redhat.com> - 0.39-1
- 0.39 bump

* Wed Feb 20 2013 Petr Pisar <ppisar@redhat.com> - 0.38-1
- 0.38 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.36-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.36-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.36-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 10 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.36-1
- Update to 0.36 (Fix FTBFS: BZ 661059).
- Update Source0-URL.
- Cleanup BuildRequires/Requires, spec-file overhaul.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.33-2
- rebuild against perl 5.10.1

* Mon Sep 21 2009 Steven Pritchard <steve@kspei.com> 0.33-1
- Update to 0.33.
- Update Source0 URL.
- Add LICENSE.
- BR Test::Pod, Test::CPAN::Meta, and Test::MinimumVersion and define
  AUTOMATED_TESTING for better test coverage.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.
- BR Test::Builder.
- Add versioned dependencies to Test::Builder::Tester and Test::More.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.30-1
- Update to 0.30.

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28.
- Update License tag.
- Bump Test::Exception requirement to 0.25.

* Mon Jul 16 2007 Steven Pritchard <steve@kspei.com> 0.24-1
- Specfile autogenerated by cpanspec 1.71.
- BR Contextual::Return, Test::Builder::Tester, and Test::More.
- Drop explicit perl BR.
