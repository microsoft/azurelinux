Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		perl-MRO-Compat
Version:	0.15
Release:	11%{?dist}
Summary:	Mro::* interface compatibility for Perls < 5.9.5
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/MRO-Compat
Source0:	https://cpan.metacpan.org/authors/id/H/HA/HAARG/MRO-Compat-%{version}.tar.gz#/perl-MRO-Compat-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test
BuildRequires:	perl(Test::More) >= 0.47
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
The "mro" namespace provides several utilities for dealing with method
resolution order and method caching in general in Perl 5.9.5 and higher.
This module provides those interfaces for earlier versions of Perl (back
to 5.6.0 anyways).

It is a harmless no-op to use this module on 5.9.5+. That is to say,
code which properly uses MRO::Compat will work unmodified on both older
Perls and 5.9.5+.

If you're writing a piece of software that would like to use the parts
of 5.9.5+'s mro:: interfaces that are supported here, and you want
compatibility with older Perls, this is the module for you.

%prep
%setup -q -n MRO-Compat-%{version}

# Fix script interpreter
perl -MExtUtils::MakeMaker -e 'ExtUtils::MM_Unix->fixin(q{t/15pkg_gen.t})'

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README t/
%{perl_vendorlib}/MRO/
%{_mandir}/man3/MRO::Compat.3*

%changelog
* Mon Dec 16 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.15-11
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.15-6
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan  8 2022 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Optimize pure perl DFS inheritance calculation on perl 5.8
  - Fix function prototypes to match core functions
  - Pod formatting fix
- Package new LICENSE file
- Drop redundant buildroot cleaning in %%install section
- Drop support for old perls without mro support in core

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-14
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-11
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-2
- Perl 5.26 rebuild

* Wed Mar 29 2017 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Don't run pod tests on user installs
  - Stop using Module::Install to fix installation when @INC doesn't have the
    current directory (CPAN RT#119016)
  - Repository migrated to the github moose organization
- This release by HAARG → update source URL
- Simplify find command using -delete

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 0.12-12
- Use distribution instead of perl version to control build-requires

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-11
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-8
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 0.12-7
- Do not hard-code interpreter name

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.12-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec  5 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Bump Class::C3 dependency on 5.8, which in turn will automatically install
    Class::C3::XS if possible
  - Fix nonfunctional SYNOPSIS (CPAN RT#78325)
- This release by BOBTFISH -> update source URL
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- BR: perl(Cwd), perl(File::Path), perl(File::Spec) for bundled Module::Install
- Bump perl(Class::C3) version requirement to 0.24
- Drop unnecessary version requirement for perl(ExtUtils::MakeMaker)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.11-10
- Perl 5.16 rebuild

* Thu Jan 26 2012 Paul Howarth <paul@city-fan.org> - 0.11-9
- Spec clean-up:
  - Only require Class::C3 with perl < 5.9.5
  - Require Class::C3::XS for performance and consistency, but only with
    perl < 5.9.5
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Make %%files list more explicit
  - Classify buildreqs by build/module/test
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11-1
- Auto-update to 0.11 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Altered br on perl(Class::C3) (0.19 => 0.20)

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.10-1
- Update to 0.10

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.09
- Update to 0.09

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.07-1
- Update to 0.07

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-6
- Rebuild for new perl

* Thu Dec 06 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-5
- Bump

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-4
- Update INstall -> install

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-3
- Add Test::Pod deps

* Tue Dec 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-2
- Make Class::C3 dep explicit

* Tue Sep 18 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-1
- Specfile autogenerated by cpanspec 1.71
