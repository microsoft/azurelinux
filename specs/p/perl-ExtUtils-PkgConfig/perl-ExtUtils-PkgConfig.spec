# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-ExtUtils-PkgConfig
Version:        1.16
Release:        27%{?dist}
Summary:        Simplistic interface to pkg-config
License:        LGPL-2.0-or-later
URL:            https://metacpan.org/release/ExtUtils-PkgConfig
Source0:        https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-PkgConfig-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(English)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  pkgconfig
# Test Suite
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Dependencies
Requires:       pkgconfig

%description
The pkg-config program retrieves information about installed libraries,
usually for the purposes of compiling against and linking to them.

ExtUtils::PkgConfig is a very simplistic interface to this utility,
intended for use in the Makefile.PL of perl extensions that bind
libraries that pkg-config knows. It is really just boilerplate code
that you would've written yourself.

%prep
%setup -q -n ExtUtils-PkgConfig-%{version}

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
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::PkgConfig.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.16-21
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 29 2019 Paul Howarth <paul@city-fan.org> - 1.16-10
- Spec tidy-up
  - Use author-independent source URL
  - Classify builds by usage
  - Drop redundant buildroot cleaning in %%install section
  - Don't need to delete empty directories from the buildroot
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-2
- Perl 5.26 rebuild

* Thu Jun 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-1
- 1.16 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.20 rebuild

* Thu Jun 26 2014 Tom Callaway <spot@fedoraproject.org> - 1.15-1
- update to 1.15

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Tom Callaway <spot@fedoraproject.org> - 1.14-1
- update to 1.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.12-16
- Allow empty cflags (CPAN RT#84026)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.12-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.12-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.12-10
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.12-9
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.12-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Upstream update.

* Wed Jul 09 2008 Ralf Corsépius <rc040203@freenet.de> - 1.11-1
- Upstream update.
- Reflect Source0-URL having changed.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-2
- rebuild for new perl

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-1
- 1.08

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Sep  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-5
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-3
- Dist tag.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.07-2
- rebuilt

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.07-1
- Update to 1.07.

* Sun Oct  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.06-0.fdr.1
- Update to 1.06.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.05-0.fdr.1
- First build.
