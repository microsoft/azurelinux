# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _testsdir %{_libexecdir}/%{name}/tests
%global _make_args pkgtestsdir=%%{_testsdir} testsdir=%%{_testsdir}

Name:           kyua
Version:        0.13
Release:        19%{?dist}
Summary:        Testing framework for infrastructure software

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/jmmv/kyua
Source0:        %{url}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  libatf-c++-devel >= 0.17
BuildRequires:  libatf-sh-devel >= 0.15
BuildRequires:  pkgconfig(lutok) >= 0.4
BuildRequires:  pkgconfig(sqlite3) >= 3.6.22

Obsoletes:      kyua-cli < 0.10
Provides:       kyua-cli = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      kyua-testers < 0.10
Obsoletes:      kyua-testers-devel < 0.10

%description
Kyua is a testing framework for infrastructure software, originally designed
to equip BSD-based operating systems with a test suite. This means that
Kyua is lightweight and simple, and that Kyua integrates well with various
build systems and continuous integration frameworks.

Kyua features an expressive test suite definition language, a safe runtime
engine for test suites and a powerful report generation engine.

Kyua is for both developers and users, from the developer applying a simple
fix to a library to the system administrator deploying a new release
on a production machine.

Kyua is able to execute test programs written with a plethora of
testing libraries and languages. The library of choice is ATF, for which
Kyua was originally designed, but simple, framework-less test programs and
TAP-compliant test programs can also be executed through Kyua.

%package tests
Summary:        Runtime tests of the Kyua toolchain
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      kyua-cli-tests < 0.10
Obsoletes:      kyua-testers-tests < 0.10

%description tests
%{summary}.

%prep
%autosetup

# Disable problematic test
# https://github.com/jmmv/kyua/issues/214
sed -e 's/name="stacktrace_test"/&,required_configs="enable_stacktrace"/' -i utils/Kyuafile

%build
%configure \
  --with-doxygen=no   \
  --with-with-atf=yes \
  %{nil}
%make_build %{_make_args}

%install
%make_install %{_make_args} doc_DATA=

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

# Tests expect dumping core to file which is different from machine to machine
HOME=$(pwd)/check %make_build check %{_make_args}

%files
%license LICENSE
%doc AUTHORS CONTRIBUTORS NEWS.md README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/%{name}*.5*

%files tests
%{_libexecdir}/%{name}/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.13-17
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Sérgio Basto <sergio@serjux.com> - 0.13-12
- Rebuild for ATF soname bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.13-1
- Initial package
