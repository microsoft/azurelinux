# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cpan_version_major 0.42
%global cpan_version_minor 34
%global cpan_version %{cpan_version_major}%{?cpan_version_minor}

# Run optional tests
%if ! (0%{?rhel})
%bcond_without perl_Module_Build_enables_optional_test
%else
%bcond_with perl_Module_Build_enables_optional_test
%endif

Name:           perl-Module-Build
Epoch:          2
Version:        %{cpan_version_major}%{?cpan_version_minor:.%cpan_version_minor}
Release: 10%{?dist}
Summary:        Build and install Perl modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Build
Source0:        https://cpan.metacpan.org/modules/by-module/Module/Module-Build-%{cpan_version}.tar.gz
# Handle missing ExtUtils::CBuilder as a missing compiler, bug #1547165.
Patch1:         Module-Build-0.4231-Do-not-die-on-missing-ExtUtils-CBuilder-in-have_c_co.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(blib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta) >= 2.142060
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.141170
BuildRequires:  perl(CPAN::Meta::Merge)
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.003
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:  perl(ExtUtils::Install) >= 0.3
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(ExtUtils::Mkbootstrap)
BuildRequires:  perl(ExtUtils::Packlist)
BuildRequires:  perl(ExtUtils::ParseXS) >= 2.21
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.15
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(inc::latest)
BuildRequires:  perl(lib)
# perl(Module::Build) is loaded from ./lib
BuildRequires:  perl(Module::Metadata) >= 1.000002
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4401
BuildRequires:  perl(Perl::OSType) >= 1
BuildRequires:  perl(strict)
# Optional tests:
%if !%{defined perl_bootstrap}
%if %{with perl_Module_Build_enables_optional_test}
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(File::ShareDir) >= 1.00
BuildRequires:  perl(PAR::Dist)
%if 0%{?fedora}  || 0%{?rhel} < 7
BuildRequires:  perl(Pod::Readme)
%endif
%endif
%endif
BuildRequires:  perl(TAP::Harness)
BuildRequires:  perl(TAP::Harness::Env)
BuildRequires:  perl(Test::Harness) >= 3.29
BuildRequires:  perl(Test::More) >= 0.49
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.87
BuildRequires:  perl(warnings)
Requires:       perl(CPAN::Meta) >= 2.142060
Requires:       perl(CPAN::Meta::Converter) >= 2.141170
Requires:       perl(CPAN::Meta::Merge)
# Do not hard-require ExtUtils::CBuilder to allow installing Module::Build
# without gcc, bug #1547165. Module::Build users have to require
# ExtUtils::CBuilder explicitly according to "XS Extensions" section in
# Module::Build::Authoring POD.
Recommends:     perl(ExtUtils::CBuilder) >= 0.27
Requires:       perl(ExtUtils::Install) >= 0.3
Requires:       perl(ExtUtils::Manifest) >= 1.54
Requires:       perl(ExtUtils::Mkbootstrap)
Requires:       perl(ExtUtils::ParseXS) >= 2.21
Requires:       perl(inc::latest)
Requires:       perl(Module::Metadata) >= 1.000002
# Keep PAR support optional (PAR::Dist)
Requires:       perl(Perl::OSType) >= 1
Requires:       perl(TAP::Harness::Env)
Requires:       perl(Test::Harness)
%if !%{defined perl_bootstrap}
# Optional run-time needed for Software::License license identifier,
# bug #1152319
Requires:       perl(Software::License)
%endif
# Optional run-time needed for generating documentation from POD:
Requires:       perl(Pod::Html)
Requires:       perl(Pod::Man) >= 2.17
Requires:       perl(Pod::Text)
# Run-time for generated Build scripts from Build.PLs:
# Those are already found by dependency generator. Just make sure they
# present.
# Cwd
# File::Basename
# File::Spec
# strict

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(DistGen\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(MBTest\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Simple\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Software::License.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Tie::CPHash\\)

%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.
Developers may alter the behavior of the module through sub-classing in a
much more straightforward way than with MakeMaker. It also does not require
a make on your system - most of the Module::Build code is pure-perl and
written in a very cross-platform way. In fact, you don't even need a shell,
so even platforms like MacOS (traditional) can use it fairly easily. Its
only prerequisites are modules that are included with perl 5.6.0, and it
works fine on perl 5.005 if you can install a few additional modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# Optional tests:
%if !%{defined perl_bootstrap}
%if %{with perl_Module_Build_enables_optional_test}
Requires:       perl(Archive::Zip)
Requires:       perl(File::ShareDir) >= 1.00
Requires:       perl(PAR::Dist)
%endif
%endif
Requires:       perl(TAP::Harness)
Requires:       perl(TAP::Harness::Env)
Requires:       perl(Text::ParseWords)
Requires:       perl(version) >= 0.87

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Module-Build-%{cpan_version}

# Help generators to recognize Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t _build %{buildroot}%{_libexecdir}/%{name}
perl -pi -e 's#%{buildroot}##' %{buildroot}%{_libexecdir}/%{name}/_build/runtime_params
rm %{buildroot}%{_libexecdir}/%{name}/_build/magicnum
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
ln -s %{_bindir}/config_data %{buildroot}%{_libexecdir}/%{name}/bin
# Requires copy of modules in test directory
rm %{buildroot}%{_libexecdir}/%{name}/t/00-compile.t
# Remove using of blib
for F in `find %{buildroot}%{_libexecdir}/%{name}/t -name *.t -o -name *.pm`; do
    perl -pi -e "s/^\s*blib_load\('([^']+)'\);/use \1;/" $F
    perl -pi -e "s/^blib_load '([^']+)';/use \1;/" $F
done
perl -pi -e "s{'-Mblib', }{'-I'.\\N{U+0024}tmp.'/Simple/blib/lib', '-I'.\\N{U+0024}tmp.'/Simple/blib/arch', }x" \
    %{buildroot}%{_libexecdir}/%{name}/t/xs.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test

%files
%license LICENSE
%doc Changes contrib/ README
%{_bindir}/config_data
%{perl_vendorlib}/Module/
%{_mandir}/man1/config_data.1*
%{_mandir}/man3/Module::Build*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 11 2024 Petr Pisar <ppisar@redhat.com> - 2:0.42.34-6
- Make perl-Module-Build-tests reproducible

* Wed Feb 14 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.34-5
- Package tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 28 2023 Paul Howarth <paul@city-fan.org> - 2:0.42.34-1
- 0.4234 bump
- Use author-independent source URL
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Jitka Plesnikova <jplesnik@redhat.com> -2:0.42.32-1
- 0.4232 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.31-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-14
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-13
- Perl 5.36 rebuild

* Mon Mar 28 2022 Petr Pisar <ppisar@redhat.com> - 2:0.42.31-12
- Handle missing ExtUtils::CBuilder as a missing compiler (bug #1547165)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.31-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.31-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-9
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-6
- Disable optional tests on RHEL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-4
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-3
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 2:0.42.31-2
- BR: perl(blib), needed for t/xs.t

* Wed Jan 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.31-1
- 0.4231 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.29-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.29-2
- Perl 5.30 rebuild

* Tue Apr 16 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.29-1
- 0.4229 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.24-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.24-9
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.24-8
- Perl 5.28 rebuild

* Thu Mar 01 2018 Petr Pisar <ppisar@redhat.com> - 2:0.42.24-7
- Do not require a compiler if c_source is an empty list (bug #1547165)

* Fri Feb 23 2018 Petr Pisar <ppisar@redhat.com> - 2:0.42.24-6
- Do not hard-require ExtUtils::CBuilder (bug #1547165)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.24-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.24-2
- Perl 5.26 rebuild

* Wed May 31 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.24-1
- 0.4224 bump

* Fri Mar 31 2017 Petr Pisar <ppisar@redhat.com> - 2:0.42.22-1
- 0.4222 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.20-1
- 0.4220 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.18-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.18-2
- Perl 5.24 rebuild

* Tue Apr 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.18-1
- 0.4218 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.42.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.16-1
- 0.4216 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.42.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.14-1
- 0.4214 bump

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.12-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.12-2
- Perl 5.22 rebuild

* Mon May 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.12-1
- 0.4212 bump

* Fri Jan 30 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.11-1
- 0.4211 bump

* Fri Jan 30 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.10-4
- Sub-package perl-inc-latest

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 2:0.42.10-3
- Disable File::ShareDir optional tests when bootstrapping

* Wed Oct 15 2014 Petr Pisar <ppisar@redhat.com> - 2:0.42.10-2
- Require Software::License to recognize more license identifiers (bug #1152319)

* Wed Sep 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.10-1
- 0.4210 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.08-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.08-2
- Perl 5.20 rebuild

* Tue Aug 19 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.42.08-1
- 0.4208 bump

* Wed Jul 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.42.06-1
- 0.4206 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.42.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.05-1
- 0.4205 bump

* Wed Jan 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.04-1
- 0.4204 bump

* Thu Nov 28 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.03-1
- 0.4203 bump

* Mon Nov 25 2013 Petr Pisar <ppisar@redhat.com> - 2:0.42.02-1
- 0.4202 bump

* Tue Nov 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.42.01-1
- 0.4201 bump

* Tue Nov 05 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.40.08-1
- 0.4008 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.40.07-3
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.40.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.40.05-1
- 0.4007 bump

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2:0.40.05-2
- Perl 5.18 rebuild

* Mon Apr 29 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:0.40.05-1
- 0.4005 bump

* Wed Apr 03 2013 Petr Šabata <contyk@redhat.com> - 2:0.40.04-1
- 0.4004 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-5
- Run-require POD convertors to get manual pages when building other packages

* Mon Dec 10 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-4
- YAML::Tiny is not needed at build time (bug #885146)

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 2:0.40.03-3
- Add a few missing deps
- Drop command macros

* Mon Sep 03 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-2
- Do not build-require Module::Build (bug #849328)

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-1
- 0.4003 bump

* Mon Jul 30 2012 Jitka Plesnikova <jplesnik@redhat.com>  2:0.40.02-1
- 0.4002 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.40.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-2
- Perl 5.16 rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-1
- 0.4001 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-3
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-2
- Do not run PAR tests on bootstrap

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-1
- 0.40 bump
- All reverse dependecies must require use 2-digit Module::Build version now

* Wed May 30 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-5
- conditionalize some test

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3800-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-3
- BR on perl-devel because this package contains macros used by rpmbuild
  for Perl packages

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-2
- rebuild with Perl 5.14.1, remove defatter

* Wed Mar 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-1
- update to 0.3800

* Wed Mar 02 2011 Petr Pisar <ppisar@redhat.com> - 1:0.3624-2
- Raise epoch to  Core level
- Remove BuildRoot stuff

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.3624-1
- update to new version
- fix BR, R

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3607-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-3
- switch off experimental test

* Tue Jun  8 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-2
- copy check part&upload key from Paul Howarth
- fix macro

* Mon May 31 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-1
- add BR, update, switch on some other tests

* Tue Mar 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3603-1
- Specfile autogenerated by cpanspec 1.78.
