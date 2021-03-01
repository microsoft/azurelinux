%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Extremely fast and user friendly build system
Name:           meson
Version:        0.57.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://mesonbuild.com/
Source0:        https://github.com/mesonbuild/meson/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       ninja-build
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
Meson is an open source build system meant to be both extremely fast,
and, even more importantly, as user friendly as possible.
The main design point of Meson is that every moment a developer spends
writing or debugging build definitions is a second wasted.
So is every second spent waiting for the build system to actually start compiling code.

%prep
%setup -q

%build

%install
python3 setup.py install --root=%{buildroot}/
install -Dpm0644 data/macros.%{name} %{buildroot}%{_libdir}/rpm/macros.d/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1
python3 ./run_tests.py

%files
%license COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild
%{python3_sitelib}/%{name}-*.egg-info
%{_mandir}/man1/%{name}.1*
%{_libdir}/rpm/macros.d/macros.%{name}
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy

%changelog
* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> - 0.57.1-1
- Update to 0.57.1.

*   Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> 0.49.2-1
-   Update to 0.49.2.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.47.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.47.2-1
-   Update to version 0.47.2

*   Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
-   Initial packaging
