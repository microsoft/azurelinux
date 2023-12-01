%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DB\\)
Summary:        Perl module to print improved warning messages
Name:           perl-Carp-Clan
Version:        6.08
Release:        4%{?dist}
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Carp-Clan
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Carp-Clan-%{version}.tar.gz#/perl-Carp-Clan-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:      noarch
%if !%{defined perl_bootstrap}
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Object::Deadly)
BuildRequires:  perl(Test::More)
# Run-time
BuildRequires:  perl(overload)
%endif

%description
This module reports errors from the perspective of the caller of a
"clan" of modules, similar to "Carp.pm" itself. But instead of giving
it a number of levels to skip on the calling stack, you give it a
pattern to characterize the package names of the "clan" of modules
which shall never be blamed for any error.

%prep
%setup -q -n Carp-Clan-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

%check
%if !%{defined perl_bootstrap}
make test
%endif

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Carp/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 6.08-4
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.08-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Petr Pisar <ppisar@redhat.com> - 6.08-1
- 6.08 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.07-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.07-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.07-1
- 6.07 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-9
- Perl 5.28 re-rebuild of bootstrapped packages

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-1
- 6.06 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-23
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-22
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-20
- Package cleanup

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-18
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-17
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-16
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-15
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-13
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.04-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 6.04-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 6.04-7
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 6.04-6
- Do not export private modules

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.04-4
- rebuild with Perl 5.14.1
- use perl_bootstrap macro

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.04-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.04-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 6.04-1
- new upstream version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.03-2
- rebuild against perl 5.10.1

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.031
- update to 6.03

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> - 6.00-4
- Really remove the no-prompt patch to avoid RPM rebuild errors

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 6.0-1
- update to 6.0

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.9-5
- rebuild for new perl (normally)

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.9-4.1
- temporarily disable BR on Object::Deadly, tests

* Mon Nov 19 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-4
- Add BR: perl-Object-Deadly now that it is included in Fedora

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-3
- Fix BuildRequires
- Various specfile cleanups

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-2
- Update license tag.

* Mon Jun 04 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-1
- Update to latest CPAN version: 5.9
- Upstream Makefile.PL prompts for user input to include
  Object::Deadly as a prerequisite.  We don't ship Object::Deadly, so
  just comment out the prompt.

* Fri Jan 26 2007 Robin Norwood <rnorwood@redhat.com> - 5.8-2
- Resolves: bz#224571 - Remove erroneous rpm 'provides' of perl(DB)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 5.8-1
- New version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.3-2
- rebuild for perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.3-1
- First build.
