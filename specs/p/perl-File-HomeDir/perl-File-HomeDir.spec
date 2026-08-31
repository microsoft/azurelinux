# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-File-HomeDir
Version:        1.006
Release:        15%{?dist}
Summary:        Find your home and other directories on any platform
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-HomeDir
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.5.3
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# POSIX not used on Linux
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd) >= 3.12
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path) >= 2.01
BuildRequires:  perl(File::Spec) >= 3.12
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(File::Which) >= 0.05
# Mac::Files not used on Linux
# Mac::SystemDirectory not used on Linux
BuildRequires:  perl(vars)
# Win32 not used on Linux
# Tests:
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.90
# Dependencies:
Requires:       perl(Cwd) >= 3.12
Requires:       perl(File::Path) >= 2.01
Requires:       perl(File::Spec) >= 3.12
Requires:       perl(File::Temp) >= 0.19
Requires:       perl(File::Which) >= 0.05

# Remove unwanted and under-specified dependencies
%global __requires_exclude perl\\(Cwd\\)|perl\\(File::Path\\)|perl\\(File::Spec\\)|perl\\(File::Temp\\)|perl\\(File::Which\\)|perl\\(Mac::|perl\\(Win32

%description
File::HomeDir is a module for locating the directories that are "owned"
by a user (typically your user) and to solve the various issues that
arise trying to find them consistently across a wide variety of
platforms.

%prep
%setup -q -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/File/
%{_mandir}/man3/File::HomeDir.3*
%{_mandir}/man3/File::HomeDir::Darwin.3*
%{_mandir}/man3/File::HomeDir::Darwin::Carbon.3*
%{_mandir}/man3/File::HomeDir::Darwin::Cocoa.3*
%{_mandir}/man3/File::HomeDir::Driver.3*
%{_mandir}/man3/File::HomeDir::FreeDesktop.3*
%{_mandir}/man3/File::HomeDir::MacOS9.3*
%{_mandir}/man3/File::HomeDir::Test.3*
%{_mandir}/man3/File::HomeDir::Unix.3*
%{_mandir}/man3/File::HomeDir::Windows.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.006-9
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.006-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.006-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 28 2020 Tom Callaway <spot@fedoraproject.org> - 1.006-1
- update to 1.006

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.004-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.004-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.004-2
- Perl 5.28 rebuild

* Thu May  3 2018 Paul Howarth <paul@city-fan.org> - 1.004-1
- 1.004 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.002-2
- Perl 5.26 rebuild

* Thu Apr 27 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.002-1
- 1.002 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.00-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-12
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.00-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-9
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 1.00-8
- Correct dependencies

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.00-4
- Perl 5.18 rebuild
- Specify all dependencies

* Thu Jan 31 2013 Petr Šabata <contyk@redhat.com> - 1.00-3
- Use the Module::Install provided by upstream (#906007)

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 1.00-2
- Re-enable the test suite
- Unbundle inc::Module::Install
- Modernize the spec

* Mon Oct 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.00-1
- update to 1.00

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.99-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.99-2
- Perl 5.16 rebuild

* Tue Jan 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.99-1
- Update to 0.99

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.98-2
- Perl mass rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 0.98-1
- update to 0.98

* Fri Jun 24 2011 Marcela Maslanova <mmaslano@redhat.com> - 0.97-2
- fix filters for future rebuild
- add perl_bootstrap macro
- rebuild for perl 5.14.1

* Mon Feb 21 2011 Tom Callaway <spot@fedoraproject.org> - 0.97-1
- update to 0.97

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.93-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 22 2010 Petr Pisar <ppisar@redhat.com> - 0.93-1
- 0.93 bump
- Consolidate dependencies
- Remove unversioned Requires
- Update Summary and Description
- Remove unneded file permission fixes

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.86-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.86-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.86-1
- update for Padre

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.84-1
- update to 0.84

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-1
- update to the latest version for Padre editor

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-1
- 0.67

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-1
- 0.66

* Wed May 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.65-1
- Update to 0.65.

* Sat Feb 10 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.64-1
- Update to 0.64.

* Thu Jan 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-1
- Update to 0.63.

* Thu Jan  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.62-1
- Update to 0.62.

* Thu Aug 03 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.58-1
- First build.
