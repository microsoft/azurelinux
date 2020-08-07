%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define LICENSE_PATH LICENSE.PTR

Summary:        Python NTP library
Name:           python-ntplib
Version:        0.3.3
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://code.google.com/archive/p/ntplib/
Source0:        https://files.pythonhosted.org/packages/29/8b/85a86e01c510665b0790d3a9fd4532ad98aba9e185a676113a0ae3879350/ntplib-%{version}.tar.gz
Source1:        %{LICENSE_PATH}

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental

Requires:       python2
Requires:       python2-libs

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
%setup -q -n ntplib-%{version}
rm -rf ../p3dir
cp -a . ../p3dir
cp %{SOURCE1} ./

%build
python2 setup.py build
python3 setup.py build

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-ntplib
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 0.3.3-5
-   Added %%license macro.
*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 0.3.3-4
-   Verified license. Removed sha1. Fixed Source0 URL. Fixed URL.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.3.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.3.3-2
-   Removed %check due to no test existence.
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.3.3-1
-   Initial packaging for Photon.
