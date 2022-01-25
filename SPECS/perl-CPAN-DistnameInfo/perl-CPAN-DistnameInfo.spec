Name:           perl-CPAN-DistnameInfo
Version:        0.12
Release:        20%{?dist}
Summary:        Extract distribution name and version from a distribution filename
License:        GPL+ OR Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/CPAN-DistnameInfo
Source0:        https://cpan.metacpan.org/authors/id/G/GB/GBARR/CPAN-DistnameInfo-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(version)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
%if %{with_check}
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
%endif
Requires:       perl

%description
Many online services that are centered around CPAN attempt to
associate multiple uploads by extracting a distribution name from the
filename of the upload. For most distributions this is easy as they
have used ExtUtils::MakeMaker or Module::Build to create the
distribution, which results in a uniform name. But sadly not all
uploads are created in this way.

CPAN::DistnameInfo uses heuristics that have been learnt by
http://search.cpan.org/ to extract the distribution name and version
from filenames and also report if the version is to be treated as a
developer release.

%prep
%setup -q -n CPAN-DistnameInfo-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::DistnameInfo.3*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12-20
- Adding 'BuildRequires: perl-generators'.

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.12-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Petr Pisar <ppisar@redhat.com> - 0.12-16
- Modernize spec file

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct  2 2013 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Grok dist names ending with something numeric containing underscores
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.11-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.11-6
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-4
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-3
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Steven Pritchard <steve@kspei.com> 0.11-1
- Update to 0.11.

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 0.10-1
- Update to 0.10.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-2
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Steven Pritchard <steve@kspei.com> 0.09-1
- Update to 0.09.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Steven Pritchard <steve@kspei.com> 0.08-1
- Update to 0.08.
- BR Test::More.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 02 2008 Steven Pritchard <steve@kspei.com> 0.07-1
- Update to 0.07.
- Improve Summary.
- Drop our copies of COPYING and Artistic.

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.06-4
- rebuild for new perl

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.06-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.06-2
- Canonicalize Source0 URL.
- Fix find option order.

* Mon Sep 19 2005 Steven Pritchard <steve@kspei.com> 0.06-1
- Specfile autogenerated.
