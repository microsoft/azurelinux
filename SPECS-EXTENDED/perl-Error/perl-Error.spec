Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Error
Version:        0.17029
Release:        4%{?dist}
Summary:        Error/exception handling in an OO-ish way
License:        (GPL+ or Artistic) and MIT
URL:            https://metacpan.org/release/Error
Source0:        https://cpan.metacpan.org/modules/by-module/Error/Error-%{version}.tar.gz#/perl-Error-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(base)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(blib)
BuildRequires:  perl(Test::More)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

# Avoid provides/requires from examples
%global __provides_exclude_from ^%{_docdir}
%global __requires_exclude_from ^%{_docdir}

%description
The Error package provides two interfaces. Firstly Error provides a
procedural interface to exception handling. Secondly Error is a base class
for errors/exceptions that can either be thrown, for subsequent catch, or
can simply be recorded.

%prep
%setup -q -n Error-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
# GPL+ or Artistic
%doc ChangeLog Changes README examples/
%{perl_vendorlib}/Error.pm
%{_mandir}/man3/Error.3*
# MIT
%{perl_vendorlib}/Error/
%{_mandir}/man3/Error::Simple.3*

%changelog
* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com> - 0.17029-4
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsoft.com> - 0.17029-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.17029-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 1:0.17029-1
- Update to 0.17029
  - Rebuild for order of 'NAME' and 'VERSION' sections in the generated POD
    documentation (VERSION used to appear before NAME)

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 1:0.17028-1
- Update to 0.17028
  - Moved the VCS repo to https://github.com/shlomif/perl-error.pm

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17027-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17027-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Paul Howarth <paul@city-fan.org> - 1:0.17027-1
- Update to 0.17027
  - Documentation and examples enhancements (GH#1)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17026-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17026-2
- Perl 5.28 rebuild

* Thu May 24 2018 Paul Howarth <paul@city-fan.org> - 1:0.17026-1
- Update to 0.17026
  - Convert to Dist-Zilla
- Switch to ExtUtils::MakeMaker flow
- Switch upstream from search.cpan.org to metacpan.org

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug  8 2017 Paul Howarth <paul@city-fan.org> - 1:0.17025-1
- Update to 0.17025
  - Fix 'use Error::Simple' overriding the $VERSION (CPAN RT#122713)
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17024-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-10
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17024-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.17024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17024-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17024-2
- Perl 5.22 rebuild

* Sun May 31 2015 Paul Howarth <paul@city-fan.org> - 1:0.17024-1
- Update to 0.17024
  - Add link to the VCS repository in META.yml

* Thu Feb 12 2015 Paul Howarth <paul@city-fan.org> - 1:0.17023-1
- Update to 0.17023
  - Minimal version of Module-Build reduced to 0.280801 (CPAN RT#102062)
- Use %%license where possible

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17022-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17022-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 29 2014 Paul Howarth <paul@city-fan.org> - 1:0.17022-1
- Update to 0.17022
  - Add "use warnings;" to everything
  - Add a separate LICENSE file

* Thu Oct  3 2013 Paul Howarth <paul@city-fan.org> - 1:0.17021-1
- Update to 0.17021
  - Fix for the format of the new Carp in bleadperl (CPAN RT#88137)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.17020-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.17020-2
- Perl 5.18 rebuild

* Sun May  5 2013 Paul Howarth <paul@city-fan.org> - 1:0.17020-1
- Update to 0.17020
  - Change to Shlomi Fish's new E-mail and web address
  - Clarify the licence of lib/Error/Simple.pm (CPAN RT#81277)
  - Correct typos (CPAN RT#85023)
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Avoid provides/requires from examples

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17018-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.17018-5
- Add MIT license

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17018-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:0.17018-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1:0.17018-2
- Perl 5.16 rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1:0.17018-1
- 0.17018 bump
- Specify all dependencies
- Skip POD tests on bootstrap

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.17016-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17016-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.17016-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.17016-3
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.17016-2
- Mass rebuild with perl-5.12.0

* Mon Jan 18 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.1716-1
- update

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.17015-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.17015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 02 2008 Steven Pritchard <steve@kspei.com> 1:0.17015-1
- Update to 0.17015.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 1:0.17014-1
- Update to 0.17014.

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.17012-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1:0.17012-1
- Update to 0.17012.

* Mon Jan 07 2008 Steven Pritchard <steve@kspei.com> 1:0.17011-1
- Update to 0.17011.
- Canonicalize Source0 URL.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Improve Summary.
- Reformat to match cpanspec output.
- Build with Module::Build.

* Tue Dec 04 2007 Ralf Corsépius <rc040203@freenet.de> - 1:0.17010-1
- Upstream update.
- Update license tag.

* Sat Oct 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17008-1
- Update to 0.17008.

* Wed Oct 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17007-1
- Update to 0.17007.

* Sat Oct  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17006-1
- Update to 0.17006.
- New build requirements: Test::Pod and Test::Pod::Coverage.

* Wed Oct  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17005-1
- Update to 0.17005.

* Mon Sep  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17004-1
- Update to 0.17004.

* Mon Aug 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17003-1
- Update to 0.17003.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17001-1
- Update to 0.17001.

* Fri Jul 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.17-1
- Update to 0.17.

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:0.16-1
- Update to 0.16.

* Fri Apr 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15009-1
- Update to 0.15009.

* Wed Apr 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15008-1
- Update to 0.15008.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-3
- Dist tag.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.15-2
- rebuilt

* Fri Jun 11 2004 Steven Pritchard <steve@kspei.com> 0:0.15-1
- Specfile autogenerated.
