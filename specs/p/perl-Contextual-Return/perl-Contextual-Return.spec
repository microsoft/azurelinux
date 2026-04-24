# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Contextual-Return
Version:        0.004014
Release: 27%{?dist}
Summary:        Create context-sensitive return values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Contextual-Return
Source0:        https://cpan.metacpan.org/modules/by-module/Contextual/Contextual-Return-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Want)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Test::More)
# Optional tests only
BuildRequires:  perl(Test::Pod) >= 1.14
# Dependencies
Requires:       perl(Data::Dumper)

%global __provides_exclude ^perl\\(DB\\)$

%description
This module allows you to define return values of a perl sub that are
appropriate given the calling context.

%prep
%setup -q -n Contextual-Return-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Contextual/
%{_mandir}/man3/Contextual::Return.3*
%{_mandir}/man3/Contextual::Return::Failure.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-12
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep  7 2019 Paul Howarth <paul@city-fan.org> - 0.004014-10
- Use author-independent source URL
- Modernize spec using %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.004014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.004014-2
- Perl 5.26 rebuild

* Fri Apr 14 2017 Paul Howarth <paul@city-fan.org> - 0.004014-1
- Update to 0.004014
  - Reverted to 0.004011 due to segfaults under optimized memory leak patch

* Wed Apr 12 2017 Paul Howarth <paul@city-fan.org> - 0.004012-1
- Update to 0.004012
  - Optimized previous patch for memory leak
  - Added missing test plan to t/fail.t
- Revert t/fail.t test plan change as test is quite flaky

* Sun Apr  9 2017 Paul Howarth <paul@city-fan.org> - 0.004011-1
- Update to 0.004011
  - Patched memory leak from use of @DB::args

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.004010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Paul Howarth <paul@city-fan.org> - 0.004010-1
- Update to 0.004010
  - Spelling fix in POD
  - Improved DUMP behaviour when passed a non-CRV argument

* Fri Nov 18 2016 Paul Howarth <paul@city-fan.org> - 0.004009-1
- Update to 0.004009
  - Improved behaviour of FREEZE
  - Improved output of DUMP
- Make %%files list more explicit

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.004008-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.004008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Petr Šabata <contyk@redhat.com> - 0.004008-1
- 0.004008 bump
- Modernize the spec

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.004007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.004007-7
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.004007-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.004007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.004007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.004007-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.004007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Iain Arnell <iarnell@gmail.com> 0.004007-1
- update to latest upstream version

* Fri Sep 07 2012 Iain Arnell <iarnell@gmail.com> 0.004005-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.004003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.004003-2
- Perl 5.16 rebuild

* Wed Apr 11 2012 Iain Arnell <iarnell@gmail.com> 0.004003-1
- update to latest upstream version

* Fri Mar 02 2012 Iain Arnell <iarnell@gmail.com> 0.004002-1
- update to latest upstream version

* Sat Feb 18 2012 Iain Arnell <iarnell@gmail.com> 0.004001-1
- update to latest upstream version

* Thu Jan 19 2012 Iain Arnell <iarnell@gmail.com> 0.003002-1
- update to latest upstream version

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> 0.003001-1
- update to latest upstream version
- drop explicit provides filtering; perl_default_filter already includes DB

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 0.2.1-11
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.2.1-10
- Perl mass rebuild

* Tue Apr 19 2011 Paul Howarth <paul@city-fan.org> - 0.2.1-9
- Filter provides in a way that works with rpm >= 4.9
- Fix typo in %%summary
- Fix argument order for find with -depth
- Run the whole test suite
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop buildroot specification and cleaning, no longer needed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2.1-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2.1-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.2.1-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2.1-2
- rebuild for new perl

* Fri Mar 30 2007 Chris Weyl <cweyl@alumni.drew.edu> v0.2.1-1
- update to v0.2.1

* Sat Mar 10 2007 Chris Weyl <cweyl@alumni.drew.edu> v0.2.0-1
- update to v0.2.0
- misc spec cleanups
- add br on perl(ExtUtils::MakeMaker) to satisfy any perl/perl-devel split

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-2
- bump for mass rebuild

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-1
- bump rel for f-e release

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-0.1
- filter unwanted provides
- add additional BR, the better to test with

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-0
- Initial spec file for F-E
