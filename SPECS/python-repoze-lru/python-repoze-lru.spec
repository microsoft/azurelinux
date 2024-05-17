%define pkgname repoze-lru
%define pypiname repoze.lru

Summary:        A tiny LRU cache implementation and decorator
Name:           python-%{pkgname}
Version:        0.7
Release:        6%{?dist}
License:        BSD
URL:            https://github.com/repoze/repoze.lru
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://pypi.io/packages/source/r/%{pypiname}/%{pypiname}-%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
A tiny LRU cache implementation and decorator.}

%description %_description

%package -n python3-%{pkgname}
Summary:        A tiny LRU cache implementation and decorator

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
Requires:       python3
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{pypiname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%check
python3 setup.py test

%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed May 15 2024 Sam Meluch <sammeluch@microsoft.com> - 0.7-6
- fix with_check macro, remove sitelibs redef to fix tests

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7-5
- Updating source URL.

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 0.7-4
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 0.7-3
- Remove `%bcond_without check`
- Use `py39` as tox environment to enable ptest

* Tue Jun 08 2021 Andrew Phelps <anphel@microsoft.com> - 0.7-2
- Fix check tests

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.7-1
- Original version for CBL-Mariner
- License verified
