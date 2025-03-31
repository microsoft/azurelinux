# Run optional test
%{bcond_without perl_Alien_Build_enables_optional_test}
# Exhibit FFI::Platypus in Test::Alien
%if !%{defined perl_bootstrap}
# Build cycle: perl-FFI-Platypus → perl-Alien-Build
%{bcond_without perl_Alien_Build_enables_platypus}
%endif

Name:           perl-Alien-Build
Version:        2.84
Release:        1%{?dist}
Summary:        Build external dependencies for use in CPAN
# lib/Alien/Build/Plugin/Test/Mock.pm contains Base64-encoded files for tests
# (a bash script, C source file, a gzipped tar archive, Mach-O 64-bit x86_64
# object file and a static library).
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Alien-Build
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-Build-%{version}.tar.gz
# Support only the most advanced pkgconfig implementation,
# the files are deleted in prep section
Patch0:         Alien-Build-2.83-Remove-redundant-pkgconfig-implementations.patch
# Support only the most common SHA implementation,
# the files are deleted in prep section
Patch1:         Alien-Build-2.65-Remove-redundant-SHA-implementations.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
# Makefile.PL executes ./inc/probebad.pl that executes XS checks
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.4
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
BuildRequires:  perl(Capture::Tiny) >= 0.17
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config::INI::Reader::Multiline)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::SHA)
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
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
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
BuildRequires:  perl(File::Glob)
# Getopt::Long not used
# IO::Socket::INET not used
# HTTP::Server::PSGI not used
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Net::FTP)
# Plack::App::Directory not used
# Plack::Builder not used
# Proc::Daemon not used
BuildRequires:  perl(Test2::V0) >= 0.000121
# URI not used
# URI::Escape not used
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
# (HTTP::Tiny and Mozilla::CA) or curl
BuildRequires:  perl(HTTP::Tiny) >= 0.044
# Prefer Mojo::DOM with Mojolicious, URI, URI::Escape over Mojo::DOM58
BuildRequires:  perl(Mojo::DOM)
BuildRequires:  perl(Mojolicious) >= 7.00
# (HTTP::Tiny and Mozilla::CA) or curl
# Mozilla::CA not used
# PkgConfig not packaged
BuildRequires:  perl(Readonly) >= 1.60
BuildRequires:  perl(Sort::Versions)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(URI::file)
%endif
# Alien::Build::Plugin::Build::Copy executes cp
Requires:       coreutils
# Alien::Base::Wrapper::cc() executes $Config{cc}.
Requires:       gcc
# make in the lib/Alien/Build/Plugin/Build/CMake.pm plugin
# make in the lib/Alien/Build/Plugin/Build/Make.pm plugin
# make or Alien::gmake
Requires:       make
# A subset of Alien-Build modules is packaged in perl-Alien-Base to minimize
# dependencies.
Requires:       perl-Alien-Base = %{?epoch:%{epoch}:}%{version}-%{release}
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
Requires:       perl(ExtUtils::CBuilder)
Requires:       perl(ExtUtils::MakeMaker) >= 6.52
Requires:       perl(ExtUtils::ParseXS) >= 3.30
%if %{with perl_Alien_Build_enables_platypus}
Recommends:     perl(FFI::Platypus) >= 0.12
%endif
Requires:       perl(Capture::Tiny) >= 0.17
Requires:       perl(File::BOM)
Requires:       perl(File::Find)
# (HTTP::Tiny and Mozilla::CA) or curl for Alien::Build::Plugin::Download::Negotiate
Requires:       perl(HTTP::Tiny) >= 0.044
# (HTTP::Tiny and Mozilla::CA) or curl for Alien::Build::Plugin::Download::Negotiate
Requires:       perl(Mozilla::CA)
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
Recommends:     perl(YAML)
# Test-Alien merged into Alien-Build
Obsoletes:      perl-Test-Alien < 0.15-13
Provides:       perl-Test-Alien = %{version}-%{release}

