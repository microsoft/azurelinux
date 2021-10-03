%define pkgname sphinxcontrib-websupport
Summary:        Python API to integrate Sphinx into a web application
Name:           python-%{pkgname}
Version:        1.1.2
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/sphinx-doc/sphinxcontrib-websupport
#Source0:       https://github.com/sphinx-doc/%{pkgname}/archive/%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz

%description
Python API to integrate Sphinx into a web application

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with check}
BuildRequires:  python3-pip
%endif
Requires:       python3

%description -n python3-%{pkgname}
The python-sphinxcontrib-websupport package provides a Python API to easily integrate Sphinx documentation into your Web application.

%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.5.0-2
- Remove python2 package
- Lint spec

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner.
- License verified.
