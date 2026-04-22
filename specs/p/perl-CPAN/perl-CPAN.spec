# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Don not run gnupg1 tests by default, they need network access
# (Socket::inet_aton('pool.sks-keyservers.net')).
%bcond_with perl_CPAN_enables_gnupg_test
# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_CPAN_enables_optional_test
%else
%bcond_with perl_CPAN_enables_optional_test
%endif

Name:           perl-CPAN
Version:        2.38
Release: 522%{?dist}
Summary:        Query, download and build perl modules from CPAN sites
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/CPAN
Source0:        https://cpan.metacpan.org/authors/id/A/AN/ANDK/CPAN-%{version}.tar.gz
# Create site paths for the first time, bug #1158873, CPAN RT#99905
Patch0:         CPAN-2.18-Attemp-to-create-site-library-directories-on-first-t.patch
# Change configuration directory name
Patch1:         CPAN-2.18-Replace-configuration-directory-string-with-a-marke.patch
# Only require config for CPAN shell operations
Patch2:         CPAN-2.38-Only-require-config-for-CPAN-shell-operations.patch
# Update man page to provide notes about first run, GH issue #194
Patch3:         CPAN-2.38-Add-notes-about-first-configuration.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
# Module::Signature not used
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Optional:
BuildRequires:  perl(File::Spec)
# YAML::Syck is not used because @ST_PREFS is empty in Makefile.PL

# Run-time:
# Prefer Archive::Tar and Compress::Zlib over tar and gzip
BuildRequires:  perl(Archive::Tar) >= 1.50
%if !%{defined perl_bootstrap}
# Prefer Archive::Zip over unzip
BuildRequires:  perl(Archive::Zip)
%endif
BuildRequires:  perl(autouse)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# Devel::Size not used at tests
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(Dumpvalue)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
# ExtUtils::Manifest not used at tests
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
# File::HomeDir 0.65 not used at tests
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Getopt::Std)
# HTTP::Date is optional, prefer in-core Time::Local
# HTTP::Request is optional
BuildRequires:  perl(HTTP::Tiny) >= 0.005
BuildRequires:  perl(if)
# IO::Socket::SSL 1.56 is optional
# YAML::XS or YAML::Syck or JSON::PP, we already use YAML::Syck at a different
# place, keep JSON::PP optional
BuildRequires:  perl(lib)
# local::lib is optional
# LWP is optional, prefer HTTP::Tiny and Net::FTP
# LWP::UserAgent is optional
# Mac::BuildTools not needed
# Mac::Files not needed
# Module::Signature is optional
# Net::Config not used at tests
# Net::FTP not used at tests
# Net::Ping is required but >= 2.13 version is a soft dependency
# Net::SSLeay 1.49 is optional
BuildRequires:  perl(Net::Ping)
BuildRequires:  perl(overload)
# Pod::Perldoc is optional
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Wrap)
# Time::Local not used at tests
# URI not used at tests
# URI::Escape not used at tests
# URI::URL 0.08 is optional 
# User::pwent not used at tests
BuildRequires:  perl(warnings)
# Optional:
#%%if !%%{defined perl_bootstrap}
# CPAN::DistnameInfo not used at tests
#%%endif
BuildRequires:  perl(CPAN::Meta) >= 2.110350
# Crypt::OpenPGP not used at tests
# Digest::MD5 not used at tests
BuildRequires:  perl(Digest::SHA)
# Keep Log::Log4perl optional
# Keep MIME::Base64 optional
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Module::Build)
%endif

# Tests:
BuildRequires:  perl(blib)
# CPAN::Checksums not used
BuildRequires:  perl(File::Which)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)

%if %{with perl_CPAN_enables_optional_test}
# Optional tests:
%if %{with perl_CPAN_enables_gnupg_test}
BuildRequires:  %{_bindir}/gpg
# CPAN::Perl::Releases is helpfull only on RC or TRIAL Perl interpreters
# Digest::SHA1 not needed if Digest::SHA is available
# Digest::SHA::PurePerl not needed if Digest::SHA is available
%endif
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Expect)
%endif
BuildRequires:  perl(Hash::Util)
%if !%{defined perl_bootstrap}
# Kwalify not yet packaged
%if %{with perl_CPAN_enables_gnupg_test}
BuildRequires:  perl(Module::Signature) >= 0.66
%endif
BuildRequires:  perl(Perl::Version)
%endif
BuildRequires:  perl(Pod::Perldoc::ToMan)
%if %{with perl_CPAN_enables_gnupg_test}
BuildRequires:  perl(Socket)
%endif
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Sort::Versions)
# Test::MinimumVersion not used
# Test::Perl::Critic not used
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 0.18
BuildRequires:  perl(YAML) >= 0.60
%endif
%endif

