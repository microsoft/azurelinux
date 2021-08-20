%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without  python2
%define pkgname sphinxcontrib-websupport

Summary:        Python API to integrate Sphinx into a web application
Name:           python-%{pkgname}
Version:        1.1.2
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/sphinx-doc/sphinxcontrib-websupport
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/sphinx-doc/%{pkgname}/archive/%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
The python-sphinxcontrib-websupport package provides a Python API to easily integrate Sphinx documentation into your Web application.}

%description %_description


%if %{with python2}
%package -n python2-%{pkgname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
Requires:       python2
%if %{with check}
BuildRequires:  python-pip
%endif

%description -n python2-%{pkgname} %_description
%endif

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with check}
BuildRequires:  python3-pip
%endif

%description -n python3-%{pkgname} %_description


%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info


%build
%if %{with python2}
python2 setup.py build
%endif
python3 setup.py build


%install
%if %{with python2}
python2 setup.py install --skip-build --root=%{buildroot}
%endif
python3 setup.py install --skip-build --root=%{buildroot}

%if %{with check}
%check
pip3 install tox
tox
%endif

%if %{with python2}
%files -n python2-%{pkgname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/sphinxcontrib/*
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*.pth
%endif


%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth


%changelog
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner.
- License verified.
