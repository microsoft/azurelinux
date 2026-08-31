# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform author tests
%bcond_without perl_Test_YAML_enables_extra_test

Name:		perl-Test-YAML
Version:	1.07
Release:	22%{?dist}
Summary:	Testing Module for YAML Implementations
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-YAML
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-YAML-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) > 6.75
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Module Runtime
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Test::Base) >= 0.89
BuildRequires:	perl(Test::Base::Filter)
# Test Suite
BuildRequires:	perl(Test::More)
%if %{with perl_Test_YAML_enables_extra_test}
BuildRequires:	perl(Test::Pod) >= 1.41
%endif
# Dependencies
Requires:	perl(Data::Dumper)

%description
Test::YAML is a subclass of Test::Base with YAML specific support.

%prep
%setup -q -n Test-YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

# Exclude script that does nothing
rm %{buildroot}%{_bindir}/test-yaml

%check
unset AUTHOR_TESTING
make test %{?with_perl_Test_YAML_enables_extra_test:AUTHOR_TESTING=1}

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::YAML.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-14
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Perl 5.28 rebuild

* Sun Jun 17 2018 Paul Howarth <paul@city-fan.org> - 1.07-1
- Update to 1.07
  - Add a test so that cpan clients don't return "NOTESTS" (GH#4)
- This release by TINITA → update source URL
- Switch upstream from search.cpan.org to metacpan.org
- Pod syntax test switched from release test to author test

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 22 2015 Paul Howarth <paul@city-fan.org> - 1.06-1
- Update to 1.06
  - Remove perl req from Meta so can use on 5.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-3
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Paul Howarth <paul@city-fan.org> - 1.05-1
- Update to 1.05
  - Add 000-none to Meta
  - Remove t/use_ok.t
  - Meta 0.0.2
  - Dep on Test::Base 0.86

* Fri Aug  8 2014 Paul Howarth <paul@city-fan.org> - 1.01-1
- Update to 1.01
  - Remove "use lib 'lib';" (CPAN RT#20342, GH#1)
- Incorporate review feedback (#1127808)
  - Drop redundant BuildRoot specification
  - Take advantage of modern EU::MM in F-21 onwards

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 1.00-2
- Sanitize for Fedora submission

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 1.00-1
- Initial RPM version
