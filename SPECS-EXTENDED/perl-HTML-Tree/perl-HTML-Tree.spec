Name:           perl-HTML-Tree
Version:        5.07
Release:        12%{?dist}
Summary:        HTML tree handling modules for Perl
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/HTML-Tree
Source0:        https://cpan.metacpan.org/authors/id/K/KE/KENTNL/HTML-Tree-%{version}.tar.gz#/perl-HTML-Tree-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::Parser) >= 3.46
BuildRequires:  perl(HTML::Tagset) >= 3.02
BuildRequires:  perl(integer)
BuildRequires:  perl(lib)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI::file)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
%if !%{defined perl_bootstrap}
# HTML::FormatText (perl-HTML-Format) has BR: perl(HTML::TreeBuilder) from this package
BuildRequires:  perl(HTML::FormatText)
%if ! (0%{?rhel} >= 7)
# perl-Test-LeakTrace -> perl-Test-Valgrind -> perl-XML-Twig -> perl-HTML-Tree
BuildRequires:  perl(Test::LeakTrace)
%endif
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(HTML::Parser) >= 3.46
Requires:       perl(HTML::Tagset) >= 3.02

%description
This distribution contains a suite of modules for representing,
creating, and extracting information from HTML syntax trees; there is
also relevant documentation.  These modules used to be part of the
libwww-perl distribution, but are now unbundled in order to facilitate
a separate development track.

%prep
%setup -q -n HTML-Tree-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir="%{buildroot}" create_packlist=0
%{_fixperms} %{buildroot}

%check
./Build test

%files
%doc Changes README TODO
%{_bindir}/htmltree
%{perl_vendorlib}/HTML
%{_mandir}/man1/*1*
%{_mandir}/man3/HTML::*3*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 5.07-12
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:5.07-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.07-8
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.07-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.07-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.07-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep  1 2017 Tom Callaway <spot@fedoraproject.org> - 1:5.07-1
- update to 5.07

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.06-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.06-2
- Perl 5.26 rebuild

* Wed May 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.06-1
- 5.06 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.03-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-14
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-13
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-10
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-9
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.03-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1:5.03-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Petr Šabata <contyk@redhat.com> - 1:5.03-1
- 5.03 bump

* Tue Oct 16 2012 Petr Pisar <ppisar@redhat.com> - 1:5.02-6
- Do not build-require Test::LeakTrace on RHEL >= 7

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Paul Howarth <paul@city-fan.org> - 1:5.02-4
- Don't BR: perl(Test::LeakTrace) when bootstrapping
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Drop explicit provides for perl(HTML::Tree) now that CPAN and RPM versions
  are back in sync

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:5.02-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 1:5.02-2
- Perl 5.16 rebuild
- Break dependency cycle with perl-HTML-FormatText during bootstrap

* Mon Jul  2 2012 Tom Callaway <spot@fedoraproject.org> - 1:5.02-1
- update to 5.02

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1:4.2-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:4.2-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:4.2-2
- Perl mass rebuild

* Tue Jun 28 2011 Tom Callaway <spot@fedoraproject.org> - 1:4.2-1
- update to 4.2

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:4.1-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1:4.1-1
- update to 4.1

* Mon Oct 18 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:3.40-1
- update, adjust specfile to use Build.PL

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:3.23-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:3.23-10
- rebuild against perl 5.10.1

* Mon Sep 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-9
- apply Jeff Fearn's fix for the missing close tag bug (bz 535587)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-5
- fix source url

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-4
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-3
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-2
- license tag fix

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-1
- bump to 3.23

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.21-1
- bump to 3.21

* Tue Jul 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.20-2
- bump epoch to ensure clean upgrades

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.20-1
- bump to 3.20

* Mon Jan 16 2006 Ralf Corsépius <rc040203@freenet.de> - 3.1901-2
- BR: perl(Test::Pod).

* Mon Jan 16 2006 Ralf Corsépius <rc040203@freenet.de> - 3.1901-1
- Spec cleanup.
- Filter Provides: perl(main).
- Upstream update.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Jan  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.18-2
- Don't install htmltree into %%{_bindir} but include it in docs.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.18-0.fdr.1
- First build.
