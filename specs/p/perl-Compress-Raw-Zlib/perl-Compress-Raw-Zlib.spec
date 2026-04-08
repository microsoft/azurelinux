# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Compress_Raw_Zlib_enables_optional_test
%else
%bcond_with perl_Compress_Raw_Zlib_enables_optional_test
%endif


Name:           perl-Compress-Raw-Zlib
Version:        2.213
Release:        521%{?dist}
Summary:        Low-level interface to the zlib compression library
# Zlib.xs:  (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Zlib
# Others:   GPL-1.0-or-later OR Artistic-1.0-Perl
## Not used to produce binary packages
# zlib-src: Zlib
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Zlib
URL:            https://metacpan.org/release/Compress-Raw-Zlib
Source0:        https://cpan.metacpan.org/modules/by-module/Compress/Compress-Raw-Zlib-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::Install)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
BuildRequires:  perl(vars)
BuildRequires:  zlib-devel >= 1.3
# Module Runtime
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(File::Path)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(threads::shared)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::More)
%endif
%if %{with perl_Compress_Raw_Zlib_enables_optional_test}
# Optional Tests
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
# Release tests are deleted
BuildRequires:  perl(Test::NoWarnings)
%endif
%endif
# Runtime
Requires:       perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(CompTestUtils\\)
%if %{defined perl_bootstrap}
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Builder)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::More)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Simple)\s*$
%endif
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}


%description
The Compress::Raw::Zlib module provides a Perl interface to the zlib
compression library, which is used by IO::Compress::Zlib.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Compress_Raw_Zlib_enables_optional_test}
# Optional Tests
Requires:       perl(File::Temp)
Requires:       perl(overload)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
Requires:       perl(Test::NoWarnings)
%endif
%endif

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Compress-Raw-Zlib-%{version}

# Remove bundled zlib
rm -rf zlib-src
perl -i -ne 'print $_ unless m{^zlib-src/}' MANIFEST

%if ! %{defined perl_bootstrap}
# Remove bundled Test::* modules
rm -rf t/Test
perl -i -ne 'print $_ unless m{^t/Test/}' MANIFEST
%endif

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1' "$F"
    chmod +x "$F"
done

%build
OLD_ZLIB=False
BUILD_ZLIB=False 
ZLIB_LIB=%{_libdir}
ZLIB_INCLUDE=%{_includedir}
export BUILD_ZLIB OLD_ZLIB ZLIB_LIB ZLIB_INCLUDE
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove release tests
rm %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
rm %{buildroot}%{_libexecdir}/%{name}/t/meta-*.t
perl -i -pe "s{DIR => '.'}{DIR => '/tmp'}" %{buildroot}%{_libexecdir}/%{name}/t/compress/CompTestUtils.pm
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset PERL_CORE
COMPRESS_ZLIB_RUN_MOST=1
export COMPRESS_ZLIB_RUN_MOST
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset PERL_CORE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test COMPRESS_ZLIB_RUN_MOST=1

%files
%doc Changes README
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Zlib.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.213-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.213-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.213-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.213-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 29 2024 Paul Howarth <paul@city-fan.org> - 2.213-1
- 2.213 bump

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.212-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.212-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.212-510
- Increase release to favour standalone package

