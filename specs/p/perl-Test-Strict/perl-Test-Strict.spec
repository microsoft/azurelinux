# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Test_Strict_enables_optional_test
%else
%bcond_with perl_Test_Strict_enables_optional_test
%endif

Name:           perl-Test-Strict
Version:        0.54
Release: 4%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:        Check syntax, presence of use strict/warnings, and test coverage
Source:         https://cpan.metacpan.org/authors/id/M/MA/MANWAR/Test-Strict-%{version}.tar.gz
Url:            https://metacpan.org/release/Test-Strict
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::Builder)
# Tests only
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(Test::More)
# Optional tests only
%if %{with perl_Test_Strict_enables_optional_test}
BuildRequires:  perl(Moose::Autobox)
BuildRequires:  perl(Test::CheckManifest) >= 1.28
BuildRequires:  perl(Test::DistManifest) >= 1.012
BuildRequires:  perl(Test::Version) >= 1.003001
BuildRequires:  perl(Test::Pod) >= 1.48
BuildRequires:  perl(Test::Pod::Coverage) >= 1.10
%endif

%description
"Test::Strict" lets you check the syntax, presence of "use strict;" and
"use warnings;" in your perl code.  It reports its results in standard 
"Test::Simple" fashion. 

%prep
%setup -q -n Test-Strict-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
find . -type f -name '*.list' -delete
make test

%files
%license LICENSE
%doc README Changes 
%{perl_vendorlib}/Test*
%{_mandir}/man3/Test::Strict*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-1
- 0.54 bump (rhbz#2299297)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-13
- Fix tests failing with Perl 5.38

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-10
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-1
- 0.52 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-2
- Perl 5.30 rebuild

* Wed May 29 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-1
- 0.48 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-1
- 0.47 bump

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-2
- Perl 5.28 rebuild

* Fri Feb 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-1
- 0.45 bump

* Wed Feb 21 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump

* Mon Feb 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-1
- 0.41 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-1
- 0.40 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump

* Wed Jun 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-1
- 0.37 bump

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Petr Šabata <contyk@redhat.com> - 0.36-1
- 0.36 bump

* Mon Nov 16 2015 Petr Šabata <contyk@redhat.com> - 0.34-1
- 0.34 bump

* Tue Nov 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-1
- 0.32 bump

* Tue Oct 27 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-1
- 0.31 bump

* Mon Oct 26 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-1
- 0.29 bump

* Mon Oct 05 2015 Petr Šabata <contyk@redhat.com> - 0.28-1
- 0.28 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.22 rebuild

* Thu May 14 2015 Petr Šabata <contyk@redhat.com> - 0.27-1
- 0.27 bump

* Fri Oct 17 2014 Petr Šabata <contyk@redhat.com> - 0.26-1
- 0.26 bump

* Wed Oct 08 2014 Petr Šabata <contyk@redhat.com> - 0.24-1
- 0.24 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump, warnings and strict API change

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.22-2
- Perl 5.18 rebuild

* Fri Mar 01 2013 Petr Šabata <contyk@redhat.com> - 0.22-1
- 0.22 bump, distribution cleanup

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 0.21-1
- 0.21 bump

* Mon Feb 25 2013 Petr Šabata <contyk@redhat.com> - 0.20-1
- 0.20 bump, detect even more modules

* Thu Feb 21 2013 Petr Pisar <ppisar@redhat.com> - 0.19-1
- 0.19 bump

* Mon Feb 18 2013 Petr Šabata <contyk@redhat.com> - 0.18-1
- 0.18 bump, Moose::Autobox doesn't enable strictures

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Petr Šabata <contyk@redhat.com> - 0.17-1
- 0.17 bump
- Modernize the spec a bit
- Remove unused build dependencies
- Update source URL

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.14-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.14-2
- Perl mass rebuild

* Thu Feb 24 2011 Iain Arnell <iarnell@gmail.com> 0.14-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13

* Tue Nov 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- bump

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update for submission

* Wed Nov 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

