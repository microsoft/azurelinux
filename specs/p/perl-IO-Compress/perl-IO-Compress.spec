# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run time expensive tests
%bcond_without long_tests
# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_IO_Compress_enables_optional_test
%else
%bcond_with perl_IO_Compress_enables_optional_test
%endif

# Dependency version if different to this package version
#global depver 2.201

%{?perl_default_filter}

Name:           perl-IO-Compress
Version:        2.213
Release: 522%{?dist}
Summary:        Read and write compressed data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Compress
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Compress-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
# Module Runtime
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Bzip2) >= %{?depver}%{!?depver:%{version}}
BuildRequires:  perl(Compress::Raw::Zlib) >= %{?depver}%{!?depver:%{version}}
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Path)
BuildRequires:  perl(lib)
BuildRequires:  perl(threads::shared)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::More)
%endif
%if %{with perl_IO_Compress_enables_optional_test}
# Optional Tests
BuildRequires:  perl(bytes)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(overload)
# Dual-lived module needs building early in the boot process
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::NoWarnings)
%endif
%endif
# Runtime
Requires:       perl(File::Glob)

# This is wrapper for different Compress modules
Obsoletes:      perl-Compress-Zlib < %{version}-%{release}
Provides:       perl-Compress-Zlib = %{version}-%{release}
Obsoletes:      perl-IO-Compress-Base < %{version}-%{release}
Provides:       perl-IO-Compress-Base = %{version}-%{release}
Obsoletes:      perl-IO-Compress-Bzip2 < %{version}-%{release}
Provides:       perl-IO-Compress-Bzip2 = %{version}-%{release}
Obsoletes:      perl-IO-Compress-Zlib < %{version}-%{release}
Provides:       perl-IO-Compress-Zlib = %{version}-%{release}

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(CompTestUtils\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(.*\.pl)\s*$
%if %{defined perl_bootstrap}
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Builder)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::More)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Test::Simple)\s*$
%endif
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
This distribution provides a Perl interface to allow reading and writing of
compressed data created with the zlib and bzip2 libraries.

IO-Compress supports reading and writing of bzip2, RFC 1950, RFC 1951,
RFC 1952 (i.e. gzip) and zip files/buffers.

The following modules used to be distributed separately, but are now
included with the IO-Compress distribution:
* Compress-Zlib
* IO-Compress-Zlib
* IO-Compress-Bzip2
* IO-Compress-Base

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n IO-Compress-%{version}

# Remove spurious exec permissions
chmod -c -x lib/IO/Uncompress/{Adapter/Identity,RawInflate}.pm
find examples -type f -exec chmod -c -x {} \;

%if ! %{defined perl_bootstrap}
# Remove bundled Test::* modules
rm -rf t/Test
perl -i -ne 'print $_ unless m{^t/Test/}' MANIFEST
%endif

# Fix shellbangs in examples
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl\b|$Config{startperl}|' examples/io/anycat \
        examples/io/bzip2/* examples/io/gzip/* examples/compress-zlib/*

# Help file to recognise the Perl scripts and normalize shebangs
for F in `find t -name *.t` `find t -name *.pl`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} INSTALLDIRS=perl

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a examples t %{buildroot}%{_libexecdir}/%{name}
# Remove release tests
rm %{buildroot}%{_libexecdir}/%{name}/t/999pod.t
rm %{buildroot}%{_libexecdir}/%{name}/t/999meta-*.t
perl -i -pe "s{\"./bin/\"}{\"%{_bindir}\"}" %{buildroot}%{_libexecdir}/%{name}/t/011-streamzip.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Lots of tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
unset PERL_CORE
export TEST_SKIP_VERSION_CHECK=1
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%{_fixperms} -c %{buildroot}

%check
unset PERL_CORE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
export TEST_SKIP_VERSION_CHECK=1
# Build using "--without long_tests" to avoid very long tests
# (full suite can take nearly an hour on an i7 920)
make test COMPRESS_ZLIB_RUN_%{?with_long_tests:ALL}%{!?with_long_tests:MOST}=1

