Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# SPDX-License-Identifier: GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:        Encrypt Data with Cipher Block Chaining Mode
Name:           perl-Crypt-CBC
Version:        3.04
Release:        17%{?dist}
# Upstream confirms that they're under the same license as perl.
# Wording in CBC.pm is less than clear, but still.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Crypt-CBC
Source0:        https://cpan.metacpan.org/authors/id/L/LD/LDS/Crypt-CBC-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        cbctest1.pl
Source2:        Crypt-CBC-GH6.pl
Patch0:         Crypt-CBC-3.04-3.05.patch
Patch1:         randomiv.patch
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::MD5) >= 2.00
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(File::Basename)
# Not available on 32-bit platforms (#1948957)
#BuildRequires:  perl(Math::Int128)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(Encode)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(warnings)
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
%if 0%{?with_check}
BuildRequires: perl(CPAN)
%endif
# Crypt::IDEA doesn't need bootstrapping and we get extra test coverage by including it
BuildRequires:  perl(Crypt::IDEA)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Scalar::Util)
# Optional module needed for CTR mode
Recommends:     perl(Math::Int128)

%description
This is Crypt::CBC, a Perl-only implementation of the cryptographic
cipher block chaining mode (CBC).  In combination with a block cipher
such as Crypt::DES or Crypt::IDEA, you can encrypt and decrypt
messages of arbitrarily long length.  The encrypted messages are
compatible with the encryption format used by SSLeay.

%prep
%setup -q -n Crypt-CBC-%{version}

# Upstream tagged a 3.05 release but didn't upload it to PAUSE
# This fixes an issue around the -literal_key option
# https://github.com/lstein/Lib-Crypt-CBC/issues/4
%patch -P 0 -p1

# Fix decryption of ciphertext created with 'header' => 'randomiv'
# https://bugzilla.redhat.com/show_bug.cgi?id=2235322
# https://github.com/lstein/Lib-Crypt-CBC/issues/6
# https://github.com/lstein/Lib-Crypt-CBC/pull/7
cd lib/Crypt
%patch -P 1
cd -

chmod -c 644 eg/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
#cpan Crypt::Meta
#cpan Crypt::PBKDF2
#make test

# Tests for #2235322, GH#6 (both require Crypt::Blowfish)
%if 0%{!?perl_bootstrap:1} && ! (0%{?rhel} >= 7)
PERL5LIB=%{buildroot}%{perl_vendorlib} perl %{SOURCE1}
PERL5LIB=%{buildroot}%{perl_vendorlib} perl %{SOURCE2}
%endif

%files
%doc Changes README eg/
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::CBC.3*

%changelog
* Thu May 08 2025 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 3.04-17
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep  5 2023 Paul Howarth <paul@city-fan.org> - 3.04-13
- Fix decryption of ciphertext created with 'header' => 'randomiv'
  https://bugzilla.redhat.com/show_bug.cgi?id=2235322
  https://github.com/lstein/Lib-Crypt-CBC/issues/6
  https://github.com/lstein/Lib-Crypt-CBC/pull/7

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Michal Josef Špaček <mspacek@redhat.com> - 3.04-11
- Fix %%patch macro
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-8
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-7
- Perl 5.36 rebuild

* Wed Mar  2 2022 Paul Howarth <paul@city-fan.org> - 3.04-6
- Fix an issue around the -literal_key option (GH#4)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-2
- Perl 5.34 rebuild

* Tue May 18 2021 Paul Howarth <paul@city-fan.org> - 3.04-1
- Update to 3.04
  - Fixed bug involving manually-specified IV not being used in some
    circumstances

* Mon May  3 2021 Paul Howarth <paul@city-fan.org> - 3.03-2
- Crypt::Cipher::AES is used in the absence of any explicitly-specified cipher,
  so make it a hard dependency (#1956206)

* Mon Apr 19 2021 Paul Howarth <paul@city-fan.org> - 3.03-1
- Update to 3.03
  - Fixed bug that caused an extraneous block of garbage data to be appended to
    encrypted string when "nopadding" specified and plaintext is even multiple
    of blocksize

* Thu Apr 15 2021 Paul Howarth <paul@city-fan.org> - 3.02-2
- Soften dependency on perl(Math::Int128) (needed for CTR mode) as it's not
  available on 32-bit platforms (#1948957)

* Mon Apr 12 2021 Paul Howarth <paul@city-fan.org> - 3.02-1
- Update to 3.02
  - CTR mode now requires the Math::Int128 module, which gives a ~5x
    performance boost over Math::BigInt

* Fri Feb 12 2021 Paul Howarth <paul@city-fan.org> - 3.01-1
- Update to 3.01
  - Support for openssl SHA-256 key derivation algorithm
  - Add support for PBKDF2 key derivation algorithm
    - New dependencies: Digest::SHA, Crypt::PBKDF2, Crypt::Cipher::AES
  - Add support for OFB, CFB and CTR chain modes
    - New dependency: Math::BigInt
  - Added better argument checking
  - Fixed long-standing standard padding bug: plaintext ending with bytes
    between 0x00 and 0x0A would be truncated in some conditions
  - Fixed Rijndael_compat padding
  - Warn when the deprecated opensslv1 PBKDF (key derivation function) is used
    for encryption; turn off with -nodeprecate=>1 or by choosing a different
    PBKDF, such as -pbkdf=>'pbkdf2'
  - Fix a regression when passing the legacy -salt=>1 argument
  - Released version 3.01 in recognition of multiple new features and clean-ups

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-28
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-27
- Perl 5.32 rebuild

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

