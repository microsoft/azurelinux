# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%bcond_without perl_ExtUtils_MakeMaker_enables_optional_test

%global cpan_name ExtUtils-MakeMaker

Name:           perl-%{cpan_name}
Epoch:          2
Version:        7.76
Release:        521%{?dist}
Summary:        Create a module Makefile
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/%{cpan_name}
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/%{cpan_name}-%{version}.tar.gz
# Do not set RPATH to perl shared-library modules by default. Bug #773622.
# This is copy from `perl' package. This is a distributor extension.
Patch0:         %{cpan_name}-7.36-USE_MM_LD_RUN_PATH.patch
# Link to libperl.so explicitly. Bug #960048.
Patch1:         %{cpan_name}-7.30-Link-to-libperl-explicitly-on-Linux.patch
# Unbundle version modules
Patch2:         %{cpan_name}-7.04-Unbundle-version.patch
# Unbundle Encode::Locale module
Patch3:         %{cpan_name}-7.22-Unbundle-Encode-Locale.patch
# Provide maybe_command independently, bug #1129443
Patch4:         %{cpan_name}-7.11-Provide-ExtUtils-MM-methods-as-standalone-ExtUtils-M.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Makefile.Pl uses ExtUtils::MakeMaker from ./lib
# B needed only for CPAN::Meta::Requirements
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
# CPAN::Meta::Requirements has a fallback
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# If an XS module is compiled, xsubpp(1) is needed
BuildRequires:  perl-ExtUtils-ParseXS
# Tests:
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN::Meta) >= 2.143240
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::Install) >= 1.52
# ExtUtils::Installed not used at tests
BuildRequires:  perl(ExtUtils::Manifest) >= 1.70
# ExtUtils::Packlist not used at tests
# ExtUtils::XSSymSet is not needed (VMS only)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(Getopt::Long)
# IO::File not used at tests
# IO::Handle not used
BuildRequires:  perl(less)
BuildRequires:  perl(overload)
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4414
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(subs)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::ParseWords)
# threads::shared not used
BuildRequires:  perl(utf8)
# XSLoader not used
%if %{with perl_ExtUtils_MakeMaker_enables_optional_test}
# Optional tests
BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(PerlIO)
# Keep YAML optional
# Keep YAML::Tiny optional
%endif
Recommends:     perl(CPAN::Meta) >= 2.143240
Suggests:       perl(CPAN::Meta::Converter) >= 2.141170
# CPAN::Meta::Requirements to support version ranges
Recommends:     perl(CPAN::Meta::Requirements) >= 2.130
Requires:       perl(Data::Dumper)
Requires:       perl(DynaLoader)
# Encode is needed for producing POD with =encoding statement correctly
Requires:       perl(Encode)
%if !%{defined perl_bootstrap}
Recommends:     perl(Encode::Locale)
%endif
Requires:       perl(ExtUtils::Command) >= 1.19
Requires:       perl(ExtUtils::Install) >= 1.54
Requires:       perl(ExtUtils::Manifest) >= 1.70
# ExtUtils::XSSymSet is not needed (VMS only)
Requires:       perl(File::Find)
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Getopt::Long)
Suggests:       perl(JSON::PP)
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       perl(Pod::Man)
Requires:       perl(POSIX)
Requires:       perl(Test::Harness)
Recommends:     perl(Time::HiRes)
Requires:       perl(Text::ParseWords)
# VMS::Filespec is not needed (VMS only)
# Win32 is not needed (Win32 only)
# If an XS module is compiled, xsubpp(1) is needed
Requires:       perl-ExtUtils-ParseXS
# These dependencies are weak in order to relieve building noarch
# packages from perl-devel and gcc. See bug #1547165.
# If an XS module is built, code generated from XS will be compiled and it
# includes Perl header files.
Recommends:     perl-devel
# If an XS module is built, the generated Makefile executes gcc.
Recommends:     gcc

# Do not export underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)\s*$
# Do not export private redefinitions
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader|ExtUtils::MakeMaker::_version\\)

