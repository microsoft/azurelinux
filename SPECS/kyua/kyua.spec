%global _testsdir %{_libexecdir}/%{name}/tests
%global _make_args pkgtestsdir=%%{_testsdir} testsdir=%%{_testsdir}

Name:           kyua
Version:        0.13
Release:        7%{?dist}
Summary:        Testing framework for infrastructure software

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/jmmv/kyua
Source0:        %{url}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  libatf-c++-devel >= 0.17
BuildRequires:  libatf-sh-devel >= 0.15
BuildRequires:  pkgconfig(lutok) >= 0.4
BuildRequires:  pkgconfig(sqlite3) >= 3.6.22

Obsoletes:      kyua-cli < 0.10
Provides:       kyua-cli = %{version}-%{release}
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
Requires:       %{name} = %{version}-%{release}
Obsoletes:      kyua-cli-tests < 0.10
Obsoletes:      kyua-testers-tests < 0.10

%description tests
%{summary}.

%prep
%autosetup

%build
%configure \
  --with-doxygen=no   \
  --with-with-atf=yes \
  %{nil}
%make_build %{_make_args}

%install
%make_install %{_make_args} doc_DATA=

%if %{with_check}
%check
# Tests expect dumping core to file which is different from machine to machine
HOME=$(pwd)/check %make_build check %{_make_args} || :
%endif

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
* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 0.13-7
- Remove epoch

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 0.13-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add with_check conditional.
- License verified.

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
