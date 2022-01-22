Name:           perl-String-ShellQuote
Version:        1.04
Release:        31%{?dist}
Summary:        Perl module for quoting strings for passing through the shell
License:        (GPL+ OR Artistic) and GPLv2+
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/String-ShellQuote
Source0:        https://cpan.metacpan.org/authors/id/R/RO/ROSCH/String-ShellQuote-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# RS::Handy is never used
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests only
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Getopt::Long)

%description
This package contains a Perl module and a command line utility which
are useful for quoting strings which are going to pass through the
shell or a shell-like object.

%prep
%setup -q -n String-ShellQuote-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{_bindir}/shell-quote
%{perl_vendorlib}/String
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-31
- Adding 'BuildRequires: perl-generators'.

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.04-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-27
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-24
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-21
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-19
- Perl 5.24 rebuild

* Tue Mar 01 2016 Petr Šabata <contyk@redhat.com> - 1.04-18
- Package cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-15
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.04-12
- Perl 5.18 rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.04-11
- Add GPLv2+ to the license declaration due to shell-quote(1)
- Specify all dependencies

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.04-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.04-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.04-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.04-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Dec 18 2010 Steven Pritchard <steve@kspei.com> 1.04-1
- Update to 1.04.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.03-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-5
- rebuild for new perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.03-4
- Reformat to match cpanspec output.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Tue Aug 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.03-3
- Fix order of arguments to find(1).
- Drop version from perl build dependency.

* Wed May  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.03-2
- 1.03.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-8
- Sync with fedora-rpmdevtools' Perl spec template to fix x86_64 build.

* Thu Sep 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.7
- Specfile cleanup, using INSTALLDIRS=vendor, PERL_INSTALL_ROOT and
  INSTALLARCHLIB.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.6
- Get rid of perllocal.pod, .packlist and empty *.bs.
  Some of the files don't exist with this package but I want a good template
  %%install section :)

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.5
- Install into vendor dirs.

* Sun Jul 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.4
- Update description.
- Small spec cleanups.

* Sun May  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.3
- Own more dirs.

* Sun Apr 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.2
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.1
- Update to current Fedora guidelines.

* Fri Feb  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.00-1.fedora.1
- First Fedora release.
