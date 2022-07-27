%{bcond_without perl_HTML_Tagset_enables_optional_test}

Name:           perl-HTML-Tagset
Version:        3.20
Release:        43%{?dist}
Summary:        HTML::Tagset - data tables useful in parsing HTML
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/HTML-Tagset
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/HTML-Tagset-%{version}.tar.gz#/perl-HTML-Tagset-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.4
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional tests
# Test::Pod -> Pod::Simple -> HTML::Entities (HTML::Parser) -> HTML::Tagset
%if 0%{!?perl_bootstrap:1}
%if %{with perl_HTML_Tagset_enables_optional_test}
BuildRequires:  perl(Test::Pod) >= 1.14
%endif
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module contains several data tables useful in various kinds of
HTML parsing operations, such as tag and entity names.

%prep
%setup -q -n HTML-Tagset-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML::Tagset.3pm*

%changelog
* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 3.20-43
- License Verified
- Remove usage of macros not applied for CBL-Mariner

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.20-42
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-39
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-38
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-35
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-34
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-32
- Specify all dependencies; Modernize spec

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-30
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-29
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-27
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-26
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-23
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-22
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-21
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-20
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-18
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.20-16
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Petr Šabata <contyk@redhat.com> - 3.20-14
- Add a missing dependency

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.20-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 3.20-11
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 3.20-10
- Clean up spec file for modern rpmbuild:
  - Drop BuildRoot definition
  - Drop %%defattr
  - Drop %%clean section
  - Drop cleaning of buildroot in %%install
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Don't use macros for commands
- Break build dependency loop by only using perl(Test::Pod) if we're not
  bootstrapping
- BR: perl(Test::More)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.20-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.20-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.20-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.20-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Marcela Mašláňová <mmaslano@redhat.com> - 3.20-1
- update to 3.20

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.10-8
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.10-7
- rebuild for new perl

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-6
- Update license tag
- Add BuildRequires

* Mon Feb 05 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-5
- perl(Test::Pod) doesn't exist in our buildroots because it isn't in
  core.  Removing for now.

* Sun Feb 04 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-4
- Also add BuildRequires suggested by Jose.

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.10-3
- Minor corrections.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.10-2.1.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.10-2.1
- rebuild for new perl-5.8.8

* Tue Jan 10 2006 Jason Vas Dias <jvdias@redhat.com> - 3.10-1
- fix bug 176720: upgrade to 3.10
- make .spec file conform to fedora-rpmdevtools spectemplate-perl.spec

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com>
- remove brp-compress

* Tue Mar 29 2005 Robert Scheck <redhat@linuxnetz.de> 3.04-1
- upgrade to 3.04 and spec file cleanup (#140914, #150360)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 3.03-30
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 3.03-28
- rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated. 
