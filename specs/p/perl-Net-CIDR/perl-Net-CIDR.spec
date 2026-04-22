# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Net-CIDR
Version:        0.27
Release: 2%{?dist}
Summary:        Manipulate IPv4/IPv6 netblocks in CIDR notation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-CIDR
Source0:        https://cpan.metacpan.org/modules/by-module/Net/Net-CIDR-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Test Suite
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Dependencies
# (no additional dependencies)

%description
The Net::CIDR package contains functions that manipulate lists of IP netblocks
expressed in CIDR notation. The Net::CIDR functions handle both IPv4 and IPv6
addresses.

%prep
%setup -q -n Net-CIDR-%{version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%{make_build} test

%files
%license COPYING
%doc ChangeLog README
%{perl_vendorlib}/Net/
%{_mandir}/man3/Net::CIDR.3*

%changelog
* Wed Aug 13 2025 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27 (rhbz#2388145)
  - cidrvalidate() bug fix (GH#9)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26 (rhbz#2374271)
  - cidrvalidate() should accept IPv6 addresses with one uncompressed 0

* Sat May 24 2025 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25 (rhbz#2368340)
  - Fix warning with Perl 5.40

* Wed May 21 2025 Paul Howarth <paul@city-fan.org> - 0.24.1-1
- Update to 0.24.1
  - Strip extra leading zeros from octets in addr2cidr (GH#4)

* Tue May 20 2025 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24 (no changes)

* Mon Mar 10 2025 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Add metadata to Makefile.PL and use Test::More (GH#3)

* Sun Mar 09 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 0.22-1
- Update to 0.22
  - Improve several error messages
  - Allow unabbreviated IPv6 addresses
- Use %%{make_build} and %%{make_install} where appropriate

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-2
- Perl 5.34 rebuild

* Wed Mar 31 2021 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Update perldoc to emphasize proper usage of ciddrvalidate()

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-2
- Perl 5.30 rebuild

* Wed Apr 17 2019 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - _ipcmp: Handle comparison of mixed IPv4 and IPv6-specified addresses,
    allowing cidrlookup() to look up IPv6-mapped IPv4 addresses in IPv4
    address ranges, and vice versa

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.19-2
- Perl 5.28 rebuild

* Tue Jun 12 2018 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
- Drop redundant %%{?perl_default_filter}
- Classify buildreqs by usage
- Don't need to delete empty directories from the buildroot
- Use %%license
- Make %%files list more explicit

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-2
- Perl 5.22 rebuild

* Sun Feb 08 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.18-1
- Update to 0.18

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.17-2
- Perl 5.18 rebuild

* Sun Jun 09 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.17-1
- Update to 0.17
- Add perl default filter
- Remove no-longer-used macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.15-2
- Perl 5.16 rebuild

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.15-1
- Update to 0.15

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul 01 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.14-1
- Update to 0.14

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-3
- rebuild against perl 5.10.1

* Mon Nov  9 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.13-2
- Fix License tag
- Remove Net-CIDR.spec from %%doc
- List files more explicitely

* Fri Sep 25 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.13-1
- Specfile autogenerated by cpanspec 1.78.
