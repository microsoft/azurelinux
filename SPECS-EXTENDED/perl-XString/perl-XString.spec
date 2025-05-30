Name:		perl-XString
Version:	0.005
Release:	15%{?dist}
Summary:	Isolated String helpers from B
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/XString
Source0:	https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/XString-%{version}.tar.gz
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
# Dependencies
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
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.005-15
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-13
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-9
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 20 2020 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005
  - Fix cstring for Perl 5.32 (GH#6, GH#7)
  - Remove unneeded module dependencies (GH#2)
  - Add compatibility with Perl 5.8 (GH#9)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-4
- Perl 5.32 rebuild

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
