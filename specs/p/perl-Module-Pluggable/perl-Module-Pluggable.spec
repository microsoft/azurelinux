# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Module_Pluggable_enables_optional_test
%else
%bcond_with perl_Module_Pluggable_enables_optional_test
%endif

Name:           perl-Module-Pluggable
Epoch:          2
Version:        6.3
Release:        3%{?dist}
Summary:        Automatically give your module the ability to have plugins
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Pluggable
Source0:        https://cpan.metacpan.org/authors/id/S/SI/SIMONW/Module-Pluggable-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions) >= 3.00
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(if)
BuildRequires:  perl(vars)
BuildRequires:  perl(Scalar::Util)
# Recommended run-time:
BuildRequires:  perl(Module::Runtime) >= 0.012
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.62
# IncTest is a locally overloaded module in t/lib/Text/Abbrev.pm
%if %{with perl_Module_Pluggable_enables_optional_test}
# Optional tests:
BuildRequires:  perl(App::FatPacker) >= 0.10.0
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
%endif
Requires:       perl(File::Spec::Functions) >= 3.00
Requires:       perl(deprecate)
# Recommended run-time:
Recommends:     perl(Module::Runtime) >= 0.012

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec::Functions\\)$
# Remove private modules
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(No::Middle\\)$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
This package provides a simple but, hopefully, extensible way of having
'plugins' for your module. Essentially all it does is export a method into
your name space that looks through a search path for .pm files and turn those
into class names. Optionally it instantiates those classes for you.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(File::Spec::Functions) >= 3.00

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-Pluggable-%{version}
find -type f -exec chmod -x {} +
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Michal Josef Špaček <mspacek@redhat.com> - 2:6.3-1
- 6.3 bump (#2337044)

* Fri Oct 25 2024 Michal Josef Špaček <mspacek@redhat.com> - 2:6.2-2
- Add comment for previous patch
- Fix issue with root in tests

* Fri Oct 25 2024 Michal Josef Špaček <mspacek@redhat.com> - 2:6.2-1
- 6.2 bump (#2321226)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 2:5.2-24
- Fix required packages in *tests package

* Wed Dec 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 2:5.2-23
- Fix list of provided packages in *tests package

* Thu Dec 01 2022 Michal Josef Špaček <mspacek@redhat.com> - 2:5.2-22
- Package tests
- Simplify build and install phases
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:5.2-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Petr Pisar <ppisar@redhat.com> - 2:5.2-1
- 5.2 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.10-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.10-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.10-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 1:5.10-1
- 5.1 bump

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 1:5.00-1
- 5.0 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.80-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:4.80-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:4.8-2
- Perl 5.18 rebuild

* Tue May 28 2013 Petr Pisar <ppisar@redhat.com> - 1:4.8-1
- 4.8 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 1:4.7-1
- 4.7 bump

* Thu Jan 24 2013 Petr Pisar <ppisar@redhat.com> 1:4.6-1
- Specfile autogenerated by cpanspec 1.78.