* Sun Apr 28 2024 Paul Howarth <paul@city-fan.org> - 2.212-1
- 2.212 bump (rhbz#2277504)

* Sun Apr  7 2024 Paul Howarth <paul@city-fan.org> - 2.211-1
- 2.211 bump (rhbz#2273785)

* Tue Feb 27 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.209-1
- 2.209 bump (rhbz#2266094)

* Wed Feb 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.208-1
- 2.208 bump (rhbz#2265216)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Paul Howarth <paul@city-fan.org> - 2.206-2
- Rebuild for zlib-ng in Rawhide

* Wed Jul 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.206-1
- 2.206 bump (rhbz#2225674)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.205-1
- 2.205 bump (rhbz#2223211)

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-499
- Increase release to favour standalone package

* Thu Feb 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-2
- Update for disttag

* Thu Feb 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-1
- 2.204 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.202-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Paul Howarth <paul@city-fan.org> - 2.202-4
- Rebuild for zlib 1.2.13

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.202-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Paul Howarth <paul@city-fan.org> - 2.202-2
- Rebuilt for zlib 1.2.12

* Mon Jun 27 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.202-1
- 2.202 bump

* Sat Jun 25 2022 Paul Howarth <paul@city-fan.org> - 2.201-1
- 2.201 bump

* Wed Jun 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.200-1
- 2.200 bump

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.105-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.105-488
- Increase release to favour standalone package

* Sat May 14 2022 Paul Howarth <paul@city-fan.org> - 2.105-1
- 2.105 bump

* Fri May 13 2022 Paul Howarth <paul@city-fan.org> - 2.104-1
- 2.104 bump

* Mon Apr 04 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.103-1
- 2.103 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.101-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.101-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-477
- Increase release to favour standalone package

* Mon Feb 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-3
- Fix dependencies for ELN

* Mon Feb 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-2
- Package tests

* Sat Feb 20 2021 Paul Howarth <paul@city-fan.org> - 2.101-1
- 2.101 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.100-1
- 2.100 bump

* Sat Aug  1 2020 Paul Howarth <paul@city-fan.org> - 2.096-1
- 2.096 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Petr Pisar <ppisar@redhat.com> - 2.095-1
- 2.095 bump

* Mon Jul 13 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.094-1
- 2.094 bump

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.093-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec  8 2019 Paul Howarth <paul@city-fan.org> - 2.093-1
- 2.093 bump

* Thu Dec 05 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.092-1
- 2.092 bump

* Sun Nov 24 2019 Paul Howarth <paul@city-fan.org> - 2.091-1
- 2.091 bump

* Sun Nov 10 2019 Paul Howarth <paul@city-fan.org> - 2.090-1
- 2.090 bump

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.089-1
- 2.089 bump

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.088-1
- 2.088 bump

* Mon Aug 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.087-1
- 2.087 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.086-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.086-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.086-2
- Perl 5.30 rebuild

* Mon Apr 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.086-1
- 2.086 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.084-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.084-1
- 2.084 bump

* Wed Jan 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.083-1
- 2.083 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.081-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-2
- Perl 5.28 rebuild

* Mon Apr 09 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-1
- 2.081 bump

* Wed Apr 04 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.080-1
- 2.080 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.076-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.076-1
- 2.076 bump

* Wed Nov 15 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.075-1
- 2.075 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-393
- Perl 5.26 rebuild

* Mon Feb 20 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-1
- 2.074 bump

* Mon Feb 13 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.072-1
- 2.072 bump

* Tue Feb 07 2017 Petr Pisar <ppisar@redhat.com> - 2.071-2
- Adapt tests to zlib-1.2.11 (bug #1419841)

* Sat Dec 31 2016 Paul Howarth <paul@city-fan.org> - 2.071-1
- Update to 2.071
  - One (last?) compilation warning in bundled inflate.c (CPAN RT#119580,
    https://github.com/madler/zlib/issues/111)

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070
  - Fix compilation warning from inflate.c (CPAN RT#107642)
  - Fix wrong FLAG_APPEND logic, analog to Bzip2 (CPAN RT#119007)
- Simplify find commands using -empty and -delete

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 27 2015 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069
  - Reduce compiler warnings and stderr noise (CPAN RT#101341)
  - amigaos4: cpan/Compress-Raw-Zlib: also __amigaos4__ (CPAN RT#106799)
  - const all global data (CPAN RT#101298)
  - Coverity finding: Unused value (CPAN RT#105414)
  - Coverity findings (CPAN RT#102399)
  - Coverity finding: Overlapping buffer in memory copy (CPAN RT#105413)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.068-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-3
- Perl 5.22 rebuild

* Thu Mar 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-2
- Correct license from (GPL+ or Artistic) to ((GPL+ or Artistic) and zlib)

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068
  - Silence more compiler warnings
  - Disable running of 07bufsize.t by default; COMPRESS_ZLIB_RUN_MOST needs to
    be set to run it, which makes life more bearable on legacy platforms

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067 (silence compiler warnings)
- Classify buildreqs by usage

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066
  - Another COW violation (CPAN RT#98069)
  - Misleading nesting/indentation found by Coverity (CPAN RT#95405)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.065-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.065-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.065-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.065-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.065-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Paul Howarth <paul@city-fan.org> - 2.065-1
- Update to 2.065
  - Resolve c++ build failure in core (CPAN RT#92657)
  - gcc -g3: final link failed: Memory exhausted (CPAN RT#88936)

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Handle non-PVs better (CPAN RT#91558)
  - Z_OK instead of Z_BUF_ERROR (CPAN RT#92521)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063
  - gcc -g3: final link failed: Memory exhausted (CPAN RT#88936)
  - Compress::Raw::Zlib uses AutoLoader for no reason (CPAN RT#88260)
  - Typo in Compress::Zlib _combine function documentation (CPAN RT#89305)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.062-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Typo fix (CPAN RT#86417)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Include zlib 1.2.8 source
  - Typo fix (CPAN RT#85431)
  - Silence compiler warning by making 2nd parameter to DispStream a const char*

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (mention SimpleZip in POD)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Copy-on-write support (CPAN RT#81353)

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Compress::Raw::Zlib needs to use PERL_NO_GET_CONTEXT (CPAN RT#80319)
  - Install to 'site' instead of 'perl' when perl version is 5.11+
    (CPAN RT#79812)
  - Update to ppport.h that includes SvPV_nomg_nolen (CPAN RT#78079)

* Sat Aug 11 2012 Paul Howarth <paul@city-fan.org> - 2.056-1
- Update to 2.056
  - Fix C++ build issue

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Fix misuse of magic in API (CPAN RT#78079)
  - Include zlib 1.2.7 source
- BR: perl(Exporter) and perl(lib)
- BR: perl(Test::NoWarnings) except when bootstrapping
- Drop redundant explicit require for perl(Exporter)
- Drop BR: perl(bytes), not dual-lived

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.054-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.054-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.054-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.054-2
- Omit optional Test::Pod tests on bootstrap

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 2.054-1
- Update to 2.054
  - Fix build issue on Win32 (CPAN RT#77030)

* Sun May  6 2012 Paul Howarth <paul@city-fan.org> - 2.053-1
- Update to 2.053
  - Include zlib 1.2.7 source

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052
  - Fix build issue when Perl is built with C++
- Don't need to remove empty directories from buildroot

* Thu Feb 23 2012 Paul Howarth <paul@city-fan.org> - 2.051-1
- Update to 2.051
  - Fix bug in Compress::Raw::Zlib on 64-bit Windows (CPAN RT#75222)

* Tue Feb 21 2012 Paul Howarth <paul@city-fan.org> - 2.050-1
- Update to 2.050
  - Fix build failure on Irix and Solaris (CPAN RT#75151)

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049
  - Include zlib 1.2.6 source

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048
  - Allow flush to be called multiple times without any intermediate call to
    deflate and still return Z_OK
  - Added support for zlibCompileFlags
  - Set minimum Perl version to 5.6
  - Set minimum zlib version to 1.2.0
- Don't use macros for commands

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod into Zlib.pm

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Croak if attempt to freeze/thaw compression object (CPAN RT#69985)
- BR: perl(Carp)

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.037-4
- Install to vendorlib so that our debuginfo does not conflict with that of
  the main perl package

* Thu Jul 28 2011 Karsten Hopp <karsten@redhat.com> 2.037-3
- Bump and rebuild as it got compiled with the old perl on ppc

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (added offset parameter to CRC32)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Fri Jun 17 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Perl mass rebuild

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot and defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.033-3
- remove epoch again, it's actually rpmdev bug
 https://fedorahosted.org/rpmdevtools/ticket/13

* Fri Jan 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.033-2
- re-add epoch. rpmdev-vercmp "0" 2.032 2 "" 2.033 1 -> 2.032

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81782)
- Drop redundant Obsoletes and Epoch tags
- Simplify provides filter

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 0:2.032-2
- BuildRequire perl(Test::Pod) for tests

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 0:2.032-1
- 2.032 bump

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.030-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> - 0:2.030-1
- 2.030 version bump

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.027-1
- update

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.024-3
- Mass rebuild with perl-5.12.0

* Mon Mar 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-2
- split again from main package for updated version

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-2
- Bump release to beat F-7 version

* Sun Jul 01 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-1
- update to 2.005.

* Tue Jun 05 2007 Robin Norwood <rnorwood@redhat.com> - 2.004-1
- Initial build from CPAN

