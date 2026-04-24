# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-UNIVERSAL-isa
Version:        1.20171012
Release: 25%{?dist}
Summary:        Hack around module authors using UNIVERSAL::isa as a function
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/UNIVERSAL-isa
Source0:        https://cpan.metacpan.org/modules/by-module/UNIVERSAL/UNIVERSAL-isa-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(overload)
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
# Dependencies
# (none)

%description
Whenever you use "isa" in UNIVERSAL as a function, a kitten using
Test::MockObject dies. Normally, the kittens would be helpless, but
if they use UNIVERSAL::isa (the module whose docs you are reading),
the kittens can live long and prosper.

This module replaces UNIVERSAL::isa with a version that makes sure
that if it's called as a function on objects which override isa,
isa will be called on those objects as a method.

In all other cases the real UNIVERSAL::isa is just called directly.

%prep
%setup -q -n UNIVERSAL-isa-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/UNIVERSAL/
%{_mandir}/man3/UNIVERSAL::isa.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep  9 2024 Paul Howarth <paul@city-fan.org> - 1.20171012-22
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Drop redundant %%{?perl_default_filter}
  - Drop redundant shellbang mangling
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely
  - Make %%files list more explicit
  - Package CONTRIBUTING file

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 1.20171012-21
- Convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-14
- Perl 5.36 rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20171012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 18 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20171012-1
- Update to 1.20171012

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20150614-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20150614-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20150614-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20150614-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20150614-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Tom Callaway <spot@fedoraproject.org> - 1.20150614-1
- update to 1.20150614

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140927-2
- Perl 5.22 rebuild

* Fri Mar 20 2015 Tom Callaway <spot@fedoraproject.org> - 1.2040927-1
- update to 1.20140927

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20120726-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.20120726-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Tom Callaway <spot@fedoraproject.org> - 1.20120726-1
- update to 1.20120726

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.03-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-7
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-6
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.03-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-1
- update to 1.01

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-5
- rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 0.06-4
- Update License-tag.

* Tue Dec 11 2007 Ralf Corsépius <rc040203@freenet.de> - 0.06-3
- Add BR: perl(Test::More).

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.06-2
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.06-1
- Update to 0.06.
- New files: Changes and README.

* Tue Jan 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-2
- Source URL correction.

* Tue Dec 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-1
- First build.
