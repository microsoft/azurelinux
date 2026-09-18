# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Optional features
# Run Tk tests
%bcond_with perl_Pod_Perldoc_enables_tk_test
# Support for groff
%bcond_without perl_enables_groff

%global base_version 3.28
Name:           perl-Pod-Perldoc
# let's overwrite the module from perl.srpm
Version:        3.28.01
Release:        521%{?dist}
Summary:        Look up Perl documentation in Pod format
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Pod-Perldoc
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MALLEN/Pod-Perldoc-%{base_version}.tar.gz
# Unbundled from perl 5.28.0-RC1
Patch0:         Pod-Perldoc-3.28-Upgrade-to-3.2801.patch
# 1/2 Fix searching for builtins in perlop POD, bug #1739463, CPAN RT#126015
Patch1:         Pod-Perldoc-3.28-Add-a-test-for-a-truncated-perldoc-f-tr-output.patch
# 1/2 Fix searching for builtins in perlop POD, bug #1739463, CPAN RT#126015
Patch2:         Pod-Perldoc-3.28-Search-for-X-in-the-whole-perlop-document.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
%if %{with perl_enables_groff}
# Pod::Perldoc::ToMan executes roff
BuildRequires:  groff-base
%endif
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
# File::Temp 0.22 not used by tests
# HTTP::Tiny not used by tests
# IO::Handle not used by tests
BuildRequires:  perl(IO::Select)
# IPC::Open3 not used by tests
BuildRequires:  perl(parent)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
BuildRequires:  perl(Pod::Man) >= 2.18
BuildRequires:  perl(Pod::Simple::Checker)
BuildRequires:  perl(Pod::Simple::RTF) >= 3.16
BuildRequires:  perl(Pod::Simple::XMLOutStream) >= 3.16
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Pod::Text::Color)
BuildRequires:  perl(Pod::Text::Termcap)
# Symbol not used by tests
# Text::ParseWords not used by tests
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
%if !( 0%{?rhel} >= 7 )
%if %{with perl_Pod_Perldoc_enables_tk_test}
BuildRequires:  perl(Tk)
# Tk::FcyEntry is optional
BuildRequires:  perl(Tk::Pod)
%endif
%endif
%endif
%if %{with perl_enables_groff}
# Pod::Perldoc::ToMan executes roff
Requires:       groff-base
%endif
Requires:       perl(File::Temp) >= 0.22
Requires:       perl(HTTP::Tiny)
Requires:       perl(IO::Handle)
Requires:       perl(IPC::Open3)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
Requires:       perl(Pod::Simple::Checker)
Requires:       perl(Pod::Simple::RTF) >= 3.16
Requires:       perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       perl(Text::ParseWords)
# Tk is optional
Requires:       perl(Symbol)

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Pod::Man|Pod::Simple::XMLOutStream|Pod::Simple::RTF)\\)$

%description
perldoc looks up a piece of documentation in POD format that is embedded
in the perl installation tree or in a Perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the Perl library modules.

%prep
%setup -q -n Pod-Perldoc-%{base_version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{_bindir}/perldoc
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-456
- Increase release to favour standalone package

* Tue Mar 03 2020 Petr Pisar <ppisar@redhat.com> - 3.28.01-444
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-443
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Petr Pisar <ppisar@redhat.com> - 3.28.01-442
- Build-require blib module for tests (bug #1739463)

* Thu Aug 15 2019 Petr Pisar <ppisar@redhat.com> - 3.28.01-441
- Fix searching for builtins in perlop POD (bug #1739463)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.01-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-416
- Increase release to favour standalone package

* Thu May 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.28.01-1
- Upgrade to 3.2801 as provided in perl-5.28.0-RC1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.28-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.28-393
- Perl 5.26 rebuild

* Mon Apr 03 2017 Petr Pisar <ppisar@redhat.com> - 3.28-2
- Introduce a build-condition on groff
- Rename a _without_tk build-condition to
  _without_perl_Pod_Perldoc_enables_tk_test

* Thu Mar 16 2017 Petr Pisar <ppisar@redhat.com> - 3.28-1
- 3.28 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.27-1
- 3.27 bump

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 3.26-1
- 3.26 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-349
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 3.25-348
- Current generator detects dependency on Encode and Pod::Man properly

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.25-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.25-2
- Perl 5.22 rebuild

* Fri Feb 13 2015 Petr Pisar <ppisar@redhat.com> - 3.25-1
- 3.25 bump

* Mon Sep 15 2014 Petr Pisar <ppisar@redhat.com> - 3.24-4
- Enable perl(Tk) tests

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.24-3
- Perl 5.20 re-rebuild of bootstrapped packages
- Disable Perl(Tk) tests temporarily until Perl-Tk works with perl-5.20

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.24-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Petr Pisar <ppisar@redhat.com> - 3.24-1
- 3.24 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Petr Pisar <ppisar@redhat.com> - 3.23-1
- 3.23 bump

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 3.21-1
- 3.21 bump

* Mon Oct 07 2013 Petr Pisar <ppisar@redhat.com> - 3.20-7
- Correct perldoc.pod location (bug #1010057)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.20-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 3.20-4
- Specify all dependencies

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.20-3
- Link minimal build-root packages against libperl.so explicitly

* Thu May 23 2013 Petr Pisar <ppisar@redhat.com> - 3.20-2
- Specify all dependencies

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 3.20-1
- 3.20 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 3.19.01-1
- 3.19_01 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 3.19.00-1
- 3.19 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17.00-241
- Do not build-require perl(Tk) on RHEL >= 7
- Depend on perl(HTTP::Tiny)

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17.00-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.17-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-7
- Perl 5.16 rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-6
- Require groff-base because Pod::Perldoc::ToMan executes roff

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.17-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 3.17-4
- Omit optional Tk tests on bootstrap

* Wed May 30 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17-3
- conditionalize optional BR tests

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17-2
- Fix perldoc synopsis (bug #821632)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 3.17-1
- 3.17 bump
- Fix displaying long POD in groff

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> 3.15-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr from spec code.
- perl(Config) BR removed
- Source URL fixed to point to BDFOY author
- Do not require unversioned perl(Pod::Simple::RTF)
