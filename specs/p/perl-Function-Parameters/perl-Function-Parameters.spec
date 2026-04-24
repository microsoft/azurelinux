# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%bcond_without perl_Function_Parameters_enables_optional_test

Name:           perl-Function-Parameters
%global cpan_version 2.002006
Version:        2.2.6
Release: 2%{?dist}
Summary:        Subroutine definitions with parameter lists
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Function-Parameters
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MAUKE/Function-Parameters-%{cpan_version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Hash::Util) >= 0.07
BuildRequires:  perl(integer)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
%if %{with perl_Function_Parameters_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Util)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(MooseX::Types::Moose)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
%endif
# Dependencies
# perl(Moose::Util::TypeConstraints) only used with Moose

%description
This module extends Perl with keywords that let you define functions with
parameter lists. It uses Perl's keyword plugin API, so it works reliably
and doesn't require a source filter.

%prep
%setup -q -n Function-Parameters-%{cpan_version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Function/
%{perl_vendorarch}/Function/
%{_mandir}/man3/Function::Parameters.3*
%{_mandir}/man3/Function::Parameters::Info.3*

%changelog
* Sun Aug 17 2025 Paul Howarth <paul@city-fan.org> - 2.2.6-1
- Update to 2.002006 (rhbz#2388952)
  - Fix a parse-time memory leak with undef or default initializers
    ('fun ($x = undef)' or 'fun ($ =)'); this leak mostly manifests as noise
    from memory checkers because non-leaked ops aren't freed anyway while perl
    is still running
  - Update bugtracker info in README

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.5-2
- Perl 5.42 rebuild

* Sun Jan 19 2025 Paul Howarth <paul@city-fan.org> - 2.2.5-1
- Update to 2.002005 (rhbz#2338807)
  - When debugging (perl -d), skip over invisible (generated) parameter
    initialization code even if single-step mode is active
  - Move repository and bugtracker to https://codeberg.org/

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.4-5
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Paul Howarth <paul@city-fan.org> - 2.2.4-1
- Update to 2.002004 (rhbz#2223063)
  - Remove 'perl -T' from t/info.t, so we can run on perls compiled without
    support for taint mode; the test didn't actually care about taint anyway

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.3-2
- Perl 5.38 rebuild

* Wed Apr 19 2023 Paul Howarth <paul@city-fan.org> - 2.2.3-1
- Update to 2.002003 (rhbz#2188007)
  - Fix line numbers after inlined type checks (GH#42)
    Previously, the code for type checks was inlined literally, so if a
    particular check took 5 lines of code, all the following line numbers in
    the source file would be off by 5 (they would be "pushed down" by the
    interpolated code); these bad line numbers would show up in error messages
    from Perl (including warn and die) as well as __LINE__ and caller (and
    thus stack traces)
- Drop explicit dependency on perl(Moose::Util::TypeConstraints), which is
  only required when using this module in conjunction with Moose, and that
  would pull in the dependency anyway

* Sun Apr  2 2023 Paul Howarth <paul@city-fan.org> - 2.2.2-1
- Update to 2.002002 (rhbz#2183727)
  - Provide //= for default arguments, which are also used when the caller
    passes in undef
  - Provide more type combinators in parameter declarations: In addition to |
    (union types), now ~ & / are also supported (for
    complement types, intersection types, and alternative types, respectively)
  - Enable type coercions: if a parameter has a declared type and that type
    supports coercions ($type->has_coercion returns true), call its
    ->coerce($value) method to transform arguments before type checking
  - Enable inline type checks: if a parameter has a declared type and that
    type supports inlining ($type->can_be_inlined returns true), its inline
    code (as provided by ->inline_check('$value')) is baked into the function
    definition instead of a call to ->check($value), which may speed up type
    checks
  - Move a big chunk of tests to xt/ (author testing only)
  - Remove xt/ from the distribution
  - Enable parallel testing by default (with -j4)
  - Fix (hopefully) Windows builds using nmake.exe
  - Work around old versions of ExtUtils::MakeMaker not providing
    is_make_type(), whose version dependency is undocumented (sigh)
  - Restrict GNU syntax for exporting variables to type 'gmake'; should fix
    building on BSD, Solaris, etc.
  - Declare dependency on ExtUtils::MakeMaker 7+ and remove compatibility code
    for older versions

* Mon Mar 27 2023 Paul Howarth <paul@city-fan.org> - 2.1.6-1
- Update to 2.001006 (rhbz#2182064)
  - Work around perl core issue GH#20950 (use re "eval" doesn't capture lexical
    %%^H environment like eval() does and stringifies it instead), by
    downgrading the previous hard error to a warning (in the new category
    'Function::Parameters') and switching Function::Parameters off in the
    affected scope

* Fri Jan 27 2023 Paul Howarth <paul@city-fan.org> - 2.1.5-1
- Update to 2.001005 (rhbz#2164971)
  - Fix failures with perl 5.37.5..5.37.6 caused by new internal opcode
    structure for anonymous subs

* Fri Jan 20 2023 Paul Howarth <paul@city-fan.org> - 2.1.4-1
- Update to 2.001004 (rhbz#2162566)
  - Drop Dir::Self test dependency (use FindBin instead)
- Use SPDX-format license tag
- Use %%{make_build} and %%{make_install}
- Make %%files list more explicit

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 13 2017 Petr Pisar <ppisar@redhat.com> - 2.1.3-1
- 2.001003 bump

* Thu Nov 09 2017 Petr Pisar <ppisar@redhat.com> - 2.1.2-1
- 2.001002 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Petr Pisar <ppisar@redhat.com> - 2.1.1-1
- 2.001001 bump

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.7-2
- Perl 5.26 rebuild

* Tue May 16 2017 Petr Pisar <ppisar@redhat.com> - 2.0.7-1
- 2.000007 bump

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 2.0.6-2
- 2.000006 bump

* Mon Apr 03 2017 Petr Pisar <ppisar@redhat.com> - 2.0.3-1
- 2.000003 bump

* Tue Mar 28 2017 Petr Pisar <ppisar@redhat.com> - 2.0.2-1
- 2.000002 bump

* Fri Mar 17 2017 Petr Pisar <ppisar@redhat.com> - 1.0706-1
- 1.0706 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 1.0705-1
- 1.0705 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.0704-2
- Perl 5.24 rebuild

* Mon Feb 15 2016 Petr Pisar <ppisar@redhat.com> - 1.0704-1
- 1.0704 bump

* Thu Feb 04 2016 Petr Pisar <ppisar@redhat.com> 1.0703-1
- Specfile autogenerated by cpanspec 1.78.
- Address mistakes found by review
