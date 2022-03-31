Summary:        A Perl module for inspecting Perl's symbol table
Name:           perl-Devel-Symdump
Version:        2.18
Release:        16%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Devel-Symdump
Source0:        https://cpan.metacpan.org/authors/id/A/AN/ANDK/Devel-Symdump-%{version}.tar.gz#/perl-Devel-Symdump-%{version}.tar.gz

BuildArch:      noarch

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)

# Test Suite
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Harness) >= 3.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# Author Tests
%if 0%{!?perl_bootstrap:1}
# Compress::Zlib (IO-Compress) ⇒ Test::NoWarnings ⇒ Devel::StackTrace ⇒
#   Test::NoTabs ⇒ Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Test::Pod) >= 1.00
# Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
BuildRequires:  perl(Test::Pod::Coverage)
%endif

# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)

%description
The perl module Devel::Symdump provides a convenient way to inspect
perl's symbol table and the class hierarchy within a running program.

%prep
%setup -q -n Devel-Symdump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test %{!?perl_bootstrap:AUTHOR_TEST=1}

%files
%license README
%doc Changes README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::Symdump.3*

%changelog
* Tue Mar 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.18-16
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.18-15
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.18-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-11
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-7
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.18-2
- Perl 5.26 rebuild

* Tue Feb  7 2017 Paul Howarth <paul@city-fan.org> - 1:2.18-1
- Update to 2.18
  - Makefile.PL changes to support perls without "." in @INC; no functional
    change

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.17-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.17-2
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1:2.17-1
- Update to 2.17
  - Unlist Compress::Zlib as a prereq; it was and still is only used by a test
    that won't run for normal user installs (CPAN RT#113886)
- Author tests now require AUTHOR_TEST variable rather than --doit parameter

* Tue Apr 12 2016 Paul Howarth <paul@city-fan.org> - 1:2.16-1
- Update to 2.16
  - docs only change: create a real link to perlref.pod
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Paul Howarth <paul@city-fan.org> - 1:2.15-1
- Update to 2.15
  - In the tests, always check for exists before checking for definedness
- Classify buildreqs by usage
- Run the release tests unless we're bootstrapping

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.14-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.14-2
- Perl 5.22 rebuild

* Thu Dec 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.14-1
- 2.14 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.12-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.12-2
- Perl 5.20 rebuild

* Sun Jun 22 2014 Paul Howarth <paul@city-fan.org> - 1:2.12-1
- Update to 2.12
  - v5.21.0-424-ge35475d stopped supporting defined(@$ref), which was used in
    t/symdump.t

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 01 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.11-1
- 2.11 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.10-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:2.10-2
- Perl 5.18 rebuild

* Wed Mar 27 2013 Petr Šabata <contyk@redhat.com> - 1:2.10-1
- 2.10 bump
- Minor cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.08-13
- Change Exporter to BR, add lib dependency.

* Mon Nov  5 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.08-12
- Add missing requirement - Exporter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:2.08-10
- Perl 5.16 re-rebuild of bootstrapped packages

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1:2.08-9
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1:2.08-8
- Spec clean-up:
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - BR: perl(Carp)
  - BR: perl(Test::Pod) and perl(Test::Pod::Coverage) if not bootstrapping
  - Use %%{_fixperms} macro instead of our own chmod incantation
  - Make %%files list more explicit

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.08-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.08-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.08-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.08-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:2.08-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 1:2.08-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.07-5
- Rebuild for perl 5.10 (again)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.07-4
- rebuild for new perl

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 1:2.07-3
- Add missing BuildRequires

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 1:2.07-2
- Fix license tag
- Fix broken changelog entry

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:2.07-1
- Update to 2.07.
- Minor corrections/cleanings.

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 2.0604-1
- Upgrade to latest CPAN version: 2.0604

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 2.0601-1
- Upgrade to 2.0601

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 2.06-1
- Upgrade to 2.0.6
- rebuild for new perl-5.8.8

* Tue Jan 10 2006 Jason Vas Dias <jvdias@redhat.com> - 2.05-1
- fix bug 176718: Upgrade to 2.05

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.03-20
- (#155463)
- BuildArch correction (noarch).
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Chip Turner <cturner@redhat.com> 2.03-18
- fix typo, bugzilla 122905

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Sat Jan 26 2002 Tim Powers <timp@redhat.com>
- added provides

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated.
