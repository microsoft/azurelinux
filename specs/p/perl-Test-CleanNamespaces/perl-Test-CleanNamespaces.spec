# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_Test_CleanNamespaces_enables_extra_test
%else
%bcond_with perl_Test_CleanNamespaces_enables_extra_test
%endif

Name:		perl-Test-CleanNamespaces
Summary:	Check for uncleaned imports
Version:	0.24
Release:	25%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-CleanNamespaces
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-CleanNamespaces-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.120620
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Module::Metadata)
# Module
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Module::Runtime)
BuildRequires:	perl(Package::Stash) >= 0.14
BuildRequires:	perl(Package::Stash::XS)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Identify)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(warnings)
# Optional Runtime
BuildRequires:	perl(Role::Tiny) >= 1.003000
# Test Suite
BuildRequires:	perl(constant)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(File::pushd)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(if)
BuildRequires:	perl(lib)
BuildRequires:	perl(Module::Runtime)
BuildRequires:	perl(namespace::clean)
BuildRequires:	perl(overload)
BuildRequires:	perl(parent)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Sub::Exporter)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::Needs)
BuildRequires:	perl(Test::Tester)
BuildRequires:	perl(Test::Warnings) >= 0.009
# Optional Test Requirements
%if 0%{!?perl_bootstrap:1} && %{with perl_Test_CleanNamespaces_enables_extra_test}
BuildRequires:	perl(Class::MOP::Class)
BuildRequires:	perl(metaclass)
BuildRequires:	perl(Moo) >= 1.000007
BuildRequires:	perl(Moo::Role)
BuildRequires:	perl(Moose)
BuildRequires:	perl(Moose::Exporter)
BuildRequires:	perl(Moose::Role)
BuildRequires:	perl(MooseX::Role::Parameterized)
BuildRequires:	perl(Mouse)
BuildRequires:	perl(Mouse::Role)
%endif
# Dependencies
Recommends:	perl(Role::Tiny) >= 1.003000

%description
This module lets you check your module's namespaces for imported functions you
might have forgotten to remove with namespace::autoclean or namespace::clean
and are therefore available to be called as methods, which usually isn't want
you want.

%prep
%setup -q -n Test-CleanNamespaces-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test AUTOMATED_TESTING=1

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CleanNamespaces.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-17
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-16
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-13
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-9
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 0.24-6
- Don't run optional tests for EPEL builds (avoids need for bootstrapping)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix detection of constant subs on some platforms

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-2
- Perl 5.28 rebuild

* Tue Jun 26 2018 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Properly skip potentially-problematic tests when needed, due to circular
    dependencies between Moose and Test::CleanNamespaces (CPAN RT#125678)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 19 2016 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Properly find the list of modules to test (regression since 0.19)

* Tue Aug 16 2016 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Switch to plain old Exporter, removing build_* subs from the API

* Fri Jun 17 2016 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - Removed dependencies on namespace::clean, Sub::Exporter, File::Find::Rule
- Simplify find command using -delete
- Downgrade Role::Tiny dependency to Recommends: on Fedora
- BR: perl-generators where available

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-2
- Perl 5.22 rebuild

* Wed Jan 21 2015 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Remove Moose test requires <-> Test::CleanNamespaces test recommends
    circular relationship (softened to suggests)

* Tue Jan 20 2015 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Skip Mouse tests if some required interfaces are not available

* Mon Nov 10 2014 Paul Howarth <paul@city-fan.org> - 0.16-2
- Sanitize for Fedora submission

* Thu Sep  4 2014 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Bump Package::Stash prereq to ensure used methods are available
  - Skip Moose-related tests for normal installs, to get out of circularity
    hell if Moose is installed but broken and needing an upgrade

* Wed Aug 27 2014 Paul Howarth <paul@city-fan.org> - 0.14-2
- Don't run the optional tests when bootstrapping, to avoid circular build
  dependencies
- perl(Test::Warnings) is required when bootstrapping

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Remove accidental dependency on Class::MOP (which turned into a circular
    dependency with Moose-2.1211)
- Use %%license where possible

* Wed Jun 25 2014 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Bump (optional) prereq on Moo to get some fixes for handling roles
- Edit out use of Test::Warnings in the test suite for old distributions that
  can't provide it

* Wed Jun 18 2014 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Also special case constant subs, which show up in the symbol table before
    perl 5.010 as 'constant::__ANON__'

* Tue Jun 17 2014 Paul Howarth <paul@city-fan.org> - 0.11-2
- Add upstream fix for Perl 5.8 compatibility

* Mon Jun 16 2014 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Increased version for optional Role::Tiny prereq, to get the needed is_role
    interface
  - Now ignoring 'import', 'unimport' subs; also handle users of
    Moose::Exporter without erroring
  - Now ignoring overloaded methods
  - Now also properly handle classes using Class::MOP directly
  - Fix test diagnostics in the success case
  - Fix use of a new Scalar::Util export in tests
  - The return value of namespaces_clean() and all_namespaces_clean() is now
    consistent with the result of the test(s)
  - Fixed tests to expose an issue with Mouse classes, and documented this
    (now) known issue
- Switch to ExtUtils::MakeMaker flow
- Test suite now relies on perl 5.10 or later, so don't build for anything
  older
- Drop %%defattr, redundant since rpm 4.4
- BR: perl(Test::Requires) unconditionally

* Sun Mar  9 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Fixed method identification in Moose and Mouse roles
- Update patch for building without Test::Requires

* Mon Mar  3 2014 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Lots more tests
  - In failing tests, identify the source of the uncleaned sub(s)
  - Remove the dependency on Class::MOP by inspecting the package stash
    directly
- Switch to Module::Build::Tiny flow
- Package upstream's new CONTRIBUTING and README.md files
- Don't bother trying to run the extra tests
- Test suite actually requires Test::More ≥ 0.94, so bundle a suitable
  version to use if necessary
- Drop all existing patches
- Add a patch to support building with old Module::Build::Tiny versions
- Add a patch to support building without Test::Requires if necessary

* Wed Sep 25 2013 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Re-release with fixed compile test
- Update patches as needed

* Thu Sep 19 2013 Paul Howarth <paul@city-fan.org> - 0.04-2
- Don't run the extra tests when bootstrapping

* Sun Sep 15 2013 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - Remove use of deprecated Class::MOP::load_class
- This release by ETHER -> update source URL
- Add patches to support building with old Test::More versions
- Add buildreqs for and explicitly run the extra tests

* Thu Jul 25 2013 Paul Howarth <paul@city-fan.org> - 0.03-2
- Perl 5.18 rebuild

* Sat Jun 29 2013 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
