%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname cherrypy
%define pypiname CherryPy

Summary:        A pythonic, object-oriented HTTP framework
Name:           python-%{pkgname}
Version:        18.9.0
Release:        1%{?dist}
License:        BSD
Url:            https://cherrypy.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/C/%{pypiname}/%{pypiname}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
CherryPy allows developers to build web applications in much the same way they would
build any other object-oriented Python program. This results in smaller source code 
developed in less time.

CherryPy is now more than ten years old and it is has proven to be fast and reliable.
It is being used in production by many sites, from the simplest to the most demanding.}

%description %_description

%package -n python3-%{pkgname}
Summary:        A pythonic, object-oriented HTTP framework

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
Requires:       python3
Requires:       python3-libs
%if 0%{with check}
BuildRequires:  python3-pip
%endif

%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{pypiname}-%{version}
# suppress depracation warning in the pytest.ini 
# Feb 2023 setuptools added deprecation warning for pkg_resources.declare_namespace causing all the test to fail for python-cherrypy 
# https://setuptools.pypa.io/en/latest/history.html#v67-3-0
# supressing deprecation warning so that test doesn't fail just because of a deprecation warning message.
# for the future update of this package, cherrypy might stop using pkg_resources.declare_namespace. Might be ok to delete this in the future 
# when that happens.
sed -i '/ignore:Use/a \    \ignore::DeprecationWarning' pytest.ini

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%if 0%{with check}
%check
pip3 install tox
tox -e py%{python3_version_nodots}
%endif

%files -n python3-%{pkgname}
%license LICENSE.md
%doc README.rst docs/
%{python3_sitelib}/*
%{_bindir}/cherryd

%changelog
* Tue Jan 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 18.9.0-1
- Auto-upgrade to 18.9.0 - Azure Linux 3.0 - package upgrades

* Wed Mar 08 2023 Riken Maharjan <rmaharjan@microsoft.com> - 18.6.1-3
- Suppress pytest deprecation warning 

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 18.6.1-2
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 18.6.1-1
- Bump version to 18.6.1
- Use 'py39' as tox environment to enable ptest

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 18.6.0-1
- Original version for CBL-Mariner
- License verified
