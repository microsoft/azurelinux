Name:		perl-XString
Version:	0.002
Release:	4%{?dist}
Summary:	Isolated String helpers from B
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/XString
Source0:	https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/XString-%{version}.tar.gz#/perl-XString-%{version}.tar.gz
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:	perl(:VERSION) >= 5.10.0
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(B)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More) >= 0.88
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
# Requirements from upstream metadata that are not actually used
# https://github.com/atoomic/XString/issues/2
BuildRequires:	perl(Test2::Bundle::Extended)
BuildRequires:	perl(Test2::Plugin::NoWarnings)
BuildRequires:	perl(Test2::Tools::Explain)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(XSLoader)

%description
XString provides the B string helpers in one isolated package. Right now only
cstring and perlstring are available.

%prep
%setup -q -n XString-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/XString.pm
%{perl_vendorarch}/auto/XString/
%{_mandir}/man3/XString.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.002-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Paul Howarth <paul@city-fan.org> - 0.002-2
- Incorporate feedback from package review (#1776513)
  - BR: findutils
  - BR: perl(CPAN::Meta::Prereqs)
  - Need perl(ExtUtils::MakeMaker) >= 6.76
  - Add reference to upstream ticket about unnecessary build requirements
    https://github.com/atoomic/XString/issues/2
  - Add run-time dependency on perl(XSLoader)

* Mon Nov 25 2019 Paul Howarth <paul@city-fan.org> - 0.002-1
- Initial RPM version
