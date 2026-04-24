# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-ConfigFromFile
Version:        0.14
Release: 34%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:        An abstract Moose role for setting attributes from a configfile
URL:            https://metacpan.org/release/MooseX-ConfigFromFile
Source:         https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-ConfigFromFile-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build::Tiny) >= 0.007
BuildRequires:  perl(strict)
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(MooseX::Types::Moose)
BuildRequires:  perl(MooseX::Types::Path::Tiny) >= 0.005
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::Without::Module)
# Optional Test Requirements
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Prereqs) >= 2.120900
BuildRequires:  perl(MooseX::Getopt)
# Dependencies
# (none)

# Avoid doc-file dependencies from tests
%{?perl_default_filter}

%description
This is an abstract role which provides an alternate constructor for
creating objects using parameters passed in from a configuration file. The
actual implementation of reading the configuration file is left to concrete
subroles.

It declares an attribute 'configfile' and a class method 'new_with_config',
and requires that concrete roles derived from it implement the class method
'get_config_from_file'.

Attributes specified directly as arguments to 'new_with_config' supersede
those in the configfile.

%prep
%setup -q -n MooseX-ConfigFromFile-%{version}

# Fix shellbangs in tests to placate rpmlint
sed -i '1s,#!perl,#!%{__perl},' t/*.t

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::ConfigFromFile.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-25
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-22
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-19
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Paul Howarth <paul@city-fan.org> - 0.14-17
- Spec tidy-up
  - Use author-independent source URL
  - Refresh stale list of build dependencies

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-15
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-11
- Perl 5.28 re-rebuild of bootstrapped packages

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-7
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 19 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.14-1
- Update to 0.14

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-7
- Perl 5.22 re-rebuild of bootstrapped packages

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-6
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-5
- Perl 5.20 re-rebuild of bootstrapped packages

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  8 2014 Paul Howarth <paul@city-fan.org> - 0.13-2
- Don't BR: perl(MooseX::SimpleConfig) when bootstrapping

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Documentation corrected to demostrate how to properly override the
    configfile method to provide a default from the consuming class, without
    having to redefine the attribute itself
  - If MooseX::Getopt is installed, the configfile attribute has the Getopt
    trait applied
  - The configfile attribute is now a Path::Tiny, not a Path::Class (coercions
    from strings are still supported, and now also from any other type that has
    a string coercion)
  - Allow configfiles called "0"
  - configfile value now passed through to new()
  - New _get_default_configfile method added, which consumers can override to
    provide a default value without having to redefine the attribute itself
    (via CPAN RT#79746) - PLEASE READ THE DOCUMENTATION if you override the
    configfile attribute!
  - Allow clean composition into a role, without requiring an -exclude
  - Bump prereq version for MooseX::Types::Path::Tiny to ensure a broken
    version is not installed
  - Warnings tests bypassed during installation
  - Repository migrated from shadowcat to the github moose organization
- This release by ETHER -> update source URL
- Switch to Module::Build::Tiny flow
- Classify buildreqs by usage
- Package upstream's CONTRIBUTING, LICENSE and README.md files

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.04-7
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.04-3
- Perl 5.16 rebuild

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.04-2
- rebuilt again for F17 mass rebuild

* Fri Jan 13 2012 Iain Arnell <iarnell@gmail.com> 0.04-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.03-2
- Perl mass rebuild

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.03-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use perl_default_filter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- brush up for submission

* Mon Oct 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

