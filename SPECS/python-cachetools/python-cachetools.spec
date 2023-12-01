%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global pkgname cachetools

Summary:        Various memoizing collections and decorators
Name:           python-%{pkgname}
Version:        5.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/tkem/cachetools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/source/c/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:  noarch

%description
This module provides various memoizing collections and decorators, including variants of the Python Standard Library’s @lru_cache function decorator.

%package -n python3-%{pkgname}
Summary:    Various memoizing collections and decorators

BuildRequires:  python3-devel >= 3.7
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3 >= 3.7

%description -n python3-%{pkgname}
This module provides various memoizing collections and decorators, including variants of the Python Standard Library’s @lru_cache function decorator.

%prep
%autosetup -n %{pkgname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info

%changelog
* Wed Feb 09 2022 Nick Samson <nisamson@microsoft.com> - 5.0.0-1
- Updated to 5.0.0

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.20.1-1
- Original version for CBL-Mariner
- License verified
