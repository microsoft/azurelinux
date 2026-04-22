# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Parse-Distname
Version:	0.05
Release: 12%{?dist}
Summary:	Parse a distribution name
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/dist/Parse-Distname
Source0:	https://cpan.metacpan.org/modules/by-module/Parse/Parse-Distname-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(ExtUtils::MakeMaker::CPANfile) >= 0.08
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(Test::Differences)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::UseAllModules) >= 0.17
# Dependencies
# (none)

%description
Parse::Distname is yet another distribution name parser. It works almost the
same as CPAN::DistnameInfo, but Parse::Distname takes a different approach. It
tries to extract the version part of a distribution and treat the rest as a
distribution name, contrary to CPAN::DistnameInfo which tries to define a name
part and treat the rest as a version.

Because of this difference, when Parse::Distname parses a weird distribution
name such as "AUTHOR/v1.0.tar.gz", it says the name is empty and the version
is "v1.0", while CPAN::DistnameInfo says the name is "v" and the version is
"1.0". See test files in this distribution if you need more details. As of this
writing, Parse::Distname returns a different result for about 200+
distributions among about 320000 BackPan distributions.

%prep
%setup -q -n Parse-Distname-%{version}

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
%{perl_vendorlib}/Parse/
%{_mandir}/man3/Parse::Distname.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-3
- Perl 5.36 rebuild

* Thu Apr 28 2022 Paul Howarth <paul@city-fan.org> - 0.05-2
- Incorporate feedback from package review (#2073377)
  - perl(strict) is a run-time dependency, not just a test dependency
  - Don't package the tests as documentation

* Fri Apr  8 2022 Paul Howarth <paul@city-fan.org> - 0.05-1
- Initial RPM version
