# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Sub_Identify_enables_optional_test
%else
%bcond_with perl_Sub_Identify_enables_optional_test
%endif

Name:		perl-Sub-Identify
Version:	0.14
Release:	13%{?dist}
Summary:	Retrieve names of code references
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Sub-Identify
Source0:	https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Sub-Identify-%{version}.tar.gz#/perl-Sub-Identify-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl(Config)
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(B)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(XSLoader)
# Test Suite
# feature required with perl ≥ 5.020

BuildRequires:	perl(feature)

BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(warnings)
%if %{with perl_Sub_Identify_enables_optional_test}
# Optional tests
BuildRequires:	perl(Test::Pod) >= 1.14
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(B)
Requires:	perl(XSLoader)

# Don't provide private perl libs
%{?perl_default_filter}

%description
Sub::Identify allows you to retrieve the real name of code references. For
this, it uses Perl's introspection mechanism, provided by the B module.

%prep
%setup -q -n Sub-Identify-%{version}

# Fix script interpreters
perl -MConfig -pi -e 's|^#!perl|$Config{startperl}|' t/*

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
%doc Changes README.mdown TODO.mdown t/
%{perl_vendorarch}/auto/Sub/
%{perl_vendorarch}/Sub/
%{_mandir}/man3/Sub::Identify.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-10
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Petr Pisar <ppisar@redhat.com> - 0.14-5
- Rewrite script interpreters correctly

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-2
- Perl 5.26 rebuild

* Tue Apr 11 2017 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Make tests pass without . in @INC (actual fix)

* Mon Apr  3 2017 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Reformatted Changes to follow basic format in CPAN::Changes::Spec
  - Make tests pass without . in @INC

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Petr Pisar <ppisar@redhat.com> - 0.12-4
- Check for distribution instead of perl version

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep  8 2015 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Fix build on perl 5.8

* Fri Sep  4 2015 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Add test for Perl's subroutine signatures feature (GH#5)
  - Do not let get_code_location() segfault on XSUBs
- BR: perl-devel for EXTERN.h
- Drop EL-5 support

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-2
- Perl 5.22 rebuild

* Wed Jan  7 2015 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Fix test failure due to hard-coded filenames

* Thu Sep 18 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Add test for function prototypes
  - Better, simpler code for testing if we can load the XS version
  - Add gitignore file
  - Experimental implementation of get_code_location
  - Add XS implementation of get_code_location()
  - Add test for the prototype of get_code_location
  - Make get_code_location work on undefined subs
  - Add link to github repo in the meta file
  - Add TODO file
  - Add pure-perl implementation of is_sub_constant()
  - Add XS implementation of is_constant_sub()
  - Add documentation
  - Skip tests that rely on perls more recent than 5.14.0
  - Update ppport.h
  - Use the pure-perl version of is_sub_constant on perls earlier than 5.16
  - Require B unconditionally on older perls
  - Require at least perl 5.8.0
  - Improve docs beyond a really terse synopsis
- Classify buildreqs by usage
- Drop %%defattr, redundant since rpm 4.4

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-21
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.04-17
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.04-14
- Perl 5.16 rebuild

* Mon Mar  5 2012 Paul Howarth <paul@city-fan.org> - 0.04-13
- Use %%{optflags}
- BR: perl(Exporter) and perl(Test::Pod)
- Make %%files list more explicit
- Use DESTDIR rather than PERL_INSTALL_ROOT
- No need to remove empty directories from buildroot
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-9
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-7
- Rebuild against perl 5.10.1

* Fri Aug 28 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-6
- Bump

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-5
- Filtering errant private provides

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-2
- Aaaand change files to look in the the arch-dependent dirs

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update to 0.04
- Drop buildarch noarch, as we have some XS bits now

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Update to 0.03

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-3
- Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-2.2
- Add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-2.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-2
- Bump

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Specfile autogenerated by cpanspec 1.69.1
