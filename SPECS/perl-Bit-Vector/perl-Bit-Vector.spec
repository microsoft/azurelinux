%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Bit::Vector\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Carp::Clan\\)\s*$
Summary:        Efficient bit vector, set of integers and "big int" math library
Name:           perl-Bit-Vector
Version:        7.4
Release:        21%{?dist}
# Outdated FSF address reported, rt#85827
# Clarified by a private mail from the author:
License:        (GPL+ or Artistic) and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Bit-Vector
Source0:        https://cpan.metacpan.org/authors/id/S/ST/STBEY/Bit-Vector-%{version}.tar.gz#/perl-Bit-Vector-%{version}.tar.gz
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp::Clan) >= 5.3
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Storable) >= 2.21
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Carp::Clan) >= 5.3
Requires:       perl(Storable) >= 2.21
%{?perl_default_filter}

%description
Bit::Vector is an efficient C library which allows you to handle bit
vectors, sets (of integers), "big integer arithmetic" and boolean
matrices, all of arbitrary sizes.

The library is efficient (in terms of algorithmic complexity) and
therefore fast (in terms of execution speed) for instance through the
widespread use of divide-and-conquer algorithms.

%prep
%setup -q -n Bit-Vector-%{version}
chmod -c 644 examples/*.pl
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl\b|$Config{startperl}|' \
    examples/benchmk1.pl
perl -MConfig -pi -e 's|^#!perl\b|$Config{startperl}|' \
    examples/{benchmk{2,3},primes,SetObject}.pl

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  NO_PERLLOCAL=1 NO_PACKLIST=1
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license Artistic.txt GNU_GPL.txt GNU_LGPL.txt
%doc CHANGES.txt CREDITS.txt README.txt examples/
%{perl_vendorarch}/Bit/
%{perl_vendorarch}/auto/Bit/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.4-21
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.4-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 10 2020 Petr Pisar <ppisar@redhat.com> - 7.4-19
- Correct a spelling

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 7.4-18
- Use make_build macro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-12
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-11
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.4-1
- 7.4 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.3-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 7.3-2
- Perl 5.18 rebuild

* Mon Jun 03 2013 Petr Šabata <contyk@redhat.com> - 7.3-1
- 7.3 bump, 5.18 compatibility changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 19 2012 Jitka Plesnikova <jplesnik@redhat.com> - 7.2-4
- Use latest version of Bit-Vector-7.2.tar.gz from CPAN

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 7.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 7.2-1
- 7.2 bumpity
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-7
- filter *.so library incorectly provided by package
- clean spec file

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- rebuild against perl 5.10.1

* Fri Oct  2 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- fixed the license tag

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 7.1-1
- new upstream release

* Tue Aug  4 2009 Stepan Kasal <skasal@redhat.com> - 6.6-1
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.4-7
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-6
- fix license tag, rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.4-5
- Rebuild for selinux ppc32 issue.

* Fri Jul 06 2007 Robin Norwood <rnorwood@redhat.com> 6.4-4
- Resolves: rhbz#247212
- Fix broken perl_provides script - it was removing both the versioned
  and unversioned Provides: perl(Bit::Vector)

* Sat Jun 30 2007 Steven Pritchard <steve@kspei.com> 6.4-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Remove check macro cruft.
- Improve Summary.
- Remove redundant perl build dependency.
- BR ExtUtils::MakeMaker.
- Set OPTIMIZE when we run Makefile.PL, not make.
- BR perl(Carp::Clan) instead of perl-Carp-Clan.
- Remove redundant Carp::Clan dependency.
- Filter unversioned Provides: perl(Bit::Vector)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 6.4-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 6.4-1
- Update to 6.4.
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 6.3-1
- update to 6.3

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 
- Rebuild, remove unpackaged files

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Aug 15 2002 Chip Turner <cturner@redhat.com>
- file list fix for Clan stuff

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated
