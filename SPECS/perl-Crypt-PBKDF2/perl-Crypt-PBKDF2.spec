# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	The PBKDF2 password hashing algorithm
Name:		perl-Crypt-PBKDF2
Version:	0.161520
Release:	24%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Crypt-PBKDF2
Source0:	https://cpan.metacpan.org/modules/by-module/Crypt/Crypt-PBKDF2-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest) >= 1.16
BuildRequires:	perl(Digest::HMAC) >= 1.01
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl(Digest::SHA3) >= 0.22
BuildRequires:	perl(MIME::Base64)
BuildRequires:	perl(Module::Runtime)
BuildRequires:	perl(Moo) >= 2
BuildRequires:	perl(Moo::Role) >= 2
BuildRequires:	perl(namespace::autoclean)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strictures) >= 2
BuildRequires:	perl(Try::Tiny) >= 0.04
BuildRequires:	perl(Type::Tiny)
BuildRequires:	perl(Types::Standard) >= 1.000005
# Test Suite
BuildRequires:	perl(constant)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
# Runtime

%description
PBKDF2 is a secure password hashing algorithm that uses the techniques of "key
strengthening" to make the complexity of a brute-force attack arbitrarily high.
PBKDF2 uses any other cryptographic hash or cipher (by convention, usually
HMAC-SHA1, but Crypt::PBKDF2 is fully pluggable), and allows for an arbitrary
number of iterations of the hashing function, and a nearly unlimited output
hash size (up to 2**32-1 times the size of the output of the backend hash).
The hash is salted, as any password hash should be, and the salt may also be of
arbitrary size.

%prep
%setup -q -n Crypt-PBKDF2-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::PBKDF2.3*
%{_mandir}/man3/Crypt::PBKDF2::Hash.3*
%{_mandir}/man3/Crypt::PBKDF2::Hash::DigestHMAC.3*
%{_mandir}/man3/Crypt::PBKDF2::Hash::HMACSHA1.3*
%{_mandir}/man3/Crypt::PBKDF2::Hash::HMACSHA2.3*
%{_mandir}/man3/Crypt::PBKDF2::Hash::HMACSHA3.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-16
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-13
- Perl 5.34 rebuild

* Fri Feb 12 2021 Paul Howarth <paul@city-fan.org> - 0.161520-12
- Unretired, spec re-written and re-reviewed (#1928111)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.161520-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.161520-1
- 0.161520 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.160410-2
- Perl 5.24 rebuild

* Wed Mar 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.160410
- 0.160410 bump; Moose was replaced by Moo

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.150900-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.150900-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.150900-2
- Perl 5.22 rebuild

* Thu Apr 30 2015 David Dick <ddick@cpan.org> - 0.150900-1
- Upgrade to 0.150900.  Bugfix

* Sat Oct 18 2014 David Dick <ddick@cpan.org> - 0.142390-1
- Added option for password length limit, add HMACSHA3 hasher

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.140890-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.140890-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 David Dick <ddick@cpan.org> - 0.140890-1
- Initial release
