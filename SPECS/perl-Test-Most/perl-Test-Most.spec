# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Test-Most
Version:        0.38
Release:        8%{?dist}
Summary:        Perl module with test functions and features
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Most
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Most-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Data::Dumper::Names) >= 0.03
BuildRequires:  perl(Exception::Class) >= 1.14
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::Deep) >= 0.119
BuildRequires:  perl(Test::Differences) >= 0.64
BuildRequires:  perl(Test::Exception) >= 0.43
BuildRequires:  perl(Test::Harness) >= 3.35
BuildRequires:  perl(Test::More) >= 1.302047
BuildRequires:  perl(Test::Warn) >= 0.30
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(lib)
# Not automatically detected
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Data::Dumper::Names) >= 0.03
Requires:       perl(Test::Deep) >= 0.119
Requires:       perl(Test::Differences) >= 0.64
Requires:       perl(Test::Exception) >= 0.43
Requires:       perl(Test::Harness) >= 3.35
Requires:       perl(Test::More) >= 1.302047
Requires:       perl(Test::Warn) >= 0.30
Requires:       perl(Time::HiRes)

%description
Most commonly needed test functions and features. This module provides you with 
the most commonly used testing functions and gives you a bit more fine-grained 
control over your test suite.

%prep
%setup -q -n Test-Most-%{version}

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
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Most.3*
%{_mandir}/man3/Test::Most::Exception.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 26 2022 Paul Howarth <paul@city-fan.org> - 0.38-1
- Update to 0.38 (rhbz#2129537)
  - Stop permanently altering Test::More's export list (CPAN RT#73299)
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-8
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-2
- Perl 5.32 rebuild

* Sun Apr  5 2020 Paul Howarth <paul@city-fan.org> - 0.37-1
- Update to 0.37
  - Don't call parent DESTROY method if it does not exist

* Sat Apr  4 2020 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Ensure Test::Builder's original DESTROY is called (GH#10)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 0.35-11
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 11 2016 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Bump module deps due to Test2; Test2 is tested well enough that you're
    probably OK, but you'll want to retest your code with this release
- BR: perl-generators
- Simplify find command using -delete
- Drop legacy Group: tag

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug  8 2015 Paul Howarth <paul@city-fan.org> - 0.34-5
- Classify buildreqs by usage
- BR:/R: perl(Time::HiRes) - fixes FTBFS on Rawhide

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-3
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-2
- Perl 5.20 rebuild

* Tue Aug 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-1
- 0.34 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-1
- 0.33 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.31-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-1
- 0.31 bump
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.25-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Petr Sabata <contyk@redhat.com> - 0.25-1
- 0.25 bump

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> - 0.24-1
- 0.24 bump
- Removing now obsolete Buildroot and defattr

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Iain Arnell <iarnell@gmail.com> 0.23-2
- add explicit requires that are no longer automatically detected

* Tue Sep 14 2010 Petr Sabata <psabata@redhat.com> - 0.23-1
- New release, 0.23

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.21-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr  6 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.21-3
- remove unnecesarry requirements

* Thu Apr 02 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.21-1
- Specfile autogenerated by cpanspec 1.78.
