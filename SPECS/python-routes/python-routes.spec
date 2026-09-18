%bcond_without check
%define pkgname routes
%define upname Routes

Summary:        Python re-implementation of the Rails routes system
Name:           python-%{pkgname}
Version:        2.5.1
Release:        5%{?dist}
License:        MIT
URL:            https://routes.readthedocs.io/en/latest/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://pypi.io/packages/source/R/%{upname}/%{upname}-%{version}.tar.gz
BuildArch:      noarch


%global _description %{expand:
Routes is a Python re-implementation of the Rails routes system for mapping URL's to Controllers/Actions and generating URL's. Routes makes it easy to create pretty and concise URL's that are RESTful with little effort.

Speedy and dynamic URL generation means you get a URL with minimal cruft (no big dangling query args). Shortcut features like Named Routes cut down on repetitive typing.}

%description %_description

%package -n python3-%{pkgname}
Summary:        Python re-implementation of the Rails routes system

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-repoze-lru
Requires:       python3

%if %{with check}
BuildRequires:  python3-pip
%endif


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{upname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%check
# pin packaging==23.2 to avoid uninstall conflict; tox 4.x needed for py312 env
pip3 install packaging==23.2 tox
tox -e py%{python3_version_nodots}

%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/*

%changelog
* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 2.5.1-5
- Pin packaging==23.2 and drop tox version pin in %%check; tox 4.x is
  required for the py312 environment.

* Sat Mar 26 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.5.1-1
- Upgrade to version 2.5.1

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 2.4.1-4
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 2.4.1-3
- Use tox env `py39` to enable ptest

* Wed Jun 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 2.4.1-2
- Pass check section

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 2.4.1-1
- Original version for CBL-Mariner
- License verified
