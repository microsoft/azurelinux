Summary:        Encrypt Data with Cipher Block Chaining Mode
Name:           perl-Crypt-CBC
Version:        2.33
Release:        27%{?dist}
# Upstream confirms that they're under the same license as perl.
# Wording in CBC.pm is less than clear, but still.
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Crypt-CBC
Source0:        https://cpan.metacpan.org/modules/by-module/Crypt/Crypt-CBC-%{version}.tar.gz#/perl-Crypt-CBC-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::MD5) >= 2.00
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(lib)
# Optional Tests
# Modules used for test suite, skipped when bootstrapping as
# some of these modules use Crypt::CBC themselves
%if 0%{!?perl_bootstrap:1} && ! (0%{?rhel} >= 7)
# Crypt::CAST5 not yet packaged in Fedora
BuildRequires:  perl(Crypt::DES)
BuildRequires:  perl(Crypt::Blowfish)
BuildRequires:  perl(Crypt::Blowfish_PP)
BuildRequires:  perl(Crypt::Rijndael)
%endif
# Crypt::IDEA doesn't need bootstrapping and we get extra test coverage by including it
BuildRequires:  perl(Crypt::IDEA)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Scalar::Util)

%description
This is Crypt::CBC, a Perl-only implementation of the cryptographic
cipher block chaining mode (CBC).  In combination with a block cipher
such as Crypt::DES or Crypt::IDEA, you can encrypt and decrypt
messages of arbitrarily long length.  The encrypted messages are
compatible with the encryption format used by SSLeay.

%prep
%setup -q -n Crypt-CBC-%{version}
chmod -c 644 eg/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README eg/
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::CBC.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.33-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Paul Howarth <paul@city-fan.org> - 2.33-25
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Fix permissions verbosely
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-23
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-22
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-19
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-18
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-15
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-14
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-12
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-11
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-8
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-7
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-6
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-3
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Paul Howarth <paul@city-fan.org> - 2.33-1
- Update to 2.33
  - Fixes to regular expressions to avoid rare failures to correctly strip
    padding in decoded messages
  - Add padding type = "none"
  - Fix "Taint checks are turned on and your key is tainted" error when
    autogenerating salt and IV
  - Fix minor bugs CPAN RT#83175 and CPAN RT#86455
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.29-16
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.29-13
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.29-12
- Perl 5.16 rebuild

* Mon Jun 11 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.29-11
- Do not build-require Crypt::Blowfish, Crypt::Blowfish_PP, and Crypt::Rijndael
  on RHEL >= 7
- Resolves: rhbz#822812

* Sat Apr 21 2012 Paul Howarth <paul@city-fan.org> - 2.29-10
- BR: perl(bytes), perl(constant), perl(Digest::MD5) - required by module
- BR: perl(Crypt::Blowfish), perl(Crypt::Blowfish_PP), perl(Crypt::DES),
  perl(Crypt::Rijndael) for improved test coverage, except when bootstrapping

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.29-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.29-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.29-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.29-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Tom "spot" Callawau <tcallawa@redhat.com> - 2.29-1
- update to 2.29

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-3
- work around buildsystem burp

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1.1
- add BR: perl(ExtUtils::MakeMaker)

* Wed Feb 07 2007 Andreas Thienemann <andreas@bawue.net> - 2.22-1
- Upgrade to 2.22

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.19-1
- Upgrade to 2.19

* Fri Feb 24 2006 Andreas Thienemann <andreas@bawue.net> - 2.17-1
- Upgrade to 2.17

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-2
- Remove execute permissions from example files

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-1
- Initial package

