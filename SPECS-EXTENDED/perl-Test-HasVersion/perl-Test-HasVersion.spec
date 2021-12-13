Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Test-HasVersion
Version:        0.014
Release:        14%{?dist}
Summary:        Check Perl modules have version numbers
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-HasVersion
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-HasVersion-%{version}.tar.gz#/perl-Test-HasVersion-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Module Runtime
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Test::Builder::Tester) >= 1.04
BuildRequires:  perl(Test::More)
# Optional Tests
BuildRequires:  perl(Test::Pod) >= 1.18
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Do you want to check that every one of your Perl modules in a distribution has
a version number? You want to make sure you don't forget the brand new modules
you just added? Well, this is the module you have been looking for.

Do you want to check someone else's distribution to make sure the author has
not committed the sin of leaving Perl modules without a version that can be
used to tell if you have this or that feature? Test::HasVersion is also for
you.

%prep
%setup -q -n Test-HasVersion-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{_bindir}/test_version
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::HasVersion.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.014-14
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Thu Sep 26 2019 Paul Howarth <paul@city-fan.org> - 0.014-13
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-11
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan  3 2016 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Fix spelling error in manpage (CPAN RT#110709)
  - Add LICENSE file to the distribution (GH#1)
  - Fix all_pm_version_ok() failure reporting (CPAN RT#78758)
  - Rewrite t/04_all_ok.t using Test::Builder::Tester (CPAN RT#78758)
- Classify buildreqs by usage
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-12
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-11
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.012-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.012-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Iain Arnell <iarnell@gmail.com> 0.012-3
- drop unnecessary runtime dependency on perl(Test::Builder::Tester)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.012-2
- Perl mass rebuild

* Sat Apr 02 2011 Iain Arnell <iarnell@gmail.com> 0.012-1
- Specfile autogenerated by cpanspec 1.79.
