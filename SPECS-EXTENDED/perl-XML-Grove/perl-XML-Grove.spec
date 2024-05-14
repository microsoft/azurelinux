Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global cpan_version 0.46alpha
Name:           perl-XML-Grove
Version:        0.46
Release:        2%{?dist}
Summary:        Simple access to infoset of parsed XML, HTML, or SGML instances

License:        GPL+ or Artistic
URL:            https://metacpan.org/release/XML-Grove
Source0:        https://cpan.metacpan.org/authors/id/K/KM/KMACLEOD/XML-Grove-%{cpan_version}.tar.gz#/perl-XML-Grove-%{cpan_version}.tar.gz
Patch1:         perl-XML-Grove-test.patch
# Patch is based on upstream changes
# see https://perl-xml.cvs.sourceforge.net/perl-xml/XML-Grove/COPYING?revision=1.2&view=markup
Patch2:         perl-XML-Grove-fix-COPYING.patch

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Data::Grove)
BuildRequires:  perl(Data::Grove::Visitor)
BuildRequires:  perl(strict)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(utf8)
BuildRequires:  perl(XML::Parser::PerlSAX)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
XML::Grove is a tree-based object model for accessing the information
set of parsed or stored XML, HTML, or SGML instances. XML::Grove
objects are Perl hashes and arrays where you access the properties of
the objects using normal Perl syntax.


# Remove bogus and redundant provides
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(My(HTML|Visitor)\\)|^perl\\(XML::Grove\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(XML::Parser::PerlSAX\\)$

%prep
%setup -q -n XML-Grove-%{cpan_version}
%patch 1 -p1 -b .test
%patch 2 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%files
%doc ChangeLog Changes COPYING DOM README examples/
%doc %{perl_vendorlib}/XML/DOM-ecmascript.pod
%{perl_vendorlib}/XML/Grove*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.46-2
- Remove epoch

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.46-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.10.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.9.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.46-0.8.alpha
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.7.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.6.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.46-0.5.alpha
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.46-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.46-0.2.alpha
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Petr Pisar <ppisar@redhat.com> - 1:0.46-0.1.alpha
- Make package version conformant to packaging guidelines

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-63
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46alpha-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-61
- Perl 5.24 rebuild

* Fri Feb 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-60
- Package cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.46alpha-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-57
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-56
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.46alpha-53
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Petr Pisar <ppisar@redhat.com> - 0.46alpha-51
- Provide versioned perl(XML::Grove)

* Thu Nov 22 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-50
- Update filters for provides/requires
- Patch COPYING due to upstream changes

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.46alpha-49
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.46alpha-47
- Perl 5.16 rebuild
- Depend on modules instead on perl-libxml-perl package

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.46alpha-45
- Perl mass rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.46alpha-44
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46alpha-42
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46alpha-41
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.46alpha-40
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46alpha-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 17 2008 Stepan Kasal <skasal@redhat.com> - 0.46alpha-37
- avoid packing DOM-ecmascript.pod twice

* Thu Oct 16 2008 Stepan Kasal <skasal@redhat.com> - 0.46alpha-36
- flag DOM-ecmascript.pod as doc

* Tue Oct 14 2008 Stepan Kasal <skasal@redhat.com> - 0.46alpha-35
- re-enable check, it seems to work
- improved the explanation of the non-standard Version tag (Patrice Dumas)
- filter out bogus and redundant reuires (Paul Howarth)
- move -depth to the right place on find cmd line (Paul Howarth)

* Tue Oct 14 2008 Stepan Kasal <skasal@redhat.com> - 0.46alpha-34
- cleaned up universe vs. tab conflict
- added an explanation why the Version tag does not conform to the rules
- fixed the source tarball (bz2->gz), to match the upstream exactly
- improved BuildRoot tag

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.46alpha-33
- use utf8 in test -> all are passing

* Sun Jul 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.46alpha-32
- fix license tag with upstream confirmation
  see: https://perl-xml.cvs.sourceforge.net/perl-xml/XML-Grove/COPYING?revision=1.2&view=markup

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.46alpha-31
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.46alpha-30
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.46alpha-29.1
- rebuild for new perl-5.8.8

* Fri Jan  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.46alpha-29
- Rewrite specfile using fedora-rpmdevtools' spec template, fixes #176889.
- Fix License, include docs.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com>
- remove brp-compress

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.46alpha-26
- rebuild

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 0.46alpha-26
- bump

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Sat Jan 26 2002 Jeff Johnson <jbj@redhat.com>
- add internal provides.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jul 23 2001 Crutcher Dunnavant <crutcher@redhat.com> 0.46alpha-2
- imported from mandrake

* Mon Jun 18 2001 Till Kamppeter <till@mandrakesoft.com> 0.46alpha-1mdk
- Newly introduced for Foomatic.
