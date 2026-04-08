# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-Role-WithOverloading
Version:        0.17
Release:        34%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:        Roles that support overloading
URL:            https://metacpan.org/release/MooseX-Role-WithOverloading
Source0:        https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-Role-WithOverloading-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Module Runtime
BuildRequires:  perl(aliased)
BuildRequires:  perl(Moose) >= 0.94
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Role) >= 1.15
BuildRequires:  perl(Moose::Util::MetaRole)
BuildRequires:  perl(namespace::autoclean) >= 0.16
BuildRequires:  perl(namespace::clean) >= 0.19
BuildRequires:  perl(overload)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.96
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
# note: Test::Warnings only used if $ENV{AUTHOR_TESTING}
BuildRequires:  perl(Test::Warnings)
# Dependencies
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
MooseX::Role::WithOverloading allows you to write a Moose::Role
that defines overloaded operators and allows those operator
overloadings to be composed into the classes/roles/instances it's
compiled to, while plain roles would lose the overloading.

%prep
%setup -q -n MooseX-Role-WithOverloading-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
AUTHOR_TESTING=1 make test

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/MooseX/
%{perl_vendorarch}/MooseX/
%{_mandir}/man3/MooseX::Role::WithOverloading.3*
%{_mandir}/man3/MooseX::Role::WithOverloading::Meta::Role::Application.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-33
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-30
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-26
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-23
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-20
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-17
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Paul Howarth <paul@city-fan.org> - 0.17-15
- Spec tidy-up
  - Use author-independent source URL
  - Use %%{make_build} and %%{make_install}
  - Simplify find command using -empty and -delete
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-10
- Perl 5.28 rebuild

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 0.17-9
- Specify all dependencies

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 09 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.17-1
- Update to 0.17

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-2
- Perl 5.22 rebuild

* Thu Nov 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.16-1
- Update to 0.16

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Forward-compat mode added for Moose 2.1300, which cores all of this
    distribution's functionality

* Tue Aug  5 2014 Paul Howarth <paul@city-fan.org> - 0.14-2
- Remove installed README.pod and corresponding manpage, potentially
  conflicting (#1126416)
  https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker/issues/119

* Fri Aug  1 2014 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Fixed a bug with Perl 5.18+ that caused this module to simply blow up with
    an error like "Use of uninitialized value in subroutine entry at
    .../Class/MOP/Package.pm ..."
  - Line numbers in shipped code are now almost the same (within 3) as the
    repository source, for easier debugging
  - Repository migrated to the github moose organization
  - Unneeded init_meta method removed
- Use %%license
- Make %%files list more explicit

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Paul Howarth <paul@city-fan.org> - 0.13-3
- We have Test::CheckDeps now

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.13-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.09-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.09-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.09-1
- update to latest upstream version
- update BR perl(Moose::Role) >= 1.15

* Wed Oct 06 2010 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream version

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-2
- Mass rebuild with perl-5.12.0

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- submission

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

