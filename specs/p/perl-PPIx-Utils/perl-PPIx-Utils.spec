# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-PPIx-Utils
Version:        0.004
Release:        1%{?dist}
Summary:        Utility functions for PPI
License:        GPL-1.0-or-later OR Artistic-1.0-Perl

URL:            https://metacpan.org/release/PPIx-Utils/
Source0:        https://cpan.metacpan.org/authors/id/D/DB/DBOOK/PPIx-Utils-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  %{__make}
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6

BuildRequires:  perl(B::Keywords) >= 1.09
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(PPI) >= 1.250
BuildRequires:  perl(PPI::Dumper)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88

Requires:       perl(B::Keywords) >= 1.09
Requires:       perl(PPI) >= 1.250


# Filter duplicate unversioned requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(B::Keywords\\)$

%description
PPIx::Utils is a collection of utility functions for working with PPI
documents. The functions are organized into submodules, and may be imported
from the appropriate submodule or via this module.

%prep
%setup -q -n PPIx-Utils-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/PPIx
%{_mandir}/man3/PPIx::Utils*

%changelog
* Tue Aug 05 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-1
- 0.004 bump (rhbz#2363947)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.003-8
- BR: perl(:VERSION) >= 0:5.006 instead of perl >= 0:5.006.
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-3
- Perl 5.34 rebuild

* Tue May 04 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.003-1
- Reflect review.

* Tue Apr 27 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.003-1
- Initial Fedora package.
