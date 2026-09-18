# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_Devel_Declare_enables_extra_test
%else
%bcond_with perl_Devel_Declare_enables_extra_test
%endif

Name:           perl-Devel-Declare
Version:        0.006022
Release:        25%{?dist}
Summary:        Adding keywords to perl, in perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Devel-Declare
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-Declare-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::Depends)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(B::Hooks::EndOfScope) >= 0.05
BuildRequires:  perl(B::Hooks::OP::Check) >= 0.19
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Scalar::Util) >= 1.11
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Name)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl-debugger
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
# Optional Tests
BuildRequires:  perl(B::Compiling)
%if !%{defined perl_bootstrap} && %{with perl_Devel_Declare_enables_extra_test}
# Break build-cycle: perl-Devel-Declare → perl-Devel-CallParser → perl-Devel-Declare
BuildRequires:  perl(Devel::CallParser)
%endif
BuildRequires:  perl(Filter::Util::Call)
# Dependencies
# Necessary minimum versions not automatically detected
Requires:       perl(B::Hooks::EndOfScope) >= 0.05

# Avoid provides from perl shared objects
%{?perl_default_filter}

%description
Devel::Declare can install subroutines called declarators which locally take
over Perl's parser, allowing the creation of new syntax.

This module is now deprecated: keyword handling has been included in the perl
core since perl 5.14, and better alternatives for Devel::Declare functionality
include Devel::CallParser, Function::Parameters, and Keyword::Simple.

%prep
%setup -q -n Devel-Declare-%{version}

%build
perl Makefile.PL \
  INSTALLDIRS=vendor \
  OPTIMIZE="%{optflags}" \
  NO_PACKLIST=1 \
  NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/Devel/
%{perl_vendorarch}/Devel/
%{_mandir}/man3/Devel::Declare.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-24
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-23
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-20
- Perl 5.40 re-rebuild of bootstrapped packages

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-19
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-15
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-14
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-11
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-10
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-7
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.006022-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.006022-2
- Perl 5.32 rebuild

* Sun Apr 26 2020 Paul Howarth <paul@city-fan.org> - 0.006022-1
- Update to 0.006022
  - Use ppport.h for compatibility with earlier perls
  - Update to work with Perl 5.31.7 (GH#1)
- Use %%{make_build} and %%{make_install}
- Package LICENSE file

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.006019-16
- BR: perl-debugger for t/debug.t

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov  6 2019 Paul Howarth <paul@city-fan.org> - 0.006019-14
- Avoid need for bootstrapping in EPEL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-12
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.006019-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.006019-2
- Perl 5.26 rebuild

* Tue Mar 28 2017 Paul Howarth <paul@city-fan.org> - 0.006019-1
- Update to 0.006019
  - Added deprecated flag to metadata; no deprecation warning is given at
    runtime... for now
  - Added "WARNING" section in pod, advising the deprecated status of this
    module

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.006018-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.006018-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.006018-7
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 0.006018-6
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.006018-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006018-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.006018-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.006018-2
- Perl 5.22 rebuild

* Wed Mar 25 2015 Paul Howarth <paul@city-fan.org> - 0.006018-1
- Update to 0.006018
  - Tests fixed for blead (5.21.*) (CPAN RT#102918)

* Tue Feb 24 2015 Petr Pisar <ppisar@redhat.com> - 0.006017-2
- Break build-cycle: perl-Devel-Declare → perl-Devel-CallParser →
  perl-Devel-Declare

* Tue Dec  2 2014 Paul Howarth <paul@city-fan.org> - 0.006017-1
- Update to 0.006017
  - Updates for some deprecations in perl 5.17 (CPAN RT#83968)
  - Fix use of wrong sprintf formatting codes (CPAN RT#91983)
  - Fixed syntax error in a test
  - Fix for changes in 5.21.4 (avoid creating GVs when subs are declared,
    CPAN RT#99102)
  - Converted dist to Distar
- This release by ETHER → update source URL
- Classify buildreqs by usage
- Make %%files list more explicit

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.006011-9
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006011-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006011-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006011-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.006011-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.006011-2
- Perl 5.16 rebuild

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 0.006011-1
- update to latest upstream version

* Wed Feb 08 2012 Iain Arnell <iarnell@gmail.com> 0.006010-1
- update to latest upstream version

* Fri Feb 03 2012 Iain Arnell <iarnell@gmail.com> 0.006009-1
- update to latest upstream version
- add README to docs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 06 2011 Iain Arnell <iarnell@gmail.com> 0.006008-1
- update to latest upstream version

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 0.006007-1
- update to latest upstream version

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 0.006006-1
- update to latest upstream

* Tue Jul 26 2011 Iain Arnell <iarnell@gmail.com> 0.006005-1
- update to latest upstream

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.006004-2
- Perl mass rebuild

* Tue May 03 2011 Iain Arnell <iarnell@gmail.com> 0.006004-1
- update to latest upstream version

* Wed Apr 20 2011 Iain Arnell <iarnell@gmail.com> 0.006003-1
- update to latest upstream version

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.006002-1
- update to latest upstream version

* Sun Feb 27 2011 Iain Arnell <iarnell@gmail.com> 0.006001-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.006000-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat Jul 17 2010 Iain Arnell <iarnell@gmail.com> 0.006000-2
- cleanup spec for moderm rpmbuild
- BR perl(B::Compiling)

* Sat Jul 03 2010 Iain Arnell <iarnell@gmail.com> 0.006000-1
- Specfile autogenerated by cpanspec 1.78.