# Filter modules bundled for tests
%global __requires_exclude %{__requires_exclude}|^perl\\(MY)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(TieIn)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(TieOut)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(MakeMaker::Test.*)\s*$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
This utility is designed to write a Makefile for an extension module from a
Makefile.PL. It is based on the Makefile.SH model provided by Andy
Dougherty and the perl5-porters.

%package -n perl-ExtUtils-Command
Summary:        Perl routines to replace common UNIX commands in Makefiles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
Requires:       perl(Carp)
Requires:       perl(File::Copy)
Requires:       perl(File::Find)
Requires:       perl(File::Path)
# File::Spec not used
# VMS::Feature not used

%description -n perl-ExtUtils-Command
This Perl module is used to replace common UNIX commands. In all cases the
functions work with @ARGV rather than taking arguments. This makes them
easier to deal with in Makefiles.

%package -n perl-ExtUtils-MM-Utils
Summary:        ExtUtils::MM methods without dependency on ExtUtils::MakeMaker
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch

%description -n perl-ExtUtils-MM-Utils
This is a collection of ExtUtils::MM subroutines that are used by many
other modules but that do not need full-featured ExtUtils::MakeMaker. The
issue with ExtUtils::MakeMaker is it pulls in Perl header files and that
is an overkill for small subroutines.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(CPAN::Meta) >= 2.143240
Requires:       perl(Encode)
Requires:       perl(File::Spec)
Requires:       perl(Parse::CPAN::Meta) >= 1.4414
Requires:       perl(Pod::Man)
Requires:       perl(version)
%if %{with perl_ExtUtils_MakeMaker_enables_optional_test}
# Optional tests
Requires:       perl-devel
Requires:       perl(ExtUtils::CBuilder)
Requires:       perl(PerlIO)
%endif

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n ExtUtils-MakeMaker-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
# Remove bundled modules
rm -rf bundled
perl -i -ne 'print $_ unless m{^bundled/}' MANIFEST
rm -rf t/lib/Test
perl -i -ne 'print $_ unless m{^t/lib/Test/}' MANIFEST
rm -rf lib/ExtUtils/MakeMaker/version{,.pm}
perl -i -ne 'print $_ unless m{^lib/ExtUtils/MakeMaker/version(?:/|\.pm)}' MANIFEST
rm -rf lib/ExtUtils/MakeMaker/Locale.pm
perl -i -ne 'print $_ unless m{^lib/ExtUtils/MakeMaker/Locale\.pm}' MANIFEST

%if !%{with perl_ExtUtils_MakeMaker_enables_optional_test}
# Remove optional tests
rm t/02-xsdynamic.t t/03-xsstatic.t
perl -i -ne 'print $_ unless m{^t/02-xsdynamic\.t}' MANIFEST
perl -i -ne 'print $_ unless m{^t/03-xsstatic\.t}' MANIFEST
perl -i -ne 'print $_ unless m{^t/unicode\.t}' MANIFEST
%endif

