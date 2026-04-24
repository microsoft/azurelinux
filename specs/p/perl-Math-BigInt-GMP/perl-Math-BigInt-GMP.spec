# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Math-BigInt-GMP
Version:        1.7003
Release: 4%{?dist}
Summary:        Use the GMP library for Math::BigInt routines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Math-BigInt-GMP
Source0:        https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-GMP-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Module Runtime
BuildRequires:  perl(Math::BigInt::Lib) >= 1.999801
BuildRequires:  perl(XSLoader) >= 0.02
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Math::BigFloat) >= 1.994
BuildRequires:  perl(Math::BigInt) >= 2.005001
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(threads)
Requires:       perl(Math::BigInt) >= 2.005001

%{?perl_default_filter}

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(.::t/.*.inc\\)
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Provides support for big integer calculations by means of the GMP library, as
a replacement (drop-in) module for Math::BigInt's core, Math::BigInt::Calc.pm.
Math::BigInt::GMP does not use Math::GMP, but provides its own XS layer to
access the GMP library. This cuts out another (perl subroutine) layer and
also reduces the memory footprint by not loading Math::GMP and Carp at all.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Math::BigInt) >= 2.005001

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Math-BigInt-GMP-%{version}

# Remove bundled libraries
rm -r inc
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST
find -type f -exec chmod -x {} +

# Get rid of bogus exec permissions
chmod -c -x CHANGES lib/Math/BigInt/GMP.pm

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/00sig.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset TEST_SIGNATURE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc BUGS CHANGES CREDITS README TODO
%{perl_vendorarch}/auto/Math/
%{perl_vendorarch}/Math/
%{_mandir}/man3/Math::BigInt::GMP.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.7003-2
- Perl 5.42 rebuild

