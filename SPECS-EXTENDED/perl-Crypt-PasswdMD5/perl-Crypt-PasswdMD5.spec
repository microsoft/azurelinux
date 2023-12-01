Vendor:         Microsoft Corporation
Distribution:   Mariner
%global cpan_version 1.40

Name:           perl-Crypt-PasswdMD5
# Keep 1-digit version because of history
Version:        %(echo '%{cpan_version}' | sed 's/\.\(.\)/.\1./')
Release:        19%{?dist}
Summary:        Provides interoperable MD5-based crypt() functions
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Crypt-PasswdMD5
Source0:        https://cpan.metacpan.org/modules/by-module/Crypt/Crypt-PasswdMD5-%{cpan_version}.tgz
Patch0:         Crypt-PasswdMD5-1.40-d-md5-version.patch
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Digest::MD5) >= 2.53
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More) >= 0.94
# Dependencies:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This package provides MD5-based crypt() functions.

%prep
%setup -q -n Crypt-PasswdMD5-%{cpan_version}

# Specify version requirement for Digest::MD5
# This avoids the need to add an explicit dependency in the spec file
# and the need to filter the underspecified auto-generated dependency
%patch0

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::PasswdMD5.3*

%changelog
* Wed Apr 28 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove colons from patchnames

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Paul Howarth <paul@city-fan.org> - 1.4.0-17
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Simplify Digest::MD5 versioned dependency generation using a patch
  - Simplify find command using -delete
  - Fix permissions verbosely
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 01 2013 Petr Pisar <ppisar@redhat.com> - 1.4.0-1
- 1.40 bump
- License changed to (GPL+ or Artistic)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-16
- Add license Beerware
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot

* Thu Nov 01 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-15
- Add BR perl(Exporter)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.3-13
- Perl 5.16 rebuild

* Mon Jan 16 2012 Petr Šabata <psabata@redhat.com> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
- Spec cleanup, fix dependencies

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-11
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-10
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-3.1
- Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Feb 27 2007 Mike McGrath <mmcgrath@redhat.com> - 1.3-2
- Basic fixes (BZ 230228)

* Tue Feb 27 2007 Mike McGrath <mmcgrath@redhat.com> - 1.3-1
- Initial Packaging
