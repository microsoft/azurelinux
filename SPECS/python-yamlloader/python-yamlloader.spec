%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define pkgname yamlloader

Summary:        Loaders and dumpers for PyYAML
Name:           python-%{pkgname}
Version:        0.5.4
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/Phynix/yamlloader
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/Phynix/%{pkgname}/archive/%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description 
This module provides loaders and dumpers for PyYAML. 


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-PyYAML
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
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.4-1
- Original version for CBL-Mariner
- License verified
