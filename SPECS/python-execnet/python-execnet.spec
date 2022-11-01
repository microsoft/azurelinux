%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname execnet

Summary:        Python execution distributor
Name:           python-%{pkgname}
Version:        1.7.1
Release:        3%{?dist}
License:        MIT
URL:            https://codespeak.net/execnet/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/e/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It provides
a minimal and fast API targetting the following uses:

-distribute tasks to local or remote processes
-write and deploy hybrid multi-process applications
-write scripts to administer multiple hosts}

%description %_description

%package -n python3-%{pkgname}
Summary:        Python execution distributor

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
Requires:       python3
# python3-apipkg is provided by python3-py in Mariner
# Requires:     python3-apipkg
Requires:       python3-py
%if %{with check}
BuildRequires:       python3-pip
%endif


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{pkgname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%if %{with check}
%check
pip3 install tox
sed -i "s/pytest$/pytest==7.1.3/" tox.ini
LANG=en_US.UTF-8 tox -e py37
%endif

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Jon Slobodzian <joslobo@microsoft.com> 1.7.1-3
- Fix check tests to enforce the 7.1.3 version of pytest. 
* Tue Jun 08 2021 Andrew Phelps <anphel@microsoft.com> 1.7.1-2
- Fix check tests
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 1.7.1-1
- Original version for CBL-Mariner
- License verified
