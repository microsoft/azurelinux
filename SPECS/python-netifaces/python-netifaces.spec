Summary:        Python library to retrieve information about network interfaces
Name:           python-netifaces
Version:        0.10.9
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://alastairs-place.net/netifaces/
Source0:        https://pypi.python.org/packages/source/n/netifaces/netifaces-%{version}.tar.gz

%description
This package provides a cross platform API for getting address information
from network interfaces.

%package -n python3-netifaces
Summary:        Python library to retrieve information about network interfaces
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-netifaces
This package provides a cross platform API for getting address information
from network interfaces.

%prep
%autosetup -n netifaces-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-netifaces
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.10.9-4
- Add build instructions
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.10.9-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.10.9-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jul 23 2019 Tapas Kundu <tkundu@vmware.com> - 0.10.9-1
- Initial packaging for photon OS
