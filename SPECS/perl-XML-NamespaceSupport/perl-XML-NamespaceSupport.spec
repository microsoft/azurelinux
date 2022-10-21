Name:           perl-XML-NamespaceSupport
Version:        1.12
Release:        12%{?dist}
Summary:        A simple generic name space support class
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://metacpan.org/release/XML-NamespaceSupport
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERIGRIN/XML-NamespaceSupport-%{version}.tar.gz#/perl-XML-NamespaceSupport-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(constant)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module offers a simple to process name-spaced XML names (unames) from
within any application that may need them. It also helps maintain a prefix
to name space URI map, and provides a number of basic checks.

%prep
%setup -q -n XML-NamespaceSupport-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*

%changelog
* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 1.12-12
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-8
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-2
- Perl 5.26 rebuild

* Fri Mar 31 2017 Petr Pisar <ppisar@redhat.com> - 1.12-1
- 1.12 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-19
- Perl 5.24 rebuild

* Mon Feb 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-18
- Package cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-15
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.11-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-9
- Specify all dependencies.
- Update %%description.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.11-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 29 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.11-2
- Rebuild 1.11 for perl 5.12 as well

* Tue May 11 2010 Petr Pisar <ppisar@redhat.com> - 1.11-1
- 1.11 version bump

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-4
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1.10-3
- fix upstream URL

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.10-2
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-4
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-3
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Feb 17 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-2
- Minor specfile cleanups.
- Dist tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.09-1.2.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.09-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Sat Apr 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-7
- Bring up to date with current Fedora.Extras perl spec template. (#156511)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.08-6
- rebuild

* Thu Oct 17 2002 cturner@redhat.com
- Specfile autogenerated

