# Run optional test
%{bcond_without perl_Alien_Build_enables_optional_test}
# Exhibit FFI::Platypus in Test::Alien
%if !%{defined perl_bootstrap}
# Build cycle: perl-FFI-Platypus → perl-Alien-Build
%{bcond_without perl_Alien_Build_enables_platypus}
%endif

Name:           perl-Alien-Build
Version:        2.17
Release:        3%{?dist}
Summary:        Build external dependencies for use in CPAN
# lib/Alien/Build/Plugin/Test/Mock.pm contains Base64-encoded files for tests
# (a bash script, C source file, a gzipped tar archive, Mach-O 64-bit x86_64
# object file and a static library).
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Alien-Build
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-Build-%{version}.tar.gz#/perl-Alien-Build-%{version}.tar.gz
# Support only the most advanced pkgconfig implementation,
# the files are deleted in prep section
Patch0:         Alien-Build-1.96-Remove-redundant-pkgconfig-implementations.patch
BuildArch:      noarch
BuildRequires:  make
# Makefile.PL executes ./inc/probebad.pl that executes XS checks
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(File::Which) >= 1.10
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
%if !%{defined perl_bootstrap}
# t/alien_build_plugin_build_cmake.t executes gcc via cmake (bug #923024)
# Build cycle: perl-Alien-cmake3 → perl-Alien-Build
BuildRequires:  perl(Alien::cmake3) >= 0.02
%endif
# Archive::Tar or (tar and bzip2 and gzip and xz)
BuildRequires:  perl(Archive::Tar)
# Archive::Zip or unzip
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(base)
BuildRequires:  perl(Capture::Tiny) >= 0.17
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config::INI::Reader::Multiline)
BuildRequires:  perl(constant)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Env)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::ParseXS) >= 3.30
BuildRequires:  perl(FFI::CheckLib)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::BOM)
BuildRequires:  perl(File::chdir)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(JSON::PP)
# List::Util 1.33 not used at tests
BuildRequires:  perl(overload)
BuildRequires:  perl(Path::Tiny) >= 0.077
# Alien::Build::Plugin::PkgConfig::Negotiate finds a pkgconfig implementation
# in this order:
# PkgConfig::LibPkgConf 0.04, pkgconf, pkg-config, PkgConfig 0.14026.
# We selected the most advanced PkgConfig::LibPkgConf and removed the other
# plugins.
BuildRequires:  perl(PkgConfig::LibPkgConf::Client) >= 0.04
BuildRequires:  perl(PkgConfig::LibPkgConf::Util) >= 0.04
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Test2::API) >= 1.302096
BuildRequires:  perl(Text::ParseWords) >= 3.26
# YAML or Data::Dumper
BuildRequires:  perl(YAML)
# Optional run-time:
%if %{with perl_Alien_Build_enables_platypus}
BuildRequires:  perl(FFI::Platypus) >= 0.12
%endif
# Tests:
# AnyEvent not used
# AnyEvent::FTP::Server not used
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Glob)
# Getopt::Long not used
# IO::Socket::INET not used
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util) >= 1.33
# Mojo::JSON not used
# Mojo::URL not used
# Mojolicious::Lite not used
BuildRequires:  perl(Net::FTP)
# Proc::Daemon not used
BuildRequires:  perl(Test2::V0) >= 0.000060
# URI not used
BuildRequires:  perl(utf8)
%if %{with perl_Alien_Build_enables_optional_test}
# Optional tests:
%if !%{defined perl_bootstrap}
# Break build cycle: Acme::Alien::DontPanic → Test::Alien
BuildRequires:  perl(Acme::Alien::DontPanic) >= 0.026
# Break build cycle: perl-Alien-Base-ModuleBuild → perl-Alien-Build
BuildRequires:  perl(Alien::Base::ModuleBuild) >= 0.040
%endif
BuildRequires:  perl(Devel::Hide)
BuildRequires:  perl(Env::ShellWords)
# FFI::Platypus not packaged
# HTTP::Tiny or curl
BuildRequires:  perl(HTTP::Tiny) >= 0.044
# Prefer Mojo::DOM with Mojolicious, URI, URI::Escape over Mojo::DOM58
BuildRequires:  perl(Mojo::DOM)
BuildRequires:  perl(Mojolicious) >= 7.00
# PkgConfig not packaged
BuildRequires:  perl(Readonly) >= 1.60
BuildRequires:  perl(Sort::Versions)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(URI::file)
%endif
# make in the lib/Alien/Build/Plugin/Build/CMake.pm plugin
# make in the lib/Alien/Build/Plugin/Build/Make.pm plugin
# make or Alien::gmake
BuildRequires:  make
Suggests:       curl
# Alien::Base::Wrapper::cc() executes $Config{cc}.
Requires:       gcc
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if !%{defined perl_bootstrap}
# Build cycle: perl-Alien-cmake3 → perl-Alien-Build
Requires:       perl(Alien::cmake3) >= 0.02
%endif
# Alien::Build::Plugin::Download::Negotiate defaults to Decode::Mojo instead
# of Decode::HTML
Suggests:       perl(Alien::Build::Plugin::Decode::HTML)
Requires:       perl(Alien::Build::Plugin::Decode::Mojo)
# Archive::Tar or (tar and bzip2 and gzip and xz)
Requires:       perl(Archive::Tar)
# Archive::Zip or unzip
Requires:       perl(Archive::Zip)
Requires:       perl(Config::INI::Reader::Multiline)
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::CBuilder)
Requires:       perl(ExtUtils::MakeMaker) >= 6.52
Requires:       perl(ExtUtils::ParseXS) >= 3.30
Requires:       perl(FFI::CheckLib)
%if %{with perl_Alien_Build_enables_platypus}
Recommends:     perl(FFI::Platypus) >= 0.12
%endif
Requires:       perl(File::BOM)
Requires:       perl(File::Find)
Requires:       perl(Path::Tiny) >= 0.077
# Alien::Build::Plugin::PkgConfig::Negotiate finds a pkgconfig implementation
# in this order:
# PkgConfig::LibPkgConf 0.04, pkgconf, pkg-config, PkgConfig 0.14026
# We selected the most advanced PkgConfig::LibPkgConf and removed the other
# plugins.
Requires:       perl(PkgConfig::LibPkgConf::Client) >= 0.04
Requires:       perl(PkgConfig::LibPkgConf::Util) >= 0.04
Requires:       perl(Storable)
Requires:       perl(Test2::API) >= 1.302096
Requires:       perl(Text::ParseWords) >= 3.26
# YAML or Data::Dumper
Requires:       perl(YAML)
Suggests:       wget
# Alien::Base::PkgConfig moved from perl-Alien-Base-ModuleBuild
Conflicts:      perl-Alien-Base-ModuleBuild < 1.00

