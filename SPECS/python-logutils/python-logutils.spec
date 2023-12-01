%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname logutils

Summary:        A set of handlers for the Python standard library’s logging package
Name:           python-%{pkgname}
Version:        0.3.5
Release:        1%{?dist}
License:        BSD
Url:            https://logutils.readthedocs.io/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
The logutils package provides a set of handlers for the Python standard library’s logging package.

Some of these handlers are out-of-scope for the standard library, and so they are packaged here.
Others are updated versions which have appeared in recent Python releases, but are usable with 
older versions of Python, and so are packaged here..}

%description %_description

%package -n python3-%{pkgname}
Summary:        A lean and fast WSGI object-dispatching web framework

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{pkgname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%if %{with check}
%check
python3 setup.py test
%endif

%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst doc/
%{python3_sitelib}/*

%changelog
* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> 1.4.0-1
- Original version for CBL-Mariner
- License verified
