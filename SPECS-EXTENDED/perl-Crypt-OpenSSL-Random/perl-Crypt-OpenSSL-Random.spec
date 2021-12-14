Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Crypt-OpenSSL-Random
Version:        0.15
Release:        8%{?dist}
Summary:        OpenSSL/LibreSSL pseudo-random number generator access
License:        GPL+ or Artistic 
URL:            https://metacpan.org/release/Crypt-OpenSSL-Random
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Crypt-OpenSSL-Random-%{version}.tar.gz#/perl-Crypt-OpenSSL-Random-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Crypt::OpenSSL::Guess) >= 0.11
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Crypt::OpenSSL::Random provides the ability to seed and query the OpenSSL
and LibreSSL library's pseudo-random number generators.

%prep
%setup -q -n Crypt-OpenSSL-Random-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f \( -name .packlist -o \
        -name '*.bs' -empty \) -exec rm -f {} \;
find %{buildroot} -depth -type d -empty -exec rmdir {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc Changes
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.15-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.28 rebuild

* Mon Jun 18 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-1
- 0.15 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Petr Pisar <ppisar@redhat.com> - 0.11-4
- Rebuild against OpenSSL 1.1.0

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-1
- 0.11 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.22 rebuild

* Tue Feb 17 2015 Wes Hardaker <wjhns174@hardakers.net> - 0.10-2
- build-req test::more

* Tue Feb 17 2015 Wes Hardaker <wjhns174@hardakers.net> - 0.10-1
- Update to 0.10

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.06-2
- Perl 5.18 rebuild

* Wed Jul 17 2013 Wes Hardaker <wjhns174@hardakers.net> - 0.06-1
- Updated to upstream 0.6 for bug fixes

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.04-21
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-19
- Update dependencies
- Add perl_default_filter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.04-17
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-15
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-12
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 0.04-11
- fix the package name for error messages

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.04-10
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.04-9
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.04-6
- rebuild with new openssl

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-5
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.04-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.04-3
 - Rebuild for deps

* Wed May 23 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.04-2
- Add document file: LICENSE

* Mon May 21 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.04-1
- Update to upstream 0.4 with proper license

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-3
- BuildRequire perl(ExtUtils::MakeMaker)

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-1
- Initial version