# Do not gather dependencies from the documentation
%{?perl_default_filter}

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Capture::Tiny|Path::Tiny|Test2::API|Test2::V0|Text::ParseWords)\\)$
# Remove private redefinitions
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(Alien::Build::rc\\)$
# Remove private modules
%global __provides_exclude %{__provides_exclude}|^perl\\(Alien::Build::Plugin::(Download::Foo|Fetch::Corpus|Fetch::Foo|NesAdvantage::Controller|NesAdvantage::HelperTest|NesAdvantage::Negotiate|RogerRamjet)|Alien::Foo|Alien::Foo1|Alien::Foo1::ConfigData|Alien::Foo2|Alien::Foo2::ConfigData|Alien::foomake|Alien::libfoo1|Alien::libfoo2|Alien::libfoo3|Alien::perlhelp|Alien::SansShare|Foo::Bar::Baz|Foo::Bar::Baz1|MyTest::.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Alien::Build::Plugin::RogerRamjet|Alien::Foo|Alien::libfoo1|Alien::libfoo2|Alien::perlhelp|MyTest::.*\\)$

# Some tests, e.g. t/alien_build_plugin_extract_negotiate.t, compare a script file
# content against an archived one. Do not rewrite their shebangs.
%global __brp_mangle_shebangs_exclude_from %{?__brp_mangle_shebangs_exclude_from:%{__brp_mangle_shebangs_exclude_from}|}^%{_libexecdir}/%{name}/corpus/dist/foo-1\.00/configure$

%description
This package provides tools for building external (non-CPAN) dependencies
for CPAN. It is mainly designed to be used at install time of a CPAN
client, and work closely with Alien::Base which is used at run time.

%package -n perl-Alien-Base
Summary:        Base classes for Alien:: modules
Requires:       perl(DynaLoader)
Requires:       perl(FFI::CheckLib)
Requires:       perl(File::Find)
Requires:       perl(JSON::PP)
Requires:       perl(Path::Tiny) >= 0.077
Requires:       perl(Storable)
Requires:       perl(Text::ParseWords) >= 3.26
# pkgconf-pkg-config for pkg-config tool executed by
# Alien::Base::PkgConfig::pkg_config_command()
Requires:       pkgconf-pkg-config
# Alien::Base::PkgConfig moved from perl-Alien-Base-ModuleBuild
Conflicts:      perl-Alien-Base-ModuleBuild < 1.00
# Subpackaged from perl-Alien-Build-2.47-1
Conflicts:      perl-Alien-Build < 2.47-2

%description -n perl-Alien-Base
Alien::Base comprises base classes to help in the construction of
"Alien::" modules.

%package Plugin-Decode-HTML
Summary:        Alien::Build plugin to extract links from HTML
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
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
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
# Prefer Mojo::DOM with Mojolicious >= 7.00 over Mojo::DOM58 that is not yet
# packaged.
Requires:       perl(Mojo::DOM)
Requires:       perl(Mojolicious) >= 7.00
Requires:       perl(URI)
Requires:       perl(URI::Escape)

%description Plugin-Decode-Mojo
This Alien::Build plugin decodes an HTML file listing into a list of
candidates for your Prefer plugin.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness
Requires:       perl(Net::FTP)
Requires:       perl(Test2::V0) >= 0.000121
%if %{with perl_Alien_Build_enables_optional_test}
%if !%{defined perl_bootstrap}
# Break build cycle: Acme::Alien::DontPanic → Test::Alien
Requires:       perl(Acme::Alien::DontPanic) >= 0.026
# Break build cycle: perl-Alien-Base-ModuleBuild → perl-Alien-Build
Requires:       perl(Alien::Base::ModuleBuild) >= 0.040
%endif
Requires:       perl(Devel::Hide)
Requires:       perl(Env::ShellWords)
# FFI::Platypus not packaged
# (HTTP::Tiny and Mozilla::CA) or curl
Requires:       perl(HTTP::Tiny) >= 0.044
# Prefer Mojo::DOM with Mojolicious, URI, URI::Escape over Mojo::DOM58
Requires:       perl(Mojo::DOM)
Requires:       perl(Mojolicious) >= 7.00
# (HTTP::Tiny and Mozilla::CA) or curl
# Mozilla::CA not used
# PkgConfig not packaged
Requires:       perl(Readonly) >= 1.60
Requires:       perl(Sort::Versions)
Requires:       perl(URI::file)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Alien-Build-%{version}
# Remove redundant pkgconfig implementations, keep
# Alien::Build::Plugin::PkgConfig::LibPkgConf,
# MANIFEST is updated by Remove-redundant-pkgconfig-implementations.patch.
%patch -p1 -P 0
rm lib/Alien/Build/Plugin/PkgConfig/{CommandLine,PP}.pm 
rm t/alien_build_plugin_pkgconfig_{commandline,makestatic,pp}.t
# Remove redundant SHA digest imlementations, keep
# Alien::Build::Plugin::Digest::SHA, MANIFEST is updated by
# Alien-Build-2.59-Remove-redundant-SHA-implementations.patch.
%patch -p1 -P 1
rm lib/Alien/Build/Plugin/Digest/SHAPP.pm
rm t/alien_build_plugin_digest_shapp.t
# Remove unused tests
for F in \
    t/alien_build_plugin_probe_vcpkg.t \
    t/bin/ftpd \
    t/bin/httpd \
