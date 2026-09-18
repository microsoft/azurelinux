# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Module-Install-TestBase
Version:        0.86
Release:        36%{?dist}
Summary:        Module::Install support for Test::Base
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Install-TestBase
Source0:        https://cpan.metacpan.org/authors/id/I/IN/INGY/Module-Install-TestBase-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
# Filter::Util::Call not used at tests
# The Module::Install::Base version constrain is phony, bug #1134351,
# <https://github.com/ingydotnet/module-install-testbase-pm/issues/2>
BuildRequires:  perl(Module::Install::Base)
# Spiffy not used at tests
# Test::Base 0.86 not used at tests
# Test::Base::Filter not used at tests
# Test::Builder not used at tests
# Test::Builder::Module not used at tests
# Test::More not used at tests
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Test::More)
# Test::Pod not used
Requires:   perl(Filter::Util::Call)
Requires:   perl(Spiffy)
Requires:   perl(Test::Base) >= 0.86
Requires:   perl(Test::Base::Filter)
Requires:   perl(Test::Builder)
Requires:   perl(Test::Builder::Module)
Requires:   perl(Test::More)
# Module::Install::TestBase splitted from Test-Base in 0.85
Conflicts:  perl-Test-Base < 0.85

%description
This Perl module adds the use_test_base directive to Module::Install. Now you
can get full Test-Base support for you module with no external dependency on
Test::Base.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-Install-TestBase-%{version}
# Remove release tests
rm t/release-pod-syntax.t
perl -i -ne 'print $_ unless m{^t/release-pod-syntax.t}' MANIFEST

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
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_libexecdir}/%{name}/lib/Module/Install
# t/000-compile-modules.t inspect ./lib, but rpmbuild follows symlinks
# and that would place identical Provides to main and tests subpackage.
# Fortunatelly the test only needs a file name. Hence create an empty file.
# Bug #2063919.
touch %{buildroot}%{_libexecdir}/%{name}/lib/Module/Install/TestBase.pm
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%dir %{perl_vendorlib}/Module
%dir %{perl_vendorlib}/Module/Install
%{perl_vendorlib}/Module/Install/TestBase.*
%{_mandir}/man3/Module::Install::TestBase.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 22 2024 Petr Pisar <ppisar@redhat.com> - 0.86-34
- Modernize a spec file

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 0.86-33
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-26
- Perl 5.36 rebuild

* Mon Mar 14 2022 Petr Pisar <ppisar@redhat.com> - 0.86-25
- Do not provide perl(Module::Install::TestBase) by a tests package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Petr Pisar <ppisar@redhat.com> - 0.86-23
- Modernize a spec file
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-21
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-18
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-3
- Perl 5.20 rebuild

* Thu Aug 28 2014 Petr Pisar <ppisar@redhat.com> - 0.86-2
- Do not require exact version of Module::Install::Base (bug #1134351)

* Wed Aug 27 2014 Petr Pisar <ppisar@redhat.com> 0.86-1
- Specfile autogenerated by cpanspec 1.78.
