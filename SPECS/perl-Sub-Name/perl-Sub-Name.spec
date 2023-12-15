# TODO: BR: perl(B::C) when available
# Run optional test
%bcond_without perl_Sub_Name_enables_optional_test

Name:		perl-Sub-Name
Version:	0.26
Release:	3%{?dist}
Summary:	Name - or rename - a sub
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Sub-Name
Source0:	https://cpan.metacpan.org/modules/by-module/Sub/Sub-Name-%{version}.tar.gz#/perl-Sub-Name-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(B)
BuildRequires:	perl(B::Deparse)
BuildRequires:	perl(Carp)
BuildRequires:	perl(feature)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(if)
BuildRequires:	perl(Test::More)
%if %{with perl_Sub_Name_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(Devel::CheckBin)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private perl objects
%{?perl_default_filter}

%description
This module allows one to "name" or rename subroutines, including anonymous
ones.

Note that this is mainly for aid in debugging; you still cannot call the sub
by the new name (without some deep magic).

%prep
%setup -q -n Sub-Name-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor optimize="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENCE
%else
%doc LICENCE
%endif
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/Sub/
%{perl_vendorarch}/Sub/
%{_mandir}/man3/Sub::Name.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.26-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct  6 2019 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - %%DB::sub is now populated correctly for sub names with wide characters or
    nulls (GH#9)
  - Better Perl 5.6 compatibility by lowering prereqs of core modules
  - Test for renaming lexical subs, which should work on Perl 5.22+ (GH#10)
  - Small internal changes to bring implementation in line with changes to
    Sub::Util
  - Fix "Undefined symbol "DPPP_my_croak_xs_usage"" error on some perls
    (CPAN RT#125158)
- Use author-independent source URL
- Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-10
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct  2 2016 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Fix occasional segmentation fault on OpenBSD when malloc randomization
    causes nameptr to be at the beginning of the page (CPAN RT#117072)

* Fri Aug 19 2016 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - Fix checking of SvUTF8 flag
- Simplify find commands using -empty and -delete

* Tue Aug 16 2016 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Support binary and unicode symbol names (PR#8)
  - Fixed parsing error where the name contains a single colon but the last
    separator is ::

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.24 rebuild

* Wed Mar 16 2016 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Fix uninitialized warning in test on perls < 5.8.6 (CPAN RT#104510)
  - Repository moved to the github p5sagit organization (the primary is on
    shadowcat, mirrored to github)
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-2
- Perl 5.22 rebuild

* Fri Apr 24 2015 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Remove mandatory dependencies for optional test
  - Mark the test with B::C as TODO, as it seems to fail frequently and should
    not block normal installations

* Sun Mar 29 2015 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Fix optional test of interaction with B::C that sometimes invalidly failed

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Move variable declaration to fix warning under
    -Werror=declaration-after-statement, to allow compilation under MSVC (GH#3)
  - Converted distribution packaging to Dist::Zilla
  - Fix licence in LICENSE and pod
- Package new upstream CONTRIBUTING and LICENSE files
- Classify buildreqs by usage

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Copy the contents of the %%DB::sub entry if it exists; fixes
    Devel::NYTProf's anon sub handling (CPAN RT#50524)
- Drop upstreamed debugger patch
- Drop EL-5 compatibility since we need Devel::CheckBin, which can't be
  built for EPEL-5 or EPEL-6

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Fix leak when setting a fully-qualified name (GH#1)
- Update debugger patch

* Mon Jul 14 2014 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Skip optional test if B::C 1.48 is not installed

* Fri Jul 11 2014 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Do not change the string arg in XS, use copy instead (CPAN RT#96893)
  - Add README make target
  - Add more distribution metadata
- This release by ETHER → update source URL
- Update debugger patch (CPAN RT#96893)
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.05-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.05-7
- Perl 5.16 rebuild

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 0.05-6
- Add patch for CPAN RT#50524 (copy contents of %%DB::sub entry if it exists)
- Reinstate compatibility with old distributions like EL-5
  - Add BuildRoot definition
  - Clean buildroot in %%install
  - Restore %%clean section
  - Restore %%defattr
  - Don't use + to terminate find -exec commands
- Spec clean-up
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Don't use macros for commands
  - Use tabs
  - Add buildreqs for Perl core modules that might be dual-lived
  - Explicit requires for "use base XXX;" only required prior to rpm 4.9

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat Dec 18 2010 Iain Arnell <iarnell@gmail.com> - 0.05-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- BR perl(Test::More)
- Requires perl(DynaLoader) and perl(Exporter)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-5
- Rebuild against perl 5.10.1

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-4
- Filtering errant private provides

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 03 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update to 0.04

* Sat Mar 15 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Update to 0.03

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-5
- Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.02-4.1
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-3.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-3
- Bump

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-2
- Bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Specfile autogenerated by cpanspec 1.69.1
