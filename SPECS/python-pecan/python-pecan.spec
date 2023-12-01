%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname pecan

Summary:        A lean and fast WSGI object-dispatching web framework
Name:           python-%{pkgname}
Version:        1.4.0
Release:        2%{?dist}
License:        BSD
Url:            https://www.pecanpy.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
Pecan was created to fill a void in the Python web-framework world – a very
lightweight framework that provides object-dispatch style routing. Pecan does
not aim to be a “full stack” framework, and therefore includes no out of the
box support for things like sessions or databases (although tutorials are
included for integrating these yourself in just a few lines of code). Pecan
instead focuses on HTTP itself.}

%description %_description

%package -n python3-%{pkgname}
Summary:        A lean and fast WSGI object-dispatching web framework

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-webob
Requires:       python3-mako
Requires:       python3-six
Requires:       python3-logutils
%if %{with check}
BuildRequires:  python3-pip
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
pip3 install tox==3.4.0
tox
%endif

%files -n python3-%{pkgname}
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/pecan
%{_bindir}/gunicorn_pecan

%changelog
* Wed Jun 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> 1.4.0-2
- Pass check section

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> 1.4.0-1
- Original version for CBL-Mariner
- License verified
