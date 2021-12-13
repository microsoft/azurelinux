Name:           perl-DateTime-Format-HTTP
Version:        0.42
Release:        16%{?dist}
Summary:        HTTP protocol date conversion routines
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/DateTime-Format-HTTP
Source0:        https://cpan.metacpan.org/authors/id/C/CK/CKRAS/DateTime-Format-HTTP-%{version}.tar.gz#/perl-DateTime-Format-HTTP-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(DateTime) >= 0.17
BuildRequires:  perl(HTTP::Date) >= 1.44
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.47
Requires:  perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(DateTime) >= 0.17
Requires:       perl(HTTP::Date) >= 1.44

%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(DateTime\\)$
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(HTTP::Date\\)$

%description
This module provides functions that deal with the date formats used by the
HTTP protocol (and then some).

%prep
%setup -q -n DateTime-Format-HTTP-%{version}
sed -i -e 's/\r//' LICENSE README Changes CREDITS

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc LICENSE Changes CREDITS README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.42-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-2
- Perl 5.22 rebuild

* Fri Nov 14 2014 Petr Šabata <contyk@redhat.com> - 0.42-1
- 0.42 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-12
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.40-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.40-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.40-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.40-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Iain Arnell <iarnell@gmail.com> 0.40-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- PERL_INSTALL_ROOT -> DESTDIR
- fix up crlf in docs

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.38-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.38-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.38-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.38-2
- rearrange the files in doc as the tarball has changed contents

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.38-1
- auto-update to 0.38 (by cpan-spec-update 0.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.37-3
- rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 0.37-2
- bump for mass rebuild

* Wed Aug 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.37-1
- update to 0.37
- nix the SIGNATURE checking bits of the spec file as the author has dropped
  it from this version

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-3
- bump for build & release

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-2
- add missing buildrequires: perl(File::Find::Rule)

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-1
- Initial spec file for F-E