%if !%{with perl_Alien_Build_enables_optional_test} || %{defined perl_bootstrap}
    t/alien_base__system_installed.t \
%endif
%if !%{with perl_Alien_Build_enables_optional_test}
    t/alien_build_plugin_build_searchdep.t \
    t/alien_build_plugin_extract_commandline__tar_can.t \
    t/alien_build_plugin_prefer_badversion.t \
    t/alien_build_plugin_prefer_goodversion.t \
%endif
; do
    rm "$F"
    perl -i -ne 'print $_ unless m{\A\Q'"$F"'\E\b}' MANIFEST
    perl -i -ne 'print $_ unless m{\b\Q'"$F"'\E\b}' t/01_use.t
done
# Symlink identical files
function symlink_duplicates {
    local KEEP="$1"
    local DUPLICATE_GLOB="$2"
    local F
    shopt -s globstar
    for F in $DUPLICATE_GLOB; do
        test "$KEEP" = "$F" && continue
        cmp "$KEEP" "$F" || continue
        rm "$F"
        ln -s "$(realpath --relative-to $(dirname $F) $KEEP)" "$F"
    done
}
symlink_duplicates 'corpus/alien_build_plugin_fetch_curlcommand/dir/foo-1.00.tar' 'corpus/*/dir/foo-1.00.tar'
symlink_duplicates 'corpus/alien_build_plugin_fetch_curlcommand/dir/foo-1.01.tar' 'corpus/*/dir/foo-1.01.tar'
symlink_duplicates 'corpus/alien_build_plugin_fetch_curlcommand/dir/foo-1.02.tar' 'corpus/*/dir/foo-1.02.tar'
symlink_duplicates 'corpus/alien_build_plugin_fetch_curlcommand/dir/html_test.html' 'corpus/*/dir/html_test.html'
symlink_duplicates 'example/user/ffi-platypus/t/lzma_example.t' 'example/user/*/t/lzma_example.t'
symlink_duplicates 'example/user/xs-dzil/Example.xs' 'example/**/Example.xs'
symlink_duplicates 'example/user/xs-dzil/lib/LZMA/Example.pm' 'example/**/Example.pm'
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset PKG_CONFIG
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a corpus t %{buildroot}%{_libexecdir}/%{name}
# t/alienfile.t uses example/*.alienfile
mkdir %{buildroot}%{_libexecdir}/%{name}/example
cp -a example/*.alienfile %{buildroot}%{_libexecdir}/%{name}/example
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Many tests, e.g. t/alien_build_commandsequence.t, write into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
unset ACLOCAL_PATH ALIEN_BASE_WRAPPER_QUIET ALIEN_BUILD_LIVE_TEST \
    ALIEN_BUILD_LOG ALIEN_BUILD_PKG_CONFIG ALIEN_BUILD_POSTLOAD \
    ALIEN_BUILD_PRELOAD ALIEN_BUILD_RC ALIEN_BUILD_SITE_CONFIG \
    ALIEN_CPU_COUNT ALIEN_DOWNLOAD_RULE ALIEN_FORCE \
    ALIEN_INSTALL_NETWORK ALIEN_INSTALL_TYPE CONFIG_SITE CURL DESTDIR \
    FOO1 FOO2 FOO3 TEST_ALIEN_ALIENS_MISSING TEST_ALIEN_ALWAYS_KEEP VERBOSE WGET
export CIPSOMETHING=true
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset ACLOCAL_PATH ALIEN_BASE_WRAPPER_QUIET ALIEN_BUILD_LIVE_TEST \
    ALIEN_BUILD_LOG ALIEN_BUILD_PKG_CONFIG ALIEN_BUILD_POSTLOAD \
    ALIEN_BUILD_PRELOAD ALIEN_BUILD_RC ALIEN_BUILD_SITE_CONFIG \
    ALIEN_CPU_COUNT ALIEN_DOWNLOAD_RULE ALIEN_FORCE \
    ALIEN_INSTALL_NETWORK ALIEN_INSTALL_TYPE CONFIG_SITE CURL DESTDIR \
    FOO1 FOO2 FOO3 TEST_ALIEN_ALIENS_MISSING TEST_ALIEN_ALWAYS_KEEP VERBOSE WGET
export CIPSOMETHING=true
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes.Alien-Base-Wrapper Changes.Test-Alien
%doc example
%{perl_vendorlib}/Alien/Base/Authoring.pod
%{perl_vendorlib}/Alien/Base/FAQ.pod
%{perl_vendorlib}/Alien/Base/Wrapper.pm
%{perl_vendorlib}/Alien/Build.pm
%{perl_vendorlib}/Alien/Build
%exclude %{perl_vendorlib}/Alien/Build/Plugin/Decode/HTML.pm
%exclude %{perl_vendorlib}/Alien/Build/Plugin/Decode/Mojo.pm
%{perl_vendorlib}/Alien/Role.pm
%{perl_vendorlib}/alienfile.pm
%dir %{perl_vendorlib}/Test
%{perl_vendorlib}/Test/Alien
%{perl_vendorlib}/Test/Alien.pm
%{_mandir}/man3/Alien::Base::Authoring.*
%{_mandir}/man3/Alien::Base::FAQ.*
%{_mandir}/man3/Alien::Base::Wrapper.*
%{_mandir}/man3/Alien::Build.*
%{_mandir}/man3/Alien::Build::*
%exclude %{_mandir}/man3/Alien::Build::Plugin::Decode::HTML.3pm.*
%exclude %{_mandir}/man3/Alien::Build::Plugin::Decode::Mojo.3pm.*
%{_mandir}/man3/Alien::Role.*
%{_mandir}/man3/alienfile.*
%{_mandir}/man3/Test::Alien.*
%{_mandir}/man3/Test::Alien::*

%files -n perl-Alien-Base
%license LICENSE
%doc Changes Changes.Alien-Base
%doc README SUPPORT
%dir %{perl_vendorlib}/Alien
%{perl_vendorlib}/Alien/Base.pm
%dir %{perl_vendorlib}/Alien/Base
%{perl_vendorlib}/Alien/Base/PkgConfig.pm
%{perl_vendorlib}/Alien/Util.pm
%{_mandir}/man3/Alien::Base.3pm.*
%{_mandir}/man3/Alien::Base::PkgConfig.3pm.*
%{_mandir}/man3/Alien::Util.3pm.*

%files Plugin-Decode-HTML
%{perl_vendorlib}/Alien/Build/Plugin/Decode/HTML.pm
%{_mandir}/man3/Alien::Build::Plugin::Decode::HTML.3pm.*

%files Plugin-Decode-Mojo
%doc Changes.Alien-Build-Decode-Mojo
%{perl_vendorlib}/Alien/Build/Plugin/Decode/Mojo.pm
%{_mandir}/man3/Alien::Build::Plugin::Decode::Mojo.3pm.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Oct 29 2024 Petr Pisar <ppisar@redhat.com> - 2.84-1
- 2.84 bump

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 06 2024 Petr Pisar <ppisar@redhat.com> - 2.83-1
- 2.83 bump
- Remove more always skipped tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Petr Pisar <ppisar@redhat.com> - 2.80-1
- 2.80 bump

* Thu May 11 2023 Petr Pisar <ppisar@redhat.com> - 2.79-1
- 2.79 bump

* Wed Mar 08 2023 Petr Pisar <ppisar@redhat.com> - 2.78-1
- 2.78 bump

* Fri Jan 20 2023 Petr Pisar <ppisar@redhat.com> - 2.77-1
- 2.77 bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Petr Pisar <ppisar@redhat.com> - 2.76-1
- 2.76 bump

* Wed Dec 07 2022 Petr Pisar <ppisar@redhat.com> - 2.74-2
- Remove private provides from tests

* Wed Nov 30 2022 Petr Pisar <ppisar@redhat.com> - 2.74-1
- 2.74 bump

* Sun Nov 27 2022 Florian Weimer <fweimer@redhat.com> - 2.73-2
- Avoid triggering C99 implit int/function declaration errors

* Mon Nov 21 2022 Petr Pisar <ppisar@redhat.com> - 2.73-1
- 2.73 bump

* Thu Oct 27 2022 Petr Pisar <ppisar@redhat.com> - 2.72-1
- 2.72 bump

* Wed Oct 05 2022 Petr Pisar <ppisar@redhat.com> - 2.71-1
- 2.71 bump

* Mon Sep 26 2022 Petr Pisar <ppisar@redhat.com> - 2.70-1
- 2.70 bump

* Tue Sep 06 2022 Petr Pisar <ppisar@redhat.com> - 2.68-1
- 2.68 bump

* Mon Sep 05 2022 Petr Pisar <ppisar@redhat.com> - 2.67-1
- 2.67 bump

* Wed Aug 31 2022 Petr Pisar <ppisar@redhat.com> - 2.65-1
- 2.65 bump

* Tue Aug 16 2022 Petr Pisar <ppisar@redhat.com> - 2.59-1
- 2.59 bump

* Thu Aug 04 2022 Petr Pisar <ppisar@redhat.com> - 2.51-1
- 2.51 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Petr Pisar <ppisar@redhat.com> - 2.50-1
- 2.50 bump

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.48-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.48-2
- Perl 5.36 rebuild

* Tue Mar 15 2022 Petr Pisar <ppisar@redhat.com> - 2.48-1
- 2.48 bump

* Fri Mar 11 2022 Petr Pisar <ppisar@redhat.com> - 2.47-2
- Move Alien::Base and Alien::Base::PkgConfig to perl-Alien-Base (bug #2063125)

* Mon Mar 07 2022 Petr Pisar <ppisar@redhat.com> - 2.47-1
- 2.47 bump

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-1
- 2.46 bump

* Fri Oct 29 2021 Petr Pisar <ppisar@redhat.com> - 2.45-1
- 2.45 bump

* Thu Oct 21 2021 Petr Pisar <ppisar@redhat.com> - 2.44-1
- 2.44 bump

* Thu Sep 30 2021 Petr Pisar <ppisar@redhat.com> - 2.42-1
- 2.42 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Petr Pisar <ppisar@redhat.com> - 2.41-1
- 2.41 bump

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.40-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.40-2
- Perl 5.34 rebuild

* Thu May 13 2021 Petr Pisar <ppisar@redhat.com> - 2.40-1
- 2.40 bump
- Package the tests

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Petr Pisar <ppisar@redhat.com> - 2.38-2
- Test-Alien merged into Alien-Build

* Tue Jan 12 2021 Petr Pisar <ppisar@redhat.com> - 2.38-1
- 2.38 bump

* Tue Nov 03 2020 Petr Pisar <ppisar@redhat.com> - 2.37-1
- 2.37 bump

* Mon Sep 21 2020 Petr Pisar <ppisar@redhat.com> - 2.33-1
- 2.33 bump

* Mon Sep 14 2020 Petr Pisar <ppisar@redhat.com> - 2.32-1
- 2.32 bump

* Tue Aug 11 2020 Petr Pisar <ppisar@redhat.com> - 2.29-1
- 2.29 bump

* Wed Aug 05 2020 Petr Pisar <ppisar@redhat.com> - 2.28-1
- 2.28 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-2
- Perl 5.32 rebuild

* Wed Jun 17 2020 Petr Pisar <ppisar@redhat.com> - 2.26-1
- 2.26 bump

* Mon May 18 2020 Petr Pisar <ppisar@redhat.com> - 2.23-1
- 2.23 bump

* Wed May 06 2020 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Tue Apr 14 2020 Petr Pisar <ppisar@redhat.com> - 2.21-1
- 2.21 bump

* Thu Apr 09 2020 Petr Pisar <ppisar@redhat.com> - 2.19-1
- 2.19 bump

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
