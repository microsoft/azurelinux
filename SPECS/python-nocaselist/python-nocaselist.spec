%global srcname nocaselist

Name:           python-%{srcname}
Version:        2.0.0
Release:        1%{?dist}
Summary:        A case-insensitive list for Python
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pywbem/nocaselist
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
Python class 'NocaseList' is a case-insensitive list that preserves the
lexical case of its items.

It supports the functionality of the built-in 'list' class of Python 3.8 on
all Python versions it supports (except for being case-insensitive, of course).
This includes the 'clear()' and 'copy()' methods added in Python 3.3 to the
built-in 'list' class.}

%description %{_description}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%if 0%{?with_check}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-six
%endif

%description -n python%{python3_pkgversion}-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip install iniconfig
%{python3} setup.py test

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Wed Mar 06 2024 Yash Panchal <yashpanchal@microsoft.com> - 2.0.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
