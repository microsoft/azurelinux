%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname jwt

Summary:        JSON Web Token library for Python 3
Name:           python-%{pkgname}
Version:        1.0.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/GehirnInc/python-jwt
Vendor:         Microsoft
Distribution:   Mariner
#Source0:       https://github.com/GehirnInc/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
python-jwt is a JSON Web Token (JWT) implementation in Python developed by Gehirn Inc.}

%description %_description

%package -n python3-%{pkgname}
Summary:        JSON Web Token library for Python 3

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-cryptography
%if %{with check}
BuildRequires:  python3-pip
%endif


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%if %{with check}
%check
pip3 install tox
tox
%endif

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 1.0.0-1
- Original CBL-Mariner version
