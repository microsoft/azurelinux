# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-Role-Parameterized
Summary:        Make your roles flexible through parameterization
Version:        1.11
Release: 19%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MooseX-Role-Parameterized
Source0:        https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-Role-Parameterized-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moose) >= 2.0300
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Meta::Role)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(namespace::clean) >= 0.19
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(CPAN::Meta::Check) >= 0.011
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(overload)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Needs)
# Optional Test Dependencies
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(MooseX::Role::WithOverloading)
# Dependencies
Requires:       perl(Moose) >= 2.0300

%description
Roles are composable units of behavior. They are useful for factoring out
functionality common to many classes from any part of your class hierarchy.
(See Moose::Cookbook::Roles::Recipe1 for an introduction to Moose::Role.)

While combining roles affords you a great deal of flexibility, individual
roles have very little in the way of configurability. Core Moose provides
alias for renaming methods to avoid conflicts, and excludes for ignoring
methods you don't want or need (see Moose::Cookbook::Roles::Recipe2 for more
about alias and excludes).

Because roles serve many different masters, they usually provide only the
least common denominator of functionality. To empower roles further, more
configurability than alias and excludes is required. Perhaps your role needs
to know which method to call when it is done. Or what default value to use for
its url attribute.

Parameterized roles offer exactly this solution.

%prep
%setup -q -n MooseX-Role-Parameterized-%{version}
sed -i -e '1s,#!.*perl,,' t/*.t

%build
PERL_MM_FALLBACK_SILENCE_WARNING=1 perl Makefile.PL \
  INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-10
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Remove MooseX::Role::WithOverloading from test dependencies
    (CPAN RT#130075)
- Specify all build dependencies
- Modernize spec using %%{make_build} and %%{make_install}

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-2
- Perl 5.26 rebuild

* Sun Apr 23 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 1.10-1
- Update to 1.10
- Shorten file listing for documentation

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Aug 27 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.09-1
- Update to 1.09

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 1.08-1
- Update to 1.08
   - Add x_breaks metadata for incompatibility issue with MooseX::Storage (now
     resolved with MooseX-Storage-0.47)
- Silence annoying toolchain message from Makefile.PL

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Perl 5.20 rebuild

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 1.07-1
- Update to 1.07
  - Restored MooseX::Role::Parameterized->current_metaclass as a public
    method; apparently there is code on CPAN that relies on this
  - Remove README.pod from shipped dist
- This release by ETHER → update source URL
- Drop workarounds for problems in earlier releases

* Tue Aug  5 2014 Paul Howarth <paul@city-fan.org> - 1.05-2
- Remove installed README.pod and corresponding manpage, potentially
  conflicting (#1126416)
  https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker/issues/119

* Fri Aug  1 2014 Paul Howarth <paul@city-fan.org> - 1.05-1
- Update to 1.05
  - If a parameterizable role was reinitialized after any parameters or a role
    block was declared, those declarations were lost; reinitialization usually
    occurs when new metaroles are applied to the role by other MooseX modules
- This release by DROLSKY → update source URL
- Silence warnings about old toolchain since we really don't need
  Module::Build::Tiny

* Thu Jul 31 2014 Paul Howarth <paul@city-fan.org> - 1.04-1
- Update to 1.04
  - This extension is now implemented as a role metarole, which means it can
    (mostly) cooperate with other role extensions, such as
    MooseX::Role::WithOverloading; note that you should load
    MooseX::Role::Parameterized _after_ other extensions
  - This module no longer supports passing a "-metaclass" parameter when you
    load it; this was an artifact from a much earlier era of Moose extensions
  - Repository migrated to the github moose organization
  - Convert this distribution to Dist::Zilla to resolve packaging insanity
- This release by ETHER → update source URL
- Use %%license
- Make %%files list more explicit
- Classify buildreqs by usage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar  9 2014 Paul Howarth <paul@city-fan.org> - 1.02-1
- Update to latest upstream version
- Drop obsoletes/provides for old tests sub-package
- Don't need to remove empty directories from the buildroot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 1.00-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.00-4
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1.00-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 1.00-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 1.00-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.26-2
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 13 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.18-2
- perl-5.12.0 mass rebuild.

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.18)

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- auto-update to 0.15 (by cpan-spec-update 0.01)
- altered br on perl(Test::More) (0 => 0.88)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- drop README, LICENSE from doc

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- auto-update to 0.09 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new req on perl(Moose) (version 0.78)

* Wed May 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- auto-update to 0.06 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0 => 0.27)
- altered br on perl(Moose) (0.63 => 0.78)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update to 0.04

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update to 0.03

* Mon Jan 12 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- update for submission

* Sun Jan 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.7)
