# This file is licensed under the terms of GNU GPLv2+.

# Run optional tests
%if ! (0%{?rhel})
%{bcond_without perl_Module_Runtime_enables_optional_test}
%else
%{bcond_with perl_Module_Runtime_enables_optional_test}
%endif

Name:           perl-Module-Runtime
Version:        0.016
Release:        10%{?dist}
Summary:        Runtime module handling
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Module-Runtime
Source0:        https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Module-Runtime-%{version}.tar.gz#/perl-Module-Runtime-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Tests:
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.41
BuildRequires:  perl(warnings)
%if %{with perl_Module_Runtime_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
The functions exported by this module deal with runtime handling of Perl
modules, which are normally handled at compile time.

%prep
%setup -q -n Module-Runtime-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Runtime.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.016-10
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.016-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 19 2017 Paul Howarth <paul@city-fan.org> - 0.016-1
- 0.016 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Petr Pisar <ppisar@redhat.com> - 0.015-1
- 0.015 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 20 2015 Petr Pisar <ppisar@redhat.com> - 0.014-6
- Specify all dependencies

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Petr Pisar <ppisar@redhat.com> - 0.014-1
- 0.014 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 0.013-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.013-2
- Perl 5.16 rebuild

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Mon Feb 13 2012 Petr Pisar <ppisar@redhat.com> - 0.012-1
- 0.012 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Petr Pisar <ppisar@redhat.com> - 0.011-1
- 0.011 bump

* Fri Oct 07 2011 Petr Pisar <ppisar@redhat.com> - 0.010-1
- 0.010 bump

* Wed Oct 05 2011 Petr Pisar <ppisar@redhat.com> - 0.009-1
- 0.009 bump
- Remove defattr now

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.008-2
- Perl mass rebuild

* Mon Jul 11 2011 Petr Pisar <ppisar@redhat.com> 0.008-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr
