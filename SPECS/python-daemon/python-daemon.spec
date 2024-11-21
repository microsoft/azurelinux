Summary:        Library to implement a well-behaved Unix daemon process.
Name:           python-daemon
Version:        2.2.0
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/python-daemon/
Source0:        https://files.pythonhosted.org/packages/source/p/python-daemon/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.

%package -n python3-daemon
Summary:        Library to implement a well-behaved Unix daemon process.
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-lockfile
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-lockfile

%description -n python3-daemon
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.
A well-behaved Unix daemon process is tricky to get right, but the required steps are much the same for every
daemon program. A DaemonContext instance holds the behaviour and configured process environment for the program;
use the instance as a context manager to enter a daemon state.

%prep
%autosetup
sed -i 's/distclass=version.ChangelogAwareDistribution,/ /g' setup.py

%build
%py3_build

%install
%py3_install

%check
pip3 install mock testscenarios testtools
%python3 -m unittest discover

%files -n python3-daemon
%license LICENSE.ASF-2
%{python3_sitelib}/*

%changelog
* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.0-6
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Dec 19 2018 Tapas Kundu <tkundu@vmware.com> - 2.2.0-2
- Fix makecheck

* Sat Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.2.0-1
- Updated to 2.2.0

* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> - 2.1.2-4
- Fixed check command to run unit tests
- Added packages required to run tests
- Added missing runtime dependent packages

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.1.2-2
- Corrected an error in command

* Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.2-1
- Initial packaging for Photon
