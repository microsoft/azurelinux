Name:           perl-libxml-perl
Version:        0.08
Release:        40%{?dist}
Summary:        A collection of Perl modules for working with XML
License:        (GPL+ or Artistic) and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/libxml-perl
Source0:        https://cpan.metacpan.org/authors/id/K/KM/KMACLEOD/libxml-perl-%{version}.tar.gz#/perl-libxml-perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.5.0
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(strict)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(vars)
BuildRequires:  perl(XML::Parser) >= 2.19
# Tests:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(XML::Parser) >= 2.19

# Filter out unversioned provides
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(Data::Grove\\)$
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(XML::Parser\\)$

%description
libxml-perl is a collection of smaller Perl modules, scripts, and
documents for working with XML in Perl.  libxml-perl software works in
combination with XML::Parser, PerlSAX, XML::DOM, XML::Grove and
others.

%prep
%setup -q -n libxml-perl-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc ChangeLog Changes README
%{perl_vendorlib}/Data/
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.08-40
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-37
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-34
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-31
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Petr Pisar <ppisar@redhat.com> - 0.08-30
- Modernize spec file

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-29
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-27
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-24
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-23
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.08-20
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Petr Šabata <contyk@redhat.com> - 0.08-18
- Correct buildtime dependencies
- Correct the licence tag
- Update the provides filter
- Drop command macros
- Modernize spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.08-16
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.08-14
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-12
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-6
- don't filter out all Data::Grove provides, only unversioned one

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-5
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-4
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.08-3
- Fix old changelog entry
- Fix issues from package review:
- Remove extra BR: perl
- Remove "|| :" from check section
- Add dist tag to release
- Remove extra Provides: perl(Data::Grove)
- Clean up tabs and spacing
- Resolves: bz#226269

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-2
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.08-1.3
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.08-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-1
- Update to 0.08.
- spec cleanup (#153199)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.07-30
- rebuild

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 0.07-29
- bump

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Mar 27 2002 Chip Turner <cturner@redhat.com>
- move to vendor_perl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 0.07-5
- imported from mandrake. tweaked man path.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.07-4mdk
- Rebuild for the latest perl.
- Remove Distribution and Vendor tag.
- Don't run make test for now.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.07-3mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean up spec a bit
- run automated tests

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 0.07-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.07-1mdk
- Macroize package
