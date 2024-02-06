Summary:        Make sure you didn't emit any warnings while testing
Name:           perl-Test-NoWarnings
Version:        1.06
Release:        1%{?dist}
License:        LGPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/dist/Test-NoWarnings
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-NoWarnings-%{version}.tar.gz#/perl-Test-NoWarnings-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6

# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Devel::StackTrace)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Test::Builder) >= 0.86

# Tests:
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Tester) >= 0.107
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Suggests:       perl(Devel::StackTrace)

%description
In general, your tests shouldn't produce warnings. This module causes any
warnings to be captured and stored. It automatically adds an extra test
that will run when your script ends to check that there were no warnings.
If there were any warnings, the test will give a "not ok" and diagnostics of
where, when and what the warning was, including a stack trace of what was
going on when the it occurred.

%prep
%setup -q -n Test-NoWarnings-%{version}

%build
perl Makefile.PL NO_PACKLIST=1 INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 01 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.06-1
- Upgrade to 1.06

* Tue May 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-23
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-19
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-16
- Perl 5.28 rebuild

* Wed Apr 04 2018 Petr Pisar <ppisar@redhat.com> - 1.04-15
- Modernize spec file

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-7
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.04-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 05 2013 Iain Arnell <iarnell@gmail.com> 1.04-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Thu Nov 08 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-7
- Update dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.02-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.02-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 1.02-1
- Update to 1.02.
- Update Source0 URL.
- BR Test::Builder and Test::More, plus update versioned Test::Tester BR.
- CHANGES renamed to Changes, and LGPL renamed to LICENSE.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.084-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.084-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.084-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.084-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.084-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.084-2
- rebuild for new perl

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.084-1
- Update to 0.084.
- Update License.
- BR Devel::StackTrace.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.083-2
- BR ExtUtils::MakeMaker.

* Tue Dec 26 2006 Steven Pritchard <steve@kspei.com> 0.083-1
- Update to 0.083.
- Use fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.082-2
- Fix find option order.

* Sat Apr 08 2006 Steven Pritchard <steve@kspei.com> 0.082-1
- Specfile autogenerated by cpanspec 1.64.
- Fix License.
- Drop explicit dependency on perl(Test::Tester).  (Seems to be bogus.)
