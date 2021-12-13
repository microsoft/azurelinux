Name:		perl-Test2-Tools-Explain
Version:	0.02
Release:	4%{?dist}
Summary:	Explain tools for the Perl Test2 framework
License:	Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Test2-Tools-Explain
Source0:	https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Test2-Tools-Explain-%{version}.tar.gz#/perl-Test2-Tools-Explain-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	perl(:VERSION) >= 5.8.1
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Test2::Bundle::Extended)
BuildRequires:	perl(Test::More)
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Data::Dumper)

%description
Test2::Suite dropped the explain() function that had been part of Test::More.
For those who miss it in Test2, you can use Test2::Tools::Explain.

%prep
%setup -q -n Test2-Tools-Explain-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README.md
%{perl_vendorlib}/Test2/
%{_mandir}/man3/Test2::Tools::Explain.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.02-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Paul Howarth <paul@city-fan.org> - 0.02-2
- Incorporate feedback from package review (#1776509)
  - Rephrase %%summary
  - BR: perl(:VERSION) >= 5.8.1

* Mon Nov 25 2019 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
