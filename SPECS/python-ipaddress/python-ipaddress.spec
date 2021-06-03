%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ipaddress
Version:        1.0.22
Release:        5%{?dist}
Summary:        Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2
License:        Python Software Foundation License (Python Software Foundation License)
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ipaddress
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/i/ipaddress/ipaddress-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
IPv4/IPv6 manipulation library

%prep
%setup -n ipaddress-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.22-5
- Added %%license line automatically

*   Fri Apr 24 2020 Andrew Phelps <anphel@microsoft.com> 1.0.22-4
-   Updated Source0. Remove sha1 definition. Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.22-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-2
-   Updated the license
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-1
-   Update to version 1.0.22
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.18-2
-   Change python to python2
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.18-1
-   Initial packaging for Photon
