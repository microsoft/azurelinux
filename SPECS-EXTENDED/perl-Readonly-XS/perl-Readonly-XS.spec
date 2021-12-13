Vendor:         Microsoft Corporation
Distribution:   Mariner
# Provides/Requires filtering is different from rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -p -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e' 2>/dev/null || echo 0)

Name:		perl-Readonly-XS
Version:	1.05
Release:	37%{?dist}
Summary:	Companion module for Readonly
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Readonly-XS
Source0:	https://cpan.metacpan.org/authors/id/R/RO/ROODE/Readonly-XS-%{version}.tar.gz#/perl-Readonly-XS-%{version}.tar.gz
Patch0:		Readonly-XS-1.05-prereq.patch
Patch1:		Readonly-XS-1.05-interpreter.patch
# Build (perl-devel split from main perl package at F-7)
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test suite
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Readonly) >= 1.02

# Don't provide the private XS.so() lib
%{?perl_default_filter}

%description
Readonly::XS is a companion module for Readonly, to speed up read-only
scalar variables.

%prep
%setup -q -n Readonly-XS-%{version}

# Build process does not actually need perl(Readonly)
%patch0

# Fix script interpreter for test suite since we're packaging it
%patch1

# And tests don't need to be executable either
chmod -c -x t/test.t

# Avoid doc-file dependencies from tests if we don't have %%perl_default_filter
%if ! %{rpm49}
%global perl_reqfilt /bin/sh -c "%{__perl_requires} | grep -Fvx 'perl(Test::More)'"
%global __perl_requires %{perl_reqfilt}
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc README Changes t/
%{perl_vendorarch}/auto/Readonly/
%{perl_vendorarch}/Readonly/
%{_mandir}/man3/Readonly::XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.05-37
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-34
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-31
- Perl 5.28 rebuild

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 1.05-30
- BR: gcc
- Remove redundant exec permissions from tests
- Simplify find commands using -empty and -delete
- Drop EL-5 support
  - BR: perl-devel unconditionally
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-26
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-24
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Paul Howarth <paul@city-fan.org> - 1.05-22
- Spec clean-up:
  - Drop %%defattr, redundant since rpm 4.4
  - Prefer %%global over %%define
  - Drop obsoletes/provides for old -tests sub-package
  - Flesh out buildreqs
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-20
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-19
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.05-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.05-13
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.05-11
- Perl 5.16 rebuild

* Thu Mar  1 2012 Paul Howarth <paul@city-fan.org> - 1.05-10
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't use macros for commands
- No need to remove empty directories from buildroot
- Add buildreqs for Perl core modules that might be dual-lived
- Rename makefile patch to include module name and version
- Fix script interpreter for test suite since we're packaging it
- Add filter for doc-file dependencies if we don't have %%perl_default_filter
- Make %%files list more explicit
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-5
- Mass rebuild with perl-5.12.0

* Sun Feb 21 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.05-4
- Add perl_default_filter, etc
- PERL_INSTALL_ROOT => DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.05-1
- Update to 1.05
- Filter our provides to prevent private lib from showing up
- Drop patch1; incorporated upstream as of 1.05

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-11
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.04-10.2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-9.2
- Patch Carp::croak call for new perl

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-9
- Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-8.2
- Add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-8.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-8
- Bump

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-7
- Bump for missing patch...

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-6
- Drop br on perl(Readonly), patch Makefile.PL as well
- Rework spec to use macros

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.04-5
- Rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-4
- Bump for mass rebuild

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-3
- Proper version on perl(Readonly) BuildRequires & Requires

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-1
- New Version
- BuildRequires perl(Readonly), remove explicit requires on
  perl-Readonly version

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-2
- Fix license and BuildRequires

* Sat Nov 12 2005 Michael A. Peters <mpeters@mac.com> - 1.03-1
- Created spec file
