Summary:        pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
Name:           python-pyvmomi
Version:        6.7.3
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pyvmomi
#Source0:       https://github.com/vmware/pyvmomi/archive/6.7.3.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         python-pyvmomi-make-check-fix.patch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%package -n     python3-pyvmomi
Summary:        python-pyvmomi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3

%description -n python3-pyvmomi
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%prep
%autosetup -p 1 -n pyvmomi-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-pyvmomi
%defattr(-,root,root)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 6.7.3-3
- Add license to python3 package
- Remove python2 package
- Lint spec

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