* Fri Mar 28 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.7003-1
- 1.7003 bump (rhbz#2355195)

* Mon Mar 03 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.7002-1
- 1.7002 bump (rhbz#2349245)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7001-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.7001-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.7001-1
- 1.7001 bump (rhbz#2257057)

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.7000-1
- 1.7000 bump (rhbz#2255972)

* Thu Sep 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.6013-1
- 1.6013 bump (rhbz#2239929)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6012-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.6012-2
- Perl 5.38 rebuild

* Mon Apr  3 2023 Paul Howarth <paul@city-fan.org> - 1.6012-1
- 1.6012 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.6011-2
- Perl 5.36 rebuild

* Tue May 17 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.6011-1
- 1.6011 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 30 2021 Paul Howarth <paul@city-fan.org> - 1.6010-1
- 1.6010 bump

* Wed Sep 29 2021 Paul Howarth <paul@city-fan.org> - 1.6009-1
- 1.6009 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.6008-1
- 1.6008 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.6007-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.6007-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 14 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.6007-1
- 1.6007 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.6006-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.6006-1
- 1.6006 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.6005-3
- Perl 5.28 rebuild

* Wed Apr 18 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.6005-1
- 1.6005 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.6004-2
- Perl 5.26 rebuild

* Mon Feb 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.6004-1
- 1.6004 bump

* Thu Jan 12 2017 Paul Howarth <paul@city-fan.org> - 1.6003-1
- 1.6003 bump

* Mon Dec 05 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6002-1
- 1.6002 bump

* Fri Nov 25 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6001-1
- 1.6001 bump

* Fri Nov 18 2016 Paul Howarth <paul@city-fan.org> - 1.6000-1
- Update to 1.6000
  - Sync test files with Math-BigInt-1.999800
  - Update bundled Devel::CheckLib from v1.03 to v1.07
  - Math::BigInt::GMP is now a subclass of Math::BigInt::Lib, so remove pure
    Perl methods from Math::BigInt::GMP that are implemented in the superclass
    Math::BigInt::Lib; the methods removed are _digit(), _num(), _nok(), and
    _log_int() (the version of _log_int() implemented in Math::BigInt::GMP was
    buggy anyway)
  - Fix _check() so it doesn't give a "use of uninitialized value" warning if
    given an undefined "object"
  - Trim whitespace in all files
  - Better use of the functionality in Test::More in t/bigintg.t
- Add support for build --with author_tests

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-2
- Perl 5.24 rebuild

* Tue Apr 26 2016 Paul Howarth <paul@city-fan.org> - 1.51-1
- Update to 1.51
  - Sync test files with Math-BigInt-1.999719

* Fri Apr 22 2016 Paul Howarth <paul@city-fan.org> - 1.50-1
- Update to 1.50
  - Sync test files with Math-BigInt-1.999718

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 1.49-3
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find command using -empty and -delete
- Drop redundant Group: tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan  3 2016 Paul Howarth <paul@city-fan.org> - 1.49-1
- Update to 1.49
  - Sync test files with Math-BigInt-1.999714

* Thu Dec 31 2015 Paul Howarth <paul@city-fan.org> - 1.48-1
- Update to 1.48
  - Sync test files with Math-BigInt-1.999713

* Tue Dec 15 2015 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  - Fix problems with the new() method when Perl is compiled with support for
    64-bit integers, but on platforms when the underlying OS is 32-bit
    (CPAN RT#71548)

* Fri Dec  4 2015 Paul Howarth <paul@city-fan.org> - 1.46-1
- Update to 1.46
  - Add patch and new test file 't/mbi-from-big-scalar.t' regarding
    CPAN RT#103517
  - Fix spelling in GMP.xs ('modifing' → 'modifying')
  - Whitespace/formatting in t/bigintg.t to make it more readable and more in
    accordance with the 'perlstyle' manpage

* Mon Nov  9 2015 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  - Sync test files with Math-BigInt-1.999709
  - Required version of Test::More is 0.47

* Fri Oct 30 2015 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - Sync test files with Math-BigInt-1.999707
  - Update the README file
  - Replace 'use vars ...' with 'our ...'; we require a Perl newer than 5.6.0
    anyway
  - Required version of Math-BigInt is now 1.999706
  - Add 'Test::More' to TEST_REQUIRES in Makefile.PL
  - Enable 'use warnings'; we require a Perl newer than 5.6.0 anyway
  - Add 'assertlib.*\.exe' to MANIFEST.SKIP, since make generates temporary
    files like 'assertlibzxjE4WfG.exe' on Cygwin

* Tue Sep 22 2015 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - Sync test files with Math-BigInt-1.999703
  - Required version of Math-BigInt is now 1.999703
  - Update author information

* Fri Sep 18 2015 Paul Howarth <paul@city-fan.org> - 1.42-1
- Update to 1.42
  - Sync test files with Math-BigInt-1.999702
  - Required version of Math-BigInt is now 1.999702

* Mon Sep 14 2015 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - Synced tests with the Math-BigInt distribution
- Bumped Math::BigInt version requirement to 1.999701

* Wed Aug 19 2015 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - Add changes for the newest release
  - Reorder change entries into descending chronological order
  - Update bundled Devel::CheckLib from v1.01 to v1.03
  - Update required version of Math-BigInt to 1.9994
  - Various test fixes to ensure correct backend is used
  - Rather than an early exit(), use skip() to skip tests

* Tue Aug 18 2015 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - Updated test files with those from Math-BigInt-1.9997

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-2
- Fixed test scripts for Perl 5.22 (CPAN RT#96113)

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - Updated test files from the Math::BigInt distribution
  - Updated POD
  - Updated bundled Devel::CheckLib from v0.93 to v1.01
- Classify buildreqs by usage
- Use features from recent EU::MM since we need Math::BigInt ≥ 1.9993
- Always run the test suite
- Improve %%summary and %%description
- Use %%license
- Make %%files list more explicit
- Remove spurious exec permissions from text files
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-8
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 1.37-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.36-4.1
- Perl 5.16 rebuild
- Update to 1.37

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 1.36-2.1
- rebuild with new gmp

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.36-2
- Perl mass rebuild

* Sat Jun 18 2011 Iain Arnell <iarnell@gmail.com> 1.36-1
- update to latest upstream version to fix perl-5.14 FTBFS
- clean up spec for modern rpmbuild
- use perl_default_filter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Steven Pritchard <steve@kspei.com> 1.32-1
- Update to 1.32.
- Update Source0 URL.
- BR threads.

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-7
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-6
- Mass rebuild with perl-5.12.0

* Tue Dec 15 2009 Stepan Kasal <skasal@redhat.com> - 1.24-5
- skip check in distributions with perl-5.8

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.24-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May 18 2008 Steven Pritchard <steve@kspei.com> 1.24-1
- Specfile autogenerated by cpanspec 1.75.
- BR Test::More, Test::Pod, Test::Pod::Coverage, and gmp-devel.
