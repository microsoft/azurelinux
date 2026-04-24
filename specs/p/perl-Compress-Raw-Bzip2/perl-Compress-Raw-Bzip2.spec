# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Compress_Raw_Bzip2_enables_optional_test
%else
%bcond_with perl_Compress_Raw_Bzip2_enables_optional_test
%endif

Name:           perl-Compress-Raw-Bzip2
Summary:        Low-level interface to bzip2 compression library
Version:        2.213
Release: 522%{?dist}
# Other files:  GPL-1.0-or-later OR Artistic-1.0-Perl
## unbundled
# bzip2-src:    BSD
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Compress-Raw-Bzip2
Source0:        https://cpan.metacpan.org/modules/by-module/Compress/Compress-Raw-Bzip2-%{version}.tar.gz
# Module Build
BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
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
BuildRequires:  perl(threads::shared)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::More)
%endif
%if %{with perl_Compress_Raw_Bzip2_enables_optional_test}
# Optional Tests
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
%if !%{defined perl_bootstrap}
# Release tests are deleted
BuildRequires:  perl(Test::NoWarnings)
%endif
BuildRequires:  perl(Scalar::Util)
%endif
BuildRequires:  perl(vars)
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
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Compress_Raw_Bzip2_enables_optional_test}
# Optional Tests
Requires:       perl(File::Temp)
Requires:       perl(overload)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
Requires:       perl(Test::NoWarnings)
%endif
Requires:       perl(Scalar::Util)
%endif

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Compress-Raw-Bzip2-%{version}
# Remove bundled bzip2 sources
rm -r bzip2-src
perl -i -ne 'print unless /^bzip2-src\//' MANIFEST

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

# Remove release tests
rm t/99pod.t t/meta-*.t
perl -i -ne 'print $_ unless m{^t/99pod\.t}' MANIFEST
perl -i -ne 'print $_ unless m{^t/meta-.*\.t}' MANIFEST

%build
BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -pe "s{DIR => '.'}{DIR => '/tmp'}" %{buildroot}%{_libexecdir}/%{name}/t/compress/CompTestUtils.pm
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset PERL_CORE
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%{_fixperms} -c %{buildroot}

%check
unset PERL_CORE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Bzip2.3*

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
- 2.212 bump (rhbz#2277505)

* Sun Apr  7 2024 Paul Howarth <paul@city-fan.org> - 2.211-1
- 2.211 bump (rhbz#2273784)

* Mon Feb 26 2024 Paul Howarth <paul@city-fan.org> - 2.210-1
- 2.210 bump (rhbz#2266016)

* Wed Feb 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.209-1
- 2.209 bump (rhbz#2265215)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.206-1
- 2.206 bump (rhbz#2225675)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.205-1
- 2.205 bump (rhbz#2223210)

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-499
- Increase release to favour standalone package

* Thu Feb 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-2
- Update for disttag

* Thu Feb 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-1
- 2.204 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.201-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 25 2022 Paul Howarth <paul@city-fan.org> - 2.201-1
- 2.201 bump

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.103-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.103-488
- Increase release to favour standalone package

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

* Mon Jul 30 2018 Petr Pisar <ppisar@redhat.com> - 2.081-5
- Prune bundled bzip2 sources

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

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-397
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.070-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070
  - Fix wrong APPEND_OUTPUT logic (CPAN RT#119005, CPAN RT#119141)
  - Fix some gcc warnings (CPAN RT#100817, CPAN RT#105647)
- Simplify find commands using -empty and -delete

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 27 2015 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069
  - Reduce compiler warnings and stderr noise (CPAN RT#101340)
  - consting misc tables (CPAN RT#101296)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.068-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-2
- Perl 5.22 rebuild

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068 (no changes)

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067 (silence compiler warnings)
- Classify buildreqs by usage

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066 (no changes)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Handle non-PVs better (CPAN RT#91558)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063
  - gcc -g3: final link failed: Memory exhausted (CPAN RT#88936)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.062-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062 (no changes)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Silence compiler warning by making 2nd parameter to DispStream a const char*

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (no changes)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Copy-on-write support (CPAN RT#81352)

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Compress::Raw::Bzip2 needs to use PERL_NO_GET_CONTEXT (CPAN RT#80318)
  - Install to 'site' instead of 'perl' when perl version is 5.11+
    (CPAN RT#79811)
  - Update to ppport.h that includes SvPV_nomg_nolen (CPAN RT#78080)

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Fix misuse of magic in API (CPAN RT#78080)
- Drop redundant explicit requires for perl(Exporter) and perl(File::Temp)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.052-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.052-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.052-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.052-2
- Omit optional Test::Pod tests on bootstrap

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052 (no changes)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049 (no changes)

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048 (set minimum Perl version to 5.6)
- Don't use macros for commands

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod to IO::Compress

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

* Thu Jul 28 2011 Karsten Hopp <karsten@redhat.com> 2.037-3
- Bump and rebuild, got compiled with old perl on ppc

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (no changes)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Fri Jun 17 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Perl mass rebuild

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot cleanup, defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81782)

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 2.032-1
- 2.032 bump

* Wed Sep 29 2010 jkeating - 2.031-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Petr Pisar <ppisar@redhat.com> - 2.031-1
- 2.031 bump

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> - 2.030-1
- 2.030 version bump

* Thu May  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.027-1
- update
 
* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.026-2
- Mass rebuild with perl-5.12.0

* Sat Apr 10 2010 Chris Weyl <cweyl@alumni.drew.edu> 2.026-1
- PERL_INSTALL_ROOT => DESTDIR, use _fixperms incantation
- add perl_default_filter (XS package)
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.026)

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.020-2
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.020-1
- update

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.005-5
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.005-4
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-3
- Update license tag.

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-2
- Bump release to beat F-7 version

* Sun Jul 01 2007 Steven Pritchard <steve@kspei.com> 2.005-1
- Update to 2.005.
- Build against system libbz2 (#246401).

* Tue Jun 05 2007 Robin Norwood <rnorwood@redhat.com> - 2.004-1
- Initial build from CPAN
