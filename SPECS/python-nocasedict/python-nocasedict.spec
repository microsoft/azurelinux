%define pkgname nocasedict
%define six_version 1.14.0
Summary:        Case-insensitive ordered dictionary library for Python
Name:           python-%{pkgname}
Version:        2.0.1
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pywbem/nocasedict
Source0:        https://github.com/pywbem/nocasedict/archive/refs/tags/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six >= %{six_version}
BuildRequires:  python3-wheel
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.

%package -n     python3-%{pkgname}
Summary:        %{summary}
Requires:       python3
Requires:       python3-six >= %{six_version}

%description -n python3-%{pkgname}
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.

%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install 'tox>=3.27.1,<4.0.0'
PYTHONPATH=%{buildroot}%{python3_sitelib} tox -e py%{python3_version_nodots}

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info

%changelog
* Fri Nov 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-1
- Auto-upgrade to 2.0.1 - Azure Linux 3.0 - package upgrades

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 1.0.2-2
- Update version of tox used for package tests

* Tue Mar 15 2022 Thomas Crain <thcrain@microsoft.com> - 1.0.2-1
- Upgrade to latest upstream release
- Use tox as a test runner
- Lint spec

* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 0.5.0-2
- Disable auto dependency generator.
- Add explicit dist provides.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner.
- License verified.
