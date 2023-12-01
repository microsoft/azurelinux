%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Bit::Vector\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Carp::Clan\\)$
# Filter unwanted Provides:
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Date::Calc\\)$
Summary:        Gregorian calendar date calculations
Name:           perl-Date-Calc
Version:        6.4
Release:        17%{?dist}
License:        (GPL+ or Artistic) and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Date-Calc
Source0:        https://cpan.metacpan.org/authors/id/S/ST/STBEY/Date-Calc-%{version}.tar.gz#/perl-Date-Calc-%{version}.tar.gz
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Bit::Vector) >= 7.1
BuildRequires:  perl(Carp::Clan) >= 6.04
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(POSIX)
BuildRequires:  perl(bytes)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Bit::Vector) >= 7.1
Requires:       perl(Carp::Clan) >= 6.04
BuildArch:      noarch

%description
The library provides all sorts of date calculations based on the
Gregorian calendar (the one used in all western countries today),
thereby complying with all relevant norms and standards: ISO/R
2015-1971, DIN 1355 and, to some extent, ISO 8601 (where applicable).

%prep
%setup -q -n Date-Calc-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} +
chmod -R u+w %{buildroot}/*
for file in %{buildroot}%{_mandir}/man3/Date::Calc.3pm \
            CREDITS.txt; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done

%check
make test

%files
%license license/Artistic.txt license/GNU_GPL.txt license/GNU_LGPL.txt
%doc CHANGES.txt CREDITS.txt README.txt
%{perl_vendorlib}/Date/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 6.4-17
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.4-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-2
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.4-1
- 6.4 bump

* Wed Jan 07 2015 Petr Šabata <contyk@redhat.com> - 6.3-18
- Adapt the test suite for the 2015-2115 era

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.3-17
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 6.3-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Jitka Plesnikova <jplesnik@redhat.com> - 6.3-12
- Update filter
- Add BR perl(Carp)
- Don't need to remove examples and tools, they don't exist

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.3-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-8
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-7
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.3-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.3-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.3-2
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.3-1
- new upstream version - noarch, because since 6.0 there were bigger
 changes like stripping this module into more of them

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.2-1
- new upstream version

* Tue Aug  4 2009 Stepan Kasal <skasal@redhat.com> - 5.6-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.4-6
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.4-5
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.4-4
- filtered out too many provides

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 5.4-3
- various specfile fixes

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.4-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 5.4-2
- Update License tag
- Clean up minor specfile issues

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.4-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.4-1
- Update to 5.4.
- Bring up to date with current Fedora.Extras perl spec template.

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 5.3-10
- Convert man page to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.3-5
- rebuilt

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated
