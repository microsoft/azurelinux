Name:           perl-Test-Deep
Version:        1.204
Release:        1%{?dist}
Summary:        Extremely flexible deep comparison
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-Deep
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Deep-%{version}.tar.gz#/perl-Test-Deep-%{version}.tar.gz
Source1:        LICENSE.PTR
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util) >= 1.09
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Tester) >= 0.04
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Test::Builder)

%description
Test::Deep gives you very flexible ways to check that the result you
got is the result you were expecting. At its simplest it compares two
structures by going through each level, ensuring that the values
match, that arrays and hashes have the same elements and that
references are blessed into the correct class. It also handles
circular data structures without getting caught in an infinite loop.

%prep
%setup -q -n Test-Deep-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

cp %{SOURCE1} .

%check
make test

%files
%license LICENSE.PTR
%doc Changes README TODO
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Deep.3*
%{_mandir}/man3/Test::Deep::NoTest.3*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.204-1
- Auto-upgrade to 1.204 - Azure Linux 3.0 - package upgrades

* Thu Aug 04 2022 Muhammad Falak <mwani@microsoft.com> - 1.130-3
- Add `%license`
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.130-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Mar  2 2020 Paul Howarth <paul@city-fan.org> - 1.130-1
- Update to 1.128
  - Allow 'use Test::Deep' while other modules use Test::Deep::NoTest (GH#76)
  - Added true/false optional imports (GH#41, GH#44)
  - Documentation fixes (GH#79)
- Use author-independent source URL

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.128-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.128-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.128-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.128-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.128-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.128-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 1.128-1
- Update to 1.128
  - Numerous small improvements to documentation
  - Improved CI setup

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.127-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.127-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.127-2
- Perl 5.26 rebuild

* Thu May  4 2017 Paul Howarth <paul@city-fan.org> - 1.127-1
- Update to 1.127
  - Do not eagerly convert simple scalars into tests in the all, any and none
    tests; this was breaking LeafWrapper application
- Drop EL-5-isms
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.126-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan  1 2017 Paul Howarth <paul@city-fan.org> - 1.126-1
- Update to 1.126
  - If objects in the "expected" structure have an as_test_deep_cmp method, it
    will be called and its return (which should be a Test::Deep::Cmp object)
    will be used as the test for that location in the structure
  - Internal undocumented class_base routine has been replaced with a
    different, clearly private routine
  - The LeafWrapper is also used for objects with an unknown reftype (like
    LVALUE or other weird ones)

* Sun Nov  6 2016 Paul Howarth <paul@city-fan.org> - 1.124-1
- Update to 1.124
  - Avoid an uninitialized warning when array_each() compares to a
    non-reference

* Sat Sep 10 2016 Paul Howarth <paul@city-fan.org> - 1.123-1
- Update to 1.123
  - Remove test suite reliance on "." appearing @INC
  - When an object with stringification overloading fails to match a "re" test,
    its stringification is included in the diagnostics

* Thu Sep  8 2016 Paul Howarth <paul@city-fan.org> - 1.122-1
- Update to 1.122
  - Added $Test::Deep::LeafWrapper to control the behavior of simple values in
    the "expected" definition
  - Documentation improvements
  - Avoid a few evals, localize $@ in a few places where eval is used
  - Goodbye tabs, hello spaces
- BR: perl-generators
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.120-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Paul Howarth <paul@city-fan.org> - 1.120-1
- Update to 1.120
  - Add none() test; it's like any(), but negative
  - Fix stringification of any() expectations

* Wed Sep 30 2015 Paul Howarth <paul@city-fan.org> - 0.119-1
- Update to 0.119
  - Overloading of & and | no longer can change All or Any objects found as
    arguments
  - An All as an argument to an All constructed is flattened out into its
    All-ed values; the same goes for Any
  - Remove use of Test::NoWarnings for user-facing tests

* Mon Jun 22 2015 Paul Howarth <paul@city-fan.org> - 0.117-1
- Update to 0.117
  - Do not lose argument(s) to import
    (https://github.com/rjbs/Test-Deep/issues/29)

* Sun Jun 21 2015 Paul Howarth <paul@city-fan.org> - 0.116-1
- Update to 0.116
  - On its own, :preload options uses default group of exports

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.115-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.115-2
- Perl 5.22 rebuild

* Sat Jan 10 2015 Paul Howarth <paul@city-fan.org> - 0.115-1
- Update to 0.115
  - Worked around a bug in chained goto on 5.8.5

* Mon Dec 15 2014 Paul Howarth <paul@city-fan.org> - 0.114-1
- Update to 0.114
  - Improve prereqs metadata
  - Add a noneof() set test
  - regexponly hasn't worked... ever; now it does
  - Passing :preload to import loads all plugins up front
  - A few more tests have been documented
  - The many exports of Test::Deep are now documented!

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 0.113-1
- Update to 0.113
  - Fix a compile error (!!) in RegexpOnly
  - Fix some documentation typos
  - Add license to META file

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.112-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 30 2013 Paul Howarth <paul@city-fan.org> - 0.112-1
- Update to 0.112
  - When printing diagnostics, differentiate the type of a blessed object from
    the name of the class itself (CPAN RT#78288)
  - Typo fixes
  - Fixes to clarity and accuracy of documentation
  - Add metadata links to repo and issue tracker
  - Added obj_isa for testing ->isa without falling back to ref($x)
  - Added the *experimental* ":v1" export group to skip importing Isa, isa, and
    blessed

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.110-2
- Perl 5.18 rebuild

* Wed Feb 20 2013 Paul Howarth <paul@city-fan.org> - 0.110-1
- Update to 0.110
  - Allow methods() and listmethods() to work again on class methods
    (CPAN RT#77804)
- Drop redundant BR: perl(Data::Dumper)
- Drop arrayeach patch - similar change introduced upstream
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.108-6
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.108-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.108-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat Dec 18 2010 Steven Pritchard <steve@kspei.com> 0.108-1
- Update to 0.108.
- Update Source0 URL.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.106-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 0.106-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Lubomir Rintel <lubo.rintel@gooddata.com> 0.103-2
- Fix crash on matching array_each() against non-array

* Wed Jun 04 2008 Steven Pritchard <steve@kspei.com> 0.103-1
- Update to 0.103.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 0.102-1
- Update to 0.102.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.101-1
- Update to 0.101.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.100-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.100-1
- Update to 0.100.

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.099-1
- Update to 0.099.
- Update License tag.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.098-1
- Update to 0.098.

* Fri Aug 10 2007 Steven Pritchard <steve@kspei.com> 0.097-1
- Update to 0.097.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.096-2
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 0.096-1
- Update to 0.096.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.095-2
- Fix find option order.

* Fri Apr 21 2006 Steven Pritchard <steve@kspei.com> 0.095-1
- Update to 0.095.

* Sat Apr 08 2006 Steven Pritchard <steve@kspei.com> 0.093-1
- Specfile autogenerated by cpanspec 1.64.
- Improve description.
- Fix License.
- Remove explicit dependency on Test::Tester and Test::NoWarnings.