%files
%doc Changes README examples/*
%{_bindir}/streamzip
%{_bindir}/zipdetails
%{perl_privlib}/Compress/
%{perl_privlib}/File/
%dir %{perl_privlib}/IO/
%dir %{perl_privlib}/IO/Compress/
%doc %{perl_privlib}/IO/Compress/FAQ.pod
%{perl_privlib}/IO/Compress.pm
%{perl_privlib}/IO/Compress/Adapter/
%{perl_privlib}/IO/Compress/Base/
%{perl_privlib}/IO/Compress/Base.pm
%{perl_privlib}/IO/Compress/Bzip2.pm
%{perl_privlib}/IO/Compress/Deflate.pm
%{perl_privlib}/IO/Compress/Gzip/
%{perl_privlib}/IO/Compress/Gzip.pm
%{perl_privlib}/IO/Compress/RawDeflate.pm
%{perl_privlib}/IO/Compress/Zip/
%{perl_privlib}/IO/Compress/Zip.pm
%{perl_privlib}/IO/Compress/Zlib/
%{perl_privlib}/IO/Uncompress/
%{_mandir}/man1/streamzip.1*
%{_mandir}/man1/zipdetails.1*
%{_mandir}/man3/Compress::Zlib.3*
%{_mandir}/man3/File::GlobMapper.3*
%{_mandir}/man3/IO::Compress.3*
%{_mandir}/man3/IO::Compress::*.3*
%{_mandir}/man3/IO::Uncompress::*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.213-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.213-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.213-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.213-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Michal Josef Špaček <mspacek@redhat.com> - 2.213-2
- Fix shell

* Thu Aug 29 2024 Paul Howarth <paul@city-fan.org> - 2.213-1
- 2.213 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.212-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.212-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.212-510
- Increase release to favour standalone package

* Sun Apr 28 2024 Paul Howarth <paul@city-fan.org> - 2.212-1
- 2.212 bump (rhbz#2277506)

* Sun Apr  7 2024 Paul Howarth <paul@city-fan.org> - 2.211-1
- 2.211 bump (rhbz#2273778)

* Mon Apr  1 2024 Paul Howarth <paul@city-fan.org> - 2.208-1
- 2.208 bump (rhbz#2272395)

* Wed Feb 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.207-1
- 2.207 bump (rhbz#2265222)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.206-1
- 2.206 bump (rhbz#2225676)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.205-1
- 2.205 bump (rhbz#2223222)

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-499
- Increase release to favour standalone package

* Thu Feb 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.204-1
- 2.204 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.201-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.201-2
- Disable version check in tests

* Sat Jun 25 2022 Paul Howarth <paul@city-fan.org> - 2.201-1
- 2.201 bump

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.106-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.106-488
- Increase release to favour standalone package

* Mon Apr 25 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.103-1
- 2.106 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.102-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.102-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.102-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.102-477
- Increase release to favour standalone package

* Mon Mar 01 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.102-2
- Package tests

* Sun Feb 28 2021 Paul Howarth <paul@city-fan.org> - 2.102-1
- 2.102 bump

* Sat Feb 20 2021 Paul Howarth <paul@city-fan.org> - 2.101-1
- 2.101 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 2021 Paul Howarth <paul@city-fan.org> - 2.100-1
- 2.100 bump
- Use %%{make_build} and %%{make_install}

* Sat Aug  1 2020 Paul Howarth <paul@city-fan.org> - 2.096-1
- 2.096 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Petr Pisar <ppisar@redhat.com> - 2.095-1
- 2.095 bump

* Tue Jul 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.094-1
- 2.094 bump

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.093-2
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

* Mon Jan  7 2019 Paul Howarth <paul@city-fan.org> - 2.084-1
- 2.084 bump

* Wed Jan 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.083-1
- 2.083 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.081-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-2
- Perl 5.28 rebuild

* Mon Apr 09 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-1
- 2.081 bump

* Wed Apr  4 2018 Paul Howarth <paul@city-fan.org> - 2.080-1
- 2.080 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-397
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Petr Pisar <ppisar@redhat.com> - 2.074-396
- Rewrite shell bangs using running perl

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

* Fri Feb 10 2017 Petr Pisar <ppisar@redhat.com> - 2.070-2
- Adjust tests to zlib-1.2.11 (bug #1420012)

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070
  - Fix prototype errors while lazy loading File::GlobMapper (CPAN RT#117675)
  - zipdetails: Avoid loading optional modules from default . (CPAN RT#116538,
    CVE-2016-1238)
- Simplify find command using -delete

* Tue Aug 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-367
- Avoid loading optional modules from default . (CVE-2016-1238)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 27 2015 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069
  - IO::Compress::FAQ - Added a section on bgzip (CPAN RT#103295)
  - IO::Compress::Zip - Zip64 needs to be first in extra field to work around
    a Windows Explorer bug (see
    http://www.info-zip.org/phpBB3/viewtopic.php?f=3&t=440 for details)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.068-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-2
- Perl 5.22 rebuild

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068
  - Disable running of some of the slower test harnesses by default;
    COMPRESS_ZLIB_RUN_MOST needs to be set to run them, which makes life more
    bearable on legacy platforms

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067
  - IO::Compress::RawDeflate unnecessarily loads IO::Seekable (CPAN RT#100257)
- Classify buildreqs by usage

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066
  - IO::Uncompress::Gzip
    - Documentation of ExtraFlags stated the XFL values for BEST_COMPRESSION
      and BEST_SPEED use the values 2 and 4 respectively; they should be 4 and
      2 (code for setting XFL was correct)
  - IO::Uncompress::Gunzip
    - Fix regression preventing gunzip to in-memory file handle (CPAN RT#95494)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Use android-compatible flags when calling gzip in
    IO-Compress/t/050interop-gzip.t (CPAN RT#90216)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063
  - Typo in Compress::Zlib _combine function documentation (CPAN RT#89305)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.062-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Fix up tests for imminent bleadperl changes (CPAN RT#87335)
  - Typo fixes (CPAN RT#84647)
  - IO::Compress::Gzip test t/100generic-bzip2.t hung on Cygwin (CPAN RT#86814)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - zipdetails (1.06)
    - Get it to cope with Android 'zipalign' non-standard extra fields; these
      are used to make sure that a non-compressed member starts on a 4 byte
      boundary
  - unzip example with IO::Uncompress::Unzip (CPAN RT#84647)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060
  - Updated POD
    - CPAN RT#82138: Example code not clear - gunzip() takes filenames!
  - IO::Compress::Base
    - Remove the flush call when opening a filehandle

* Sun Dec 16 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - IO::Compress::Base
    - Added "Encode" option (fixes the encoding half of CPAN RT#42656)

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 2.058-2
- Add missing File::* buildtime dependencies

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - IO::Compress::Zip
    - Allow member name and Zip Comment to be "0"
  - IO::Compress::Base::Common
    - Remove "-r" test - the file open will catch this
    - IO::Compress::Base::Common returned that it could not read readable files
      in NFS (CPAN RT#80855)
  - Install to 'site' instead of 'perl' when perl version is 5.11+
    (CPAN RT#79820)
  - General performance improvements
  - Fix failing 01misc.t subtest introduced in 2.057 (CPAN RT#81119)
- Explicitly install to 'perl' directories

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - FAQ: added a few paragraphs on how to deal with pbzip2 files
    (CPAN RT#77743)
  - Compress::Zip: speed up compress, uncompress, memGzip and memGunzip
    (CPAN RT#77350)
- BR: perl(lib)
- Drop BR: perl(Test::Builder) and perl(Test::More) as they're bundled
- Drop BR: perl(Config), perl(Fcntl), perl(File::Copy), perl(File::Glob),
  perl(POSIX) and perl(Symbol) as they're not dual-lived
- Drop redundant explicit require for perl(Exporter)
- Don't use macros for commands

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.052-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.052-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.052-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.052-2
- Omit optional Test::Pod and Test::NoWarnings tests on bootstrap

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052
  - IO::Compress::Zip: force a ZIP64 archive when it contains ≥ 0xFFFF entries
  - Fix typo in POD (CPAN RT#76130)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049
  - IO::Compress::Zip:
    - Error in t/cz-03zlib-v1.t that caused warnings with 5.15 (Perl RT#110736)

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048
  - Set minimum Perl version to 5.6
  - Set minimum zlib version to 1.2.0
  - IO::Compress::Zip:
    - In one-shot zip, set the Text Flag if "-T" thinks the file is a text file
    - In one-shot mode, wrote mod time and access time in wrong order in the
      "UT" extended field
  - IO::Compress test suite fails with Compress::Raw::Zlib 2.047 and zlib < 1.2.4
    (CPAN RT#74503)
- Resync Compress::Raw::* dependency versions
- Add buildreqs for core perl modules, which might be dual-lived
- Don't use macros for commands

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.046-2
- Fedora 17 mass rebuild

* Mon Dec 19 2011 Paul Howarth <paul@city-fan.org> - 2.046-1
- Update to 2.046
  - Minor update to bin/zipdetails
  - Typo in name of IO::Compress::FAQ.pod
  - IO::Uncompress::Unzip:
    - Example for walking a zip file used eof to control the outer loop; this
      is wrong
  - IO::Compress::Zip:
    - Change default for CanonicalName to false (CPAN RT#72974)
- Freeze Compress::Raw::* dependency versions until next synchronized release

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Restructured IO::Compress::FAQ.pod

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed
  - Added bin/zipdetails
  - In IO::Compress::Zip, in one-shot mode, enable Zip64 mode if the input
    file/buffer ≥ 0xFFFFFFFF bytes
  - Update IO::Compress::FAQ

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043
  - IO::Compress::Base:
    - Fixed issue that with handling of Zip files with two (or more) entries
      that were STORED; symptom is the first is uncompressed ok but the next
      will terminate early if the size of the file is greater than BlockSize
      (CPAN RT#72548)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042
  - IO::Compress::Zip:
    - Added exUnixN option to allow creation of the "ux" extra field, which
      allows 32-bit UID/GID to be stored
    - In one-shot mode use exUnixN rather than exUnix2 for the UID/GID
  - IO::Compress::Zlib::Extra::parseExtraField:
    - Fixed bad test for length of ID field (CPAN RT#72329, CPAN RT#72505)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - IO::Compress::Zip:
    - Added CanonicalName option (note this option is set to true by default)
    - Added FilterName option
    - ExtAttr now populates MSDOS attributes
  - IO::Uncompress::Base:
    - Fixed issue where setting $\ would corrupt the uncompressed data
  - t/050interop-*.t:
    - Handle case when external command contains a whitespace (CPAN RT#71335)
  - t/105oneshot-zip-only.t:
    - CanonicalName test failure on Windows (CPAN RT#68926)

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (support streamed stored content in IO::Uncompress::Unzip)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (Zip/Unzip enhancements)

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (fix test failure on Windows - CPAN RT#67931)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot and defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81816)
- Use more explicit %%files list
- Simplify inclusion of IO::Compress::FAQ
- Drop redundant explicit requires of Compress::Raw::{Bzip2,Zlib}
- Drop installdirs patch, not needed with perl 5.12
- Default installdirs are perl, so no need to specify it explicitly
- Make %%summary less generic

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 2.032-1
- 2.032 bump
- Small improvements in spec file

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.030-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 21 2010 Paul Howarth <paul@city-fan.org> 2.030-3
- Turn long-running tests back on and support build --without long_tests
  to skip them

* Thu Sep 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.030-2
- Install IO::Compress::FAQ into usual POD and man dirs (#634722)

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> 2.030-1
- 2.030 version bump

* Thu May 06 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.027-1
- update

* Mon Apr 12 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-3
- few fixes in specfile 573932

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-2
- Specfile autogenerated by cpanspec 1.78.
- thanks with fixes of specfile to Paul Howarth

