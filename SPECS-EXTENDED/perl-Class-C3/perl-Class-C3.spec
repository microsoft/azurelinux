Name:		perl-Class-C3
Version:	0.35
Release:	1%{?dist}
Summary:	Pragma to use the C3 method resolution order algorithm
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Class-C3
Source0:	https://cpan.metacpan.org/modules/by-module/Class/Class-C3-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Text::ParseWords)
# Build (dependencies of bundled ExtUtils::HasCompiler)
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Module
BuildRequires:	perl(Algorithm::C3) >= 0.07
BuildRequires:	perl(Scalar::Util) >= 1.10
# Test Suite
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(lib)
BuildRequires:	perl(NEXT)
BuildRequires:	perl(Sub::Name)
BuildRequires:	perl(Test::Exception) >= 0.15
BuildRequires:	perl(Test::More) >= 0.88
# MRO::Compat itself requires Class::C3
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(MRO::Compat)
%endif
# Dependencies
Requires:	perl(Algorithm::C3) >= 0.07
Requires:	perl(Scalar::Util) >= 1.10

# Let people "use c3;"
Provides:	perl(c3) = %{version}

%description
This is a pragma to change Perl 5's standard method resolution order from
depth-first left-to-right (a.k.a - pre-order) to the more sophisticated C3
method resolution order.

%prep
%setup -q -n Class-C3-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
cp -p opt/c3.pm %{buildroot}%{perl_vendorlib}/
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/c3.pm
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::C3.3*
%{_mandir}/man3/Class::C3::next.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.35-1
- Update to version 0.35
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.34-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-7
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Update bundled ExtUtils::HasCompiler to 0.021
  - Fix some examples in pod

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-2
- Perl 5.26 rebuild

* Mon Apr 24 2017 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Update bundled ExtUtils::HasCompiler to 0.017
  - Moved repository to Moose GitHub org
  - Avoid using base.pm in tests (CPAN RT#120530)
  - Minor pod and test clean ups

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Update bundled ExtUtils::HasCompiler to 0.016

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-2
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Update bundled ExtUtils::HasCompiler to 0.013 to fix possible false
    negative (CPAN RT#113635)
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Paul Howarth <paul@city-fan.org> - 0.30-2
- Don't ship the tests
- Drop requires/provides filters, only needed due to shipping tests

* Mon Oct 19 2015 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Update compiler detection to use ExtUtils::HasCompiler

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-2
- Perl 5.22 rebuild

* Tue Apr 14 2015 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - Change link to Dylan paper to use archive.org, as the original link has
    gone offline (CPAN RT#99756)
- Pod tests moved to xt/ so drop build requirements for them

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Sep 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.20 rebuild

* Thu Sep  4 2014 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27:
  - Declare minimum perl version of 5.6 in metadata
- Upstream ChangeLog renamed to Changes
- Upstream dropped visualize_c3.pl utility script

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar  5 2014 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26:
  - Fix bug in Makefile.PL when ExtUtils::CBuilder not available
- This release by HAARG -> update source URL
- Clean up for modern rpmbuild since build requirements are not available in
  EL-5
- Drop obsoletes/provides for old tests sub-package
- Drop unnecessary %%perl_ext_env_unset macro usage
- Add optional test requirements

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.25-2
- Perl 5.18 rebuild

* Thu Jul  4 2013 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25:
  - Drop compatibility from 5.6.2 to 5.6.0
  - Pod typo fixes (CPAN RT#77453, CPAN RT#85357)
  - Only ask for Devel::Hide on perls where it will be actually used
    (CPAN RT#81106)
  - Fix SYNOPSIS to actually be executable (CPAN RT#78327)
- This release by MSTROUT -> update source URL
- BR: perl(ExtUtils::CBuilder) and perl(File::Glob)
- Bump perl(Class::C3::XS) version requirement to 0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.24-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.24-2
- Perl 5.16 rebuild

* Sat May 12 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24:
  - Require Class::C3::XS on 5.8 perls if a working compiler is found
- Bump Algorithm::C3 version requirement to 0.07
- Always BR:/R: Algorithm::C3 and Scalar::Util
- Don't need to remove empty directories from buildroot

* Sat Jan 21 2012 Paul Howarth <paul@city-fan.org> - 0.23-5
- Obsolete/provide old -tests subpackage to support upgrades

* Wed Jan 18 2012 Paul Howarth <paul@city-fan.org> - 0.23-4
- Reinstate compatibility with older distributions like EL-5
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- BR: perl(MRO::Compat) for testing if we're not bootstrapping
- Don't use macros for commands
- Make %%files list more explicit
- Filter unwanted requires and provides
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> - 0.23-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- No more need to disable __perl_provides

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-4
- Bump

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-3
- Install c3.pm as well; drop opt/ from doc
- Conditionalise

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-2
- Mass rebuild with perl-5.12.0

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-1
- PERL_INSTALL_ROOT => DESTDIR
- Add perl_default_subpackage_tests, and drop t/ from doc
- Add perl_default_filter (and update filtering)
- Auto-update to 0.22 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Added a new br on perl(Scalar::Util) (version 1.10)
- Altered br on perl(Test::More) (0 => 0.47)
- Added a new req on perl(Scalar::Util) (version 1.10)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.21-3
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.21-1
- Update to 0.21

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.20-1
- Update to 0.20

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-2
- Rebuild for new perl

* Wed Oct 10 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.19-1
- Update to 0.19

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.18-1
- Update to 0.18

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.17-1
- Update to 0.17
- BR Class::C3::XS

* Mon Sep 25 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.14-1
- Update to 0.14

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-4
- Fix autoprovides (#205801)

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-3
- Bump

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-2
- Additional br's, minor spec tweaks

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-1
- Specfile autogenerated by cpanspec 1.69.1
