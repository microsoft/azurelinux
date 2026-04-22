# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-MooseX-Types-Path-Tiny
Summary:	Path::Tiny types and coercions for Moose
Version:	0.012
Release: 27%{?dist}
License:	Apache-2.0
URL:		https://metacpan.org/release/MooseX-Types-Path-Tiny
Source0:	https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-Types-Path-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Module::Build::Tiny) >= 0.034
# Module Runtime
BuildRequires:	perl(if)
BuildRequires:	perl(Moose) >= 2
BuildRequires:	perl(MooseX::Getopt)
BuildRequires:	perl(MooseX::Types)
BuildRequires:	perl(MooseX::Types::Moose)
BuildRequires:	perl(MooseX::Types::Stringlike)
BuildRequires:	perl(namespace::autoclean)
BuildRequires:	perl(Path::Tiny)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp) >= 0.18
BuildRequires:	perl(File::pushd)
BuildRequires:	perl(Module::Metadata)
BuildRequires:	perl(Moose::Conflicts)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.96
# Optional Test Requirements
BuildRequires:	perl(CPAN::Meta) >= 2.120900
# Dependencies
Requires:	perl(MooseX::Getopt)
Requires:	perl(namespace::autoclean)

%description
This module provides Path::Tiny types for Moose. It handles two important
types of coercion:

 * Coercing objects with overloaded stringification

 * Coercing to absolute paths

It also can check to ensure that files or directories exist.

%prep
%setup -q -n MooseX-Types-Path-Tiny-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::Types::Path::Tiny.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Paul Howarth <paul@city-fan.org> - 0.012-10
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-2
- Perl 5.26 rebuild

* Thu Apr  6 2017 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012
  - Repository migrated to the github moose organization
  - Switch from Test::Requires to Test::Needs in tests
  - Add MooseX::Getopt option type maps when MooseX::Getopt is installed

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - Documentation amendments
  - Add missing prereq declaration
- Use %%license
- Add explicit dependency on perl(namespace::autoclean)

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Paul Howarth <paul@city-fan.org> - 0.010-2
- Incorporate feedback from package review (#1081966)
  - BR: perl(Moose::Conflicts) for test suite

* Thu Mar 27 2014 Paul Howarth <paul@city-fan.org> - 0.010-1
- Initial RPM version