# Do not gather dependencies from the documentation
%{?perl_default_filter}

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Capture::Tiny|Path::Tiny|Test2::API|Text::ParseWords)\\)$
# Remove private redefinitions
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(Alien::Build::rc\\)$

%description
This package provides tools for building external (non-CPAN) dependencies
for CPAN. It is mainly designed to be used at install time of a CPAN
client, and work closely with Alien::Base which is used at run time.

%package Plugin-Decode-HTML
Summary:        Alien::Build plugin to extract links from HTML
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(HTML::LinkExtor)
Requires:       perl(URI)
Requires:       perl(URI::Escape)
# Subpackaged from perl-Alien-Build-1.76
Conflicts:      perl-Alien-Build < 1.76

%description Plugin-Decode-HTML
This Alien::Build plugin decodes an HTML file listing into a list of
candidates for your Prefer plugin.

%package Plugin-Decode-Mojo
Summary:        Alien::Build plugin to extract links from HTML
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Prefer Mojo::DOM with Mojolicious >= 7.00 over Mojo::DOM58 that is not yet
# packaged.
Requires:       perl(Mojo::DOM)
Requires:       perl(Mojolicious) >= 7.00
Requires:       perl(URI)
Requires:       perl(URI::Escape)

%description Plugin-Decode-Mojo
This Alien::Build plugin decodes an HTML file listing into a list of
candidates for your Prefer plugin.

%prep
%setup -q -n Alien-Build-%{version}
# Remove redundant pkgconfig implementations, keep
# Alien::Build::Plugin::PkgConfig::LibPkgConf,
# MANIFEST is updated by Remove-redundant-pkgconfig-implementations.patch
%patch0 -p1
rm lib/Alien/Build/Plugin/PkgConfig/{CommandLine,PP}.pm 
rm t/alien_build_plugin_pkgconfig_{commandline,pp}.t

