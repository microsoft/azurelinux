%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname routes
%define upname Routes

Summary:        Python re-implementation of the Rails routes system
Name:           python-%{pkgname}
Version:        2.4.1
Release:        1%{?dist}
License:        MIT
URL:            https://routes.readthedocs.io/en/latest/
Vendor:         Microsoft
Distribution:   Mariner
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

%if %{with check}
%check
pip3 install tox
tox
%endif

%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/*

%changelog
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 2.4.1-1
- Original CBL-Mariner version
