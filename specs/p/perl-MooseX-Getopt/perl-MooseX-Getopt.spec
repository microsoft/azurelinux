# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_MooseX_Getopt_enables_extra_test
%else
%bcond_with perl_MooseX_Getopt_enables_extra_test
%endif

Name:           perl-MooseX-Getopt
Summary:        Moose role for processing command line options
Version:        0.78
Release: 4%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MooseX-Getopt
Source0:        https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-Getopt-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build::Tiny) >= 0.034
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Getopt::Long) >= 2.37
BuildRequires:  perl(Getopt::Long::Descriptive) >= 0.081
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Meta::Attribute)
BuildRequires:  perl(Moose::Role) >= 0.56
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(MooseX::Role::Parameterized)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(if)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moose::Meta::Class)
BuildRequires:  perl(Moose::Util)
BuildRequires:  perl(Path::Tiny) >= 0.009
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(Test::Requires) >= 0.05
BuildRequires:  perl(Test::Trap)
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(version)
# Optional Test Requirements
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120900
# MooseX::SimpleConfig → MooseX::ConfigFromFile → MooseX::Types::Path::Class → MooseX::Getopt
%if !0%{?perl_bootstrap} && %{with perl_MooseX_Getopt_enables_extra_test}
BuildRequires:  perl(MooseX::ConfigFromFile) >= 0.08
BuildRequires:  perl(MooseX::SimpleConfig) >= 0.07
BuildRequires:  perl(MooseX::StrictConstructor)
%endif
BuildRequires:  perl(Test::Warnings) >= 0.034
BuildRequires:  perl(YAML)
# Dependencies
# (none)

# Make sure we don't get doc-file dependencies from the tests
%{?perl_default_filter}

%description
This is a Moose role which provides an alternate constructor for creating
objects using parameters passed in from the command line.

%prep
%setup -q -n MooseX-Getopt-%{version}

# Silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t
chmod -c -x t/104_override_usage.t

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
%{_mandir}/man3/MooseX::Getopt.3*
%{_mandir}/man3/MooseX::Getopt::Basic.3*
%{_mandir}/man3/MooseX::Getopt::Dashes.3*
%{_mandir}/man3/MooseX::Getopt::GLD.3*
%{_mandir}/man3/MooseX::Getopt::Meta::Attribute.3*
%{_mandir}/man3/MooseX::Getopt::Meta::Attribute::NoGetopt.3*
%{_mandir}/man3/MooseX::Getopt::Meta::Attribute::Trait.3*
%{_mandir}/man3/MooseX::Getopt::Meta::Attribute::Trait::NoGetopt.3*
%{_mandir}/man3/MooseX::Getopt::OptionTypeMap.3*
%{_mandir}/man3/MooseX::Getopt::ProcessedArgv.3*
%{_mandir}/man3/MooseX::Getopt::Strict.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan  3 2025 Paul Howarth <paul@city-fan.org> - 0.78-1
- Update to 0.78 (rhbz#2335439)

* Fri Jan  3 2025 Paul Howarth <paul@city-fan.org> - 0.77-1
- Update to 0.77 (rhbz#2335370)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Paul Howarth <paul@city-fan.org> - 0.76-1
- Update to 0.76 (rhbz#2255149)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.75-7
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.75-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.75-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.75-2
- Perl 5.34 rebuild

* Thu Mar 18 2021 Paul Howarth <paul@city-fan.org> - 0.75-1
- Update to 0.75

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.74-9
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.74-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Paul Howarth <paul@city-fan.org> - 0.74-6
- Avoid the need for bootstrapping EPEL builds

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.74-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.74-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Paul Howarth <paul@city-fan.org> - 0.74-1
- Update to 0.74

* Tue Sep  4 2018 Paul Howarth <paul@city-fan.org> - 0.73-1
- Update to 0.73
- Drop legacy Group: tag

* Sun Aug 05 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.72-1
- Update to 0.72

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 24 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.71-1
- Update to 0.71

* Tue May 31 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.70-1
- Update to 0.70

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-2
- Perl 5.24 rebuild

* Sat May 07 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.69-1
- Update to 0.69

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.68-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-2
- Perl 5.22 rebuild

* Sun Mar 08 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.68-1
- Update to 0.68

* Sun Mar 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.67-1
- Update to 0.67

* Sun Feb 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.66-1
- Update to 0.66
- Use %%license tag

* Tue Nov 11 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.65-1
- Update to 0.65

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.63-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.63-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Paul Howarth <paul@city-fan.org> - 0.63-1
- Update to latest upstream version
- Switch to Module::Build::Tiny flow
- Drop provides/obsoletes for old tests sub-package
- Package new upstream CONTRIBUTING and README.md files
- Classify buildreqs by usage
- Make %%files list more explicit

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.47-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 0.47-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.45-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.45-2
- Perl 5.16 rebuild

* Fri May 18 2012 Iain Arnell <iarnell@gmail.com> 0.45-1
- update to latest upstream version

* Fri Apr 20 2012 Iain Arnell <iarnell@gmail.com> 0.40-1
- update to latest upstream version

* Mon Apr 09 2012 Iain Arnell <iarnell@gmail.com> 0.39-2
- avoid circular dependencies (patch from Paul Howarth rhbz#810707)

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 0.39-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.38-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.38-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.38-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.37-2
- Perl mass rebuild

* Thu May 05 2011 Iain Arnell <iarnell@gmail.com> 0.37-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.35-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 0.33-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.33)
- altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- altered br on perl(Test::More) (0.62 => 0.88)
- added a new br on perl(Test::Requires) (version 0.05)
- added a new br on perl(Test::Warn) (version 0.21)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.27)
- altered br on perl(Getopt::Long::Descriptive) (0.077 => 0.081)
- dropped old BR on perl(Scalar::Util)
- dropped old BR on perl(Test::Pod::Coverage)
- altered req on perl(Getopt::Long::Descriptive) (0.077 => 0.081)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.26-1
- add perl_default_filter
- PERL_INSTALL_ROOT => DESTDIR in install
- auto-update to 0.26 (by cpan-spec-update 0.01)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- auto-update to 0.22 (by cpan-spec-update 0.01)
- altered br on perl(Getopt::Long::Descriptive) (0 => 0.077)
- added a new br on perl(Test::Moose) (version 0)
- altered req on perl(Getopt::Long::Descriptive) (0 => 0.077)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- auto-update to 0.20 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Getopt::Long) (2.35 => 2.37)
- added a new req on perl(Getopt::Long) (version 2.37)
- added a new req on perl(Getopt::Long::Descriptive) (version 0)
- added a new req on perl(Moose) (version 0.56)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update to 0.18

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- update to 0.15

* Thu Jul 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-2
- tweak Getopt::Long dep to 2.35; passes tests just fine with 2.35, and that's
  what we have in F-8 perl

* Sat Jun 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13
- switch to Module::Install invocations, rather than Module::Build

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-2
- rebuild for new perl

* Fri Aug 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05
- license tag: GPL -> GPL+

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-2
- bump

* Thu May 03 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update to 0.03

* Fri Apr 20 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- Specfile autogenerated by cpanspec 1.69.1.