%build
unset PKG_CONFIG
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
unset ACLOCAL_PATH ALIEN_BASE_WRAPPER_QUIET ALIEN_BUILD_LIVE_TEST \
    ALIEN_BUILD_LOG ALIEN_BUILD_PKG_CONFIG ALIEN_BUILD_POSTLOAD \
    ALIEN_BUILD_PRELOAD ALIEN_BUILD_RC ALIEN_BUILD_SITE_CONFIG ALIEN_FORCE \
    ALIEN_INSTALL_NETWORK ALIEN_INSTALL_TYPE CIPDIST CONFIG_SITE CURL DESTDIR \
    FOO1 FOO2 FOO3 VERBOSE WGET
make test

%files
%license LICENSE
%doc Changes Changes.Alien-Base Changes.Alien-Base-Wrapper Changes.Test-Alien
%doc example README SUPPORT
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/Alien/Build/Plugin/Decode/HTML.pm
%exclude %{perl_vendorlib}/Alien/Build/Plugin/Decode/Mojo.pm
%{_mandir}/man3/*
%exclude %{_mandir}/man3/Alien::Build::Plugin::Decode::HTML.3pm.*
%exclude %{_mandir}/man3/Alien::Build::Plugin::Decode::Mojo.3pm.*

%files Plugin-Decode-HTML
%{perl_vendorlib}/Alien/Build/Plugin/Decode/HTML.pm
%{_mandir}/man3/Alien::Build::Plugin::Decode::HTML.3pm.*

%files Plugin-Decode-Mojo
%doc Changes.Alien-Build-Decode-Mojo
%{perl_vendorlib}/Alien/Build/Plugin/Decode/Mojo.pm
%{_mandir}/man3/Alien::Build::Plugin::Decode::Mojo.3pm.*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.17-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.17-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Fri Mar 20 2020 Petr Pisar <ppisar@redhat.com> - 2.17-1
- 2.17 bump

* Mon Mar 16 2020 Petr Pisar <ppisar@redhat.com> - 2.15-1
- 2.15 bump

* Tue Mar 10 2020 Petr Pisar <ppisar@redhat.com> - 2.12-1
- 2.12 bump

* Mon Mar 09 2020 Petr Pisar <ppisar@redhat.com> - 2.11-1
- 2.11 bump

* Mon Feb 17 2020 Petr Pisar <ppisar@redhat.com> - 2.08-1
- 2.08 bump

* Thu Feb 06 2020 Petr Pisar <ppisar@redhat.com> - 2.04-1
- 2.04 bump

* Wed Feb 05 2020 Petr Pisar <ppisar@redhat.com> - 2.02-1
- 2.02 bump

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 2.00-1
- 2.00 bump

* Fri Jan 31 2020 Petr Pisar <ppisar@redhat.com> - 1.98-1
- 1.98 bump

* Tue Jan 28 2020 Petr Pisar <ppisar@redhat.com> - 1.96-1
- 1.96 bump

* Tue Dec 17 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.94-1
- 1.94 bump

* Tue Dec 10 2019 Petr Pisar <ppisar@redhat.com> - 1.93-1
- 1.93 bump

* Mon Nov 04 2019 Petr Pisar <ppisar@redhat.com> - 1.92-1
- 1.92 bump

* Mon Nov 04 2019 Petr Pisar <ppisar@redhat.com> - 1.91-1
- 1.91 bump

* Thu Sep 26 2019 Petr Pisar <ppisar@redhat.com> - 1.89-1
- 1.89 bump

* Fri Sep 13 2019 Petr Pisar <ppisar@redhat.com> - 1.86-1
- 1.86 bump

* Mon Sep 02 2019 Petr Pisar <ppisar@redhat.com> - 1.85-1
- 1.85 bump

* Tue Aug 20 2019 Petr Pisar <ppisar@redhat.com> - 1.83-1
- 1.83 bump

* Mon Aug 19 2019 Petr Pisar <ppisar@redhat.com> - 1.79-1
- 1.79 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Petr Pisar <ppisar@redhat.com> - 1.78-1
- 1.78 bump

* Mon Jun 24 2019 Petr Pisar <ppisar@redhat.com> - 1.76-1
- 1.76 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-2
- Perl 5.30 rebuild

* Wed May 22 2019 Petr Pisar <ppisar@redhat.com> - 1.74-1
- 1.74 bump

* Tue May 21 2019 Petr Pisar <ppisar@redhat.com> - 1.73-1
- 1.73 bump

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 1.69-1
- 1.69 bump

* Tue Apr 23 2019 Petr Pisar <ppisar@redhat.com> - 1.68-1
- 1.68 bump

* Thu Apr 11 2019 Petr Pisar <ppisar@redhat.com> - 1.65-1
- 1.65 bump

* Tue Apr 09 2019 Petr Pisar <ppisar@redhat.com> - 1.63-1
- 1.63 bump

* Thu Mar 28 2019 Petr Pisar <ppisar@redhat.com> - 1.62-1
- 1.62 bump

* Wed Mar 13 2019 Petr Pisar <ppisar@redhat.com> - 1.60-2
- Use now-packaged FFI::Platypus

* Fri Mar 01 2019 Petr Pisar <ppisar@redhat.com> - 1.60-1
- 1.60 bump

* Mon Feb 25 2019 Petr Pisar <ppisar@redhat.com> - 1.55-1
- 1.55 bump

* Mon Feb 11 2019 Petr Pisar <ppisar@redhat.com> - 1.52-1
- 1.52 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Petr Pisar <ppisar@redhat.com> - 1.51-1
- 1.51 bump

* Fri Jan 18 2019 Petr Pisar <ppisar@redhat.com> - 1.50-1
- 1.50 bump

* Mon Nov 05 2018 Petr Pisar <ppisar@redhat.com> - 1.49-1
- 1.49 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 1.48-1
- 1.48 bump

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.46-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.46-2
- Perl 5.28 rebuild

* Mon Jun 25 2018 Petr Pisar <ppisar@redhat.com> - 1.46-1
- 1.46 bump

* Mon Jun 04 2018 Petr Pisar <ppisar@redhat.com> - 1.43-1
- 1.43 bump

* Thu May 10 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Tue Apr 24 2018 Petr Pisar <ppisar@redhat.com> - 1.41-1
- 1.41 bump

* Mon Mar 12 2018 Petr Pisar <ppisar@redhat.com> - 1.39-1
- 1.39 bump

* Mon Feb 26 2018 Petr Pisar <ppisar@redhat.com> - 1.37-1
- 1.37 bump

* Fri Feb 23 2018 Petr Pisar <ppisar@redhat.com> - 1.36-2
- Do not require C++ for build ing C tests (bug #923024)
- Build-require gcc because it is executed by tests via cmake (bug #923024)
- Run-requires gcc for Alien::Base::Wrapper::cc()

* Tue Feb 06 2018 Petr Pisar <ppisar@redhat.com> - 1.36-1
- 1.36 bump

* Mon Nov 06 2017 Petr Pisar <ppisar@redhat.com> - 1.32-1
- 1.32 bump

* Fri Nov 03 2017 Petr Pisar <ppisar@redhat.com> - 1.28-2
- Conflict with perl-Alien-Base-ModuleBuild < 1.00 because of
  Alien::Base::PkgConfig

* Fri Nov 03 2017 Petr Pisar <ppisar@redhat.com> - 1.28-1
- 1.28 bump

* Tue Sep 26 2017 Petr Pisar <ppisar@redhat.com> - 1.18-1
- 1.18 bump

* Tue Sep 19 2017 Petr Pisar <ppisar@redhat.com> - 1.16-1
- 1.16 bump

* Fri Sep 08 2017 Petr Pisar <ppisar@redhat.com> - 1.10-1
- 1.10 bump

* Tue Aug 29 2017 Petr Pisar <ppisar@redhat.com> - 1.05-1
- 1.05 bump

* Mon Aug 28 2017 Petr Pisar <ppisar@redhat.com> - 1.04-1
- 1.04 bump

* Fri Aug 18 2017 Petr Pisar <ppisar@redhat.com> - 0.99-1
- 0.99 bump

* Thu Aug 17 2017 Petr Pisar <ppisar@redhat.com> 0.95-1
- Specfile autogenerated by cpanspec 1.78.
