%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Fedora::VSP\\)
Summary:        Perl version normalization for RPM
Name:           perl-Fedora-VSP
Version:        0.001
Release:        19%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://ppisar.fedorapeople.org/Fedora-VSP/
Source0:        %{url}Fedora-VSP-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
# Break build cycle: perl-Fedora-VSP → perl-generators → perl-Fedora-VSP
%if %{defined perl_bootstrap}
Provides:       perl(Fedora::VSP) = %{version}
%else
BuildRequires:  perl-generators
%endif
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Test::More)
%endif

BuildArch:      noarch

%description
This module provides functions for normalizing Perl version strings for
Red Hat Package (RPM) based Linux distributions.

%prep
%autosetup -n Fedora-VSP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license COPYING
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 0.001-19
- Add BR on `perl(Test::More)` to fix ptest

* Mon Aug 30 2021 Bala <balakumaran.kannan@microsoft.com> - 0.001-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-15
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-11
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-7
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 30 2016 Petr Pisar <ppisar@redhat.com> - 0.001-4
- Break build cycle when bootstrapping: perl-Fedora-VSP → perl-generators
  → perl-Fedora-VSP

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 09 2015 Petr Pisar <ppisar@redhat.com> 0.001-1
- First package
