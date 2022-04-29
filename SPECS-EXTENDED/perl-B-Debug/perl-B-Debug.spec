Vendor:         Microsoft Corporation
Distribution:   Mariner
# Run optional test
%if !%{defined perl_bootstrap}
%if ! (0%{?rhel})
%bcond_without perl_B_Debug_enables_optional_test
%else
%bcond_with perl_B_Debug_enables_optional_test
%endif
%else
%global _without_perl_B_Debug_enables_optional_test 1
%global _with_perl_B_Debug_enables_optional_test 0
%endif


Name:           perl-B-Debug
Version:        1.26
Release:        425%{?dist}
Summary:        Walk Perl syntax tree, print debug information about op-codes
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/B-Debug
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-Debug-%{version}.tar.gz#/perl-B-Debug-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(deprecate)
# Run-time:
BuildRequires:  perl(B)
# B::Asmdata not used
BuildRequires:  perl(Config)
# deprecate since perl 5.27.1
BuildRequires:  perl(strict)
# Optional run-time:
# B::Flags 0.04 not packaged
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
%if %{with perl_B_Debug_enables_optional_test}
# Optional test:
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# deprecate since perl 5.27.1

%description
Walk Perl syntax tree and print debug information about op-codes. See
B::Concise and B::Terse for other details.

%prep
%setup -q -n B-Debug-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license Artistic Copying
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Apr 21 2022 Muhammad Falak <mwani@microsoft.com> - 1.26-425
- Add an explicit BR on `perl(deprecate)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26-424
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-423
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-422
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-421
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-420
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Petr Pisar <ppisar@redhat.com> - 1.26-1
- 1.26 bump

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Rebuild to solve f27-rebuild tag merge conflict

* Thu Jul 27 2017 Petr Pisar <ppisar@redhat.com> - 1.25-1
- 1.25 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Petr Pisar <ppisar@redhat.com> - 1.24-1
- 1.24 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Petr Pisar <ppisar@redhat.com> - 1.23-1
- 1.23 bump

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 1.22-2
- Do not build-require version module

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 1.22-1
- 1.22 bump

* Wed Sep 17 2014 Petr Pisar <ppisar@redhat.com> 1.21-1
- Specfile autogenerated by cpanspec 1.78.
