%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library to implement a well-behaved Unix daemon process.
Name:           python-daemon
Version:        2.2.0
Release:        4%{?dist}
License:        Apache-2
Url:            https://pypi.python.org/pypi/python-daemon/
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/p/python-daemon/%{name}-%{version}.tar.gz
%define sha1    python-daemon=9135b7edafa5bcd457d88bb2c0dfae024b3d8778

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-docutils
BuildRequires:  python-lockfile
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python2
Requires:       python-lockfile

BuildArch:      noarch

%description
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.

A well-behaved Unix daemon process is tricky to get right, but the required steps are much the same for every daemon program. A DaemonContext instance holds the behaviour and configured process environment for the program; use the instance as a context manager to enter a daemon state.

%package -n python3-daemon
Summary:        Python3-daemon
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-lockfile
Requires:       python3
Requires:       python3-lockfile

%description -n python3-daemon
Python 3 version.

%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir
pushd ../p3dir
sed -i 's/distclass=version.ChangelogAwareDistribution,/ /g' setup.py
popd

%build
python2 setup.py build

pushd ../p3dir
python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install --root=%{buildroot}

pushd ../p3dir
python3 setup.py install --root=%{buildroot}
popd

%check
#test incompatible with python2.7,so running only python3 tests
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 mock
$easy_install_3 testscenarios
$easy_install_3 testtools
python3 -m unittest discover
popd

%files
%defattr(-, root, root, -)
%license LICENSE.ASF-2
%{python2_sitelib}/*

%files -n python3-daemon
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Dec 19 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-2
-   Fix makecheck
*   Sat Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
-   Updated to 2.2.0
*   Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-4
-   Fixed check command to run unit tests
-   Added packages required to run tests
-   Added missing runtime dependent packages
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-2
-   Corrected an error in command
*   Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-1
-   Initial packaging for Photon
