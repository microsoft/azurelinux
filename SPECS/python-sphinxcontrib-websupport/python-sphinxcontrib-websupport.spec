%global pypi_name_prefix sphinxcontrib
%global pypi_name_suffix websupport
%global pypi_name %{pypi_name_prefix}-${pypi_name_suffix}
%global pypi_name_underscore %{pypi_name_prefix}_${pypi_name_suffix}

Summary:        Python API to integrate Sphinx into a web application
Name:           python-%{pypi_name}
Version:        1.2.4
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/sphinx-doc/%{pypi_name}
Source0:        https://github.com/sphinx-doc/%{pypi_name}/archive/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Python API to integrate Sphinx into a web application

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with check}
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-sphinxcontrib-serializinghtml

%description -n python3-%{pypi_name}
The python-sphinxcontrib-websupport package provides a Python API to easily integrate Sphinx documentation into your Web application.

%prep
%autosetup -n %{pypi_name}-%{version} -p 1
rm -rf *.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name_prefix}/*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth

%changelog
* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-3
- Updating source URL.

* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-2
- Adding a dependency on "python3-sphinxcontrib-serializinghtml".

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-1
- Updating to version 1.2.4.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.5.0-2
- Remove python2 package
- Lint spec

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner.
- License verified.
