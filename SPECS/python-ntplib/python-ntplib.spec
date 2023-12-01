Summary:        Python NTP library
Name:           python-ntplib
Version:        0.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.org/project/ntplib/
Source0:        https://files.pythonhosted.org/packages/b4/14/6b018fb602602d9f6cc7485cbad7c1be3a85d25cea18c233854f05284aed/ntplib-%{version}.tar.gz
BuildArch:      noarch

%description
This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode, leap indicator…). Since it’s pure Python, and only depends on core modules, it should work on any platform with a Python implementation.

%package -n     python3-ntplib
Summary:        python-ntplib
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-ntplib
Python 3 version.

%prep
%autosetup -n ntplib-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-ntplib
%license LICENSE
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Feb 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 0.4.0-1
- Upgrade to 0.4.0 for Mariner 2.0

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.3.3-6
- Remove python2 package
- Lint spec

* Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> - 0.3.3-5
- Added %%license macro.

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.3.3-4
- Verified license. Removed sha1. Fixed Source0 URL. Fixed URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.3.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> - 0.3.3-2
- Removed %check due to no test existence.

* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.3.3-1
- Initial packaging for Photon.
