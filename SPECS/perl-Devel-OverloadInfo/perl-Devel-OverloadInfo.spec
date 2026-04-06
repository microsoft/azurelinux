# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Devel-OverloadInfo
Version:	0.008
Release:	1%{?dist}
Summary:	Introspect overloaded operators
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Devel-OverloadInfo
Source0:	https://cpan.metacpan.org/modules/by-module/Devel/Devel-OverloadInfo-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::HasCompiler) >= 0.023
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(Text::ParseWords)
# Module Runtime
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(MRO::Compat)
BuildRequires:	perl(overload)
BuildRequires:	perl(Package::Stash) >= 0.14
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Util) >= 1.40
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(parent)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.88
# Dependencies
Requires:	perl(Sub::Util) >= 1.40

%description
Devel::OverloadInfo returns information about overloaded operators for a
given class (or object), including where in the inheritance hierarchy the
overloads are declared and where the code implementing it is.

%prep
%setup -q -n Devel-OverloadInfo-%{version}

# Remove bundled ExtUtils::HasCompiler
rm -rf inc/
perl -ni -e 'print unless /^inc\//;' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::OverloadInfo.3*

%changelog
* Tue Aug 12 2025 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Generate README.md in the repository
  - Move git repository to Codeberg
- Use %%{make_build} and %%{make_install}

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-2
- Perl 5.34 rebuild

* Thu Apr 29 2021 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Remove dependency on Sub::Identify
- Use %%license unconditionally

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-9
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005
  - Add overload_op_info() function for info about a single op
- Simplify find command using -delete

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004
  - Document that existence of undef 'fallback' varies between perl versions
  - Add tests for empty, inherited-only and no overloading
  - Add is_overloaded() function

* Thu Aug 13 2015 Paul Howarth <paul@city-fan.org> - 0.003-1
- Update to 0.003
  - Return an empty hash instead of undef for classes with no overloads
  - Work around overload inheritance corruption before 5.16 (CPAN RT#106379)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-3
- Perl 5.22 rebuild

* Fri Nov  7 2014 Paul Howarth <paul@city-fan.org> - 0.002-2
- Sanitize for Fedora submission

* Mon Nov  3 2014 Paul Howarth <paul@city-fan.org> - 0.002-1
- Initial RPM version
