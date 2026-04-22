# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-CPAN-Requirements-Dynamic
Version:	0.002
Release: 3%{?dist}
Summary:	Dynamic prerequisites in meta files
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/CPAN-Requirements-Dynamic
Source0:	https://cpan.metacpan.org/modules/by-module/CPAN/CPAN-Requirements-Dynamic-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(:VERSION) >= 5.6
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(CPAN::Meta::Requirements::Range)
BuildRequires:	perl(ExtUtils::Config)
BuildRequires:	perl(ExtUtils::HasCompiler)
BuildRequires:	perl(IPC::Cmd)
BuildRequires:	perl(Parse::CPAN::Meta)
BuildRequires:	perl(Perl::OSType)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(Test::More) >= 0.88
# Dependencies
Requires:	perl(CPAN::Meta::Prereqs)
Requires:	perl(CPAN::Meta::Requirements::Range)
Requires:	perl(ExtUtils::Config)
Requires:	perl(ExtUtils::HasCompiler)
Requires:	perl(IPC::Cmd)
Requires:	perl(Perl::OSType)

%description
This module implements a format for describing dynamic prerequisites of
a distribution.

%prep
%setup -q -n CPAN-Requirements-Dynamic-%{version}

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
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Requirements::Dynamic.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr  7 2025 Paul Howarth <paul@city-fan.org> - 0.002-1
- Update to 0.002
  - Remove unnecessary conditions

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 16 2024 Paul Howarth <paul@city-fan.org> - 0.001-3
- Incorporate package review feedback (rhbz#2277753)
  - Tweak %%description
  - BR: perl(VERSION) >= 5.6

* Mon Apr 29 2024 Paul Howarth <paul@city-fan.org> - 0.001-2
- Sanitize for Fedora submission

* Mon Apr 29 2024 Paul Howarth <paul@city-fan.org> - 0.001-1
- Initial RPM version
