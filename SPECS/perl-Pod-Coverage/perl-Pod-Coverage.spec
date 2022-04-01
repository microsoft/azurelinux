%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Devel::Symdump\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Find\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Parser\\)$

Summary:        Checks if the documentation of a module is comprehensive
Name:           perl-Pod-Coverage
Version:        0.23
Release:        22%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Pod-Coverage
Source0:        https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-%{version}.tar.gz#/perl-Pod-Coverage-%{version}.tar.gz
Source1:        LICENSE.PTR
# Make pod_cover more secure, CPAN RT#85540
Patch0:         Pod-Coverage-0.23-Do-not-search-.-lib-by-pod_cover.patch

BuildArch:      noarch

BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(B)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Symdump) >= 2.01
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Find) >= 0.21
BuildRequires:  perl(Pod::Parser) >= 1.13
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Devel::Symdump) >= 2.01
Requires:       perl(Pod::Find) >= 0.21
Requires:       perl(Pod::Parser) >= 1.13

Provides:       perl(Pod::Coverage::CountParents) = %{version}-%{release}

%{?perl_default_filter}

%description
Developers hate writing documentation.  They'd hate it even more if their
computer tattled on them, but maybe they'll be even more thankful in the
long run.  Even if not, perlmodstyle tells you to, so you must obey.

This module provides a mechanism for determining if the pod for a given
module is comprehensive.

%prep
%setup -q -n Pod-Coverage-%{version}
%patch0 -p1

cp %{SOURCE1} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE.PTR
%doc Changes examples
%{_bindir}/pod_cover
%{perl_vendorlib}/Pod/
%{_mandir}/man3/Pod::Coverage.3pm*
%{_mandir}/man3/Pod::Coverage::CountParents.3pm*
%{_mandir}/man3/Pod::Coverage::ExportOnly.3pm*
%{_mandir}/man3/Pod::Coverage::Overloader.3pm*

%changelog
* Wed Mar 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.23-22
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.23-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-15
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-7
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.23-3
- Perl 5.18 rebuild

* Wed May 22 2013 Petr Pisar <ppisar@redhat.com> - 0.23-2
- Do not put ./lib into @INC by pod_cover tool

* Thu May 02 2013 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.22-2
- Perl 5.16 rebuild

* Wed Feb 08 2012 Petr Šabata <contyk@redhat.com> - 0.22-1
- 0.22 bump
- Switch to EE::MM
- Modernize spec

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.21-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 14 2010 Petr Sabata <psabata@redhat.com> - 0.21-1
- New release, v0.21

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.20-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20 (test updates)
- No README in upstream distribution
- BR: perl(Test::More)
- More specific files list

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-3
- Rebuild for perl 5.10 (again), second pass with tests enabled

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-2
- Rebuild for perl 5.10 (again), first pass without Test::Pod, tests

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.19-1
- Update to 0.19.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-3
- rebuild 2, enable Test::Pod, tests

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-2.1
- rebuild (first pass, no tests, no Test::Pod)

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-2
- Version 0.18 is now a noarch package.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-5
- Rebuild for FC5 (perl 5.8.8).

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-4
- Add dist tag.

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-3
- Avoid .packlist creation with Module::Build >= 0.2609.
- Trust that %%{perl_vendorlib} is defined.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Nov 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.17-1
- Update to 0.17.

* Wed Oct 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.16-0.fdr.1
- Update to 0.16.

* Thu May 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.14-0.fdr.1
- First build.