Requires:       make
# Some subpackages modules are not dual-lived. E.g. "open". If a distribution
# on CPAN declares a dependency on such a module, CPAN client will fail
# because the only provider is perl distribution.
# Another issue is with dual-lived modules whose distribution actually does
# not declare all needed core dependencies and the installation would also
# fail.
# As a result, any CPAN client must run-require the complete perl.
Requires:       perl
Requires:       perl(Archive::Tar) >= 1.50
%if !%{defined perl_bootstrap}
Recommends:     perl(CPAN::DistnameInfo)
%endif
Requires:       perl(CPAN::Meta::Requirements) >= 2.121
Requires:       perl(Data::Dumper)
%if !%{defined perl_bootstrap}
Requires:       perl(Devel::Size)
%endif
Requires:       perl(ExtUtils::Manifest)
%if !%{defined perl_bootstrap}
Requires:       perl(File::HomeDir) >= 0.65
%endif
Requires:       perl(File::Temp) >= 0.16
# YAML::XS or YAML::Syck or JSON::PP, we already use YAML::Syck at a different
# place, keep JSON::PP optional
Requires:       perl(lib)
%if !%{defined perl_bootstrap}
Suggests:       perl(Log::Log4perl)
%endif
Requires:       perl(Net::Config)
Requires:       perl(Net::FTP)
Requires:       perl(POSIX)
Requires:       perl(Term::ReadLine)
Requires:       perl(Time::Local)
%if !%{defined perl_bootstrap}
Requires:       perl(URI)
Requires:       perl(URI::Escape)
%endif
Requires:       perl(User::pwent)
# Optional but highly recommended:
%if !%{defined perl_bootstrap}
# Prefer Archive::Zip over unzip
Requires:       perl(Archive::Zip)
Requires:       perl(Compress::Bzip2)
Requires:       perl(CPAN::Meta) >= 2.110350
%endif
Requires:       perl(Compress::Zlib)
Requires:       perl(Digest::MD5)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Dumpvalue)
Requires:       perl(ExtUtils::CBuilder)
# Optional for signature verification CVE-2020-16156
%if ! %{defined perl_bootstrap}
Requires:       perl(Module::Signature)
%endif
%if ! %{defined perl_bootstrap}
# Avoid circular deps local::lib -> Module::Install -> CPAN when bootstraping
# local::lib recommended by CPAN::FirstTime default choice, bug #1122498
Requires:       perl(local::lib)
%endif
%if ! %{defined perl_bootstrap}
Requires:       perl(Module::Build)
%endif
Recommends:     perl(Pod::Perldoc)
%if ! %{defined perl_bootstrap}
Recommends:     perl(Term::ReadKey)
Requires:       perl(Text::Glob)
# Text::Levenshtein::XS or Text::Levenshtein::Damerau::XS or Text::Levenshtein
# or Text::Levenshtein::Damerau::PP
Suggests:       perl(Text::Levenshtein::Damerau::XS)
# YAML::Syck or YAML or Data::Dumper or overload
Suggests:       perl(YAML::Syck)
%endif
Provides:       cpan = %{version}

# Filter non-Linux dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Mac::BuildTools\\)
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CPAN::Meta::Requirements\\)
# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(CPAN::MyConfig\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(local_utils\\)

%description
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use LWP, HTTP::Tiny, Net::FTP and certain
external download clients to fetch distributions from the net.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n CPAN-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

