%define pkgname execnet
Summary:        Python execution distributor
Name:           python-%{pkgname}
Version:        1.9.0
Release:        2%{?dist}
License:        MIT
URL:            https://codespeak.net/execnet/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/e/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
%if %{with check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Python execution distributor

%package -n python3-%{pkgname}
Summary:        Python execution distributor
Requires:       python3

%description -n python3-%{pkgname}
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It provides
a minimal and fast API targetting the following uses:

-distribute tasks to local or remote processes
-write and deploy hybrid multi-process applications
-write scripts to administer multiple hosts}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
sed -i "s/pytest$/pytest==7.1.3/" tox.ini
LANG=en_US.UTF-8 tox -e py%{python3_version_nodots}

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/*

%changelog
* Wed Oct 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.0-2
- Freezing 'pytest' test dependency to version 7.1.3.

* Wed Mar 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.0-1
- Upgrade to latest upstream version
- Lint spec

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.7.1-4
- Use `py%%{python3_version_nodots}` instead of harcoding `py39`

* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 1.7.1-3
- Use `py39` instead of `py37` as tox environment to enable ptest

* Tue Jun 08 2021 Andrew Phelps <anphel@microsoft.com> - 1.7.1-2
- Fix check tests

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.7.1-1
- Original version for CBL-Mariner
- License verified
