Summary:        pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
Name:           python-pyvmomi
Version:        7.0.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pyvmomi
Source0:        https://github.com/vmware/pyvmomi/archive/refs/tags/v7.0.3.tar.gz#/pyvmomi-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-six
%endif
BuildArch:      noarch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%package -n     python3-pyvmomi
Summary:        python-pyvmomi
Requires:       python3
Requires:       python3-requests
Requires:       python3-six

%description -n python3-pyvmomi
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%prep
%autosetup -p 1 -n pyvmomi-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install -r test-requirements.txt
%python3 setup.py test

%files -n python3-pyvmomi
%defattr(-,root,root)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Thu Apr 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 7.0.3-1
- Upgrade to latest upstream version

* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 6.7.3-4
- Add an explicit BR on `pip` to fix ptest

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 6.7.3-3
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.7.3-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 6.7.3-1
- Update to 6.7.3.  Fix Source0. Fix license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.2018.9-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> - 6.7.0.2018.9-2
- Fix make check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 6.7.0.2018.9-1
- Update to version 6.7.0.2018.9

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 6.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 6.5-1
- Initial packaging for Photon.