# Help file to recognise the Perl scripts and normalize shebangs
for F in `find t -name *.t`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
BUILDING_AS_PACKAGE=1 perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Lots of tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%{_fixperms} %{buildroot}/*

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes CONTRIBUTING README
%{_bindir}/*
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/ExtUtils/Command.pm
%exclude %dir %{perl_vendorlib}/ExtUtils/MM
%exclude %{perl_vendorlib}/ExtUtils/MM/Utils.pm
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/ExtUtils::Command.*
%exclude %{_mandir}/man3/ExtUtils::MM::Utils.*

%files -n perl-ExtUtils-Command
%dir %{perl_vendorlib}/ExtUtils
%{perl_vendorlib}/ExtUtils/Command.pm
%{_mandir}/man3/ExtUtils::Command.*

%files -n perl-ExtUtils-MM-Utils
%dir %{perl_vendorlib}/ExtUtils
%dir %{perl_vendorlib}/ExtUtils/MM
%{perl_vendorlib}/ExtUtils/MM/Utils.pm
%{_mandir}/man3/ExtUtils::MM::Utils.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.76-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.76-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.76-519
- Increase release to favour standalone package

* Mon May 26 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.76-1
- 7.76 bump (rhbz#2368311)

* Thu Apr 10 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.74-1
- 7.74 bump (rhbz#2358633)

* Mon Mar 17 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.72-1
- 7.72 bump (rhbz#2352533)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.70-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.70-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.70-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.70-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.70-499
- Increase release to favour standalone package

* Mon Mar 27 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.70-1
- 7.70 bump

* Mon Mar 20 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.68-1
- 7.68 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.66-1
- 7.66 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.64-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.64-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.64-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.64-1
- 7.64 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.62-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.62-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.62-477
- Increase release to favour standalone package

* Wed Apr 14 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.62-1
- 7.62 bump

* Fri Feb 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.60-1
- 7.60 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.58-1
- 7.58 bump

* Fri Nov 20 2020 Petr Pisar <ppisar@redhat.com> - 2:7.56-1
- 7.56 bump

* Fri Nov 13 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.54-1
- 7.54 bump

* Thu Nov 05 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.52-1
- 7.52 bump

* Thu Oct 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.50-1
- 7.50 bump

* Tue Oct 06 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.48-1
- 7.48 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.46-2
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Petr Pisar <ppisar@redhat.com> - 2:7.46-1
- 7.46 bump

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.44-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Petr Pisar <ppisar@redhat.com> - 2:7.44-1
- 7.44 bump

* Wed Dec 18 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.42-1
- 7.42 bump

* Tue Dec 17 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.40-1
- 7.40 bump

* Wed Sep 11 2019 Petr Pisar <ppisar@redhat.com> - 2:7.38-1
- 7.38 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.36-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.36-2
- Perl 5.30 rebuild

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 1:7.36-1
- 7.36 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.34-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.34-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.34-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.34-416
- Increase release to favour standalone package

* Mon Mar 19 2018 Petr Pisar <ppisar@redhat.com> - 1:7.34-1
- 7.34 bump

* Wed Feb 28 2018 Petr Pisar <ppisar@redhat.com> - 1:7.32-2
- Recommend gcc and perl-devel instead of a hard dependency (bug #1547165)

* Mon Feb 19 2018 Petr Pisar <ppisar@redhat.com> - 1:7.32-1
- 7.32 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Petr Pisar <ppisar@redhat.com> - 1:7.30-3
- Rebase patches
- Do not recommend non-core Encode::Locale on bootstrapping

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Petr Pisar <ppisar@redhat.com> - 1:7.30-1
- 7.30 bump

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.28-2
- Perl 5.26 rebuild

* Wed May 31 2017 Petr Pisar <ppisar@redhat.com> - 7.28-1
- 7.28 bump

* Mon May 29 2017 Petr Pisar <ppisar@redhat.com> - 7.26-1
- 7.26 bump
- Fix META generation (CPAN RT#121913)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 25 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.24-1
- 7.24 bump

* Tue Aug 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.22-1
- 7.22 bump

* Tue May 24 2016 Petr Pisar <ppisar@redhat.com> - 7.18-1
- 7.18 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.16-2
- Perl 5.24 rebuild

* Mon May 09 2016 Petr Pisar <ppisar@redhat.com> - 7.16-1
- 7.16 bump

* Mon Apr 25 2016 Petr Pisar <ppisar@redhat.com> - 7.14-1
- 7.14 bump

* Wed Apr 20 2016 Petr Pisar <ppisar@redhat.com> - 7.12-1
- 7.12 bump

* Tue Apr 19 2016 Petr Pisar <ppisar@redhat.com> - 7.10-5
- Own ExtUtils/MM directory by perl-ExtUtils-MM-Utils only
- Require perl-devel by perl-ExtUtils-MakeMaker

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 7.10-4
- Provide maybe_command independently (bug #1129443)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 03 2015 Petr Pisar <ppisar@redhat.com> - 7.10-2
- Declare optional dependencies on Recommends level

* Fri Sep 11 2015 Petr Pisar <ppisar@redhat.com> - 7.10-1
- 7.10 bump

* Wed Sep 09 2015 Petr Pisar <ppisar@redhat.com> - 7.08-1
- 7.08 bump

* Tue Sep 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.06-2
- Remove new line from INC (CPAN RT#106808)

* Tue Sep 01 2015 Petr Pisar <ppisar@redhat.com> - 7.06-1
- 7.06 bump
- ExtUtils::Command module is distributed by ExtUtils-MakeMaker

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.04-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.04-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.04-2
- Perl 5.22 rebuild

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 7.04-1
- 7.04 bump

* Tue Nov 11 2014 Petr Pisar <ppisar@redhat.com> - 7.02-1
- 7.02 bump
- Cope with missing Encode::Locale

* Wed Nov 05 2014 Petr Pisar <ppisar@redhat.com> - 7.00-2
- Fix building with older xsubpp

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 7.00-1
- 7.00 bump

* Fri Oct 24 2014 Petr Pisar <ppisar@redhat.com> - 6.98-311
- Require perl-ExtUtils-ParseXS because of xsubpp

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.98-310
- Increase release to favour standalone package

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.98-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Petr Pisar <ppisar@redhat.com> - 6.98-1
- 6.98 bump

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 6.96-1
- 6.96 bump

* Wed Mar 26 2014 Petr Pisar <ppisar@redhat.com> - 6.94-1
- 6.94 bump

* Fri Mar 14 2014 Petr Pisar <ppisar@redhat.com> - 6.92-1
- 6.92 bump

* Fri Feb 21 2014 Petr Pisar <ppisar@redhat.com> - 6.90-1
- 6.90 bump

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 6.88-1
- 6.88 bump

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 6.86-1
- 6.86 bump

* Mon Dec 02 2013 Petr Pisar <ppisar@redhat.com> - 6.84-1
- 6.84 bump

* Tue Nov 05 2013 Petr Pisar <ppisar@redhat.com> - 6.82-1
- 6.82 bump

* Wed Oct 16 2013 Petr Pisar <ppisar@redhat.com> - 6.80-1
- 6.80 bump

* Tue Sep 24 2013 Petr Pisar <ppisar@redhat.com> - 6.78-1
- 6.78 bump

* Mon Sep 16 2013 Petr Pisar <ppisar@redhat.com> - 6.76-2
- Specify all dependencies (bug #1007755)

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 6.76-1
- 6.76 bump

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 6.74-1
- 6.74 bump

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 6.72-1
- 6.72 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.68-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 6.68-4
- Perl 5.18 rebuild

* Tue Jul 02 2013 Petr Pisar <ppisar@redhat.com> - 6.68-3
- Link to libperl.so explicitly (bug #960048)

* Thu Jun 27 2013 Jitka Plesnikova <jplesnik@redhat.com> - 6.68-2
- Update BRs

* Mon Jun 17 2013 Petr Pisar <ppisar@redhat.com> - 6.68-1
- 6.68 bump

* Mon Apr 22 2013 Petr Pisar <ppisar@redhat.com> - 6.66-1
- 6.66 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 6.64-2
- Run-require POD convertors to get manual pages when building other packages

* Mon Dec 17 2012 Petr Pisar <ppisar@redhat.com> - 6.64-1
- 6.64 bump

* Tue Aug 28 2012 Petr Pisar <ppisar@redhat.com> - 6.63.02-241
- Compute RPM version
- Do not build-require itself, the build script runs from ./lib

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.63.02-240
- update version to the same as in perl.srpm
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 6.62-3
- Perl 5.16 rebuild

* Thu Jan 12 2012 Petr Pisar <ppisar@redhat.com> - 6.62-2
- Do not set RPATH to perl shared-library modules by default (bug #773622)

* Fri Nov 25 2011 Petr Pisar <ppisar@redhat.com> 6.62-1
- Specfile autogenerated by cpanspec 1.78.
- Remove defattr and BuildRoot from spec.
