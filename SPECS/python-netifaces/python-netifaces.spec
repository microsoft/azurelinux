%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-netifaces
Version:        0.10.9
Release:        3%{?dist}
Summary:        Python library to retrieve information about network interfaces
Group:          Development/Libraries
License:        MIT
URL:            http://alastairs-place.net/netifaces/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/source/n/netifaces/netifaces-%{version}.tar.gz
%define sha1    netifaces=340a91e6cdd03c941a0da464255d6e4b5cbe5512
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-xml
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs

%description
This package provides a cross platform API for getting address information
from network interfaces.

%package -n python3-netifaces
Summary:        Python library to retrieve information about network interfaces
Requires:       python3
Requires:       python3-libs

%description -n python3-netifaces
This package provides a cross platform API for getting address information
from network interfaces.


%prep
%setup -q -n netifaces-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python2_sitelib}/*

%files -n python3-netifaces
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:19 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.10.9-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.10.9-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*  Wed Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.10.9-1
-  Initial packaging for photon OS
