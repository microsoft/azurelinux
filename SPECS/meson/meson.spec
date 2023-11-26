Summary:        Extremely fast and user friendly build system
Name:           meson
Version:        1.2.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://mesonbuild.com/
Source0:        https://github.com/mesonbuild/meson/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  libgcrypt-devel
BuildRequires:  glib-devel
BuildRequires:  cmake
BuildRequires:  gtest
BuildRequires:  gmock
BuildRequires:  git
%endif

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
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.1-1
- Auto-upgrade to 1.2.1 - Azure Linux 3.0 - package upgrades

* Tue Feb 22 2022 Muhammad Falak <mwani@microsoft.com> - 0.60.2-2
- Drop BR on `gmock-devel` & `gtest-devel`
- Drop BR on `python3-libs` which is satisfied by `python3-devel`
- Add an explict BR on `libgcrypt, glib, gtest, gmock, cmake, git` to enable ptest

* Wed Dec 08 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.60.2-1
- Updating to 0.60.2.
- License Verified

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 0.57.1-2
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 0.56.0-1: Removing 'python3-xml' from '*Requires'.

* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> - 0.57.1-1
- Update to 0.57.1.

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> 0.49.2-1
- Update to 0.49.2.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.47.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.47.2-1
- Update to version 0.47.2

* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
- Initial packaging
