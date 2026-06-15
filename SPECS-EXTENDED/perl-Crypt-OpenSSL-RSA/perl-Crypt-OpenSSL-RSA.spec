Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Crypt-OpenSSL-RSA
Version:        0.33
Release:        1%{?dist}
Summary:        Perl interface to OpenSSL for RSA
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Crypt-OpenSSL-RSA
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/Crypt-OpenSSL-RSA-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Crypt::OpenSSL::Guess) >= 0.11
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Crypt::OpenSSL::Bignum)
BuildRequires:  perl(Crypt::OpenSSL::Random)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(base)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)

Requires:       perl(Crypt::OpenSSL::Random)
Requires:	perl(Crypt::OpenSSL::Bignum)

%description
Crypt::OpenSSL::RSA - RSA encoding and decoding, using the openSSL libraries

%prep
%autosetup -p1 -n Crypt-OpenSSL-RSA-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*

%changelog
* Fri Dec 23 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.33-1
- Update to version 0.33
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.31-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-1
- 0.31 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-2
- Perl 5.28 rebuild

* Tue Jun 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump
- Modernize spec file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-18
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 27 2016 Petr Pisar <ppisar@redhat.com> - 0.28-16
- Adjust to OpenSSL 1.1.0 (bug #1383650)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-15
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-12
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-11
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.28-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-5
- Update dependencies and source link
- Add perl_default_filter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.28-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 21 2011 Wes Hardaker <wjhns174@hardakers.net> - 0.28-1
- Update to latest upstream: 0.28

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.26-6
- Perl mass rebuild

* Thu May 12 2011 Wes Hardaker <wjhns174@hardakers.net> - 0.26-5
- 704257 Added a patch to correct building with perl 5.14

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Sep  9 2010 Wes Hardaker <wjhns174@hardakers.net> - 0.26-2
- version bump

* Thu Sep  9 2010 Wes Hardaker <wjhns174@hardakers.net> - 0.26-1
- Updated to the upstream 0.26

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.25-12
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.25-11
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.25-10
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.25-7
- rebuild with new openssl

* Wed Jun 18 2008 Wes Hardaker <wjhns174@hardakers.net> - 0.25-6
- Fix bug 451900: force-require the bignum module

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.25-5
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.25-4
- Autorebuild for GCC 4.3

* Sun Dec 09 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.25-3
- Rebuild for deps

* Thu Dec  6 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.25-2
- Bump to force rebuild with new openssl lib version

* Thu May 31 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.25-1
- head to upstream 0.25
- doc the new LICENSE file

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-4
- Reverse terms in license to match perl rpm exactly

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-3
- BuildRequire perl(Test) perl(ExtUtils::MakeMaker) perl(Crypt::OpenSSL::Bignum)
- Fixed source code URL

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-1
- Initial version