# Change configuration name
find -type f -exec perl -i -pe 's/XCPANCONFIGNAMEX/cpan/g' {} \;
# Remove bundled modules
rm -r ./inc/*
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t distroprefs %{buildroot}%{_libexecdir}/%{name}
# Does not work with system module
rm %{buildroot}%{_libexecdir}/%{name}/t/5*pod*.t
# Remove the tests which need ./lib and ./blib
rm %{buildroot}%{_libexecdir}/%{name}/t/03pkgs.t
rm %{buildroot}%{_libexecdir}/%{name}/t/04clean_load.t
# Needed internet connection
rm %{buildroot}%{_libexecdir}/%{name}/t/31sessions.t
# Use system modules for tests
perl -i -ple 's{-Mblib}{}' %{buildroot}%{_libexecdir}/%{name}/t/97-run.t
perl -i -ple 's{-Mblib}{}' %{buildroot}%{_libexecdir}/%{name}/t/97-return_values.t
mkdir -p %{buildroot}%{_libexecdir}/%{name}/blib/script
ln -s %{_bindir}/cpan %{buildroot}%{_libexecdir}/%{name}/blib/script
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
unset AUTHOR_TEST CPAN_EXPECT_TIMEOUT CPAN_RUN_SHELL_TEST_WITHOUT_EXPECT \
    ftp_proxy http_proxy no_proxy \
    PERL5_CPAN_IS_RUNNING PERL5_CPAN_IS_RUNNING_IN_RECURSION PERL_CORE VERBOSE
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I .
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset AUTHOR_TEST CPAN_EXPECT_TIMEOUT CPAN_RUN_SHELL_TEST_WITHOUT_EXPECT \
    ftp_proxy http_proxy no_proxy \
    PERL5_CPAN_IS_RUNNING PERL5_CPAN_IS_RUNNING_IN_RECURSION PERL_CORE VERBOSE
make test

%files
%doc Changes PAUSE*.pub README Todo
%{_bindir}/cpan*
%{perl_vendorlib}/App*
%{perl_vendorlib}/CPAN*
%{_mandir}/man1/cpan*
%{_mandir}/man3/App*
%{_mandir}/man3/CPAN*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-519
- Increase release to favour standalone package

* Fri Mar 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-4
- Require config only for CPAN shell operations
- Update man page to provide notes about first run

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-2
- Fix shell in test script

* Mon Nov 18 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-1
- 2.38 bump (rhbz#2326875)

* Mon Sep 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-1
- 2.37 bump (rhbz#2309019)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-499
- Increase release to favour standalone package

* Mon May 15 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-1
- 2.36 bump

* Tue May 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.35-1
- 2.35 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-2
- Perl 5.36 rebuild

* Wed Apr 20 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-1
- 2.34 bump

* Mon Apr 04 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-1
- 2.33 bump

* Wed Feb 09 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-3
- Package tests

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-1
- 2.29 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-477
- Increase release to favour standalone package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Petr Pisar <ppisar@redhat.com> - 2.28-5
- Run-require complete perl

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-2
- Perl 5.32 rebuild

* Mon Jun 15 2020 Petr Pisar <ppisar@redhat.com> - 2.28-1
- 2.28 bump

* Fri Jan 31 2020 Petr Pisar <ppisar@redhat.com> - 2.27-4
- Enable loading objects from session YAML files (CPAN RT#131615)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Petr Pisar <ppisar@redhat.com> - 2.27-1
- 2.27 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-2
- Perl 5.30 rebuild

* Tue Mar 19 2019 Petr Pisar <ppisar@redhat.com> - 2.26-1
- 2.26 bump

* Mon Mar 04 2019 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-416
- Increase release to favour standalone package

* Wed May 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-1
- Upgrade to 2.20 as provided in perl-5.28.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-397
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Petr Pisar <ppisar@redhat.com> - 2.18-396
- Rebase patches to prevent from installing back-up files

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-393
- Perl 5.26 rebuild

* Fri May 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-2
- Don't BR: perl(Module::Build) when bootstrapping

* Wed May 10 2017 Petr Pisar <ppisar@redhat.com> - 2.18-1
- Upgrade to CPAN-2.18 as provided in perl-5.25.12

* Wed Feb 15 2017 Petr Pisar <ppisar@redhat.com> - 2.16-1
- 2.16 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Petr Pisar <ppisar@redhat.com> - 2.14-4
- Use Perl porter's fix for searching cpan -j file (CPAN RT#116507)
- Fix logging fatal errors (https://github.com/andk/cpanpm/pull/104)

* Tue Oct 18 2016 Petr Pisar <ppisar@redhat.com> - 2.14-3
- Apply remains of CVE-2016-1238 fix from perl (CPAN RT#116507)
- Do not search cpan -j file in @INC (CPAN RT#116507)

* Wed Oct 12 2016 Petr Pisar <ppisar@redhat.com> - 2.14-2
- Fix CVE-2016-1238 properly (CPAN RT#116507)

* Mon Jun 27 2016 Petr Pisar <ppisar@redhat.com> - 2.14-1
- 2.14 bump
- Fix installation from a working directory (CPAN RT#115734)
- Fix "cpan -O" invocation (CPAN RT#115786)
- Do not use Net::FTP if ftp_proxy variable points to an HTTP server
  (CPAN RT#110833)
- Recognize URL schemata disregarding the case
- Fix CVE-2016-1238 (loading optional modules from current working directory)
- Recognize exact version dependency operator (CPAN RT#47934)
- Cope with non-digit version strings

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-349
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Petr Pisar <ppisar@redhat.com> - 2.11-348
- Require make package

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-345
- Increase release to favour standalone package

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 2.11-1
- 2.11 bump in order to dual-live with perl 5.22

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 2.10-1
- 2.10 bump

* Wed Jan 28 2015 Petr Pisar <ppisar@redhat.com> - 2.05-309
- Allow changing the configuration directory name

* Thu Oct 30 2014 Petr Pisar <ppisar@redhat.com> - 2.05-308
- Create site paths for the first time (bug #1158873)

* Wed Sep 10 2014 Petr Pisar <ppisar@redhat.com> 2.05-307
- Synchronize to perl.spec modifications
- Disable non-core modules when bootstrapping

* Tue Apr 22 2014 Petr Pisar <ppisar@redhat.com> 2.05-1
- Specfile autogenerated by cpanspec 1.78.
