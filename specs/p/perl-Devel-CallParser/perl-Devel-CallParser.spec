# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Devel-CallParser
Version:        0.002
Release:        40%{?dist}
Summary:        Custom parsing attached to subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Devel-CallParser
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CallParser-%{version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.11.2
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.15
BuildRequires:  perl(Module::Build)
# Module
BuildRequires:  perl(Devel::CallChecker) >= 0.002
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(DynaLoader::Functions) >= 0.001
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File) >= 1.03
BuildRequires:  perl(Test::More)
# Optional Tests
#BuildRequires: perl(Data::Alias) >= 1.13          # Retired in Fedora since Fedora 25, could be revived if desired
BuildRequires:  perl(Devel::Declare) >= 0.006004
BuildRequires:  perl(indirect) >= 0.27
#BuildRequires: perl(Lexical::Sub) >= 0.004        # Test fails with Lexical::Sub 0.010 (CPAN RT#147376, rhbz#2182352)
#BuildRequires: perl(Sub::StrictDecl) >= 0.001     # Not yet packaged
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
# Dependencies
Requires:       perl(Devel::CallChecker) >= 0.002
Requires:       perl(DynaLoader)
Requires:       perl(DynaLoader::Functions) >= 0.001

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Devel::CallChecker\\)

%description
This module provides a C API, for XS modules, concerned with custom parsing.
It is centered around the function cv_set_call_parser, which allows XS code to
attach a magical annotation to a Perl subroutine, resulting in resolvable
calls to that subroutine having their arguments parsed by arbitrary C code
(this is a more conveniently structured facility than the core's
PL_keyword_plugin API). This module makes cv_set_call_parser and several
supporting functions available.

%prep
%setup -q -n Devel-CallParser-%{version}

%build
perl Build.PL --installdirs=vendor --optimize="%{optflags}"
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%doc Changes README
%{perl_vendorarch}/auto/Devel/
%{perl_vendorarch}/Devel/
%{_mandir}/man3/Devel::CallParser.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-39
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-36
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-32
- Perl 5.38 rebuild

* Thu May 11 2023 Paul Howarth <paul@city-fan.org> - 0.002-31
- Drop optional test dependency Lexical::Sub for now; t/leximport.t fails with
  Lexical::Sub 0.010 (CPAN RT#147376, rhbz#2182352)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-28
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-25
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-22
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov  6 2019 Paul Howarth <paul@city-fan.org> - 0.002-20
- Spec tidy-up
  - Use author-independent source URL
  - Refresh buildreqs
  - Simplify find command using -empty
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-15
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-14
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-5
- Perl 5.22 rebuild
- Disable optional test BR Data::Alias

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 23 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-1
- 0.002 bump, bug fixes

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 0.001-6
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.001-2
- Perl 5.16 rebuild

* Mon May 21 2012 Jitka Plesnikova <jplesnik@redhat.com> 0.001-1
- Specfile autogenerated by cpanspec 1.78.
