# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 0.280236

Name:           perl-ExtUtils-CBuilder
# Compete with perl.spec
Epoch:          1
# Mimic perl.spec
Version:        0.280242
Release:        520%{?dist}
Summary:        Compile and link C code for Perl modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/ExtUtils-CBuilder
Source0:        https://cpan.metacpan.org/authors/id/A/AM/AMBS/ExtUtils-CBuilder-%{base_version}.tar.gz
# Link XS modules to libperl.so with EU::CBuilder on Linux, bug #960048
Patch0:         ExtUtils-CBuilder-0.280230-Link-XS-modules-to-libperl.so-with-EU-CBuilder-on-Li.patch
# Unbundled from perl 5.37.11
Patch1:         ExtUtils-CBuilder-0.280236-Upgrade-to-0.280238.patch
# Unbundled from perl 5.40.0-RC1
Patch2:         ExtUtils-CBuilder-0.280238-Upgrade-to-0.280240.patch
# Unbundled from perl 5.42.0
Patch3:         ExtUtils-CBuilder-0.280240-Upgrade-to-0.280242.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl-devel
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(DynaLoader)
# ExtUtils::Mksymlists 6.30 not used at test time
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 3.13
# File::Spec::Functions not used at test time
BuildRequires:  perl(File::Temp)
# IO::File not used at test time
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Perl::OSType) >= 1
BuildRequires:  perl(Text::ParseWords)
# Optional run-time:
# C and C++ compilers are highly recommended because compiling code is the
# purpose of ExtUtils::CBuilder, bug #1547165
BuildRequires:  gcc
BuildRequires:  gcc-c++
# Tests:
BuildRequires:  perl(Test::More) >= 0.47
# vmsish not used
# C and C++ compilers are highly recommended because compiling code is the
# purpose of ExtUtils::CBuilder, bug #1547165
Requires:       gcc
Requires:       gcc-c++
Requires:       perl-devel
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Mksymlists) >= 6.30
Requires:       perl(File::Spec) >= 3.13
Requires:       perl(Perl::OSType) >= 1

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec|Perl::OSType)\\)$

%description
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n ExtUtils-CBuilder-%{base_version}

# Normalize shebangs
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Tests write into temporary files/directories. The solution is to copy the
# tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README README.mkdn
%dir %{perl_vendorlib}/ExtUtils
%{perl_vendorlib}/ExtUtils/CBuilder*
%{_mandir}/man3/ExtUtils::CBuilder*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280242-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280242-519
- Upgrade to 0.280242 as provided in 5.42.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280240-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280240-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280240-510
- Increase release to favour standalone package

* Thu May 09 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280240-503
- Upgrade to 0.280240 as provided in 5.40.0-RC1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280238-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280238-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280238-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280238-499
- Increase release to favour standalone package

* Tue May 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280238-1
- Upgrade to 0.280238 as provided in perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280236-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280236-490
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280236-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280236-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280236-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280236-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280236-477
- Increase release to favour standalone package

* Tue Feb 16 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280236-2
- Package tests

* Mon Feb 15 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280236-1
- 0.280236 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280235-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280235-1
- 0.280235 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280234-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280234-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280234-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Petr Pisar <ppisar@redhat.com> - 1:0.280234-1
- 0.280234 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280231-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280231-438
- Increase release to favour standalone package

* Wed Apr 03 2019 Petr Pisar <ppisar@redhat.com> - 1:0.280231-1
- 0.280231 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280230-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280230-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280230-416
- Increase release to favour standalone package

* Fri Feb 23 2018 Petr Pisar <ppisar@redhat.com> - 1:0.280230-3
- Add a dependency on gcc and gcc-c++ (bug #1547165)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280230-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 23 2017 Petr Pisar <ppisar@redhat.com> - 1:0.280230-1
- 0.280230 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280226-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Petr Pisar <ppisar@redhat.com> - 1:0.280226-1
- 0.280226 bump

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280225-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280225-366
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280225-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280225-1
- 0.280225 bump in order to dual-live with perl 5.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.280224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 1:0.280224-1
- 0.280224 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.280223-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280223-2
- Perl 5.22 rebuild

* Thu Jun 04 2015 Petr Pisar <ppisar@redhat.com> - 1:0.280223-1
- 0.280223 bump

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.280221-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 1:0.280221-1
- 0.280221 bump in order to dual-live with perl 5.22

* Mon Nov 03 2014 Petr Pisar <ppisar@redhat.com> - 1:0.280220-1
- 0.280220 bump

* Thu Sep 18 2014 Petr Pisar <ppisar@redhat.com> - 1:0.280219-1
- Specfile autogenerated by cpanspec 1.78.
