Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Net-Patricia
Version:        1.22
Release:        25%{?dist}
Summary:        Patricia Trie perl module for fast IP address lookups
# The entire source code is GPLv2+ except libpatricia/ which is BSD
License:        GPLv2+ and BSD
URL:            https://metacpan.org/release/Net-Patricia
Source0:        https://cpan.metacpan.org/modules/by-module/Net/Net-Patricia-%{version}.tar.gz#/perl-Net-Patricia-%{version}.tar.gz
# Fix building on systems without libsnl, bug #1534596, CPAN RT#124088
Patch0:         Net-Patricia-1.22-Do-not-link-to-nsl-library.patch
BuildRequires:  gcc
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(diagnostics)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Net::CIDR::Lite) >= 0.20
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
Requires:       perl(DynaLoader)
Requires:       perl(Exporter)
Requires:       perl(Net::CIDR::Lite) >= 0.20
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module uses a Patricia Trie data structure to quickly perform IP
address prefix matching for applications such as IP subnet, network or
routing table lookups.  The data structure is based on a radix tree using a
radix of two, so sometimes you see patricia implementations called "radix"
as well.  The term "Trie" is derived from the word "retrieval" but is
pronounced like "try".  Patricia stands for "Practical Algorithm to
Retrieve Information Coded as Alphanumeric", and was first suggested for
routing table lookups by Van Jacobsen.  Patricia Trie performance
characteristics are well-known as it has been employed for routing table
lookups within the BSD kernel since the 4.3 Reno release.

%prep
%setup -q -n Net-Patricia-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
%make_build

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
# BSD
%license libpatricia/copyright
%{perl_vendorarch}/auto/*
# GPLv2+
%doc Changes COPYING README
%{perl_vendorarch}/Net/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct  8 2019 Orion Poplawski <orion@nwra.com> - 1.22-23
- Spec cleanup

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-21
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-18
- Perl 5.28 rebuild

* Mon Feb 12 2018 Petr Pisar <ppisar@redhat.com> - 1.22-17
- Fix building on systems without libsnl (bug #1534596)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-13
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-11
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Petr Šabata <contyk@redhat.com> - 1.22-9
- Prevent FTBFS by correcting the build time dependency list
- Tweak the runtime deplist as well

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-7
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Philip Prindeville <philipp@fedoraproject.org> - 1.22-3
- Redux of fix for bz#1014054

* Sun Mar 16 2014 Philip Prindeville <philipp@fedoraproject.org> - 1.22-2
- Fix licensing issues bz#1014054

* Wed Oct 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.22-1
- Update to 1.22

* Mon Sep 9 2013 Orion Poplawski <orion@cora.nwra.com> - 1.21-1
- Update to 1.21
- License changed to GPLv2+

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.20-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Orion Poplawski <orion@cora.nwra.com> - 1.20-1
- Update to 1.20

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.19-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.19-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.19-1
- 1.18_81 re-released as 1.19

* Sun Nov 14 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.18_81-1
- new upstream verion, maintenance fix
  - improve parameter checking
  - handle undef as $data parameter to add()

* Mon Nov  8 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.18_80-1
- new upstream version, maintenance fix
  - still doesn't handle 0 being passed as data argument to add()

* Sun Nov  7 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.18_01-1
- new upstream version, maintenance fix
  - bug in AFINET6 version of add() method.

* Tue Oct 26 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.18-1
- new upstream version, official release

* Sun May 23 2010 Philip Prindeville <philipp@fedoraproject.org> - 1.17_01-1
- 1.17 was yanked from CPAN because of a missing update, hence 1.17_01.

* Wed May 19 2010 Philip Prindeville <philipp@fedoraproject.org > - 1.17-3
- update changelog

* Wed May 19 2010 Philip Prindeville <philipp@fedoraproject.org > - 1.17-2
- Refresh .spec file with cpanspec.

* Wed May 19 2010 Philip Prindeville <philipp@fedoraproject.org > - 1.17-1
- new upstream version, official release

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.16-2
- Mass rebuild with perl-5.12.0

* Wed Feb 24 2010 Philip Prindeville <philipp@fedoraproject.org > - 1.16-1
- new upstream version, official release

* Fri Jan  8 2010 Stepan Kasal <skasal@redhat.com> - 1.15_07-1
- new upstream version, recommended by the upstream maintainer

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.15-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 6 2009 Orion Poplawski 1.15-1
- Update to 1.15

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.014-6.1
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.014-5.1
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.014-4.1
- add BR: perl(ExtUtils::MakeMaker)

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.014-4
- Update license tag to GPLv2+
- Rebuild for BuildID

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.014-3
- Rebuild for FC6

* Mon Feb 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.014-2
- Rebuild for FC5

* Tue Jan 31 2006 Orion Poplawski 1.014-1
- Update to 1.014

* Tue Oct 11 2005 Orion Poplawski 1.010-1
- Initial Fedora Extras release
