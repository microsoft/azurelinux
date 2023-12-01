%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define pkgname yamlloader

Summary:        Loaders and dumpers for PyYAML
Name:           python-%{pkgname}
Version:        1.1.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/Phynix/yamlloader
Source0:        https://github.com/Phynix/%{pkgname}/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description
This module provides loaders and dumpers for PyYAML.


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-PyYAML
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-PyYAML

%description -n python3-%{pkgname}
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.

%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info


%build
python3 setup.py build


%install
python3 setup.py install --skip-build --root=%{buildroot}


%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info

%changelog
* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-2
- Updating source URL.

* Fri Mar 25 2022 Andrew Phelps <anphel@microsoft.com> - 1.1.0-1
- Updated to version 1.1.0

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 0.5.4-1
- Original version for CBL-Mariner
- License verified
