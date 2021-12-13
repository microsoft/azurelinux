Name:		perl-Test-LongString
Version:	0.17
Release:	17%{?dist}
Summary:	Perl module to test long strings
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Test-LongString
Source0:	https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Test-LongString-%{version}.tar.gz#/perl-Test-LongString-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# Required by the tests
BuildRequires:	perl(Test::Builder) >= 0.12
BuildRequires:	perl(Test::Builder::Tester) >= 1.04

BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Pod) >= 1.14 

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides some drop-in replacements for the string comparison
functions of Test::More, but which are more suitable when you test against
long strings. If you've ever had to search for text in a multi-line string
like an HTML document, or find specific items in binary data, this is the
module for you.

%prep
%setup -q -n Test-LongString-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Test
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.17-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-14
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17-4
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-2
- Perl 5.22 rebuild

* Fri Nov 14 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17-1
- Upstream update.

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-2
- Perl 5.20 mass

* Mon Sep 08 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.16-1
- Upstream update.
- Modernize spec.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.15-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.15-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15-2
- Perl mass rebuild

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.15-1
- Upstream update.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.14-1
- Upstream update.
- Minor spec cleanups.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.13-1
- Upstream update.
- Minor spec cleanups.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.11-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-3
- rebuild for new perl

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.11-2
- BR: perl(ExtUtils::MakeMaker).
- Update license tag.

* Wed Feb 21 2007 Ralf Corsépius <rc040203@freenet.de> - 0.11-1
- Upstream update.
- For now, ignore BR: perl(Test::Builder::Tester) > 1.04.

* Wed Feb 21 2007 Ralf Corsépius <rc040203@freenet.de>
- Preps for 0.11. Deactivated, because perl(Test::Builder::Tester) on
  all current Fedoras is too old for this to be applicable.

* Fri Nov 03 2006 Ralf Corsépius <rc040203@freenet.de> - 0.10-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-2
- Rebuild for perl-5.8.8.

* Fri Oct 07 2005 Ralf Corsepius <rc040203@freenet.de> - 0.09-1
- Upstream update.

* Fri Aug 19 2005 Ralf Corsepius <ralf@links2linux.de> - 0.08-2
- Spec cleanup.

* Thu Aug 11 2005 Ralf Corsepius <ralf@links2linux.de> - 0.08-1
- FE submission.
